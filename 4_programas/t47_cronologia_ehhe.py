"""Declaración 33: cronología con el EHHE (formas vascas antiguas frente a modernas).

Uso / Usage:  python3 t47_cronologia_ehhe.py RUTA/ehhe_extraccion.json   (datos de Euskaltzaindia: no se redistribuyen)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ehhe_parse import entradas
from ibcomp.clases import reducida
from ibcomp.distancia import dist
from ibcomp.pruebas import generador

def par_antiguo(e):
    if not e['atestiguaciones']: return None
    forma, anio = min(e['atestiguaciones'], key=lambda x: x[1])
    a, m = reducida(forma), reducida(e['cabeceras'][0])
    return (a, m, forma, anio) if a != m else None

def puntua(ib, a, m):
    da, dm = dist(ib, a), dist(ib, m)
    return 1.0 if da < dm else (0.5 if da == dm else 0.0), da, dm

if __name__ == '__main__':
    E = entradas(sys.argv[1]); idx = {}
    for e in E:
        for c in e['cabeceras']: idx.setdefault(reducida(c), []).append(e)
    P = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't25_correspondencias.json')))['euskera']['parejas']
    filas = []
    for p in P:
        for e in idx.get(p['euskera'], []):
            pa = par_antiguo(e)
            if pa:
                s, da, dm = puntua(p['iberico'], pa[0], pa[1])
                filas.append(dict(id=p['id'], iberico=p['iberico'], entrada=e['id'], cabecera=e['cabeceras'][0], antigua=pa[2], anio=pa[3], d_antigua=da, d_moderna=dm, punto=s)); break
    con = [par_antiguo(e) for e in E]; con = [c for c in con if c]
    real = sum(f['punto'] for f in filas) / len(filas) if filas else None
    rnd = generador('t47', 'nulo'); nul = []
    for _ in range(10000):
        nul.append(sum(puntua(f['iberico'], *rnd.choice(con)[:2])[0] for f in filas) / len(filas))
    p = (1 + sum(x >= real for x in nul)) / 10001 if filas else None
    res = dict(unidades_con_variante_antigua=len(filas), filas=filas, proporcion_antigua_mas_cerca=real,
               nulo_media=sum(nul) / len(nul), p=p, entradas_ehhe=len(E), entradas_con_variante_antigua=len(con),
               previsiones={'1': real is not None and real > 0.5, '2': p is not None and p < 0.05})
    print(json.dumps(res, ensure_ascii=False, indent=1))
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't47_cronologia_ehhe.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
