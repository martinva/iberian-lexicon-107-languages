"""Apartado 8.5: contraste principal y prueba de permutación de los significados.

Análisis principal declarado: las 30 unidades de los plomos frente a las lenguas del Wikcionario con candidatas para
al menos el 40 % de las unidades. Se dan dos contrastes independientes entre sí.

 (a) Azar por sustitución, con 20.000 sorteos para la lengua más próxima (los 500 de la tabla 6 no permiten
     probabilidades menores de 0,002). La probabilidad se corrige multiplicándola por el número de lenguas comparadas
     (corrección de Bonferroni).
 (c) La prueba (b) repetida sin las cuatro unidades propuestas como préstamos latinos.
 (d) La prueba (b) condicionada por la longitud: los significados solo se intercambian entre unidades cuya primera
     forma reducida tiene la misma longitud. Responde a la objeción de que la permutación libre también premia la
     mera correspondencia de longitudes entre las formas y las palabras de su significado.
 (b) Permutación de los significados entre las unidades. No se sortea ninguna palabra del diccionario: se conservan
     las formas ibéricas y las listas de candidatas, y se cambia al azar qué significado corresponde a cada unidad
     (100.000 permutaciones). Estadístico: media, sobre las unidades, de la distancia a la candidata más próxima del
     significado asignado. Si las formas ibéricas se parecieran a las palabras de esa lengua en general, y no a las de
     su significado, la asignación real no destacaría entre las permutadas.
     p = (1 + número de permutaciones con valor ≤ real) / (permutaciones + 1); z respecto de las permutaciones.
     Se aplica a cada lengua del Wikcionario y a otros tres diccionarios del euskera.
Uso / Usage:  python3 t16_contraste_principal.py
"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import reducida
from ibcomp.distancia import dist
from ibcomp.pruebas import generador, prueba_significados, _z, z2

SORTEOS = 20000; PERMUTACIONES = 100000
TOL = 1e-12  # tolerancia numérica al contar permutaciones iguales o mejores que el valor real (declarada en la especificación, 4.11)

def permutacion(unidades, dic, campo, clave):
    """Prueba (b) para un diccionario. Devuelve None si hay menos de 12 unidades con candidatas."""
    F = {u['id']: [reducida(x) for x in u['formas']] for u in unidades}
    C = {u['id']: dic.candidatas(u, campo) for u in unidades}; ids = [i for i in F if C[i]]
    if len(ids) < 12: return None
    R = np.array([[min(dist(a, b) for a in F[i] for b in C[j]) for j in ids] for i in ids]); n = len(ids)
    real = float(np.trace(R) / n); rng = np.random.default_rng(generador('permutacion', clave, dic.nombre).getrandbits(63))   # semilla propia de cada cálculo: 63 bits tomados del generador sembrado con el texto de la clave
    filas = np.arange(n); val = np.empty(PERMUTACIONES)
    for k in range(PERMUTACIONES): val[k] = R[filas, rng.permutation(n)].mean()
    # (d) permutación condicionada por la longitud: los significados solo se intercambian entre unidades cuya primera forma tiene la misma longitud
    lon = np.array([len(F[i][0]) for i in ids]); grupos = [np.where(lon == x)[0] for x in sorted(set(lon))]; val2 = np.empty(PERMUTACIONES); distintas = 1
    for g in grupos: distintas *= math.factorial(len(g))
    for k in range(PERMUTACIONES):
        p = filas.copy()
        for g in grupos:
            if len(g) > 1: p[g] = rng.permutation(g)
        val2[k] = R[filas, p].mean()
    cond = dict(permutaciones_distintas_posibles=distintas, unidades_que_pueden_cambiar=int(sum(len(g) for g in grupos if len(g) > 1)), permutado=round(float(val2.mean()), 3),
                                        z=_z(real, val2), iguales_o_menores=int((val2 <= real + TOL).sum()), p=float((1 + (val2 <= real + TOL).sum()) / (PERMUTACIONES + 1)))
    return dict(diccionario=dic.nombre, unidades=n, real=round(real, 3), permutado=round(float(val.mean()), 3), z=_z(real, val),
                iguales_o_menores=int((val <= real + TOL).sum()), p=float((1 + (val <= real + TOL).sum()) / (PERMUTACIONES + 1)), condicionada_por_longitud=cond)

if __name__ == '__main__':
    U = fuentes.unidades_plomos(); W = fuentes.wikcionario(); res = {}
    # (b) permutación de los significados
    P = [r for r in (permutacion(U, d, 'terminos_en', 'plomos') for d in W.values()) if r and r['unidades'] >= 0.4 * len(U)]
    P = [r for r in P if r['z'] is not None]  # un diccionario con nulo constante (z None) no entra en la ordenación; se anota
    P.sort(key=lambda r: r['z']); m = len(P); res['b_permutacion_wikcionario'] = P
    print(f'(b) permutación de los significados, {m} lenguas del Wikcionario:')
    for i, r in enumerate(P[:6]): print(f"   {i + 1}. {r['diccionario']}: z {z2(r['z'])}, p {r['p']:.6f} (corregida por {m} lenguas: {min(1, r['p'] * m):.4f}); {r['iguales_o_menores']} de {PERMUTACIONES} permutaciones igualan o mejoran la asignación real")
    print('   mejor de las demás lenguas:', P[1]['diccionario'], z2(P[1]['z'])) if m >= 2 else print('   mejor de las demás lenguas: ninguna otra lengua con z definido')
    print('(d) permutación condicionada por la longitud (los significados solo se intercambian entre unidades de igual longitud):')
    for r in sorted(P, key=lambda r: (r['condicionada_por_longitud']['p'], r['condicionada_por_longitud']['z'] or 0))[:6]:
        c = r['condicionada_por_longitud']; print(f"   {r['diccionario']}: z {z2(c['z'])}, {c['iguales_o_menores']} de {PERMUTACIONES}, p {c['p']:.6f} (corregida por {m} lenguas: {min(1, c['p'] * m):.4f}); permutaciones distintas posibles {c['permutaciones_distintas_posibles']:.3g}; unidades que pueden cambiar {c['unidades_que_pueden_cambiar']}")
    sys.stdout.flush()
    otros = [(fuentes.opendata(), 'terminos_es'), (fuentes.azkue(), 'terminos_es'), (fuentes.wordnet()['Euskera, WordNet'], 'terminos_es'), (fuentes.wordnet()['Castellano, WordNet'], 'terminos_es')]
    res['b_permutacion_otros'] = [permutacion(U, d, c, 'plomos') for d, c in otros]
    for r in res['b_permutacion_otros']: print(f"   {r['diccionario']}: z {z2(r['z'])}, p {r['p']:.6f}; {r['iguales_o_menores']} de {PERMUTACIONES}")
    sys.stdout.flush()
    # (c) la misma permutación sin las cuatro unidades propuestas como préstamos latinos
    U26 = [u for u in U if not u['formas'][0].startswith(fuentes.PRESTAMOS_LATINOS)]
    P26 = [r for r in (permutacion(U26, d, 'terminos_en', 'plomos sin préstamos') for d in W.values()) if r and r['unidades'] >= 0.4 * len(U26)]
    P26 = [r for r in P26 if r['z'] is not None]; P26.sort(key=lambda r: r['z']); res['c_permutacion_sin_prestamos'] = P26
    print(f'(c) permutación de los significados sin los cuatro préstamos latinos, {len(P26)} lenguas:')
    for i, r in enumerate(P26[:5]): print(f"   {i + 1}. {r['diccionario']}: z {z2(r['z'])}, p {r['p']:.6f} (corregida por {len(P26)} lenguas: {min(1, r['p'] * len(P26)):.4f}); {r['iguales_o_menores']} de {PERMUTACIONES}")
    print('(d) condicionada por la longitud, sin los cuatro préstamos latinos:')
    for r in sorted(P26, key=lambda r: (r['condicionada_por_longitud']['p'], r['condicionada_por_longitud']['z'] or 0))[:4]:
        c = r['condicionada_por_longitud']; print(f"   {r['diccionario']}: z {z2(c['z'])}, {c['iguales_o_menores']} de {PERMUTACIONES}, p {c['p']:.6f} (corregida por {len(P26)} lenguas: {min(1, c['p'] * len(P26)):.4f})")
    sys.stdout.flush()
    # (a) sustitución con 20.000 sorteos para la primera lengua
    a = prueba_significados(U, W['Basque'], 'principal', sorteos=SORTEOS, minimo=0.4 * len(U), terminos='terminos_en'); a.pop('detalle')
    a['lenguas_comparadas'] = m; a['p_corregida'] = min(1.0, a['p'] * m); res['a_sustitucion_20000'] = a
    print(f"(a) sustitución, {SORTEOS} sorteos, euskera (Wikcionario): z {z2(a['z'])}, p {a['p']:.6f}, corregida por {m} lenguas: {a['p_corregida']:.5f}")
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't16_contraste_principal.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
