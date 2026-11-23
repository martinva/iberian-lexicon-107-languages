"""Declaración 41: ¿se traslada la huella de género a otra época, otro soporte y otra lengua?

Entrena con papiros griegos ptolemaicos y prueba en papiros romanos y bizantinos, óstraca griegos, textos latinos y coptos.
Requiere una copia local completa de https://github.com/papyri/idp.data (carpetas DDbDP y HGV_meta_EpiDoc; CC BY 3.0).
Uso / Usage:  python3 -I t55_genero_traslado.py RUTA/idp.data [ARCHIVO_CACHE.pkl]
"""
import glob, json, os, pickle, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from ibcomp import fuentes
from t52_estructura import corpus_iberico
from t54_genero import (CLASES, RASGOS, clase_de, lee_griego, letras, n_numerales, n_elementos, rasgos, ventana)

SEMILLA = 41
RASGOS2 = RASGOS + ['líneas con numeral', 'posición relativa del numeral', 'asimetría palabra antes / después']
CONJUNTOS = ['ENTRENAMIENTO papiros griegos ptolemaicos', 'E1 papiros griegos romanos', 'E2 papiros griegos bizantinos',
             'S óstraca griegos', 'L1 latín', 'L2 copto']

# ------------------------------------------------------------------ lectura
def lee_ddbdp(raiz, cache=None):
    if cache and os.path.exists(cache): return pickle.load(open(cache, 'rb'))
    meta = {os.path.basename(f)[:-4]: f for f in glob.glob(f'{raiz}/HGV_meta_EpiDoc/*/*.xml')}
    out = []
    for f in sorted(glob.glob(f'{raiz}/DDbDP/*/*.xml')):
        ident = os.path.basename(f)[:-4]
        if ident not in meta: continue
        lineas = lee_griego(open(f, encoding='utf-8').read())
        let = ''.join(it[1] for l in lineas for it in l if it[0] == 'W')
        if not let: continue
        gr = sum('Ͱ' <= ch <= 'Ͽ' or 'ἀ' <= ch <= '῿' for ch in let) / len(let)
        la = sum('a' <= ch <= 'z' for ch in let) / len(let)
        cop = sum('Ⲁ' <= ch <= '⳿' or 'Ϣ' <= ch <= 'ϯ' for ch in let) / len(let)
        mm = open(meta[ident], encoding='utf-8').read()
        mt = re.search(r'<material>([^<]*)</material>', mm); od = re.search(r'<origDate\b([^>]*)>', mm); anio = None
        if od:
            ys = [int(y) for y in re.findall(r'(?:when|notBefore|notAfter)="(-?\d{4})', od.group(1))]
            if ys: anio = sum(ys) / len(ys)
        out.append(dict(id=ident, gr=gr, la=la, cop=cop, lineas=lineas, anio=anio, material=mt.group(1).strip() if mt else None,
                        terminos=[t.strip() for t in re.findall(r'<term[^>]*>([^<]*)</term>', mm)]))
    if cache: pickle.dump(out, open(cache, 'wb'))
    return out

def conjunto_de(d):
    idioma = 'gr' if d['gr'] >= .9 else 'la' if d['la'] >= .9 else 'cop' if d['cop'] >= .9 else None
    if idioma == 'la': return 4
    if idioma == 'cop': return 5
    if idioma != 'gr': return None
    m = (d['material'] or '').lower()
    if 'ostrak' in m or 'ostrac' in m: return 3
    if 'papyrus' not in m or d['anio'] is None: return None
    return 0 if d['anio'] < -30 else 1 if d['anio'] <= 284 else 2

# ------------------------------------------------------------------ rasgos del juego 2
def rasgos2(lineas):
    r = rasgos(lineas); con = tot = 0; pos = []; antes = despues = 0
    for l in lineas:
        el = [it for it in l if it[0] != 'G']
        if not el: continue
        tot += 1; con += any(it[0] == 'N' for it in l)
        k = -1
        for j, it in enumerate(l):
            if it[0] == 'G': continue
            k += 1
            if it[0] != 'N': continue
            pos.append(k / (len(el) - 1) if len(el) > 1 else 0.5)
            antes += j >= 1 and l[j - 1][0] == 'W'; despues += j + 1 < len(l) and l[j + 1][0] == 'W'
    return r + [con / tot, float(np.mean(pos)), (antes - despues) / (antes + despues) if antes + despues else 0.0]

def muestra(textos, tamanos, rng):
    X = []; y = []
    for t in textos:
        v = None
        for _ in range(20):
            v = ventana(t['lineas'], rng.choice(tamanos), rng, intentos=1)
            if v: break
        if v: X.append(rasgos2(v)); y.append(t['clase'])
    return np.array(X), np.array(y)

def binario(): return make_pipeline(StandardScaler(), LogisticRegression(class_weight='balanced', max_iter=2000))

def auc_ic(y, p, rng, B=1000):
    obs = roc_auc_score(y, p); bs = []; n = len(y)
    while len(bs) < B:
        i = rng.integers(0, n, n)
        if 0 < y[i].sum() < n: bs.append(roc_auc_score(y[i], p[i]))
    perm = sum(roc_auc_score(rng.permutation(y), p) >= obs for _ in range(B))
    return dict(auc=round(float(obs), 3), ic95=[round(float(np.percentile(bs, 2.5)), 3), round(float(np.percentile(bs, 97.5)), 3)],
                p=round((perm + 1) / (B + 1), 4))

def tasas(y1, pred): return float(pred[y1 == 1].mean()), float(pred[y1 == 0].mean())

def main(raiz, cache=None):
    rng = random.Random(SEMILLA); nrng = np.random.default_rng(SEMILLA)
    IB = [t for t in corpus_iberico() if t['grupo'] == 'Plomo' and n_numerales(t['lineas']) >= 1 and n_elementos(t['lineas']) >= 8]
    tam = [letras(t['lineas']) for t in IB]; XI = np.array([rasgos2(t['lineas']) for t in IB])
    grupos = [[] for _ in CONJUNTOS]
    for d in lee_ddbdp(raiz, cache):
        c = clase_de(d['terminos']); k = conjunto_de(d)
        if c is None or k is None: continue
        d['clase'] = c; grupos[k].append(d)
    D = [muestra(g, tam, rng) for g in grupos]
    R = dict(declaracion=41, semilla=SEMILLA, rasgos_juego_2=RASGOS2, plomos=len(IB),
             tamanos={CONJUNTOS[k]: dict(textos_con_clase=len(grupos[k]), ventanas=int(len(D[k][1])),
                                         por_clase=[int((D[k][1] == i).sum()) for i in range(3)]) for k in range(6)})
    for k in range(6): print(CONJUNTOS[k], R['tamanos'][CONJUNTOS[k]])
    Xe, ye = D[0]; res = {}
    for nombre, cols in (('juego_1', slice(0, 6)), ('juego_2', slice(0, 9))):
        m2 = binario().fit(Xe[:, cols], (ye == 0).astype(int)); m3 = binario().fit(Xe[:, cols], ye)
        cv = StratifiedKFold(10, shuffle=True, random_state=SEMILLA)
        pcv = cross_val_predict(binario(), Xe[:, cols], (ye == 0).astype(int), cv=cv, method='predict_proba')[:, 1]
        r = {'validacion cruzada en el entrenamiento': dict(auc=round(float(roc_auc_score(ye == 0, pcv)), 3),
             tasa_aciertos_y_falsos=[round(x, 3) for x in tasas((ye == 0).astype(int), (pcv >= .5).astype(int))])}
        q = float(m2.predict(XI[:, cols]).mean()); est = {}
        for k in range(1, 6):
            X, y = D[k]; y1 = (y == 0).astype(int); p = m2.predict_proba(X[:, cols])[:, 1]; pred = (p >= .5).astype(int)
            a = auc_ic(y1, p, nrng); tp, fp = tasas(y1, pred)
            a.update(exactitud_equilibrada_3_clases=round(float(balanced_accuracy_score(y, m3.predict(X[:, cols]))), 3),
                     tasa_aciertos=round(tp, 3), tasa_falsos_positivos=round(fp, 3))
            r[CONJUNTOS[k]] = a
            bs = []                                                           # recuento ajustado (descriptivo)
            pi = m2.predict(XI[:, cols])
            for _ in range(1000):
                qi = pi[nrng.integers(0, len(pi), len(pi))].mean(); j = nrng.integers(0, len(y1), len(y1))
                if not 0 < y1[j].sum() < len(j): continue
                t, f = tasas(y1[j], pred[j])
                if t - f > 0.05: bs.append(min(1, max(0, (qi - f) / (t - f))))
            est[CONJUNTOS[k]] = dict(estimacion=round(min(1, max(0, (q - fp) / (tp - fp))), 3) if tp - fp > 0.05 else None,
                                     ic95=[round(float(np.percentile(bs, 2.5)), 3), round(float(np.percentile(bs, 97.5)), 3)] if len(bs) > 100 else None)
        r['media_auc_cinco_conjuntos'] = round(float(np.mean([r[CONJUNTOS[k]]['auc'] for k in range(1, 6)])), 3)
        r['plomos_clasificados_como_cuentas'] = dict(n=int(round(q * len(IB))), de=len(IB), proporcion=round(q, 3))
        r['descriptivo_3_recuento_ajustado'] = est
        r['coeficientes'] = [round(float(c), 2) for c in m2[-1].coef_[0]]
        res[nombre] = r
        print(nombre); [print('  ', k, json.dumps(v, ensure_ascii=False)) for k, v in r.items()]
    R.update(res)
    R['medias_de_rasgos'] = {**{CONJUNTOS[k]: {('cuentas' if c else 'resto'): [round(float(x), 3) for x in D[k][0][(D[k][1] == 0) == c].mean(0)]
                                               for c in (True, False)} for k in range(6)},
                             'ibérico': [round(float(x), 3) for x in XI.mean(0)]}
    json.dump(R, open(f'{fuentes.RAIZ}/../resultados/t55_genero_traslado.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
