"""Apartado 8.4: ensayo sobre la circularidad (resultado no concluyente). ¿Cuánto valor puede fabricar quien elige los
significados a favor de una lengua?

Para cada lengua se asigna a cada unidad ibérica, a propósito, el significado del repertorio (los 30 propuestos) que más
la acerca a esa lengua: (a) dentro de su campo; (b) entre los 30. El valor de esa asignación se compara con el que el
euskera obtiene con los significados propuestos.

Uso:  python3 t17_techo_circularidad.py
"""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from ibcomp import fuentes
from ibcomp.pruebas import generador, _z, z2
from t15_solidez_unidades import pares

SORTEOS = 200

def campos():
    """Campo de cada unidad, del conjunto CLDF: contable, predial o personas."""
    out = {}
    for r in csv.DictReader(open(os.path.join(fuentes.RAIZ, 'iberico', 'cldf', 'parameters.csv'), encoding='utf-8')):
        c = ' '.join(str(v) for v in r.values())
        if r['ID'].startswith('A'): out[r['ID']] = 'contable' if 'contable' in c else 'predial' if 'predial' in c else 'personas' if 'personas' in c else None
    assert all(out.values()) and len(out) == 30, out
    return out

def z_de_asignacion(R, A, asig):
    """asig: lista de (unidad i, significado j). z de la media de R frente a la media de A en cada sorteo."""
    real = np.mean([R[k] for k in asig]); nul = np.mean([A[k] for k in asig], axis=0)
    return _z(real, nul), float(real)

if __name__ == '__main__':
    U = fuentes.unidades_plomos(); ids = [u['id'] for u in U]; C = campos(); W = fuentes.wikcionario(); res = {}
    for l in sorted(W):
        d = W[l]; con = [u['id'] for u in U if d.candidatas(u, 'terminos_en')]
        if len(con) < 0.4 * len(U): continue
        R, A = pares(U, d, 'terminos_en', SORTEOS, generador('techo', l))
        propia = [(i, i) for i in ids if i in con]
        campo = [(i, min((j for j in con if C[j] == C[i]), key=lambda j: R[i, j])) for i in ids if any(C[j] == C[i] for j in con)]
        libre = [(i, min(con, key=lambda j: R[i, j])) for i in ids]
        zp, rp = z_de_asignacion(R, A, propia); zc, rc = z_de_asignacion(R, A, campo); zl, rl = z_de_asignacion(R, A, libre)
        res[l] = dict(propuestos=dict(z=zp, real=round(rp, 3), unidades=len(propia)), trampa_en_el_campo=dict(z=zc, real=round(rc, 3), coinciden_con_los_propuestos=sum(i == j for i, j in campo)),
                      trampa_libre=dict(z=zl, real=round(rl, 3), coinciden_con_los_propuestos=sum(i == j for i, j in libre)))
        f = lambda z: f'{z:7.2f}' if z is not None else '   None'
        print(f"{l:18s} propuestos {f(zp)} | trampa en el campo {f(zc)} | trampa libre {f(zl)}", flush=True)
    eu = res['Basque']['propuestos']['z']; otras = {l: r for l, r in res.items() if l != 'Basque' and r['trampa_en_el_campo']['z'] is not None and r['trampa_libre']['z'] is not None}
    print(f"\nEuskera con los significados propuestos: {eu}")
    if otras:  # si ninguna otra lengua tiene z definido, no hay techo que dar
        tc = min(otras.items(), key=lambda kv: kv[1]['trampa_en_el_campo']['z']); tl = min(otras.items(), key=lambda kv: kv[1]['trampa_libre']['z'])
        print(f"Techo de las demás lenguas, trampa dentro del campo: {tc[0]} {z2(tc[1]['trampa_en_el_campo']['z'])}")
        print(f"Techo de las demás lenguas, trampa libre: {tl[0]} {z2(tl[1]['trampa_libre']['z'])}")
    else: print('Techo de las demás lenguas: ninguna con z definido')
    print(f"Euskera haciendo trampa: en el campo {res['Basque']['trampa_en_el_campo']}, libre {res['Basque']['trampa_libre']}")
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't17_techo_circularidad.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
