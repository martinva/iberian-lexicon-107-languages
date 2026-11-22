#!/usr/bin/env python3
"""Regenera, a partir del Banco de Datos Hesperia (hesperia.ucm.es), los dos archivos derivados del corpus ibérico
que usan los programas:

    hesperia_iberico_1599.csv   texto de las 1.599 inscripciones ibéricas auténticas (listado del buscador)
    hesperia_metadatos.csv      metadatos de las 1.615 fichas ibéricas (pestañas de cada ficha) con columnas normalizadas

Los dos archivos no se redistribuyen con el repositorio: Hesperia es la fuente y cada réplica los descarga.
Este programa reproduce exactamente el procedimiento con el que se obtuvieron (consultas del 7 y del 12-11-2026)
y comprueba al final que el resultado coincide, byte a byte, con las sumas SHA-256 de los archivos usados en el
artículo. Si Hesperia ha cambiado alguna ficha desde entonces, lo dice y señala qué filas difieren.

Uso (solo biblioteca estándar de Python 3; unos 40 minutos, con pausas de cortesía entre peticiones):

    python3 descargar_hesperia.py                 # descarga y escribe los dos archivos en esta carpeta
    python3 descargar_hesperia.py --cache DIR     # guarda (y reutiliza) el HTML crudo de cada petición en DIR
    python3 descargar_hesperia.py --solo-listado  # solo el primer archivo (unos segundos)
    python3 descargar_hesperia.py --verificar     # no descarga: comprueba las sumas de los archivos presentes

Procedimiento (documentado en 5_especificacion, apartado 1.2):
  1. Listado completo del buscador (buscador2.php, zona TODO, orden REF_HESPERIA) y, para asignar la lengua,
     el mismo listado filtrado por cada lengua. Se conservan las fichas cuyo filtro de lengua es IBERICO.
  2. hesperia_iberico_1599.csv: de esas 1.615, se excluyen las que Hesperia marca en su referencia como
     FALSA, SUSPECTA o LATINA (16). texto_crudo se guarda tal como lo sirve Hesperia (saltos de línea, diacríticos).
  3. hesperia_metadatos.csv: de cada una de las 1.615 fichas, campos de las pestañas Generalidades, Epigrafía
     y Contexto (Generalidades.php, Epigrafia.php, Contexto.php con ?file=file_100.php&id=N), más las columnas
     normalizadas (*_norm, *_grupo, *_incierto, *_dudoso, autenticidad, dat_*) que calcula este mismo programa.

Hesperia: Luján, E. R. y Orduña, E. (dirs.), Banco de Datos de Lenguas Paleohispánicas, http://hesperia.ucm.es.
Cite siempre la fecha de consulta.
"""
import argparse, csv, hashlib, io, os, re, sys, time, unicodedata
import urllib.parse, urllib.request
from html.parser import HTMLParser

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = 'http://hesperia.ucm.es/consulta_hesperia/'
SEARCH = BASE + 'buscador2.php'
UA = 'Mozilla/5.0 (replica academica; descarga puntual con pausas) Python-urllib'
LENGUAS = ['INDET.', '^IBERICO', 'SUDOESTE', 'CELTIBERICO', 'LUSITANO', 'LATIN', 'GRIEGO', 'GALO']
FORM = {'file': '', 'zona': 'TODO', 'orden': 'REF_HESPERIA', 'descendente': '', 'inicial': '', 'texto': '', 'final': '',
        'vibrantes': '', 'silbantes': '', 'case': '/ui', 'dual': '', 'yacimiento': '', 'municipio': '', 'provincia': '',
        'ref_hesperia': '', 'catu': '', 'material': '', 'soporte': '', 'tipo_epigrafe': '', 'lengua': '', 'signario': '',
        'sistema_dual': '', 'datacion': ''}
SALIDA_TEXTO = os.path.join(AQUI, 'hesperia_iberico_1599.csv')
SALIDA_META = os.path.join(AQUI, 'hesperia_metadatos.csv')
# sumas SHA-256 de los archivos usados en el artículo (consultas del 7-11-2026 y del 12-11-2026)
SHA_ESPERADA = {
    'hesperia_iberico_1599.csv': '67384e85643cd373a2e3f63f29a1f19af33fe109a664522e6c2a61455d2f8059',
    'hesperia_metadatos.csv': 'b729562c22e70ac00c0c7a92c160e58e3d71463f469d36424fb03197327735bd',
}
COLS_TEXTO = ['ref_hesperia', 'yacimiento', 'municipio', 'ref_mlh', 'texto_crudo', 'lengua_filtro', 'id_ficha', 'href_ficha']
COLS_META = ['id_ficha', 'ref_hesperia', 'yacimiento', 'provincia', 'tipo_yac', 'material', 'soporte', 'tipo', 'forma', 'tecnica',
             'direccion_escritura', 'tipo_epigrafe', 'num_lineas', 'conserv_epg', 'lengua_ficha', 'signario', 'sistema_dual',
             'separadores', 'metrologia', 'fte_lec', 'fecha_hallazgo', 'circunstancias_hallazgo', 'datacion', 'criterios_datacion']
# campo de la ficha -> (pestaña, nombre del campo en el formulario de Hesperia)
ORIGEN_META = {'yacimiento': ('g', 'yacimiento'), 'provincia': ('g', 'provincia'), 'tipo_yac': ('g', 'tipo_yac'), 'material': ('g', 'material'),
               'soporte': ('g', 'soporte'), 'tipo': ('g', 'tipo'), 'forma': ('g', 'forma'), 'tecnica': ('g', 'tecnica'),
               'direccion_escritura': ('g', 'direccion_escritura'), 'tipo_epigrafe': ('g', 'tipo_epigrafe'), 'num_lineas': ('g', 'num_lineas'),
               'conserv_epg': ('g', 'conserv_epg'), 'lengua_ficha': ('e', 'lengua'), 'signario': ('e', 'signario'), 'sistema_dual': ('e', 'sistema_dual'),
               'separadores': ('e', 'separadores'), 'metrologia': ('e', 'metrologia'), 'fte_lec': ('e', 'fte_lec'),
               'fecha_hallazgo': ('c', 'fecha_hallazgo'), 'circunstancias_hallazgo': ('c', 'circunstancias_hallazgo'),
               'datacion': ('c', 'datacion'), 'criterios_datacion': ('c', 'criterios_datacion')}
PESTANAS = {'g': 'Generalidades', 'e': 'Epigrafia', 'c': 'Contexto'}


# ----------------------------------------------------------------------------------------------------- descarga
def http(url, data=None, cache=None, intentos=4, pausa=2.0):
    if cache and os.path.exists(cache):
        return open(cache, 'rb').read()
    cuerpo = urllib.parse.urlencode(data).encode('utf-8') if data is not None else None
    ultimo = None
    for i in range(intentos):
        try:
            req = urllib.request.Request(url, data=cuerpo, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                crudo = r.read()
            if cache:
                os.makedirs(os.path.dirname(cache), exist_ok=True); open(cache, 'wb').write(crudo)
            return crudo
        except Exception as e:
            ultimo = e; time.sleep(pausa * (i + 1))
    raise RuntimeError(f'fallo al pedir {url}: {ultimo}')


def decodifica(crudo):
    m = re.search(rb'charset=([\w-]+)', crudo[:3000], re.I)
    return crudo.decode(m.group(1).decode() if m else 'utf-8', errors='replace')


class Filas(HTMLParser):
    """Filas de resultados del buscador: seis celdas; <br> dentro del texto pasa a salto de línea."""
    def __init__(self):
        super().__init__(convert_charrefs=True); self.filas, self.cur, self.celda, self.en_td, self.href = [], None, None, False, None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'tr': self.cur, self.href = [], None
        elif tag == 'td' and self.cur is not None: self.en_td, self.celda = True, []
        elif tag == 'br' and self.en_td: self.celda.append('\n')
        elif tag == 'a' and self.en_td and a.get('href', '').startswith('Generalidades.php'): self.href = a['href']
    def handle_endtag(self, tag):
        if tag == 'td' and self.en_td: self.cur.append(''.join(self.celda)); self.en_td = False
        elif tag == 'tr' and self.cur is not None:
            if len(self.cur) >= 5 and re.search(r'\.\d', self.cur[2] or ''): self.filas.append((self.cur, self.href))
            self.cur = None
    def handle_data(self, data):
        if self.en_td: self.celda.append(data)


def limpia_texto(s):
    s = s.replace('\r', ''); s = re.sub(r'[ \t\xa0]+', ' ', s); return s.strip('\n ')


def listado(html_):
    p = Filas(); p.feed(html_); out = []
    for celdas, href in p.filas:
        c = [limpia_texto(x) for x in celdas]; m = re.search(r'[?&]id=(\d+)', href or '')
        out.append({'ref_hesperia': c[2], 'yacimiento': c[0], 'municipio': c[1], 'ref_mlh': c[3], 'texto_crudo': c[4],
                    'id_ficha': m.group(1) if m else '', 'href_ficha': href or ''})
    return out


class Campos(HTMLParser):
    """name=value de los input, textarea y select de una pestaña de ficha."""
    def __init__(self):
        super().__init__(convert_charrefs=True); self.d, self._ta, self._sel = {}, None, None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'input' and a.get('name') and a.get('type') not in ('checkbox', 'submit', 'button', 'hidden'): self.d[a['name']] = a.get('value', '') or ''
        elif tag == 'textarea' and a.get('name'): self._ta = a['name']; self.d.setdefault(self._ta, '')
        elif tag == 'select' and a.get('name'): self._sel = a['name']; self.d.setdefault(self._sel, '')
        elif tag == 'option' and self._sel is not None and 'selected' in a: self.d[self._sel] = a.get('value', '')
    def handle_endtag(self, tag):
        if tag == 'textarea': self._ta = None
        if tag == 'select': self._sel = None
    def handle_data(self, data):
        if self._ta: self.d[self._ta] += data


def campos(html_):
    c = Campos(); c.feed(html_); return {k: limpia_texto(v) for k, v in c.d.items()}


# ----------------------------------------------------------------------------------------- normalización
def fold(s):
    s = unicodedata.normalize('NFKD', s); s = ''.join(c for c in s if not unicodedata.combining(c)); return re.sub(r'\s+', ' ', s).strip().lower()

def limpia(s):
    f = fold(s); inc = '?' in f or '¿' in s; return re.sub(r'[?¿]', '', f).strip(' .,;'), inc

SOPORTE = {'recipiente': 'RECIPIENTE', 'anfora': 'RECIPIENTE', 'dolium': 'RECIPIENTE', 'tapadera': 'RECIPIENTE', 'tapa de anfora': 'RECIPIENTE',
           'recipiente, instrumento': 'RECIPIENTE', 'lamina/plancha': 'LAMINA_PLACA', 'placa': 'LAMINA_PLACA', 'placa-lingote': 'LAMINA_PLACA',
           'parietal/rupestre': 'PARIETAL', 'lapida': 'LAPIDA_ESTELA', 'estela': 'LAPIDA_ESTELA', 'pedestal': 'MONUMENTAL', 'altar': 'MONUMENTAL',
           'arula': 'MONUMENTAL', 'escultura': 'MONUMENTAL', 'estatua': 'MONUMENTAL', 'estruc. arquit': 'ARQUITECTONICO', 'ladrillo': 'ARQUITECTONICO',
           'mosaico': 'ARQUITECTONICO', 'pavimento': 'ARQUITECTONICO', 'tubulus': 'ARQUITECTONICO', 'pesa de telar': 'TEXTIL_PESO', 'fusayola': 'TEXTIL_PESO',
           'peso': 'PONDERAL', 'pesa': 'PONDERAL', 'ponderal': 'PONDERAL', 'pondus o tesera': 'PONDERAL', 'monetiforme': 'PONDERAL', 'tesera': 'TESERA',
           'ostracon': 'OSTRACON', 'ostrakon': 'OSTRACON', 'instrumento': 'INSTRUMENTO', 'arma': 'INSTRUMENTO', 'cepo de ancla': 'INSTRUMENTO',
           'disco': 'INSTRUMENTO', 'ficha de juego': 'INSTRUMENTO', 'joya': 'ADORNO', 'colgante': 'ADORNO', 'adorno personal': 'ADORNO', 'laja': 'OTROS'}

def grupo_soporte(v):
    n, _ = limpia(v); return 'SIN_DATO' if n == '' else SOPORTE.get(n, 'SIN_CLASIFICAR')

def grupo_epigrafe(v):
    n, _ = limpia(v)
    if n == '': return 'SIN_DATO'
    if n.startswith('indet') and '?' not in v and n in ('indet',): return 'INDET'
    if 'funerario' in n and 'votivo' in n: return 'AMBIGUO'
    if 'funerario' in n: return 'FUNERARIO'
    if 'votivo' in n or 'cultual' in n: return 'VOTIVO'
    if 'religioso' in n: return 'RELIGIOSO'
    if 'propiedad' in n and 'firma' in n: return 'AMBIGUO'
    if n.startswith('propiedad'): return 'PROPIEDAD'
    if 'firma artes' in n or 'fabricante' in n: return 'FIRMA_ARTESANO'
    if 'comercial' in n or n in ('contable', 'anotacion', 'ind. numero'): return 'COMERCIAL_CONTABLE'
    if 'remitente' in n: return 'CARTA_REMITENTE'
    if 'peso' in n or 'capacidad' in n or n.startswith('indic'): return 'INDIC_METROLOGICA'
    if 'hospitalidad' in n: return 'TESERA_HOSPITALIDAD'
    if n == 'publico': return 'PUBLICO'
    if n == 'falso': return 'FALSO'
    if n == 'signario': return 'ABECEDARIO_SIGNARIO'
    if n == 'multiple': return 'MULTIPLE'
    if n.startswith('indet'): return 'INDET'
    return 'SIN_CLASIFICAR'

def material_norm(v):
    n, _ = limpia(v); return {'': 'SIN_DATO', 'ceramica': 'CERAMICA', 'opus signinum': 'OPUS_SIGNINUM'}.get(n, n.upper().replace(' ', '_'))

ROM = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5, 'vi': 6, 'vii': 7, 'viii': 8, 'ix': 9, 'x': 10}

def frac(mod):
    m = mod or ''
    t = [('primera mitad', 0, 50), ('segunda mitad', 50, 100), ('primer cuarto', 0, 25), ('1er ¼', 0, 25), ('segundo cuarto', 25, 50), ('tercer cuarto', 50, 75),
         ('ultimo cuarto', 75, 100), ('primer tercio', 0, 33), ('segundo tercio', 33, 66), ('ultimo tercio', 66, 100), ('tercer tercio', 66, 100),
         ('comienzos', 0, 25), ('principios', 0, 25), ('inicios', 0, 25), ('mediados', 25, 75), ('med.', 25, 75), ('finales', 75, 100), ('fines', 75, 100),
         ('fin.', 75, 100), ('final', 75, 100)]
    for k, a, b in t:
        if fold(k) in fold(m): return a, b
    return 0, 100

def extremo(txt):
    f = fold(txt).replace('¼', ' cuarto')
    m = re.search(r'\b(i{1,3}|iv|v|vi{0,3}|ix|x)\b(?!\w)', re.sub(r'[.]', ' ', f))
    if not m: return None
    n = ROM[m.group(1)]; a, b = frac(f[:m.start()] if m.start() > 0 else f); s = -100 * n
    return s + a, s + b

def parse_dat(v):
    o = dict(dat_ini='', dat_fin='', dat_metodo='', dat_incierta=0, dat_aprox=0, dat_fuente_RR=0)
    raw = v.strip()
    if raw == '': o['dat_metodo'] = 'vacio'; return o
    f = fold(raw)
    if re.match(r'^(indeterminad|desconocid|imprecis|sin datar)', f): o['dat_metodo'] = 'sin_datacion'; return o
    if re.match(r'^(incierta|insegura)', f): o['dat_incierta'] = 1
    if re.search(r'aprox|^ca\.|en torno', f): o['dat_aprox'] = 1
    if re.search(r'\bd\.?\s?c\b|d\. c\.', f): return {**o, 'dat_metodo': 'sin_parsear_d.C.'}
    nucleo = re.sub(r'^(incierta|insegura)[:.]?\s*|^(tipologia ceramica|paleografica)[:.]?\s*', '', f.split('rodriguez ramos')[0].strip()) if not f.startswith('rodriguez ramos') else ''
    if re.search(r'\(\d{4}|\bsegun\b|considera|\bdata\b|fechad|quesada|fletcher|raddatz|olalla|moncunill|simon|barbera|bonet|panosa|ferrer|probablemente|quiza|\bsi corresponde|anterior|posterior|decadas|corresponde|amortizacion|solo es posible', nucleo) or (nucleo.count(':') > 0) or len(nucleo) > 75:
        return {**o, 'dat_metodo': 'compleja_revisar'}
    if 'rodriguez ramos' in f:
        o['dat_fuente_RR'] = 1; pre = f.split('rodriguez ramos')[0].strip(' .:')
        f = pre if re.search(r'\d|\b(i|ii|iii|iv|v)\b', pre) and not re.fullmatch(r'', pre) else f.split('rodriguez ramos')[1]
    f = re.sub(r'^(incierta|insegura)[:.]?\s*', '', f); f = re.sub(r'^(tipologia ceramica|paleografica)[:.]?\s*', '', f)
    f = re.sub(r'^(aprox\.?|ca\.?|en torno a(l)?|entre)\s*', '', f)
    f = f.split('(')[0] if 'siglo' in f or 's.' in f else f
    f = f.replace('a. c', 'a.c').replace('a. e', 'a.e').replace('a c', 'a.c').replace('ac', 'a.c') if re.search(r'\d\s*a\s*c', f) else f
    f = re.sub(r'\ba\.?\s?e\.?', 'a.c.', f)
    if not re.search(r'\b(siglos?|ss?\.)', f) and not re.search(r'\b(finales|mediados|comienzos|principios|cuarto|mitad|tercio)\b', f):
        if re.search(r'\bantes de\b|\banterior', f): return {**o, 'dat_metodo': 'compleja_revisar'}
        nums = [int(x) for x in re.findall(r'-?\d{2,3}', f)]
        if 'cambio de era' in f: nums = nums + [0]
        if nums and ('a.c' in f or '-' in f):
            nums = [abs(x) for x in nums]; o.update(dat_ini=-max(nums), dat_fin=-min(nums), dat_metodo='anios'); return o
        return {**o, 'dat_metodo': 'sin_parsear'}
    f = re.sub(r'a\.c\.?|\.$', '', f)
    f = f.replace(' a cambio de era', ' - cambio de era').replace(' a mediados', ' - mediados').replace('hasta el cambio de era', ' - cambio de era')
    partes = [p for p in re.split(r'\s*-\s*|\s+y\s+|\s+o\s+|\s+a\s+(?=(?:mediados|finales|principios|comienzos))', f) if p.strip()]
    ivs = []
    for p in partes:
        if 'cambio de era' in p: ivs.append((-1, 0)); continue
        e = extremo(p)
        if e is None: return {**o, 'dat_metodo': 'sin_parsear'}
        ivs.append(e)
    if not ivs: return {**o, 'dat_metodo': 'sin_parsear'}
    ini = min(i[0] for i in ivs[:1] + ivs[-1:]); fin = max(i[1] for i in ivs[:1] + ivs[-1:])
    o.update(dat_ini=ini, dat_fin=fin, dat_metodo='siglos'); return o

DUDA_SOPORTE = {'monetiforme': '¿ponderal, moneda o lingote?', 'pondus o tesera': 'alternativa abierta', 'disco': 'funcion incierta', 'ficha de juego': 'funcion incierta',
                'recipiente, instrumento': 'dos categorias', 'placa-lingote': '¿placa o lingote?', 'laja': 'categoria propia de Hesperia; ¿equivale a lapida?',
                'peso': 'incierto', 'tapadera': '¿recipiente?', 'estela': 'fusionada con lapida por decision propia'}
DUDA_EPIGRAFE = {'AMBIGUO': 'varias lecturas en la ficha', 'FALSO': 'Hesperia lo marca falso: decidir exclusion', 'SIN_DATO': 'campo vacio (distinto de INDET.)',
                 'ABECEDARIO_SIGNARIO': 'categoria propia', 'CARTA_REMITENTE': '¿carta? no es contable', 'TESERA_HOSPITALIDAD': 'categoria propia',
                 'MULTIPLE': 'varios tipos', 'SIN_CLASIFICAR': 'sin regla'}

def dudosa_soporte(v, g):
    n, inc = limpia(v); r = []
    if inc: r.append('valor con ?')
    if n in DUDA_SOPORTE: r.append(DUDA_SOPORTE[n])
    if g in ('SIN_DATO', 'SIN_CLASIFICAR'): r.append('sin dato o sin regla')
    return '; '.join(r)

def dudosa_epigrafe(v, g):
    n, inc = limpia(v); r = []
    if inc: r.append('valor con ?')
    if g in DUDA_EPIGRAFE: r.append(DUDA_EPIGRAFE[g])
    if n in ('anotacion', 'ind. numero', 'indic'): r.append('categoria asignada por mi, valor ambiguo')
    return '; '.join(r)

def normaliza(r):
    """Añade a una fila de metadatos las columnas normalizadas (mismas reglas que el archivo original)."""
    r = dict(r)
    r['soporte_norm'] = limpia(r['soporte'])[0].upper(); r['soporte_incierto'] = int(limpia(r['soporte'])[1]); r['soporte_grupo'] = grupo_soporte(r['soporte'])
    r['tipo_epigrafe_norm'] = limpia(r['tipo_epigrafe'])[0].upper(); r['tipo_epigrafe_incierto'] = int(limpia(r['tipo_epigrafe'])[1]); r['tipo_epigrafe_grupo'] = grupo_epigrafe(r['tipo_epigrafe'])
    r['soporte_dudoso'] = dudosa_soporte(r['soporte'], r['soporte_grupo']); r['tipo_epigrafe_dudoso'] = dudosa_epigrafe(r['tipo_epigrafe'], r['tipo_epigrafe_grupo'])
    ref = r['ref_hesperia'].upper()
    r['autenticidad'] = 'FALSA' if (ref.endswith('FALSA') or fold(r['tipo_epigrafe']) == 'falso') else ('SUSPECTA' if ref.endswith('SUSPECTA') else 'NORMAL')
    r['material_norm'] = material_norm(r['material']); r.update(parse_dat(r['datacion'])); return r

COLS_META_TODAS = COLS_META + ['soporte_norm', 'soporte_incierto', 'soporte_grupo', 'tipo_epigrafe_norm', 'tipo_epigrafe_incierto', 'tipo_epigrafe_grupo',
                               'soporte_dudoso', 'tipo_epigrafe_dudoso', 'autenticidad', 'material_norm', 'dat_ini', 'dat_fin', 'dat_metodo', 'dat_incierta', 'dat_aprox', 'dat_fuente_RR']


# ----------------------------------------------------------------------------------------------- salida
def escribe_csv(ruta, filas, cols):
    buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=cols, extrasaction='ignore', lineterminator='\n'); w.writeheader(); w.writerows(filas)
    open(ruta, 'w', encoding='utf-8', newline='').write(buf.getvalue())

def sha(ruta):
    return hashlib.sha256(open(ruta, 'rb').read()).hexdigest()

def verifica(ruta):
    esperada = SHA_ESPERADA[os.path.basename(ruta)]; obtenida = sha(ruta)
    print(f'{os.path.basename(ruta)}: {"COINCIDE con el archivo del artículo" if obtenida == esperada else "NO coincide (Hesperia ha cambiado, o el programa no reproduce algún campo)"}  sha256 {obtenida[:16]}…')
    return obtenida == esperada


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--cache', default=None); ap.add_argument('--solo-listado', action='store_true')
    ap.add_argument('--verificar', action='store_true'); ap.add_argument('--pausa', type=float, default=0.6); a = ap.parse_args()
    if a.verificar:
        ok = all(verifica(r) for r in (SALIDA_TEXTO, SALIDA_META) if os.path.exists(r)); return 0 if ok else 1
    C = (lambda nombre: os.path.join(a.cache, nombre)) if a.cache else (lambda nombre: None)
    # 1. listado y lengua
    todo = listado(decodifica(http(SEARCH, dict(FORM), C('listado_TODO.html')))); print(f'Listado completo: {len(todo)} fichas')
    lengua = {}
    for lg in LENGUAS:
        d = dict(FORM); d['lengua'] = lg
        for f in listado(decodifica(http(SEARCH, d, C(f'listado_lengua_{re.sub(r"[^A-Za-z]", "", lg)}.html')))):
            lengua.setdefault((f['ref_hesperia'], f['id_ficha']), []).append(lg.strip('^'))
        time.sleep(a.pausa)
    for f in todo: f['lengua_filtro'] = '+'.join(lengua.get((f['ref_hesperia'], f['id_ficha']), [])) or '(sin lengua asignada)'
    iber = [f for f in todo if f['lengua_filtro'] == 'IBERICO']
    autenticas = [f for f in iber if not re.search(r'FALSA|SUSPECTA|LATINA', f['ref_hesperia'])]
    escribe_csv(SALIDA_TEXTO, autenticas, COLS_TEXTO); print(f'Ibéricas: {len(iber)}; auténticas: {len(autenticas)} -> {SALIDA_TEXTO}'); verifica(SALIDA_TEXTO)
    if a.solo_listado: return 0
    # 2. fichas
    filas = []
    for i, f in enumerate(iber, 1):
        idf = f['id_ficha']; pest = {}
        for k, pagina in PESTANAS.items():
            pest[k] = campos(decodifica(http(f'{BASE}{pagina}.php?file=file_100.php&filtrar=&valor=&id={idf}', None, C(f'fichas/{idf}_{pagina}.html'))))
            if not (a.cache and os.path.exists(C(f'fichas/{idf}_{pagina}.html'))): time.sleep(a.pausa)
        r = {'id_ficha': idf, 'ref_hesperia': pest['g'].get('ref_hesperia', f['ref_hesperia'])}
        for col, (k, campo) in ORIGEN_META.items(): r[col] = pest[k].get(campo, '')
        filas.append(normaliza(r))
        if i % 100 == 0: print(f'  fichas {i}/{len(iber)}', flush=True)
    escribe_csv(SALIDA_META, filas, COLS_META_TODAS); print(f'Metadatos: {len(filas)} fichas -> {SALIDA_META}'); verifica(SALIDA_META)
    return 0


if __name__ == '__main__':
    sys.exit(main())
