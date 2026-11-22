"""Apartado 8.4: resultado sin las unidades para las que las monografías dejan abierta una lectura alternativa
(nombre de persona o término distinto) en alguna de sus apariciones. Declarada antes de ejecutarse en
resultados/DECLARACIONES_PREVIAS.md (entrada 4).

Unidades retiradas: A11 (oŕtin: segmentación antroponímica alternativa de ortinbeŕe- en T.07.02), A12 (selki: la mayoría
de sus apariciones son nombres de persona bimembres), A13 (saltu: saldulako leído como nombre de persona por Ferrer i
Jané 2026a), A16 (akari: alternativa de antropónimos con salida en -ka en V.17.02), A19 (laku: lakei como unidad de
capacidad en Ferrer i Jané 2022, además de saldulako).

Uso:  python3 t21_lecturas_alternativas.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.pruebas import z2
import t15_solidez_unidades as t15

RETIRADAS = {'A11', 'A12', 'A13', 'A16', 'A19'}

if __name__ == '__main__':
    U = fuentes.unidades_plomos(); N = len(U); W = fuentes.wikcionario(); T = {}
    for l, d in W.items():
        ids, real, azar = t15.tabla(U, d, 'plomos', 'terminos_en')
        if len(ids) >= 0.4 * N: T[l] = (ids, real, azar)
    zs = {}
    for l, (ids, real, azar) in T.items():
        sel = [i for i, x in enumerate(ids) if x not in RETIRADAS]
        if len(sel) >= 4:
            z = t15.z_de(real, azar, sel)
            if z is not None: zs[l] = z
    o = sorted(zs, key=zs.get)
    res = dict(unidades_retiradas=sorted(RETIRADAS), unidades_que_quedan=N - len(RETIRADAS), lenguas_comparadas=len(zs),
               puesto_euskera=o.index('Basque') + 1, tabla=[(l, round(zs[l], 3)) for l in o[:8]])
    print(f"Sin {len(RETIRADAS)} unidades con lectura alternativa ({', '.join(sorted(RETIRADAS))}): {N - len(RETIRADAS)} unidades, {len(zs)} lenguas")
    print(f"  euskera: puesto {res['puesto_euskera']}, z {z2(zs['Basque'])}; siguientes: {[(l, z2(zs[l])) for l in o[:4] if l != 'Basque']}")
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't21_lecturas_alternativas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
