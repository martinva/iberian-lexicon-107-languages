"""Declaración 8: regularidad de las correspondencias entre clases de sonidos (ibérico–euskera).

Para cada una de las 40 unidades (30 de los plomos y 10 numerales) se toma la candidata del Wikcionario vasco a menor
distancia y se alinea con la forma ibérica (primera forma, reducida a clases SCA) por Needleman–Wunsch con los mismos
costes que la distancia del estudio (Anexo A.1: vocal 0,5, consonante 1; empates del trazado, diagonal). Cada columna
es un par (clase ibérica, clase vasca); «−» es hueco. Regularidad R: proporción de columnas que van al correspondiente
más frecuente de su clase; R′: lo mismo solo en las columnas no idénticas. Se da por clase ibérica, por clase vasca y
la media. Azar: 1.000 permutaciones de los significados (cada forma ibérica con la candidata de otra unidad) y
referencia con las demás lenguas del Wikcionario con candidatas para al menos el 40 % de las unidades.
Uso / Usage:  python3 t25_correspondencias.py
"""
import json, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import reducida
from ibcomp.distancia import dist
from ibcomp.pruebas import generador

_V = frozenset('aeiou')
PERMUTACIONES = 1000

def alinea(a, b):
    """Alineación óptima de dos cadenas de clases con los costes de `distancia.dist`; devuelve la lista de columnas (x, y)."""
    ca = [0.5 if x in _V else 1.0 for x in a]; cb = [0.5 if y in _V else 1.0 for y in b]
    n, m = len(a), len(b); D = np.zeros((n + 1, m + 1)); T = np.zeros((n + 1, m + 1), dtype=int)  # 0 diag, 1 arriba (hueco en b), 2 izquierda (hueco en a)
    for i in range(1, n + 1): D[i][0] = D[i - 1][0] + ca[i - 1]; T[i][0] = 1
    for j in range(1, m + 1): D[0][j] = D[0][j - 1] + cb[j - 1]; T[0][j] = 2
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            x, y = a[i - 1], b[j - 1]; s = 0.0 if x == y else (0.5 if (x in _V and y in _V) else 1.0)
            opciones = ((D[i - 1][j - 1] + s, 0), (D[i - 1][j] + ca[i - 1], 1), (D[i][j - 1] + cb[j - 1], 2))
            D[i][j], T[i][j] = min(opciones, key=lambda t: (t[0], t[1]))      # a igual coste, la diagonal
    cols = []; i, j = n, m
    while i > 0 or j > 0:
        t = T[i][j]
        if t == 0: cols.append((a[i - 1], b[j - 1])); i -= 1; j -= 1
        elif t == 1: cols.append((a[i - 1], '−')); i -= 1
        else: cols.append(('−', b[j - 1])); j -= 1
    return cols[::-1]

def regularidad(columnas):
    """R (todas las columnas) y R′ (solo no idénticas), por clase ibérica, por clase vasca y media."""
    def r(cols, k):
        if not cols: return None
        por = defaultdict(Counter)
        for c in cols: por[c[k]][c[1 - k]] += 1
        return sum(max(v.values()) for v in por.values()) / len(cols)
    noid = [c for c in columnas if c[0] != c[1]]
    out = {}
    for nombre, cols in (('R', columnas), ('R_prima', noid)):
        a, b = r(cols, 0), r(cols, 1)
        out[nombre] = dict(por_clase_iberica=a, por_clase_vasca=b, media=None if a is None else (a + b) / 2, columnas=len(cols))
    return out

def parejas(unidades, dic, campo='terminos_en'):
    """[(id, forma ibérica reducida, candidata más próxima)] para las unidades con candidatas."""
    out = []
    for u in unidades:
        c = dic.candidatas(u, campo)
        if not c: continue
        f = reducida(u['formas'][0]); mejor = min(sorted(c), key=lambda x: dist(f, x)); out.append((u['id'], f, mejor))
    return out

def columnas_de(pares):
    cols = []
    for _, f, c in pares: cols += alinea(f, c)
    return cols

if __name__ == '__main__':
    U = fuentes.unidades_plomos() + fuentes.unidades_numerales(); N = len(U); W = fuentes.wikcionario(); res = {}
    P = parejas(U, W['Basque']); cols = columnas_de(P); reg = regularidad(cols)
    tabla = Counter(cols)
    res['euskera'] = dict(parejas=[dict(id=i, iberico=f, euskera=c, alineacion=' '.join(f'{x}:{y}' for x, y in alinea(f, c))) for i, f, c in P],
                          regularidad=reg, correspondencias=[dict(iberico=x, euskera=y, n=n) for (x, y), n in sorted(tabla.items(), key=lambda kv: (-kv[1], kv[0]))])
    print(f"Euskera: {len(P)} parejas, {reg['R']['columnas']} columnas, {reg['R_prima']['columnas']} no idénticas; R {reg['R']['media']:.3f}, R′ {reg['R_prima']['media']:.3f} (por clase ibérica {reg['R_prima']['por_clase_iberica']:.3f}, por clase vasca {reg['R_prima']['por_clase_vasca']:.3f})")
    # (1) permutación de los significados
    rnd = generador('correspondencias', 'permutacion'); F = [f for _, f, _ in P]; C = [c for _, _, c in P]; Rp = []; Rpp = []
    for _ in range(PERMUTACIONES):
        perm = rnd.sample(range(len(P)), len(P)); cs = []
        for f, k in zip(F, perm): cs += alinea(f, C[k])
        r = regularidad(cs); Rp.append(r['R']['media']); Rpp.append(r['R_prima']['media'])
    Rp.sort(); Rpp.sort(); obs = reg['R_prima']['media']; pct = sum(x < obs for x in Rpp) / len(Rpp) * 100
    res['permutacion'] = dict(permutaciones=PERMUTACIONES, R_prima_observada=obs, percentil=pct, mayores_o_iguales=sum(x >= obs for x in Rpp),
                              R_prima_percentil_10=Rpp[int(0.1 * len(Rpp))], R_prima_mediana=float(np.median(Rpp)), R_prima_percentil_90=Rpp[int(0.9 * len(Rpp))],
                              R_observada=reg['R']['media'], R_mediana=float(np.median(Rp)), R_percentil_90=Rp[int(0.9 * len(Rp))])
    print(f"Permutación: R′ observada {obs:.3f}, percentil {pct:.1f} de {PERMUTACIONES} (mediana {np.median(Rpp):.3f}, p90 {Rpp[int(0.9 * len(Rpp))]:.3f}); R observada {reg['R']['media']:.3f}, mediana {np.median(Rp):.3f}")
    # (2) referencia entre lenguas
    ref = {}
    for l, d in W.items():
        Pl = parejas(U, d)
        if len(Pl) < 0.4 * N: continue
        r = regularidad(columnas_de(Pl)); ref[l] = dict(parejas=len(Pl), columnas=r['R']['columnas'], no_identicas=r['R_prima']['columnas'], R=r['R']['media'], R_prima=r['R_prima']['media'])
    orden = sorted(ref, key=lambda l: (-(ref[l]['R_prima'] or 0), l)); res['lenguas'] = dict(orden_por_R_prima=[(l, ref[l]) for l in orden], puesto_euskera=orden.index('Basque') + 1, lenguas=len(ref))
    print(f"Lenguas comparadas: {len(ref)}; puesto del euskera por R′: {orden.index('Basque') + 1}")
    for l in orden[:8]: print(f"   {l:14s} parejas {ref[l]['parejas']:2d} no idénticas {ref[l]['no_identicas']:3d} R {ref[l]['R']:.3f} R′ {ref[l]['R_prima']:.3f}")
    print('Correspondencias más frecuentes (ibérico:euskera n):', ' '.join(f'{x}:{y} {n}' for (x, y), n in sorted(tabla.items(), key=lambda kv: -kv[1])[:20]))
    # (3) Comprobación añadida después de ver el resultado (21-11-2026): R′ depende del número de columnas no idénticas (con menos columnas,
    #     la proporción máxima por clase sube por azar). Se iguala el tamaño: en cada permutación y en cada lengua se toman al azar tantas
    #     columnas no idénticas como tiene el euskera (200 submuestras) y se promedia R′. Generador «correspondencias|submuestra».
    def r_prima_igualada(cols_noid, n, rnd, veces=200):
        if len(cols_noid) <= n: return regularidad(cols_noid)['R_prima']['media']
        return float(np.mean([regularidad(rnd.sample(cols_noid, n))['R_prima']['media'] for _ in range(veces)]))
    n_eu = reg['R_prima']['columnas']; rnd2 = generador('correspondencias', 'submuestra'); Rq = []
    rnd = generador('correspondencias', 'permutacion')
    for _ in range(PERMUTACIONES):
        perm = rnd.sample(range(len(P)), len(P)); cs = []
        for f, k in zip(F, perm): cs += alinea(f, C[k])
        Rq.append(r_prima_igualada([c for c in cs if c[0] != c[1]], n_eu, rnd2, 20))
    Rq.sort(); pctq = sum(x < obs for x in Rq) / len(Rq) * 100
    refq = {}
    for l, d in W.items():
        Pl = parejas(U, d)
        if len(Pl) < 0.4 * N: continue
        refq[l] = r_prima_igualada([c for c in columnas_de(Pl) if c[0] != c[1]], n_eu, rnd2)
    ordenq = sorted(refq, key=lambda l: (-refq[l], l))
    res['tamano_igualado'] = dict(columnas_no_identicas=n_eu, permutacion=dict(percentil=pctq, mayores_o_iguales=sum(x >= obs for x in Rq), mediana=float(np.median(Rq)), percentil_90=Rq[int(0.9 * len(Rq))]),
                                  lenguas=dict(puesto_euskera=ordenq.index('Basque') + 1, orden=[(l, round(refq[l], 3)) for l in ordenq]))
    print(f"Tamaño igualado a {n_eu} columnas no idénticas: permutación, percentil {pctq:.1f} (mediana {np.median(Rq):.3f}, p90 {Rq[int(0.9 * len(Rq))]:.3f}); puesto del euskera entre lenguas {ordenq.index('Basque') + 1}; primeras: {[(l, round(refq[l], 3)) for l in ordenq[:5]]}")
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't25_correspondencias.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
