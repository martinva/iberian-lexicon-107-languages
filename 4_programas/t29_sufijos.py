"""Declaración 12: sufijos con función fijada a ciegas y forma comparada (segundo artículo).

Fase 1 (`preparar`): para cada sufijo del inventario declarado, cuenta mecánicamente en todo el corpus de Hesperia
las palabras que lo llevan (palabra = tema + sufijo, donde el tema es un antropónimo de dos formantes de Rodríguez
Ramos 2014, una de las 40 unidades, u otra palabra atestiguada suelta en el corpus), por clase de tema, soporte,
posición y vecino siguiente, y escribe las fichas ciegas (`2_criterios/jurado/sufijos/FICHAS_sufijos.md`) con un
código S01…, sin el sufijo ni ninguna lengua, más la clave con su SHA-256.
Fase 2 (`puntuar`): lee las respuestas de los jueces (función de lista cerrada por ficha) y calcula la prueba de
forma declarada (distancia a los sufijos vascos de esa función frente a 10.000 permutaciones y a las lenguas de
referencia), solo para los sufijos cuya función fija el jurado por mayoría.
Uso / Usage:  python3 t29_sufijos.py preparar | puntuar
"""
import csv, hashlib, json, os, re, sys, unicodedata
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import reducida
from ibcomp.distancia import dist
from ibcomp.pruebas import generador

AQUI = os.path.dirname(__file__); RAIZ = os.path.join(AQUI, '..'); IB = os.path.join(RAIZ, '1_fuentes_lexicas', 'iberico')
SAL = os.path.join(RAIZ, '2_criterios', 'jurado', 'sufijos')
# Inventario declarado (entrada 12, con la ampliación): variantes gráficas juntas.
SUFIJOS = [('te', ['te', 'de']), ('en', ['en']), ('ar', ['ar']), ('mi', ['ḿi', 'mi']), ('ka', ['ka', 'ga']),
           ('e', ['e']), ('ai', ['ai', 'ei']), ('sken', ['sken', 'ken']), ('ban', ['ban']), ('erter', ['erter', 'erder'])]
FUNCIONES = ['agente', 'poseedor', 'destinatario', 'étnico', 'primera persona', 'determinante', 'fracción', 'indeterminable']

def corpus():
    meta = {r['ref_hesperia']: r for r in csv.DictReader(open(os.path.join(IB, 'hesperia_metadatos.csv'), encoding='utf-8'))}
    docs = []
    for r in csv.DictReader(open(os.path.join(IB, 'hesperia_iberico_1599.csv'), encoding='utf-8')):
        t = unicodedata.normalize('NFC', re.sub(r'[\[\]\(\)\+\-\?̲̱̣]', '', r['texto_crudo'])).lower()
        toks = [w for w in re.split(r'[^\wśŕḿ]+', t) if w]
        m = meta.get(r['ref_hesperia'], {})
        docs.append((r['ref_hesperia'], (m.get('soporte_norm') or m.get('material') or 'otro').lower(), toks))
    return docs

def clasificadores():
    F = sorted({e['formante'] for e in json.load(open(os.path.join(IB, 'formantes_onomasticos_rodriguez_ramos_2014.json'), encoding='utf-8'))}, key=len, reverse=True)
    U = {}
    for u in fuentes.unidades_plomos() + fuentes.unidades_numerales():
        for f in u['formas']: U[f] = u['id']
    def np(w):
        for a in F:
            if w.startswith(a):
                r = w[len(a):]
                for b in F:
                    if r == b or (r.startswith(b) and len(r) - len(b) == 0): return True
        return False
    return F, U, np

def preparar():
    os.makedirs(SAL, exist_ok=True); docs = corpus(); F, U, np = clasificadores()
    vocab = Counter(w for _, _, w0 in docs for w in w0)
    def clase(w):
        if w is None: return 'límite'
        if re.search(r'\d|[ivxlπ]{3,}', w): return 'cifra'
        if w in U: return 'unidad'
        if np(w): return 'nombre'
        return 'otra'
    filas = []; clave = []
    for i, (nombre, variantes) in enumerate(SUFIJOS):
        st = Counter(); sop = Counter(); sig = Counter(); pos = Counter(); ej = 0
        for ref, soporte, toks in docs:
            for k, w in enumerate(toks):
                for v in variantes:
                    if w.endswith(v) and len(w) > len(v) + 2:
                        tema = w[:-len(v)]
                        if np(tema): c = 'nombre de persona'
                        elif tema in U: c = 'término del léxico económico ya identificado'
                        elif vocab.get(tema, 0) >= 2: c = 'otra palabra atestiguada suelta'
                        else: continue
                        ej += 1; st[c] += 1; sop[soporte] += 1
                        sig[clase(toks[k + 1] if k + 1 < len(toks) else None)] += 1
                        pos['final del texto' if k == len(toks) - 1 else ('inicio' if k == 0 else 'interior')] += 1
                        break
        if not ej: continue
        desc = (f"{ej} palabras del corpus se analizan como tema + este elemento. Tema: " + ', '.join(f'{c} ({n})' for c, n in st.most_common()) +
                '. Soportes: ' + ', '.join(f'{s} ({n})' for s, n in sop.most_common(4)) +
                '. Palabra siguiente: ' + ', '.join(f'{s} ({n})' for s, n in sig.most_common()) +
                '. Posición: ' + ', '.join(f'{s} ({n})' for s, n in pos.most_common()) + '.')
        filas.append((f'S{len(filas) + 1:02d}', desc)); clave.append(dict(codigo=filas[-1][0], sufijo=nombre, variantes='|'.join(variantes), ejemplares=ej))
    with open(os.path.join(SAL, 'RECUENTO_mecanico.md'), 'w', encoding='utf-8') as g:
        g.write('# Recuento mecánico de los sufijos (declaración 12)\n\nApoya las fichas de FICHAS_sufijos.md. El recuento es mecánico sobre todo el corpus: una palabra se analiza como tema + sufijo solo si el tema es un nombre de persona (dos formantes del índice onomástico de referencia), un término del léxico económico ya identificado, u otra palabra atestiguada suelta al menos dos veces. Hay %d fichas.\n\n| Código | Distribución |\n|---|---|\n' % len(filas))
        for cod, desc in filas: g.write(f'| {cod} | {desc} |\n')
    with open(os.path.join(SAL, 'CLAVE_sufijos.tsv'), 'w', encoding='utf-8', newline='') as g:
        w = csv.DictWriter(g, fieldnames=list(clave[0]), delimiter='\t'); w.writeheader(); w.writerows(clave)
    h = hashlib.sha256(open(os.path.join(SAL, 'CLAVE_sufijos.tsv'), 'rb').read()).hexdigest()
    open(os.path.join(SAL, 'clave_sha256.txt'), 'w').write(h + '  CLAVE_sufijos.tsv\n')
    print('fichas', len(filas), 'SHA-256 de la clave', h)
    for c in clave: print('  ', c)

def puntuar():
    """Prueba de forma con las funciones fijadas por mayoría del jurado (≥2 de 3).

    Sufijos vascos por función (Trask 1997; Hualde y Ortiz de Urbina 2003): ergativo/agente -k; genitivo/poseedor
    -(r)en; gentilicio/étnico -(t)ar; determinante -a; «mitad» erdi. La comparación con las lenguas de referencia
    (turco, húngaro, estonio, georgiano, quechua) queda pendiente de inventarios verificados en gramáticas:
    DESVIACIÓN respecto de la declaración 12, anotada allí; se ejecutará en la revisión del artículo II.
    """
    import statistics
    EXPONENTE = {'agente': 'k', 'poseedor': 'en', 'étnico': 'tar', 'determinante': 'a', 'fracción': 'erdi', 'destinatario': 'i', 'primera persona': 'ni'}
    R = {}
    for p in sorted(os.listdir(os.path.join(SAL, "respuestas")) if os.path.isdir(os.path.join(SAL, "respuestas")) else []):
        if p.endswith('.tsv'):
            R[p[:-4]] = {r['codigo']: r['funcion'] for r in csv.DictReader(open(os.path.join(SAL, 'respuestas', p), encoding='utf-8'), delimiter='\t')}
    clave = {r['codigo']: r for r in csv.DictReader(open(os.path.join(SAL, "CLAVE_sufijos.tsv"), encoding='utf-8'), delimiter='\t')}
    fijadas = {}
    for c in clave:
        votos = Counter(R[j].get(c, 'indeterminable') for j in R)
        f, n = votos.most_common(1)[0]
        if n >= 2 and f != 'indeterminable': fijadas[c] = f
    print('Funciones fijadas por mayoría:', {clave[c]['sufijo']: f for c, f in sorted(fijadas.items())})
    pares = []
    for c, f in sorted(fijadas.items()):
        ib = reducida(clave[c]['variantes'].split('|')[0]); eu = reducida(EXPONENTE[f])
        d = dist(ib, eu); pares.append((c, clave[c]['sufijo'], f, ib, eu, round(d, 3)))
        print(f"  {c} {clave[c]['sufijo']:6s} {f:13s} {ib:6s} ~ {eu:6s} d={d:.3f}")
    real = statistics.mean(p[5] for p in pares)
    rnd = generador('sufijos', 'permutacion'); exps = [p[4] for p in pares]; peor = 0; S = []
    for _ in range(10000):
        e = exps[:]; rnd.shuffle(e)
        S.append(statistics.mean(dist(p[3], x) for p, x in zip(pares, e)))
    S.sort(); perc = sum(x < real for x in S) / 100
    print(f"Distancia media real {real:.3f}; permutaciones (10.000): mediana {S[5000]:.3f}, percentil de la real {perc:.1f}")
    res = dict(fijadas={clave[c]['sufijo']: f for c, f in fijadas.items()}, pares=[dict(codigo=c, sufijo=sf, funcion=f, iberico=ib, vasco=eu, distancia=d) for c, sf, f, ib, eu, d in pares],
               media_real=round(real, 4), mediana_permutaciones=round(S[5000], 4), percentil=round(perc, 1), permutaciones=10000,
               nota='Comparación con lenguas de referencia pendiente de inventarios verificados (desviación anotada en la declaración 12)')
    json.dump(res, open(os.path.join(RAIZ, 'resultados', 't29_sufijos.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    {'preparar': preparar, 'puntuar': puntuar}[sys.argv[1]]()
