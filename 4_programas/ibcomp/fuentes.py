"""Lectura de las fuentes léxicas. Especificación: «Fuentes léxicas y su tratamiento».

Todas las fuentes están en 1_fuentes_lexicas/ (véase allí la ficha de cada una). Un DICCIONARIO es aquí un objeto con
  nombre     etiqueta de la fuente
  formas     lista ordenada de formas reducidas distintas (clases de sonidos)
  candidatas función que, dada una unidad ibérica, devuelve las formas cuyo significado coincide con alguno de sus términos
"""
import csv, json, os, re, glob, unicodedata
from collections import defaultdict
from .clases import reducida, red_afi, red_ib, red_chan
from .normalizadores import NORM, n_rom, n_ger, n_cy, n_fi, n_hbs, n_tr_apertium, n_eu, norm_control, red_control

RAIZ = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '1_fuentes_lexicas'))
csv.field_size_limit(10 ** 9)
LMIN, LMAX = 2, 12          # longitud admitida de una forma reducida, en clases de sonidos

def terminos_de_glosa(glosa):
    """Parte una glosa inglesa en términos: se quitan los paréntesis, se corta por comas y puntos y coma, se pasa a minúsculas y se quita «to», «a», «an», «the» iniciales."""
    return {re.sub(r'^(to|a|an|the) ', '', e.strip().lower()).strip(' .') for e in re.split(r'[,;]', re.sub(r'\(.*?\)', '', glosa))}

class Diccionario:
    def __init__(self, nombre, entradas, terminos='terminos_en', sinsets=None):
        self.nombre = nombre; self.entradas = dict(entradas); self.formas = sorted(self.entradas); self.terminos = terminos; self.sinsets = sinsets
        self.por_longitud = defaultdict(list); self._cache = {}
        for f in self.formas: self.por_longitud[len(f)].append(f)
    def candidatas(self, unidad, terminos=None):
        T = frozenset(unidad.get(terminos or self.terminos) or [])
        if not T: return []
        if T not in self._cache: self._cache[T] = self._busca(T)
        return self._cache[T]
    def _busca(self, T):
        if self.sinsets is not None:                                  # WordNet: los términos castellanos se pasan a conceptos (synsets)
            S = set().union(*[self.sinsets.get(t, set()) for t in T])
            return [f for f in self.formas if self.entradas[f] & S] if S else []
        return [f for f in self.formas if self.entradas[f] & T]

def _acepta(w):
    return ' ' not in w and w.isalpha()

# ---------------------------------------------------------------- ibérico
def unidades_plomos():
    return json.load(open(f'{RAIZ}/iberico/unidades_plomos.json', encoding='utf-8'))['unidades']

def unidades_numerales():
    return json.load(open(f'{RAIZ}/iberico/unidades_numerales.json', encoding='utf-8'))['unidades']

PRESTAMOS_LATINOS = ('bale', 'koŕta', 'saltu', 'oŕtin')       # primera forma de las cuatro unidades propuestas como préstamos latinos

ZONAS = [('Narbonense–Rosellón', {'AUD', 'HER', 'PYO', 'HGA'}), ('Cataluña', {'GI', 'B', 'L'}), ('Ebro–Castellón', {'T', 'TE', 'Z', 'HU', 'CS'}), ('Valencia', {'V'}), ('Sudeste', {'A', 'MU', 'AB'})]

def hesperia():
    """Corpus ibérico: lista de fichas con su sigla, zona, si es plomo, signario y formas reducidas distintas.

    Una palabra es cada tramo entre separadores del texto, tras quitar [ ] ( ) + - ? y los signos de subrayado o punto
    inferior; se descartan los tramos con cifras o con tres o más signos numerales seguidos (i, v, x, l, π), y las
    formas reducidas de menos de 2 o más de 12 clases.
    """
    if not all(os.path.exists(f'{RAIZ}/iberico/{n}') for n in ('hesperia_iberico_1599.csv', 'hesperia_metadatos.csv')) and os.path.exists(f'{RAIZ}/iberico/hesperia_formas_reducidas.json'):
        # Repositorio público: lista mínima derivada (formas ya reducidas por ficha, sin el texto). Da el mismo resultado.
        return [dict(f, formas=set(f['formas'])) for f in json.load(open(f'{RAIZ}/iberico/hesperia_formas_reducidas.json', encoding='utf-8'))['fichas']]
    for nombre in ('hesperia_iberico_1599.csv', 'hesperia_metadatos.csv'):
        if not os.path.exists(f'{RAIZ}/iberico/{nombre}'):
            raise FileNotFoundError(f'Falta {RAIZ}/iberico/{nombre}: el corpus de Hesperia no se redistribuye; genérelo con '
                                    f'python3 1_fuentes_lexicas/iberico/descargar_hesperia.py (véase 1_fuentes_lexicas/LEEME_fuentes.md).')
    meta = {r['ref_hesperia']: r for r in csv.DictReader(open(f'{RAIZ}/iberico/hesperia_metadatos.csv', encoding='utf-8-sig'))}
    fichas = []
    for r in csv.DictReader(open(f'{RAIZ}/iberico/hesperia_iberico_1599.csv', encoding='utf-8-sig')):
        m = meta.get(r['ref_hesperia'], {}); pref = re.match(r'[A-Z]+', r['ref_hesperia']).group(0)
        formas = set()
        for t in re.split(r'[^\wśŕḿ]+', unicodedata.normalize('NFC', re.sub(r'[\[\]\(\)\+\-\?̲̱̣]', '', r['texto_crudo'])).lower()):
            if not t or re.search(r'\d|[ivxlπ]{3,}', t): continue
            x = red_ib(t)
            if LMIN <= len(x) <= LMAX: formas.add(x)
        fichas.append(dict(sigla=r['ref_hesperia'], zona=next((n for n, s in ZONAS if pref in s), None), plomo='PLOMO' in (m.get('material') or '').upper(),
                           plomo_amplio='plomo' in ' '.join(str(v) for v in m.values()).lower(), signario=(m.get('signario') or '?').upper(), formas=formas))
    return fichas

# ---------------------------------------------------------------- Wikcionario
_WIK = ('kaikki_control_20lenguas_2026-11-17.tsv', 'kaikki_control_silaba_simple_16lenguas_2026-11-18.tsv')
_EXCLUIDAS = ('name', 'character', 'suffix', 'prefix', 'romanization')

def wikcionario_lemas():
    """lengua → palabra → términos de glosa (sin reducir). Entradas del Wikcionario inglés, extracción de kaikki.org."""
    G = defaultdict(lambda: defaultdict(set))
    for fich in _WIK:
        for linea in open(f'{RAIZ}/wikcionario/{fich}', encoding='utf-8'):
            p = linea.rstrip('\n').split('\t')
            if len(p) != 4 or p[0] not in NORM or p[2] in _EXCLUIDAS: continue
            w = p[1].lower()
            if _acepta(w): G[p[0]][w] |= terminos_de_glosa(p[3])
    return G

def wikcionario():
    """lengua → Diccionario (forma reducida → términos de glosa)."""
    D = defaultdict(lambda: defaultdict(set))
    for l, lemas in wikcionario_lemas().items():
        for w, g in lemas.items():
            r = reducida(NORM[l](w))
            if LMIN <= len(r) <= LMAX: D[l][r] |= g
    return {l: Diccionario(l, d) for l, d in D.items()}

def _abre_formas():
    """Abre el archivo de formas flexionadas. Se distribuye comprimido (.gz) porque
    sin comprimir supera el tamaño que admite GitHub. / Opens the inflected-forms file (distributed gzipped)."""
    import gzip, os
    base = f'{RAIZ}/wikcionario/kaikki_formas_26lenguas_2026-11-18.tsv'
    return gzip.open(base + '.gz', 'rt', encoding='utf-8')


def formas_flexionadas(G):
    """lengua → lema → formas flexionadas (Wikcionario), más la tabla de formas verbales vascas."""
    FM = defaultdict(lambda: defaultdict(set)); lema = None; lengua_lema = None
    for linea in _abre_formas():
        p = linea.rstrip('\n').split('\t')
        if len(p) != 3: continue
        if p[1] == 'L': lengua_lema, lema = p[0], p[2].lower()
        elif lema and p[0] == lengua_lema and p[0] in G and lema in G[p[0]]:   # la forma se admite solo si su lengua es la del lema vigente: así no hay cruces entre lenguas aunque el archivo mezcle líneas
            f = p[2].lower()
            if f.isalpha() and ' ' not in f: FM[p[0]][lema].add(f)
    for r in csv.DictReader(open(f'{RAIZ}/wikcionario/wikcionario_eu_formas_verbales_v1.csv', encoding='utf-8')):
        if r['lema'] in G['Basque']: FM['Basque'][r['lema']].add(r['forma'].lower())
    return FM

# ---------------------------------------------------------------- euskera: otras capas
def trask_reconstruido():
    D = defaultdict(set)
    for e in json.load(open(f'{RAIZ}/euskera/trask_formas_glosas.json', encoding='utf-8')):
        for f in e['proto']:
            if re.search(r'[VC]', f): continue          # V y C son vocal y consonante indeterminadas en la notación: la forma no se usa
            r = reducida(n_eu(re.sub(r'[^A-Za-zñ\[\]]', '', f).lower()))
            if LMIN <= len(r) <= LMAX: D[r] |= {g.lower() for gl in e['glosas'] for g in terminos_de_glosa(gl)}
    return Diccionario('Euskera reconstruido (Trask 2008)', D)

def azkue():
    D = defaultdict(set)
    for r_ in csv.DictReader(open(f'{RAIZ}/euskera/azkue_lemas_equivalentes.csv', encoding='utf-8')):
        w = r_['lema'].lower()
        if not _acepta(w): continue
        r = reducida(n_eu(w))
        if LMIN <= len(r) <= LMAX: D[r] |= {x.strip().lower() for x in re.split(r'[,;]', r_['equivalentes']) if x.strip()}
    return Diccionario('Euskera, Azkue (1905-1906)', D, terminos='terminos_es')

def opendata():
    D = defaultdict(set)
    for linea in list(open(f'{RAIZ}/euskera/opendata_euskadi_eu_es_v1.tsv', encoding='utf-8'))[1:]:
        p = linea.rstrip('\n').split('\t')
        if len(p) < 2: continue
        w = p[0].lower(); es = p[1].lower().strip()
        if not _acepta(w) or not es: continue
        x = reducida(n_eu(w))
        if LMIN <= len(x) <= LMAX: D[x].add(es)
    return Diccionario('Euskera, Open Data Euskadi', D, terminos='terminos_es')

# ---------------------------------------------------------------- WordNet (Multilingual Central Repository 3.0)
def wordnet():
    """Diccionarios enlazados por conceptos: las candidatas son las palabras de los conceptos en que figura algún término castellano de la unidad."""
    def lee(l):
        d = defaultdict(set)
        for linea in open(f'{RAIZ}/wordnet_mcr/wn-data-{l}.tab', encoding='utf-8'):
            p = linea.rstrip('\n').split('\t')
            if len(p) == 3 and p[1].endswith('lemma'): d[p[0]].add(p[2].lower().replace('_', ' '))
        return d
    es2syn = defaultdict(set)
    for s, ls in lee('spa').items():
        for w in ls: es2syn[w].add(s)
    out = {}
    for nombre, cod, norm in (('Euskera, WordNet', 'eus', n_eu), ('Catalán, WordNet', 'cat', lambda w: n_rom(w, 'ca')), ('Gallego, WordNet', 'glg', lambda w: n_rom(w, 'gl')), ('Castellano, WordNet', 'spa', lambda w: n_rom(w, 'es'))):
        fs = defaultdict(set)
        for s, ls in lee(cod).items():
            for w in ls:
                if not _acepta(w): continue
                x = reducida(norm(w))
                if LMIN <= len(x) <= LMAX: fs[x].add(s)
        out[nombre] = Diccionario(nombre, fs, terminos='terminos_es', sinsets=es2syn)
    return out

# ---------------------------------------------------------------- Apertium (diccionarios bilingües)
_lem = lambda x: re.sub(r'<[^>]*>', '', re.sub(r'<b\s*/>', ' ', x)).strip().lower().replace('_', ' ')          # primero <b/> → espacio; después se quitan las demás etiquetas
APERTIUM_ES = [('Euskera', 'apertium-eu-es.eu-es.dix', 'l', n_eu), ('Portugués', 'apertium-es-pt.es-pt.dix', 'r', lambda w: n_rom(w, 'pt')), ('Gallego', 'apertium-es-gl.es-gl.dix', 'r', lambda w: n_rom(w, 'gl')),
               ('Aragonés', 'apertium-spa-arg.spa-arg.dix', 'r', lambda w: n_rom(w, 'an')), ('Asturiano', 'apertium-spa-ast.spa-ast.dix', 'r', lambda w: n_rom(w, 'ast')), ('Occitano', 'apertium-oc-es.oc-es.dix', 'l', lambda w: n_rom(w, 'oc')),
               ('Francés', 'apertium-fra-spa.fra-spa.dix', 'l', lambda w: n_rom(w, 'fr')), ('Italiano', 'apertium-spa-ita.spa-ita.dix', 'r', lambda w: n_rom(w, 'it')), ('Rumano', 'apertium-es-ro.es-ro.dix', 'r', lambda w: n_rom(w, 'ro'))]
APERTIUM_EN = [('Euskera', 'apertium-eu-en.eu-en.dix', 'l', n_eu), ('Castellano', 'apertium-eng-spa.eng-spa.dix', 'r', lambda w: n_rom(w, 'es')), ('Catalán', 'apertium-eng-cat.eng-cat.dix', 'r', lambda w: n_rom(w, 'ca')),
               ('Alemán', 'apertium-eng-deu.eng-deu.dix', 'r', n_ger), ('Galés', 'apertium-cym-eng.cym-eng.dix', 'l', n_cy), ('Finés', 'apertium-fin-eng.fin-eng.dix', 'l', n_fi), ('Serbocroata', 'apertium-hbs-eng.hbs-eng.dix', 'l', n_hbs),
               ('Islandés', 'apertium-isl-eng.isl-eng.dix', 'l', n_ger), ('Sueco', 'apertium-swe-eng.swe-eng.dix', 'l', n_ger), ('Turco', 'apertium-tr-en.tr-en.dix', 'l', n_tr_apertium)]

def apertium(puente):
    """Diccionarios bilingües de Apertium con el castellano ('es') o el inglés ('en') como lengua puente. `lado`: en qué lado del par está la lengua comparada."""
    lista, clave = (APERTIUM_ES, 'terminos_es') if puente == 'es' else (APERTIUM_EN, 'terminos_en'); out = {}
    for nombre, fich, lado, norm in lista:
        D = defaultdict(set); t = re.sub(r'<!--.*?-->', '', open(f'{RAIZ}/apertium/{fich}', encoding='utf-8', errors='replace').read(), flags=re.S)          # sin los comentarios del XML
        for l, r in re.findall(r'<l>(.*?)</l>\s*<r>(.*?)</r>', t, re.S):
            a, b = _lem(l), _lem(r); w, eq = (a, b) if lado == 'l' else (b, a); w = w.lower(); eq = eq.lower().strip()
            if not _acepta(w) or not eq: continue
            x = reducida(norm(w))
            if LMIN <= len(x) <= LMAX: D[x].add(eq)
        etiqueta = f'{nombre}, Apertium ({"castellano" if puente == "es" else "inglés"})'; out[etiqueta] = Diccionario(etiqueta, D, terminos=clave)
    return out

# ---------------------------------------------------------------- NorthEuraLex y numerales de Chan
def northeuralex():
    """→ (léxico: id de lengua → conjunto de formas reducidas; lenguas: id → ficha con Name y Family)."""
    lang = {r['ID']: r for r in csv.DictReader(open(f'{RAIZ}/northeuralex/languages.csv', encoding='utf-8'))}; LEX = defaultdict(set)
    for r in csv.DictReader(open(f'{RAIZ}/northeuralex/forms.csv', encoding='utf-8')):
        x = red_afi(r['Segments'].split())
        if LMIN <= len(x) <= LMAX: LEX[r['Language_ID']].add(x)
    return LEX, lang

def chan():
    """→ (formas: id de variedad → valor → lista de formas reducidas, en el orden de la base; lenguas: id → ficha)."""
    lang = {r['ID']: r for r in csv.DictReader(open(f'{RAIZ}/numerales_chan/languages.csv', encoding='utf-8'))}; F = defaultdict(lambda: defaultdict(list))
    for r in csv.DictReader(open(f'{RAIZ}/numerales_chan/forms.csv', encoding='utf-8')):
        x = red_chan(r['Form'])
        if x: F[r['Language_ID']][r['Parameter_ID']].append(x)
    return F, lang

# ---------------------------------------------------------------- lenguas de control
CONTROL = {'Umbrian': 'umbro', 'Gothic': 'gótico', 'Cornish': 'córnico', 'Dalmatian': 'dálmata', 'Etruscan': 'etrusco', 'Sumerian': 'sumerio'}

def lexico_control(lengua, lmin=3, lmax=10):
    """Palabras elegibles de una lengua de control: palabra normalizada → términos de glosa.

    Entradas que no son remisiones, de clase noun, verb, adj, adv, num o pron; forma = romanización si existe;
    al menos un término de glosa de una o dos palabras; forma reducida de `lmin` a `lmax` clases.
    """
    LEXT = defaultdict(set)
    for linea in open(f'{RAIZ}/wikcionario/kaikki_lenguas_de_control_2026-11-19.tsv', encoding='utf-8'):
        p = linea.rstrip('\n').split('\t')
        if len(p) != 6 or p[0] != lengua or p[4] != '0' or p[2] not in ('noun', 'verb', 'adj', 'adv', 'num', 'pron'): continue
        f = (p[3].split('|')[0] if p[3] else p[1]).strip(); w = norm_control(lengua, f)
        if not w or not re.fullmatch(r'[a-zñð]+', w): continue
        if not lmin <= len(red_control(w)) <= lmax: continue
        T = set()
        for g in p[5].split(' || '):
            if re.match(r'(?i)(see |the meaning|alternative|romanization|obsolete|misspelling)', g) or 'uncertain' in g.lower(): continue
            T |= {t for t in terminos_de_glosa(g) if t and re.fullmatch(r'[a-z]+( [a-z]+)?', t)}
        if T: LEXT[w] |= T
    return LEXT
