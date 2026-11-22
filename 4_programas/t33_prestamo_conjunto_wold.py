"""Declaración 18: frecuencia del préstamo conjunto de los significados de los plomos en las 41 lenguas de WOLD.

Uso:  python3 t33_prestamo_conjunto_wold.py RUTA_A/lexibank/wold/cldf
(edición CLDF lexibank/wold, commit 1df62b9bdc7292b35982aea49b4d5bd1951f6f3e)
"""
import csv, json, os, sys, math
from collections import defaultdict
from scipy.stats import beta

RAIZ = os.path.join(os.path.dirname(__file__), '..')
SI = ('1. clearly borrowed', '2. probably borrowed')

def ic(k, n):
    lo = 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1); hi = 1.0 if k == n else beta.ppf(0.975, k + 1, n - k)
    return [round(float(lo), 4), round(float(hi), 4)]

def main(cldf):
    sig = list(csv.DictReader(open(os.path.join(RAIZ, '1_fuentes_lexicas', 'wold_prestabilidad_35_unidades.csv'), encoding='utf-8')))
    wid = {s['wold_id']: s['id'] for s in sig}
    num = {s['id'] for s in sig if s['id'].startswith('N')}; otros = {s['id'] for s in sig} - num
    W = defaultdict(lambda: defaultdict(list))
    for r in csv.DictReader(open(os.path.join(cldf, 'forms.csv'), encoding='utf-8')):
        if r['Parameter_ID'] in wid: W[r['Language_ID']][wid[r['Parameter_ID']]].append(r['Borrowed'] in SI)
    lenguas = sorted(W); n = len(lenguas); res = dict(lenguas=n, commit_wold='1df62b9bdc7292b35982aea49b4d5bd1951f6f3e')
    for regla, f in (('amplia', any), ('estricta', all)):
        filas = []
        for l in lenguas:
            pn = [f(v) for k, v in W[l].items() if k in num]; po = [f(v) for k, v in W[l].items() if k in otros]
            filas.append(dict(lengua=l, numerales=[sum(pn), len(pn)], otros=[sum(po), len(po)]))
        todos_num = [x for x in filas if x['numerales'][1] and x['numerales'][0] == x['numerales'][1]]
        out = dict(por_lengua=filas, todos_los_numerales=dict(k=len(todos_num), lenguas=[x['lengua'] for x in todos_num]))
        for nombre, u in (('mitad', 0.5), ('tres_cuartos', 0.75), ('todos', 1.0)):
            o = [x for x in filas if x['otros'][1] and x['otros'][0] / x['otros'][1] >= u - 1e-9]
            both = [x for x in o if x in todos_num]
            out[f'otros_{nombre}'] = dict(k=len(o), lenguas=[x['lengua'] for x in o])
            out[f'numerales_y_otros_{nombre}'] = dict(k=len(both), lenguas=[x['lengua'] for x in both])
        for key in [k for k in out if isinstance(out[k], dict) and 'k' in out[k]]:
            k = out[key]['k']; out[key].update(frecuencia=round(k / n, 4), estimacion=round((k + 1) / (n + 2), 4), ic95=ic(k, n))
        # frecuencia por significado y producto bajo independencia
        p = {}
        for s in num | otros:
            v = [f(W[l][s]) for l in lenguas if W[l].get(s)]; p[s] = sum(v) / len(v) if v else None
        prod = lambda S: math.prod(p[s] for s in S if p[s] is not None)
        out['frecuencia_por_significado'] = {s: round(p[s], 4) for s in sorted(p) if p[s] is not None}
        out['independencia'] = dict(todos_los_numerales=prod(num), todos_los_otros=prod(otros), todo_el_conjunto=prod(num | otros))
        res[regla] = out
        print(f"\n== regla {regla}: {n} lenguas")
        for key in [k for k in out if isinstance(out[k], dict) and 'k' in out[k]]:
            print(f"  {key:28s} {out[key]['k']:2d}/{n}  est. {out[key]['estimacion']}  IC95 {out[key]['ic95']}  {out[key]['lenguas'][:8]}")
        print('  independencia:', {k: f'{v:.2e}' for k, v in out['independencia'].items()})
    json.dump(res, open(os.path.join(RAIZ, 'resultados', 't33_prestamo_conjunto_wold.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main(sys.argv[1])
