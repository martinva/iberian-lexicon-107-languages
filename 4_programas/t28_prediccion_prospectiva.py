"""Declaración 13: predicción prospectiva del significado desde el euskera, juzgada a ciegas (segundo artículo).

Fase 1 (`preparar`): construye (a) las fichas despojadas de las 36 unidades (regla mecánica sobre FICHAS_A_CIEGAS.md),
(b) las fichas mecánicas de las 11 palabras de Hesperia, (c) los cuatro significados candidatos por palabra (lema vasco,
gallego y latino más próximos en todo su diccionario del Wikcionario, y un lema vasco al azar), barajados con letras
A–D, y (d) la clave con su SHA-256. Escribe 2_criterios/jurado/prospectiva/{FICHAS_prospectiva.md, CLAVE_prospectiva.tsv,
clave_sha256.txt}. La clave no se envía al jurado; su SHA-256 se publica antes de enviar las fichas.
Fase 2 (`puntuar`): lee las respuestas (respuestas/*.tsv: código, letra) y da el recuento por juez y por mayoría,
con la binomial frente a 1/4 (o 1/5 si se admite «ninguno»).
Uso / Usage:  python3 t28_prediccion_prospectiva.py preparar | puntuar
"""
import csv, hashlib, json, math, os, re, sys, unicodedata
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import reducida
from ibcomp.distancia import dist
from ibcomp.pruebas import generador

AQUI = os.path.dirname(__file__); RAIZ = os.path.join(AQUI, '..'); IB = os.path.join(RAIZ, '1_fuentes_lexicas', 'iberico')
JUR = os.path.join(RAIZ, '2_criterios', 'jurado'); SAL = os.path.join(JUR, 'prospectiva')
# Palabras de Hesperia (declaración 13): 21 candidatas por recuento, menos los antropónimos y la variante de unidad excluidos a mano antes de calcular.
HESPERIA = ['tike', 'ŕuba', 'banḿi', 'ebanen', 'baka', 'kaka', 'eŕiar', 'baika', 'ḿiata', 'balkei', 'beii']
EXCLUIDAS = ['śaleitaŕtin', 'ḿltunśor', 'balkar', 'bilo', 'luki', 'oskar', 'baitolo', 'ildiŕ', 'aiunin', 'iustir']
# Regla de despojo (mecánica, publicada aquí): (1) dentro de cada oración se sustituye «que el autor interpreta como
# “X”» por «otro término del texto»; (2) se quita toda oración que aún contenga alguna de las cadenas de DESPOJO
# (propuestas del autor, valores, y cualquier mención de una lengua viva, romance o de un préstamo).
DESPOJO = ('autor', 'propuesto', 'propone', 'propuesta', 'El valor', 'ponen «', 'traducido', 'lengua viva', 'lengua romance', 'préstamo', 'prerromana')

def oraciones(t):
    return [o for o in re.split(r'(?<=[\.;])\s+', t.strip()) if o]

def despoja(prueba):
    t = re.sub(r'(un término |la palabra |un elemento )?que el autor interpreta como «[^»]+»', 'otro término del texto', prueba)
    out = [o for o in oraciones(t) if not any(c in o for c in DESPOJO)]
    return ' '.join(out) if out else '(solo se da el tipo del término)'

def fichas_unidades():
    """[(código, tipo, ficha despojada, id de unidad)] para las 36 unidades (sin los controles T)."""
    clave = {r['código']: r['unidad'] for r in csv.DictReader(open(os.path.join(JUR, 'respuestas', 'CLAVE.tsv'), encoding='utf-8'), delimiter='\t')}
    out = []
    for linea in open(os.path.join(JUR, 'FICHAS_A_CIEGAS.md'), encoding='utf-8'):
        m = re.match(r'\| (U\d\d) \| ([^|]+) \| (.+) \|\s*$', linea)
        if m and not clave[m.group(1)].startswith('T'):
            out.append((m.group(1), m.group(2).strip(), despoja(m.group(3).strip()), clave[m.group(1)]))
    return out

def hesperia_tokens():
    meta = {r['ref_hesperia']: r for r in csv.DictReader(open(os.path.join(IB, 'hesperia_metadatos.csv'), encoding='utf-8'))}
    F = sorted({e['formante'] for e in json.load(open(os.path.join(IB, 'formantes_onomasticos_rodriguez_ramos_2014.json'), encoding='utf-8'))}, key=len, reverse=True)
    U = {reducida(f) for u in fuentes.unidades_plomos() + fuentes.unidades_numerales() for f in u['formas']}
    def clase(w):
        if w is None: return 'límite del texto'
        if re.search(r'\d|[ivxlπ]{3,}', w): return 'cifra'
        if reducida(w) in U: return 'unidad conocida'
        for a in F:
            if w.startswith(a) and any(w[len(a):].startswith(b) for b in F): return 'nombre de persona'
        return 'otra palabra'
    docs = []
    for r in csv.DictReader(open(os.path.join(IB, 'hesperia_iberico_1599.csv'), encoding='utf-8')):
        t = unicodedata.normalize('NFC', re.sub(r'[\[\]\(\)\+\-\?̲̱̣]', '', r['texto_crudo'])).lower()
        toks = [w for w in re.split(r'[^\wśŕḿ]+', t) if w]
        docs.append((r['ref_hesperia'], meta.get(r['ref_hesperia'], {}), toks))
    return docs, clase

def fichas_hesperia():
    docs, clase = hesperia_tokens(); out = []
    for i, w in enumerate(HESPERIA):
        aps = []
        for ref, m, toks in docs:
            for k, t in enumerate(toks):
                if t == w:
                    sop = (m.get('soporte_norm') or m.get('material') or 'soporte no indicado').lower()
                    pos = 'inicio' if k == 0 else ('final' if k == len(toks) - 1 else 'interior')
                    aps.append(f"{sop}, {pos} del texto ({len(toks)} palabras), precedida de {clase(toks[k - 1] if k else None)} y seguida de {clase(toks[k + 1] if k + 1 < len(toks) else None)}")
        out.append((f'H{i + 1:02d}', 'palabra de la lengua antigua', f"Palabra de {len(w)} signos, {len(aps)} apariciones: " + '; '.join(aps) + '.', w))
    return out

def vecino(d, f):
    """Lema del diccionario `d` (Diccionario) a menor distancia de la forma reducida `f`; empate → orden alfabético."""
    return min(d.formas, key=lambda x: (dist(f, x), x))

def glosa(d, forma):
    return '; '.join(sorted(d.entradas[forma])[:3])

def preparar():
    os.makedirs(SAL, exist_ok=True)
    W = fuentes.wikcionario(); D = {'euskera': W['Basque'], 'gallego': W['Galician'], 'latín': W['Latin']}
    unidades = {u['id']: u for u in fuentes.unidades_plomos() + fuentes.unidades_numerales()}
    fichas = fichas_unidades() + fichas_hesperia(); filas = []; clave = []
    for cod, tipo, texto, ident in fichas:
        forma = unidades[ident]['formas'][0] if ident in unidades else ident; f = reducida(forma)
        cands = {l: vecino(d, f) for l, d in D.items()}
        rnd = generador('prospectiva', 'azar', cod); cands['azar'] = rnd.choice(D['euskera'].formas)
        sig = {l: glosa(D['euskera'] if l == 'azar' else D[l], c) for l, c in cands.items()}
        orden = list(sig); generador('prospectiva', 'orden', cod).shuffle(orden)
        letras = dict(zip('ABCD', orden))
        filas.append((cod, tipo, texto, {L: sig[l] for L, l in letras.items()}))
        clave.append(dict(codigo=cod, palabra=forma, **{f'letra_{l}': L for L, l in letras.items()}, **{f'lema_{l}': cands[l] for l in cands}, **{f'significado_{l}': sig[l] for l in sig}))
    with open(os.path.join(SAL, 'FICHAS_prospectiva.md'), 'w', encoding='utf-8') as g:
        g.write('# Fichas para la predicción prospectiva (declaración 13)\n\nCada ficha describe la distribución de un término de una lengua antigua no descifrada, sin dar el término ni ninguna lengua, y ofrece cuatro significados candidatos (A–D). Hay %d fichas.\n\n| Código | Tipo | Distribución | A | B | C | D |\n|---|---|---|---|---|---|---|\n' % len(filas))
        for cod, tipo, texto, L in filas: g.write(f"| {cod} | {tipo} | {texto} | {L['A']} | {L['B']} | {L['C']} | {L['D']} |\n")
    with open(os.path.join(SAL, 'CLAVE_prospectiva.tsv'), 'w', encoding='utf-8', newline='') as g:
        w = csv.DictWriter(g, fieldnames=list(clave[0]), delimiter='\t'); w.writeheader(); w.writerows(clave)
    h = hashlib.sha256(open(os.path.join(SAL, 'CLAVE_prospectiva.tsv'), 'rb').read()).hexdigest()
    open(os.path.join(SAL, 'clave_sha256.txt'), 'w').write(h + '  CLAVE_prospectiva.tsv\n'); print('fichas', len(filas), 'SHA-256 de la clave', h)

def puntuar():
    clave = {r['codigo']: r for r in csv.DictReader(open(os.path.join(SAL, 'CLAVE_prospectiva.tsv'), encoding='utf-8'), delimiter='\t')}
    letra_a_lengua = {c: {r[f'letra_{l}']: l for l in ('euskera', 'gallego', 'latín', 'azar')} for c, r in clave.items()}
    R = {}
    for p in sorted(os.listdir(os.path.join(SAL, 'respuestas'))):
        if p.endswith('.tsv'):
            R[p[:-4]] = {r['codigo']: r['letra'].strip().upper() for r in csv.DictReader(open(os.path.join(SAL, 'respuestas', p), encoding='utf-8'), delimiter='\t')}
    def binom_p(k, n, p): return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))
    res = {}
    for grupo, cods in (('unidades', [c for c in clave if c.startswith('U')]), ('unidades sin U10', [c for c in clave if c.startswith('U') and c != 'U10']), ('hesperia', [c for c in clave if c.startswith('H')])):
        res[grupo] = {}
        for juez, resp in list(R.items()) + [('mayoría', None)]:
            cnt = Counter()
            for c in cods:
                if resp is None:
                    votos = Counter(letra_a_lengua[c].get(R[j].get(c, ''), 'ninguno') for j in R); l, n = votos.most_common(1)[0]
                    cnt[l if n >= 2 else 'sin mayoría'] += 1
                else: cnt[letra_a_lengua[c].get(resp.get(c, ''), 'ninguno')] += 1
            n = len(cods); ning = cnt.get('ninguno', 0) + cnt.get('sin mayoría', 0); p0 = 1 / 5 if ning else 1 / 4
            res[grupo][juez] = dict(n=n, **cnt, p_binomial={l: round(binom_p(cnt.get(l, 0), n, p0), 4) for l in ('euskera', 'gallego', 'latín', 'azar')})
            print(grupo, juez, dict(cnt), 'p(euskera ≥ k):', res[grupo][juez]['p_binomial']['euskera'])
    json.dump(res, open(os.path.join(RAIZ, 'resultados', 't28_prediccion_prospectiva.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


# ---------------------------------------------------------------------------
# Versión 2 (declaración 15). Correcciones de la auditoría sobre la versión 1:
# (a) nulo prefijado: el encargo ofrece «ninguno», luego la binomial usa SIEMPRE p0 = 1/5 (en la v1 dependía del
#     resultado observado); (b) ningún candidato puede tener una glosa que mencione una lengua (fuga de la ficha U10,
#     «basque»); (c) los cuatro candidatos de una ficha deben tener glosas distintas (duplicados en U29 y H04);
# (d) las fichas que el despojo dejaba vacías (U14, U37, U40) llevan el recuento mecánico de apariciones en el corpus.
# Semillas nuevas ('prospectiva2'). Salida en 2_criterios/jurado/prospectiva_v2/. La versión 1 se conserva como piloto.
SAL2 = os.path.join(JUR, 'prospectiva_v2')
MENCIONA_LENGUA = re.compile(r'\b(basque|iberian|iberic|euskara|euskera|vasconic|aquitanian|galician|latin|spanish|'
                             r'french|occitan|gascon|romance|portuguese|castilian|celtic|celtiberian|gaulish)\b', re.I)
# Ampliación (antes de enviar): tampoco es elegible una glosa metalingüística, que remite a otra forma u ortografía
# en lugar de dar un significado («spelling of X», «abbreviation of X», «singular of X», «reintegrationist»...).
GLOSA_META = re.compile(r'\b(spelling|abbreviation|inflection|misspelling|singular|plural|form|indicative|imperative|'
                        r'participle)\s+of\b|\breintegrationist\b', re.I)

def apariciones_en_hesperia(formas):
    """Número de textos de Hesperia en que aparece alguna de las formas (reducidas) de la unidad."""
    docs, _ = hesperia_tokens(); R = {reducida(f) for f in formas}
    return sum(any(reducida(t) in R for t in toks) for _, _, toks in docs)

def preparar2():
    os.makedirs(SAL2, exist_ok=True)
    W = fuentes.wikcionario(); D = {'euskera': W['Basque'], 'gallego': W['Galician'], 'latín': W['Latin']}
    unidades = {u['id']: u for u in fuentes.unidades_plomos() + fuentes.unidades_numerales()}
    fichas = fichas_unidades() + fichas_hesperia(); filas = []; clave = []
    for cod, tipo, texto, ident in fichas:
        if texto == '(solo se da el tipo del término)' and ident in unidades:
            n_ap = apariciones_en_hesperia(unidades[ident]['formas'])
            texto = 'Aparece en un texto.' if n_ap == 1 else f"Aparece en {n_ap} textos."
        forma = unidades[ident]['formas'][0] if ident in unidades else ident; f = reducida(forma)
        cands = {}; usadas = set()
        def apta(d, lema):
            g = glosa(d, lema)
            return bool(g) and not MENCIONA_LENGUA.search(g) and not GLOSA_META.search(g) and g.lower() not in usadas
        for l in ('euskera', 'gallego', 'latín'):
            d = D[l]
            lema = min((x for x in d.formas if apta(d, x)), key=lambda x: (dist(f, x), x))
            cands[l] = lema; usadas.add(glosa(d, lema).lower())
        rnd = generador('prospectiva2', 'azar', cod)
        while True:
            x = rnd.choice(D['euskera'].formas)
            if apta(D['euskera'], x): cands['azar'] = x; usadas.add(glosa(D['euskera'], x).lower()); break
        sig = {l: glosa(D['euskera'] if l == 'azar' else D[l], c) for l, c in cands.items()}
        orden = list(sig); generador('prospectiva2', 'orden', cod).shuffle(orden)
        letras = dict(zip('ABCD', orden))
        filas.append((cod, tipo, texto, {L: sig[l] for L, l in letras.items()}))
        clave.append(dict(codigo=cod, palabra=forma, **{f'letra_{l}': L for L, l in letras.items()}, **{f'lema_{l}': cands[l] for l in cands}, **{f'significado_{l}': sig[l] for l in sig}))
    with open(os.path.join(SAL2, 'FICHAS_prospectiva_v2.md'), 'w', encoding='utf-8') as g:
        g.write('# Fichas para la predicción prospectiva, versión 2 (declaración 15)\n\nCada ficha describe la distribución de un término de una lengua antigua no descifrada, sin dar el término ni ninguna lengua, y ofrece cuatro significados candidatos (A–D). Hay %d fichas.\n\n| Código | Tipo | Distribución | A | B | C | D |\n|---|---|---|---|---|---|---|\n' % len(filas))
        for cod, tipo, texto, L in filas: g.write(f"| {cod} | {tipo} | {texto} | {L['A']} | {L['B']} | {L['C']} | {L['D']} |\n")
    with open(os.path.join(SAL2, 'CLAVE_prospectiva_v2.tsv'), 'w', encoding='utf-8', newline='') as g:
        w = csv.DictWriter(g, fieldnames=list(clave[0]), delimiter='\t'); w.writeheader(); w.writerows(clave)
    h = hashlib.sha256(open(os.path.join(SAL2, 'CLAVE_prospectiva_v2.tsv'), 'rb').read()).hexdigest()
    open(os.path.join(SAL2, 'clave_sha256.txt'), 'w').write(h + '  CLAVE_prospectiva_v2.tsv\n'); print('fichas', len(filas), 'SHA-256 de la clave', h)

def puntuar2():
    clave = {r['codigo']: r for r in csv.DictReader(open(os.path.join(SAL2, 'CLAVE_prospectiva_v2.tsv'), encoding='utf-8'), delimiter='\t')}
    letra_a_lengua = {c: {r[f'letra_{l}']: l for l in ('euskera', 'gallego', 'latín', 'azar')} for c, r in clave.items()}
    R = {}
    for p in sorted(os.listdir(os.path.join(SAL2, 'respuestas'))):
        if p.endswith('.tsv'):
            R[p[:-4]] = {r['codigo']: r['letra'].strip().upper() for r in csv.DictReader(open(os.path.join(SAL2, 'respuestas', p), encoding='utf-8'), delimiter='\t')}
    def binom_p(k, n, p): return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))
    res = {}; P0 = 1 / 5   # nulo prefijado: el encargo ofrece «ninguno»
    for grupo, cods in (('unidades', [c for c in clave if c.startswith('U')]), ('hesperia', [c for c in clave if c.startswith('H')]), ('todas', list(clave))):
        res[grupo] = {}
        for juez, resp in list(R.items()) + [('mayoría', None)]:
            cnt = Counter()
            for c in cods:
                if resp is None:
                    votos = Counter(letra_a_lengua[c].get(R[j].get(c, ''), 'ninguno') for j in R); l, n = votos.most_common(1)[0]
                    cnt[l if n >= 2 else 'sin mayoría'] += 1
                else: cnt[letra_a_lengua[c].get(resp.get(c, ''), 'ninguno')] += 1
            n = len(cods)
            res[grupo][juez] = dict(n=n, **cnt, p0=P0, p_binomial={l: round(binom_p(cnt.get(l, 0), n, P0), 4) for l in ('euskera', 'gallego', 'latín', 'azar')})
            print(grupo, juez, dict(cnt), 'p(euskera ≥ k):', res[grupo][juez]['p_binomial']['euskera'])
    json.dump(res, open(os.path.join(RAIZ, 'resultados', 't28_prediccion_prospectiva_v2.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    {'preparar': preparar, 'puntuar': puntuar, 'preparar2': preparar2, 'puntuar2': puntuar2}[sys.argv[1]]()
