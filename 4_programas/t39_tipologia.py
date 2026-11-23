"""Declaración 25: tipología frente a historia en la prueba de perfil (el «efecto yakuto»).

WALS (edición CLDF cldf-datasets/wals), rasgos 12A (estructura silábica) y 26A (prefijación/sufijación), unidos por
glotocódigo con NorthEuraLex. Ibérico asignado de antemano: 12A = Moderately complex, 26A = Strongly suffixing.
(1) MCO de la divergencia entre perfiles en función de «misma 12A» y «misma 26A» sobre los pares de familias distintas
con 12A; (2) residuo de cada lengua frente al ibérico; (3) pares de símbolos que más aportan a ibérico–yakuto e ibérico–euskera.

Uso / Usage:  python3 t39_tipologia.py RUTA/wals/cldf
"""
import csv, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import proyecta
from ibcomp.pruebas import perfil, divergencia

IB_12A, IB_26A = 'Moderately complex', 'Strongly suffixing'

def wals(ruta):
    L = {r['ID']: r['Glottocode'] for r in csv.DictReader(open(os.path.join(ruta, 'languages.csv'), encoding='utf-8'))}
    C = {r['ID']: r['Name'] for r in csv.DictReader(open(os.path.join(ruta, 'codes.csv'), encoding='utf-8'))}
    V = {}
    for r in csv.DictReader(open(os.path.join(ruta, 'values.csv'), encoding='utf-8')):
        if r['Parameter_ID'] in ('12A', '26A'): V.setdefault(L[r['Language_ID']], {})[r['Parameter_ID']] = C.get(r['Code_ID'], r['Value'])
    return V

def aporte(p, q):
    out = {}
    for k in set(p) | set(q):
        a = p.get(k, 0.0); b = q.get(k, 0.0); m = (a + b) / 2; d = 0.0
        if a: d += 0.5 * a * math.log2(a / m)
        if b: d += 0.5 * b * math.log2(b / m)
        out[k] = d
    return sorted(out.items(), key=lambda x: -x[1])

def analiza(etiqueta, P, pib, nombres, familia, T):
    con = [l for l in P if '12A' in T.get(l, {})]
    X, y = [], []
    for i, a in enumerate(con):
        for b in con[i + 1:]:
            if familia[a] == familia[b]: continue
            s12 = float(T[a]['12A'] == T[b]['12A'])
            s26 = float(T[a].get('26A') == T[b].get('26A')) if ('26A' in T[a] and '26A' in T[b]) else 0.0
            h26 = float('26A' in T[a] and '26A' in T[b])
            X.append([1.0, s12, s26, h26]); y.append(divergencia(P[a], P[b]))
    X = np.array(X); y = np.array(y); beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = []
    for l in con:
        s12 = float(T[l]['12A'] == IB_12A); h26 = float('26A' in T[l]); s26 = float(T[l].get('26A') == IB_26A) if h26 else 0.0
        pred = float(beta @ np.array([1.0, s12, s26, h26])); obs = divergencia(pib, P[l])
        res.append((round(obs - pred, 4), nombres[l], round(obs, 4), round(pred, 4), T[l]['12A'], T[l].get('26A', '-')))
    res.sort()
    rango = {n: i + 1 for i, (r_, n, *_) in enumerate(res)}
    out = dict(pares=len(y), coeficientes=dict(zip(['constante', 'misma_12A', 'misma_26A', 'ambas_con_26A'], [round(float(b), 5) for b in beta])),
               lenguas_con_12A=len(con), residuos_10_mas_negativos=res[:10],
               rango_euskera=rango.get('Basque'), rango_yakuto=rango.get('Sakha'), rango_fines=rango.get('Finnish'),
               p1_euskera_entre_3=rango.get('Basque', 999) <= 3,
               p2_yakuto_y_fines_menos_negativos=all(rango.get(n, 999) > rango.get('Basque', 999) for n in ('Sakha', 'Finnish')))
    print(f'\n===== {etiqueta}'); [print(f'  {k}: {v}') for k, v in out.items()]
    return out

if __name__ == '__main__':
    W = wals(sys.argv[1])
    LEX, lang = fuentes.northeuralex(); nombres = {l: lang[l]['Name'] for l in LEX}; familia = {l: lang[l].get('Family') or '' for l in LEX}
    T = {l: W[lang[l]['Glottocode']] for l in LEX if lang[l].get('Glottocode') in W}
    fichas = fuentes.hesperia(); IB = set().union(*[f['formas'] for f in fichas])
    P = {l: perfil(ws) for l, ws in LEX.items()}; Pr = {l: perfil(proyecta(ws)) for l, ws in LEX.items()}
    res = {'clases completas': analiza('clases completas', P, perfil(IB), nombres, familia, T),
           'reducidas': analiza('lenguas reducidas', Pr, perfil(proyecta(IB)), nombres, familia, T)}
    eus = next(l for l in LEX if nombres[l] == 'Basque'); sak = next(l for l in LEX if nombres[l] == 'Sakha')
    res['aporte_ibérico_yakuto_reducidas'] = [(k, round(v, 5)) for k, v in aporte(perfil(proyecta(IB)), Pr[sak])[:12]]
    res['aporte_ibérico_euskera_reducidas'] = [(k, round(v, 5)) for k, v in aporte(perfil(proyecta(IB)), Pr[eus])[:12]]
    print('\nPares que más separan ibérico–yakuto (reducidas):', res['aporte_ibérico_yakuto_reducidas'][:8])
    print('Pares que más separan ibérico–euskera (reducidas):', res['aporte_ibérico_euskera_reducidas'][:8])
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't39_tipologia.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
