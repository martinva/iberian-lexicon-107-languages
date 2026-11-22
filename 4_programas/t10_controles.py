"""Tabla 10: la prueba con significados aplicada a seis lenguas de control (cuatro de filiación conocida y dos aisladas).

De cada lengua se sacan cinco muestras de 30 palabras con glosa; cada muestra se trata como el conjunto ibérico:
candidatas = palabras de cada diccionario del Wikcionario cuya glosa comparte algún término con la de la palabra.
Parámetros: 150 sorteos; se exigen al menos 12 palabras con candidatas.
Las muestras se obtienen con la semilla 20261119 + suma de los códigos de las letras del nombre inglés de la lengua
(se sacan ocho muestras seguidas y se usan las cinco primeras), para que sean las mismas del cálculo original.
Uso:  python3 t10_controles.py [lengua …]
"""
import json, os, sys, random
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes, pruebas
from ibcomp.normalizadores import red_control

PARIENTES = {'Umbrian': {'Latin', 'Catalan', 'Galician', 'Asturian', 'Occitan', 'Romanian', 'Sicilian', 'Sardinian'}, 'Dalmatian': {'Latin', 'Catalan', 'Galician', 'Asturian', 'Occitan', 'Romanian', 'Sicilian', 'Sardinian'},
             'Cornish': {'Welsh', 'Irish'}, 'Gothic': {'Icelandic'}, 'Etruscan': set(), 'Sumerian': set()}

if __name__ == '__main__':
    wik = list(fuentes.wikcionario().values()); res = {}; ruta = os.path.join(os.path.dirname(__file__), '..', 'resultados', 't10_controles.json')
    for lengua in (sys.argv[1:] or list(fuentes.CONTROL)):
        LEXT = fuentes.lexico_control(lengua); PAL = sorted(LEXT); rnd = random.Random(20261119 + sum(map(ord, lengua))); muestras = [rnd.sample(PAL, 30) for _ in range(8)][:5]; res[lengua] = []
        for k, m in enumerate(muestras, 1):
            us = [dict(id=w, formas=[w], terminos_en=sorted(LEXT[w])) for w in m]
            filas = [r for r in (pruebas.prueba_significados(us, d, f'{lengua}|{k}', sorteos=150, minimo=12, reductor=red_control) for d in wik) if r]
            filas.sort(key=lambda r: r['z']); t = [(r['diccionario'], round(r['z'], 3)) for r in filas]; res[lengua].append(dict(muestra=k, palabras=m, tabla=t, primera_es_pariente=bool(t and t[0][0] in PARIENTES[lengua])))
            print(f'{fuentes.CONTROL[lengua]} ({len(PAL)} palabras elegibles), muestra {k}: {t[:4]}', flush=True)
            json.dump(res, open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        v = [x['tabla'][0][1] for x in res[lengua] if x['tabla']]
        print(f'  → primera lengua pariente en {sum(x["primera_es_pariente"] for x in res[lengua])} de 5; valor de la primera lengua, de {max(v)} a {min(v)}', flush=True)
