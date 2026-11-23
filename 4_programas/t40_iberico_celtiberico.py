"""Declaración 26: ibérico frente a celtibérico respecto del euskera, a igual tamaño de corpus.

Uso / Usage:  python3 t40_iberico_celtiberico.py RUTA/celtiberian_raw.csv
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import proyecta
from ibcomp.pruebas import perfil, divergencia, generador
from t38_celtiberico import formas_celtibericas

REP = 500

def corre(etiqueta, P, nombres, ib, cel):
    eus = next(l for l in P if nombres[l] == 'Basque'); d_cel = divergencia(perfil(cel), P[eus])
    rnd = generador('t40', etiqueta); ws = sorted(ib); n = len(cel); menor = primero = 0; ds = []
    for _ in range(REP):
        q = perfil(rnd.sample(ws, n)); d = divergencia(q, P[eus]); ds.append(d)
        menor += d < d_cel
        primero += min((divergencia(q, P[m]), nombres[m]) for m in P)[1] == 'Basque'
    ds.sort()
    r = dict(formas_iberico=len(ib), tamano_submuestra=n, div_celtiberico_euskera=round(d_cel, 4),
             div_iberico_euskera_media=round(sum(ds) / REP, 4), ic95=[round(ds[int(0.025 * REP)], 4), round(ds[int(0.975 * REP) - 1], 4)],
             iberico_mas_cerca_en=menor, euskera_primero_en=primero, de=REP,
             p1_cumplida=menor >= 0.95 * REP)
    print(f'===== {etiqueta}: {r}')
    return r

if __name__ == '__main__':
    LEX, lang = fuentes.northeuralex(); nombres = {l: lang[l]['Name'] for l in LEX}
    IB = set().union(*[f['formas'] for f in fuentes.hesperia()]); CEL = formas_celtibericas(sys.argv[1])['formas']
    res = {'clases completas': corre('clases completas', {l: perfil(ws) for l, ws in LEX.items()}, nombres, IB, CEL),
           'reducidas': corre('reducidas', {l: perfil(proyecta(ws)) for l, ws in LEX.items()}, nombres, proyecta(IB), proyecta(CEL))}
    res['p2_euskera_primero_90pc_completas'] = res['clases completas']['euskera_primero_en'] >= 0.9 * REP
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't40_iberico_celtiberico.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
