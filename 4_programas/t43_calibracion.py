"""Declaración 29: calibración por tamaño de los controles de escritura de la declaración 27.

Uso / Usage:  python3 t43_calibracion.py RUTA/celtiberian_raw.csv
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.pruebas import perfil, divergencia, generador
from t41_escritura import formas_cel_por_escritura

def puesto(ws, P, nombres):
    q = perfil(ws); o = sorted((divergencia(q, P[l]), nombres[l]) for l in P)
    nm = [x for _, x in o]; i = nm.index('Basque'); return i + 1, o[i][0]

def submuestras(ws, n, P, nombres, clave, rep=500):
    rnd = generador('t43', clave); ws = sorted(ws); out = []
    for _ in range(rep): out.append(puesto(rnd.sample(ws, n), P, nombres))
    return out

def resumen(xs):
    ds = sorted(d for _, d in xs); ps = [p for p, _ in xs]
    return dict(entre_5=sum(p <= 5 for p in ps), primero=sum(p == 1 for p in ps), de=len(xs),
                div_mediana=round(ds[len(ds) // 2], 4), div_ic95=[round(ds[int(.025 * len(ds))], 4), round(ds[int(.975 * len(ds)) - 1], 4)])

if __name__ == '__main__':
    LEX, lang = fuentes.northeuralex(); nombres = {l: lang[l]['Name'] for l in LEX}
    P = {l: perfil(ws) for l, ws in LEX.items()}
    fichas = fuentes.hesperia()
    gr = set().union(*[f['formas'] for f in fichas if f['signario'] == 'GRECOIBERICO'])
    lv = set().union(*[f['formas'] for f in fichas if f['signario'] == 'LEVANTINO'])
    lat, sig = formas_cel_por_escritura(sys.argv[1])
    ib = submuestras(lv, len(gr), P, nombres, 'levantino'); ce = submuestras(sig, len(lat), P, nombres, 'signario')
    r = dict(n_grecoiberico=len(gr), n_celtiberico_latino=len(lat),
             grecoiberico=dict(zip(('puesto', 'div'), puesto(gr, P, nombres))),
             celtiberico_latino=dict(zip(('puesto', 'div'), puesto(lat, P, nombres))),
             levantino_submuestras=resumen(ib), celtiberico_signario_submuestras=resumen(ce))
    dl = r['celtiberico_latino']['div']; dg = r['grecoiberico']['div']
    r['celtiberico_latino']['frac_signario_menor'] = round(sum(d < dl for _, d in ce) / len(ce), 3)
    r['grecoiberico']['frac_levantino_menor'] = round(sum(d < dg for _, d in ib) / len(ib), 3)
    r['previsiones'] = {'1': r['levantino_submuestras']['entre_5'] >= 450,
                        '2': r['celtiberico_signario_submuestras']['entre_5'] < r['levantino_submuestras']['entre_5'],
                        '3': r['celtiberico_latino']['frac_signario_menor'] >= .95,
                        '4': .025 <= r['grecoiberico']['frac_levantino_menor'] <= .975}
    for k in ('grecoiberico', 'celtiberico_latino'): r[k]['div'] = round(r[k]['div'], 4)
    print(json.dumps(r, ensure_ascii=False, indent=1))
    json.dump(r, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't43_calibracion.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
