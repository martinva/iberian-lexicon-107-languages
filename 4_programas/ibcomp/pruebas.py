"""Pruebas estadísticas. Especificación: «Prueba con significados», «Perfil de combinaciones de sonidos»."""
import math, random
from collections import Counter
import numpy as np
from . import SEMILLA
from .clases import reducida
from .distancia import dist

def generador(*clave):
    """Generador de números al azar propio de cada cálculo: la semilla es el texto «SEMILLA|clave». Así el resultado no depende del orden de ejecución."""
    return random.Random('|'.join([str(SEMILLA)] + [str(c) for c in clave]))

def _z(real, nulo):
    """(real − media) / desviación típica poblacional de los sorteos, sin redondear; None si los sorteos son constantes.

    Un nulo constante se detecta por su recorrido (máximo − mínimo), no solo por la desviación: un vector de valores
    iguales puede dar en coma flotante una desviación residual distinta de cero y un z espurio."""
    nulo = np.asarray(nulo, dtype=float); s = float(np.std(nulo))
    if s == 0 or float(nulo.max() - nulo.min()) <= 1e-12 * max(1.0, float(abs(nulo).max())): return None
    return float((real - np.mean(nulo)) / s)

def z2(z):
    """z con dos decimales para imprimir (None queda como None)."""
    return None if z is None else round(z, 2)

def sustituye(rnd, listas, por_longitud):
    """Un sorteo del azar. `listas`: una lista de candidatas (formas reducidas) por unidad.

    Cada candidata DISTINTA se sustituye por una forma tomada al azar entre las del diccionario que tienen su misma
    longitud, SIN repetir forma dentro de cada longitud. Una candidata que comparten varias unidades recibe la misma
    sustituta en todas. Así el sorteo conserva el número de candidatas distintas, sus longitudes y las candidatas
    compartidas. Devuelve, para cada unidad, la lista de sustitutas.
    """
    por_n = {}
    for c in listas:
        for x in c: por_n.setdefault(len(x), {})[x] = None
    for n, d in por_n.items():
        claves = sorted(d); fondo = por_longitud[n]
        if len(fondo) < len(claves): raise ValueError(f'el diccionario tiene menos formas de longitud {n} que candidatas: no cabe un sorteo sin repetición')
        for x, y in zip(claves, rnd.sample(fondo, len(claves))): d[x] = y
    return [[por_n[len(x)][x] for x in c] for c in listas]

def prueba_significados(unidades, dic, clave, sorteos=500, minimo=None, terminos=None, tope=None, reductor=reducida):
    """Prueba con significados de un conjunto de unidades ibéricas frente a un diccionario.

    Para cada unidad: candidatas = formas del diccionario cuyo significado coincide con alguno de sus términos;
    distancia de la unidad = la menor entre sus formas (reducidas con `reducida`) y las candidatas.
    Estadístico = media de esas distancias sobre las unidades con candidatas.
    Azar: en cada sorteo, las candidatas se sustituyen por formas al azar del mismo diccionario y de su misma longitud
    en clases, sin repetir forma y conservando las candidatas compartidas (función `sustituye`); se recalcula el
    estadístico. z = (real − media de los sorteos) / desviación típica; p = (1 + número de sorteos con valor ≤ real) / (sorteos + 1).
    Devuelve None si las unidades con candidatas son menos que `minimo`.
    `tope`: si una unidad tiene más candidatas, se toman `tope` de ellas al azar, una sola vez, y con ellas se calculan
    tanto el valor real como los sorteos.
    `reductor`: función que pasa las formas de la unidad a clases (por defecto `reducida`).
    """
    rnd = generador('significados', clave, dic.nombre); reg = []
    for u in unidades:
        c = dic.candidatas(u, terminos)
        if not c: continue
        c = sorted(c)
        if tope is not None and len(c) > tope: c = sorted(rnd.sample(c, tope))
        ri = [reductor(x) for x in u['formas']]; d, mejor = min((dist(a, b), b) for a in ri for b in c)
        reg.append((u['id'], ri, d, c, mejor, len(c)))
    if minimo is None: minimo = max(4, 0.3 * len(unidades))
    if len(reg) < minimo: return None
    real = float(np.mean([r[2] for r in reg])); BL = dic.por_longitud; nul = np.empty(sorteos); listas = [r[3] for r in reg]
    for k in range(sorteos):
        sus = sustituye(rnd, listas, BL)
        nul[k] = sum(min(dist(a, b) for b in cs for a in r[1]) for r, cs in zip(reg, sus)) / len(reg)
    return dict(diccionario=dic.nombre, formas=len(dic.formas), unidades=len(reg), real=round(real, 3), azar=round(float(nul.mean()), 3),
                z=_z(real, nul), p=float((1 + (nul <= real).sum()) / (sorteos + 1)), iguales_o_menores=int((nul <= real).sum()), ventaja=round(float(nul.mean() - real), 6),
                detalle={r[0]: dict(distancia=round(r[2], 2), forma=r[4], candidatas=r[5]) for r in reg})

def perfil(formas):
    """Perfil de combinaciones de sonidos: frecuencia relativa de cada par de símbolos consecutivos, con ^ (inicio) y $ (fin) de palabra, sobre un conjunto de formas distintas."""
    c = Counter()
    for w in formas:
        z = '^' + w + '$'
        for a, b in zip(z, z[1:]): c[a + b] += 1
    t = sum(c.values()); return {k: v / t for k, v in c.items()}

def divergencia(p, q):
    """Divergencia de Jensen-Shannon entre dos perfiles, en bits (0 = idénticos; 1 = sin nada en común)."""
    d = 0.0
    for k in sorted(set(p) | set(q)):          # orden fijo, para que la suma no dependa del orden interno del conjunto
        a = p.get(k, 0.0); b = q.get(k, 0.0); m = (a + b) / 2
        if a: d += 0.5 * a * math.log2(a / m)
        if b: d += 0.5 * b * math.log2(b / m)
    return d

GRUPOS_ESTABLES = {'N1', 'N2', 'N3', 'N4', 'N5', 'A21', 'A30', 'A24', 'A27', 'A28', 'A13'}     # uno a cinco, dar, hacer, tierra, hierba, camino, monte

def ventaja_por_grupos(formas_x, conceptos, dic, rnd, grupos, sorteos=200, tope=40):
    """Segunda parte: ventaja sobre el azar por grupos de significados.

    `formas_x`: id de significado → formas reducidas de la lengua examinada; `conceptos`: lista de (id, unidad con términos);
    `grupos`: nombre → conjunto de ids. Para cada significado con candidatas en `dic` (si pasan de `tope`, se toman `tope` al azar):
    distancia real = la menor entre las formas y las candidatas; azar = lo mismo sustituyendo las candidatas por formas
    al azar de su misma longitud, sin repetir y conservando las compartidas (función `sustituye`), `sorteos` veces.
    Para cada grupo con al menos tres significados:
    ventaja = media del azar − media real; z = (real − media del azar) / desviación típica del azar.
    """
    reg = []
    for cid, u in conceptos:
        if cid not in formas_x: continue
        c = dic.candidatas(u, 'terminos_en')
        if not c: continue
        c = sorted(c)
        if len(c) > tope: c = sorted(rnd.sample(c, tope))
        reg.append([cid, min(dist(a, b) for a in formas_x[cid] for b in c), c, []])
    for _ in range(sorteos):
        for r, cs in zip(reg, sustituye(rnd, [r[2] for r in reg], dic.por_longitud)):
            r[3].append(min(dist(a, b) for a in formas_x[r[0]] for b in cs))
    reg = [(r[0], r[1], r[3]) for r in reg]
    out = {}
    for nombre, ids in grupos.items():
        r = [x for x in reg if x[0] in ids]
        if len(r) < 3: out[nombre] = None; continue
        real = float(np.mean([x[1] for x in r])); nm = np.mean(np.array([x[2] for x in r]), axis=0)
        out[nombre] = dict(n=len(r), real=round(real, 3), azar=round(float(nm.mean()), 3), z=_z(real, nm), ventaja=round(float(nm.mean() - real), 6))
    return out
