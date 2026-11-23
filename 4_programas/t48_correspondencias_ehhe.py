"""Declaración 34: regularidad de correspondencias (t25) con las formas vascas antiguas del EHHE donde las hay.

Uso / Usage:  python3 t48_correspondencias_ehhe.py RUTA/ehhe_extraccion.json
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.pruebas import generador
from t25_correspondencias import alinea, regularidad, parejas, columnas_de, PERMUTACIONES
from t47_cronologia_ehhe import par_antiguo
from ehhe_parse import entradas
from ibcomp.clases import reducida

if __name__ == '__main__':
    E = entradas(sys.argv[1]); idx = {}
    for e in E:
        for c in e['cabeceras']: idx.setdefault(reducida(c), []).append(e)
    U = fuentes.unidades_plomos() + fuentes.unidades_numerales(); P = parejas(U, fuentes.wikcionario()['Basque'])
    P2 = []; cambios = []
    for i, f, c in P:
        nuevo = c
        for e in idx.get(c, []):
            pa = par_antiguo(e)
            if pa: nuevo = pa[0]; cambios.append((i, c, nuevo)); break
        P2.append((i, f, nuevo))
    obs = regularidad(columnas_de(P2))['R_prima']['media']; mod = regularidad(columnas_de(P))['R_prima']['media']
    rnd = generador('correspondencias', 'permutacion'); F = [f for _, f, _ in P2]; C = [c for _, _, c in P2]; R = []
    for _ in range(PERMUTACIONES):
        perm = rnd.sample(range(len(P2)), len(P2)); cs = []
        for f, k in zip(F, perm): cs += alinea(f, C[k])
        R.append(regularidad(cs)['R_prima']['media'])
    pct = sum(x < obs for x in R) / len(R) * 100
    res = dict(cambios=cambios, R_prima_moderno=mod, R_prima_antiguo=obs, percentil=pct, mediana_perm=float(np.median(R)), p90=sorted(R)[int(.9 * len(R))],
               previsiones={'1': pct >= 99, '2': obs >= mod})
    print(json.dumps(res, ensure_ascii=False, indent=1))
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't48_correspondencias_ehhe.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
