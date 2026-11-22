"""Tablas 4 y 5 y figura 3: la serie numeral ibérica frente a la base mundial de numerales de Chan (2019).

(a) Serie completa (1 a 8 y 10), una variedad por lengua: lengua más próxima al ibérico.
(b) Referencia: vecino más próximo de las lenguas sin parientes en la base, y de una muestra de 400 lenguas con parientes.
(c) Valores fijados por monedas y pesos (1, 10 y 20), todas las variedades con esos valores, primera variante.
(d) Control: valores barajados dentro de la lengua.
Uso:  python3 t04_t05_numerales.py
"""
import json, os, sys, random
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import red_ib
from ibcomp.distancia import dist
from ibcomp.pruebas import generador

KS = ['1', '2', '3', '4', '5', '6', '7', '8', '10']
IB = {u['id'][1:]: u['formas'] for u in fuentes.unidades_numerales()}     # las formas se leen del archivo de unidades (N1 … N20)
RI = {k: [red_ib(f) for f in v] for k, v in IB.items()}
NO_CLASIFICADAS = {'Bookkeeping', 'Unattested', 'Unclassifiable', 'Pidgin', 'Mixed Language', 'Artificial Language', 'Speech Register', 'Sign Language'}
SEMILLA_MUESTRA = 20261118          # semilla de la muestra de 400 lenguas (se conserva la del cálculo original para obtener la misma muestra)

if __name__ == '__main__':
    Ftodo, lang = fuentes.chan(); res = {}
    # (a) y (b): una variedad por lengua (la primera de la base con los nueve valores), primera forma de cada valor
    F = {l: {k: f[k][0] for k in KS if f.get(k)} for l, f in Ftodo.items()}; visto = set(); L = []
    for l, f in F.items():
        g = lang[l]['Glottocode']
        if len(f) == 9 and g and not g.startswith('xxxx') and g not in visto and lang[l]['Family'] not in NO_CLASIFICADAS: visto.add(g); L.append(l)
    fam = {l: (lang[l]['Family'] or 'AISLADA:' + lang[l]['Glottocode']) for l in L}; tam = Counter(fam.values()); solas = [l for l in L if tam[fam[l]] == 1]
    con = random.Random(SEMILLA_MUESTRA).sample([l for l in L if tam[fam[l]] >= 5], 400); V = [[F[l][k] for k in KS] for l in L]
    print('lenguas:', len(L), '| familias:', len(tam), '| sin parientes en la base:', len(solas))
    def vecino(l):
        a = [F[l][k] for k in KS]; mejor = (9, None)
        for m, b in zip(L, V):
            if m == l: continue
            d = sum(dist(x, y) for x, y in zip(a, b)) / 9
            if d < mejor[0]: mejor = (d, m)
        return mejor
    fil = sorted((sum(min(dist(x, F[m][k]) for x in RI[k]) for k in KS) / 9, lang[m]['Name'], fam[m]) for m in L); dib = fil[0][0]
    print('IBÉRICO, serie completa:', [(round(d, 3), n[:28], f[:16]) for d, n, f in fil[:5]])
    R1 = [vecino(l) for l in solas]; R2 = [(l,) + vecino(l) for l in con]
    print(f'(b) lenguas sin parientes: {len(R1)}; con vecino a distancia ≤ {dib:.3f}: {sum(d <= dib for d, m in R1)}; la más próxima, a {min(d for d, m in R1):.3f}')
    tramos = {}
    for lo, hi in ((0.2, 0.3), (0.3, 0.4), (0.4, 0.5), (0.2, 0.5)):
        s = [fam[l] == fam[m] for l, d, m in R2 if lo <= d < hi]; tramos[f'{lo}-{hi}'] = (sum(s), len(s)); print(f'    vecino entre {lo} y {hi}: de su misma familia en {sum(s)} de {len(s)}')
    res['serie completa'] = dict(lenguas=len(L), familias=len(tam), iberico=[(round(d, 3), n, f) for d, n, f in fil[:30]], sin_parientes=dict(n=len(R1), minimo=round(min(d for d, m in R1), 3), a_la_distancia_del_iberico=sum(d <= dib for d, m in R1), distancias=sorted(round(d, 3) for d, m in R1)), con_parientes=tramos)
    # (c) valores fijados: 1, 10 y 20
    ks = ['1', '10', '20']; filas = sorted((float(np.mean([min(dist(a, f[k][0]) for a in RI[k]) for k in ks])), l) for l, f in Ftodo.items() if all(f.get(k) for k in ks))
    eu = [(i + 1, round(p, 3)) for i, (p, l) in enumerate(filas) if lang[l]['Glottocode'] == 'basq1248']; otro = next((round(p, 3), lang[l]['Name']) for p, l in filas if lang[l]['Glottocode'] != 'basq1248')
    print(f'(c) valores fijados (1, 10, 20): {len(filas)} variedades | euskera: {eu} | primera no vasca: {otro}'); res['valores fijados'] = dict(variedades=len(filas), euskera=eu, siguiente=otro)
    # (d) valores barajados (serie de diez valores, primera variante; 2.000 barajas)
    ks = list(IB); T = sorted((float(np.mean([min(dist(a, f[k][0]) for a in RI[k]) for k in ks])), l) for l, f in Ftodo.items() if all(f.get(k) for k in ks)); rnd = generador('numerales', 'barajas'); res['barajas'] = []
    for p, l in T[:4]:
        b = []
        for _ in range(2000):
            kk = ks[:]; rnd.shuffle(kk); b.append(np.mean([min(dist(a, Ftodo[l][q][0]) for a in RI[k]) for k, q in zip(ks, kk)]))
        res['barajas'].append((lang[l]['Name'], round(p, 3), round(float(np.mean(b)), 3), round((1 + sum(x <= p for x in b)) / 2001, 4))); print('(d)', res['barajas'][-1])
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't04_t05_numerales.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
