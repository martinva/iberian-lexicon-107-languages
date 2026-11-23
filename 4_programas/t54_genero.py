"""Declaración 40: huella estructural de género con control externo (papiros documentales griegos). Piloto.

Entrena un clasificador de tipo de documento (cuentas y listas / cartas y peticiones / contratos y recibos) con
papiros griegos del DDbDP usando solo dónde están los numerales, y lo aplica a los plomos ibéricos con numerales.
No usa ningún significado ni ninguna lengua de comparación para el ibérico.

Los papiros no se redistribuyen: hay que tener una copia local de https://github.com/papyri/idp.data (CC BY 3.0)
con las carpetas DDbDP/1..6 y HGV_meta_EpiDoc/HGV2..7.
Uso / Usage:  python3 -I t54_genero.py RUTA/idp.data
"""
import glob, html, json, math, os, random, re, sys, unicodedata
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import balanced_accuracy_score, confusion_matrix
from ibcomp import fuentes
from t52_estructura import corpus_iberico

SEMILLA = 40
CLASES = ['C1 cuentas y listas', 'C2 cartas y peticiones', 'C3 contratos y recibos']
EXACTAS = [{'Abrechnung', 'Liste', 'Aufstellung', 'Register'},
           {'Petition', 'Enteuxis', 'Schreiben (amtlich)'},
           {'Vertrag', 'Quittung', 'Pacht', 'Darlehen', 'Kauf', 'Verkauf'}]
PREFIJOS = [(), ('Brief', 'Eingabe', 'Bericht'), ()]
RASGOS = ['numerales por 100 letras', 'cierran línea (exceso)', 'abren línea (exceso)',
          'numeral–palabra–numeral', 'numeral contiguo', 'concentración de la palabra previa']

# ------------------------------------------------------------------ lectura de los papiros
def clase_de(terminos, solo_primero=False):
    """Clase única del texto según las palabras clave de HGV, o None si no cae en ninguna o cae en más de una."""
    if solo_primero: terminos = terminos[:1]
    cs = set()
    for t in terminos:
        for i in range(3):
            if t in EXACTAS[i] or any(t.startswith(p) for p in PREFIJOS[i]): cs.add(i)
    return cs.pop() if len(cs) == 1 else None

def lee_griego(xml):
    """Líneas de elementos ('W', palabra) | ('N',) | ('G',) a partir de un archivo EpiDoc del DDbDP (con expresiones regulares)."""
    m = re.search(r'<div[^>]*type="edition"[^>]*>(.*)</body>', xml, re.S)
    if not m: return []
    s = m.group(1)
    for et in ('head', 'note', 'reg', 'rdg', 'corr', 'del', 'figure', 'desc'):     # lo que no está en el original o fue borrado
        s = re.sub(rf'<{et}\b[^>]*?(?<!/)>.*?</{et}>', '', s, flags=re.S)
    s = re.sub(r'<num\b[^>]*/>', ' \x05 ', s)
    s = re.sub(r'<num\b[^>]*>.*?</num>', ' \x05 ', s, flags=re.S)
    s = re.sub(r'<gap\b[^>]*/>', ' \x04 ', s)
    s = re.sub(r'<gap\b[^>]*>.*?</gap>', ' \x04 ', s, flags=re.S)
    s = s.replace('\n', ' ')
    s = re.sub(r'\s*<lb\b[^>]*break="no"[^>]*/>\s*', '\x06', s)
    s = re.sub(r'<lb\b[^>]*/>|</?(?:div|ab)\b[^>]*>', '\n', s)
    s = html.unescape(re.sub(r'<[^>]+>', '', s))
    while '\x06' in s: s = re.sub(r'(\S*)\x06(\S*)', r'\1\2\n', s, count=1)   # la palabra partida cuenta en la línea donde empieza
    lineas = []
    for linea in s.split('\n'):
        items = []
        for tok in linea.split():
            if '\x04' in tok: items.append(('G',)); continue
            if '\x05' in tok: items.append(('N',)); continue
            w = unicodedata.normalize('NFD', tok)
            w = ''.join(ch for ch in w if unicodedata.category(ch) in ('Ll', 'Lu', 'Lo')).lower().replace('ς', 'σ')
            if w: items.append(('W', w))
        if items: lineas.append(items)
    return lineas

def es_griego(lineas):
    letras = ''.join(it[1] for l in lineas for it in l if it[0] == 'W')
    return bool(letras) and sum('Ͱ' <= ch <= 'Ͽ' or 'ἀ' <= ch <= '῿' for ch in letras) / len(letras) >= 0.9

def corpus_griego(raiz, solo_primero=False):
    out = []; cuenta = Counter()
    for f in sorted(glob.glob(f'{raiz}/DDbDP/[1-6]/*.xml')):
        ident = os.path.basename(f)[:-4]; carpeta = int(os.path.basename(os.path.dirname(f))) + 1
        fm = f'{raiz}/HGV_meta_EpiDoc/HGV{carpeta}/{ident}.xml'
        if not os.path.exists(fm): cuenta['sin metadatos'] += 1; continue
        meta = open(fm, encoding='utf-8').read()
        terminos = [t.strip() for t in re.findall(r'<term[^>]*>([^<]*)</term>', meta)]
        c = clase_de(terminos, solo_primero)
        if c is None: cuenta['sin clase única'] += 1; continue
        lineas = lee_griego(open(f, encoding='utf-8').read())
        if not es_griego(lineas): cuenta['no griego o vacío'] += 1; continue
        cuenta[CLASES[c]] += 1
        out.append(dict(sigla=ident, clase=c, lineas=lineas))
    return out, dict(cuenta)

# ------------------------------------------------------------------ rasgos
def letras(lineas): return sum(len(it[1]) for l in lineas for it in l if it[0] == 'W')
def n_numerales(lineas): return sum(it[0] == 'N' for l in lineas for it in l)
def n_elementos(lineas): return sum(it[0] != 'G' for l in lineas for it in l)

def rasgos(lineas):
    nl = letras(lineas); nn = n_numerales(lineas); ne = n_elementos(lineas)
    nlin = sum(any(it[0] != 'G' for it in l) for l in lineas)
    fin = ini = alt = cont = 0; previas = []
    for l in lineas:
        for j, it in enumerate(l):
            if it[0] != 'N': continue
            fin += j == len(l) - 1; ini += j == 0
            alt += (j >= 2 and l[j - 2][0] == 'N' and l[j - 1][0] == 'W') or (j + 2 < len(l) and l[j + 2][0] == 'N' and l[j + 1][0] == 'W')
            cont += (j >= 1 and l[j - 1][0] == 'N') or (j + 1 < len(l) and l[j + 1][0] == 'N')
            if j >= 1 and l[j - 1][0] == 'W': previas.append(l[j - 1][1])
    esp = nlin / ne
    conc = 1 - len(set(previas)) / len(previas) if len(previas) >= 2 else 0.0
    return [100 * nn / max(nl, 1), fin / nn - esp, ini / nn - esp, alt / nn, cont / nn, conc]

def ventana(lineas, objetivo, rng, intentos=20):
    """Líneas consecutivas con al menos `objetivo` letras y al menos un numeral, o None."""
    for _ in range(intentos):
        a = rng.randrange(len(lineas)); b = a; n = 0
        while b < len(lineas) and n < objetivo: n += letras([lineas[b]]); b += 1
        if n >= objetivo and n_numerales(lineas[a:b]) >= 1: return lineas[a:b]
    return None

def muestra_griega(GR, tamanos, semilla):
    rng = random.Random(semilla); X = []; y = []; ids = []
    for t in GR:
        v = None
        for _ in range(20):
            v = ventana(t['lineas'], rng.choice(tamanos), rng, intentos=1)
            if v: break
        if v: X.append(rasgos(v)); y.append(t['clase']); ids.append(t['sigla'])
    return np.array(X), np.array(y), ids

def modelo(): return make_pipeline(StandardScaler(), LogisticRegression(class_weight='balanced', max_iter=2000))

def validacion(X, y, semilla, PERM=200):
    cv = StratifiedKFold(10, shuffle=True, random_state=semilla)
    pred = cross_val_predict(modelo(), X, y, cv=cv)
    obs = balanced_accuracy_score(y, pred); rng = np.random.default_rng(semilla); mayores = 0; nulos = []
    for _ in range(PERM):
        yp = rng.permutation(y); b = balanced_accuracy_score(yp, cross_val_predict(modelo(), X, yp, cv=cv))
        nulos.append(b); mayores += b >= obs
    return dict(exactitud_equilibrada=round(float(obs), 3), azar=round(1 / 3, 3), p=round((mayores + 1) / (PERM + 1), 4),
                nulo_media=round(float(np.mean(nulos)), 3), nulo_max=round(float(np.max(nulos)), 3),
                confusion=confusion_matrix(y, pred).tolist(),
                acierto_por_clase=[round(float(r[i] / r.sum()), 3) for i, r in enumerate(confusion_matrix(y, pred))])

def wilson(k, n, z=1.96):
    if n == 0: return None
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((c - h) / d, 3), round((c + h) / d, 3)]

# ------------------------------------------------------------------ principal
def aplica(X, y, XI):
    m = modelo().fit(X, y); pr = m.predict_proba(XI); cl = pr.argmax(1)
    return m, pr, cl

def main(raiz):
    IB = [t for t in corpus_iberico() if t['grupo'] == 'Plomo' and n_numerales(t['lineas']) >= 1 and n_elementos(t['lineas']) >= 8]
    tam = [letras(t['lineas']) for t in IB]
    XI = np.array([rasgos(t['lineas']) for t in IB])
    GR, cuenta = corpus_griego(raiz)
    X, y, ids = muestra_griega(GR, tam, SEMILLA)
    R = dict(declaracion=40, semilla=SEMILLA, rasgos=RASGOS, clases=CLASES,
             iberico=dict(textos=len(IB), letras_min_mediana_max=[min(tam), int(np.median(tam)), max(tam)],
                          numerales=int(sum(n_numerales(t['lineas']) for t in IB))),
             griego=dict(lectura=cuenta, textos_con_clase=len(GR), ventanas=len(y),
                         ventanas_por_clase={CLASES[i]: int((y == i).sum()) for i in range(3)}))
    print(json.dumps(R['iberico'], ensure_ascii=False)); print(json.dumps(R['griego'], ensure_ascii=False))

    R['prueba_1_validacion_en_griego'] = v = validacion(X, y, SEMILLA)
    print('1.', json.dumps(v, ensure_ascii=False))
    m, pr, cl = aplica(X, y, XI)
    k = int((cl == 0).sum())
    R['prueba_2_aplicacion_al_iberico'] = dict(
        se_aplica=bool(v['p'] < 0.05 and v['exactitud_equilibrada'] > 1 / 3),
        por_clase={CLASES[i]: int((cl == i).sum()) for i in range(3)}, proporcion_C1=round(k / len(IB), 3), ic95_wilson=wilson(k, len(IB)),
        probabilidad_media={CLASES[i]: round(float(pr[:, i].mean()), 3) for i in range(3)})
    print('2.', json.dumps(R['prueba_2_aplicacion_al_iberico'], ensure_ascii=False))
    R['descriptivo_3'] = dict(
        medias={**{CLASES[i]: [round(float(x), 3) for x in X[y == i].mean(0)] for i in range(3)}, 'ibérico': [round(float(x), 3) for x in XI.mean(0)]},
        medianas={**{CLASES[i]: [round(float(x), 3) for x in np.median(X[y == i], 0)] for i in range(3)}, 'ibérico': [round(float(x), 3) for x in np.median(XI, 0)]},
        coeficientes={CLASES[i]: [round(float(c), 2) for c in m[-1].coef_[i]] for i in range(3)},
        por_plomo=[dict(sigla=t['sigla'], letras=tam[i], numerales=n_numerales(t['lineas']), clase=CLASES[cl[i]][:2],
                        p=[round(float(p), 2) for p in pr[i]], rasgos=[round(float(x), 2) for x in XI[i]]) for i, t in enumerate(IB)])
    for c in list(R['descriptivo_3']['medias']): print(f"   {c:28s}", R['descriptivo_3']['medias'][c])

    # ---- añadidos no declarados (descriptivos; no cambian las pruebas 1 y 2)
    z = (XI - X.mean(0)) / X.std(0)
    otros = dict(nota='Añadidos después de ver el resultado; no declarados.',
                 ibericos_fuera_de_rango=dict(algun_rasgo_a_mas_de_3_dt=int((np.abs(z) > 3).any(1).sum()), de=len(IB),
                                              z_medio_por_rasgo=[round(float(x), 2) for x in z.mean(0)]))
    accs = []; props = []
    for s in range(1, 21):
        Xs, ys, _ = muestra_griega(GR, tam, s); cv = StratifiedKFold(10, shuffle=True, random_state=s)
        accs.append(balanced_accuracy_score(ys, cross_val_predict(modelo(), Xs, ys, cv=cv)))
        props.append(float((modelo().fit(Xs, ys).predict(XI) == 0).mean()))
    otros['veinte_semillas'] = dict(exactitud_min_media_max=[round(min(accs), 3), round(float(np.mean(accs)), 3), round(max(accs), 3)],
                                    proporcion_C1_min_media_max=[round(min(props), 3), round(float(np.mean(props)), 3), round(max(props), 3)])
    GR1, cuenta1 = corpus_griego(raiz, solo_primero=True)
    X1, y1, _ = muestra_griega(GR1, tam, SEMILLA); cv = StratifiedKFold(10, shuffle=True, random_state=SEMILLA)
    otros['clase_por_primer_termino'] = dict(
        ventanas_por_clase={CLASES[i]: int((y1 == i).sum()) for i in range(3)},
        exactitud_equilibrada=round(float(balanced_accuracy_score(y1, cross_val_predict(modelo(), X1, y1, cv=cv))), 3),
        ibericos_por_clase={CLASES[i]: int((modelo().fit(X1, y1).predict(XI) == i).sum()) for i in range(3)})
    R['no_declarado'] = otros
    print('no declarado:', json.dumps(otros, ensure_ascii=False))
    json.dump(R, open(f'{fuentes.RAIZ}/../resultados/t54_genero.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
