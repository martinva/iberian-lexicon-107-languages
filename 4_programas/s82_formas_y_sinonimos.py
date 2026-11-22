"""Apartado 8.2: la prueba con significados añadiendo las formas flexionadas y una lista ampliada de sinónimos.

Solo entran las lenguas del Wikcionario con más de 200 lemas con formas flexionadas, para que la ampliación sea igual para todas.
Parámetros propios de esta comprobación: 300 sorteos; si una unidad tiene más de 400 candidatas, se reducen una vez, al azar, a 400 (las mismas para el valor real y para los sorteos).
Uso:  python3 s82_formas_y_sinonimos.py
"""
import json, os, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes, pruebas
from ibcomp.clases import reducida
from ibcomp.normalizadores import NORM

if __name__ == '__main__':
    G = fuentes.wikcionario_lemas(); FM = fuentes.formas_flexionadas(G); LENG = sorted(l for l in FM if len(FM[l]) > 200); print('lenguas con formas:', len(LENG), LENG)
    def dic(l, con_formas):
        d = defaultdict(set)
        for w, g in G[l].items():
            for x in ({w} | (FM[l].get(w, set()) if con_formas else set())):
                r = reducida(NORM[l](x))
                if fuentes.LMIN <= len(r) <= fuentes.LMAX: d[r] |= g
        return fuentes.Diccionario(l, d)
    u30 = fuentes.unidades_plomos(); num = fuentes.unidades_numerales()
    VAR = [('30 unidades | forma de cita', u30, False, 'terminos_en'), ('30 unidades | + formas flexionadas', u30, True, 'terminos_en'), ('30 unidades | + sinónimos', u30, False, 'terminos_en_v2'),
           ('30 unidades | + formas y sinónimos', u30, True, 'terminos_en_v2'), ('léxico metrológico | forma de cita', num, False, 'terminos_en'), ('léxico metrológico | + formas flexionadas', num, True, 'terminos_en')]
    res = {}; filas_de = {nombre: [] for nombre, *_ in VAR}
    for fo in (False, True):          # se construye un solo diccionario cada vez, para no ocupar memoria con todos a la vez
        for l in LENG:
            d = dic(l, fo)
            for nombre, us, fo2, term in VAR:
                if fo2 != fo: continue
                r = pruebas.prueba_significados(us, d, nombre, sorteos=300, minimo=max(4, 0.4 * len(us)), terminos=term, tope=400)
                if r: filas_de[nombre].append(r)
            del d
    for nombre, us, fo, term in VAR:
        filas = filas_de[nombre]
        filas.sort(key=lambda r: r['z']); res[nombre] = filas; eu = next((r for r in filas if r['diccionario'] == 'Basque'), None)
        print(f"{nombre}: euskera z {eu['z']:.2f}, puesto {filas.index(eu) + 1} de {len(filas)}, unidades {eu['unidades']} | primeras: {[(r['diccionario'], round(r['z'], 2)) for r in filas[:4]]}", flush=True)
        json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 's82_formas_y_sinonimos.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
