"""Distancia entre dos formas reducidas. Especificación: «Medida de distancia»."""
from functools import lru_cache

_V = frozenset('aeiou')

@lru_cache(maxsize=4000000)
def dist(a, b):
    """Distancia de edición ponderada y normalizada entre dos cadenas de clases de sonidos.

    Las clases de vocal se escriben en minúscula (a e i o u); las de consonante, en mayúscula.
    Costes: insertar o borrar una vocal, 0,5; insertar o borrar una consonante, 1; sustituir vocal por vocal
    distinta, 0,5; cualquier otra sustitución, 1; símbolos iguales, 0.
    El coste mínimo de transformar `a` en `b` se divide por la media de los pesos de las dos cadenas
    (peso = 0,5 por vocal y 1 por consonante). Si alguna está vacía, la distancia es 1. Si son iguales, 0.
    """
    if not a or not b: return 1.0
    if a == b: return 0.0
    ca = [0.5 if x in _V else 1.0 for x in a]; cb = [0.5 if y in _V else 1.0 for y in b]; vb = [y in _V for y in b]
    prev = [0.0]
    for y in cb: prev.append(prev[-1] + y)
    for i, x in enumerate(a):
        cx = ca[i]; xv = x in _V; cur = [prev[0] + cx]
        for j, y in enumerate(b):
            s = 0.0 if x == y else (0.5 if (xv and vb[j]) else 1.0)
            v = prev[j] + s
            t = prev[j + 1] + cx
            if t < v: v = t
            t = cur[j] + cb[j]
            if t < v: v = t
            cur.append(v)
        prev = cur
    return prev[-1] / ((sum(ca) + sum(cb)) / 2)
