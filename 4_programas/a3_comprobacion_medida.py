"""Anexo A.3: comprobación de la medida con parentescos conocidos (NorthEuraLex, sin el euskera).

Doce veces se sacan al azar 40 conceptos; para cada pareja de lenguas se calcula la distancia media entre sus palabras
para esos conceptos (primera forma de cada concepto). Se mide con qué acierto esa distancia separa las parejas de la misma
familia de las demás: área bajo la curva (0,5 = azar; 1 = separación perfecta). Aparte, solo los parentescos antiguos:
parejas indoeuropeas o urálicas de subfamilias distintas.
Los sorteos usan la semilla 20261118 del cálculo original, sobre la lista de conceptos en orden alfabético.
Uso:  python3 a3_comprobacion_medida.py
"""
import csv, json, os, sys, random, itertools
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import red_afi
from ibcomp.distancia import dist

def auc(pos, neg):
    x = np.concatenate([pos, neg]); _, inv, cnt = np.unique(x, return_inverse=True, return_counts=True)
    r = (np.cumsum(cnt) - (cnt - 1) / 2)[inv]          # rangos medios: los empates cuentan medio
    return 1 - (r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))

if __name__ == '__main__':
    lang = {r['ID']: r for r in csv.DictReader(open(f'{fuentes.RAIZ}/northeuralex/languages.csv', encoding='utf-8'))}; F = defaultdict(dict)
    for r in csv.DictReader(open(f'{fuentes.RAIZ}/northeuralex/forms.csv', encoding='utf-8')):
        x = red_afi(r['Segments'].split())
        if x and r['Parameter_ID'] not in F[r['Language_ID']]: F[r['Language_ID']][r['Parameter_ID']] = x
    LS = sorted(l for l in F if lang[l]['Name'] != 'Basque'); conc = sorted({c for l in LS for c in F[l]}); rnd = random.Random(20261118)
    sub = {l: (lang[l].get('Subfamily') or '') for l in LS}; fam = {l: lang[l]['Family'] for l in LS}; pares = list(itertools.combinations(LS, 2))
    misma = np.array([fam[a] == fam[b] for a, b in pares]); lejana = np.array([bool(fam[a] == fam[b] and fam[a] in ('Indo-European', 'Uralic') and sub[a] != sub[b] and sub[a] and sub[b]) for a, b in pares])
    A = []; B = []
    for s in range(12):
        cs = rnd.sample(conc, 40)
        d = np.array([np.mean([dist(F[a][c], F[b][c]) for c in cs if c in F[a] and c in F[b]] or [1.0]) for a, b in pares])
        A.append(auc(d[misma], d[~misma])); B.append(auc(d[lejana], d[~misma])); print('sorteo', s + 1, round(A[-1], 3), round(B[-1], 3), flush=True)
    out = dict(lenguas=len(LS), parejas=len(pares), misma_familia=int(misma.sum()), parentesco_antiguo=int(lejana.sum()), auc=round(float(np.mean(A)), 3), auc_parentesco_antiguo=round(float(np.mean(B)), 3), minimo=round(float(np.min(A)), 3), maximo=round(float(np.max(A)), 3))
    print(out); json.dump(out, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 'a3_comprobacion_medida.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
