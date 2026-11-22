"""Tablas 6 y 7: prueba con significados, 30 unidades de los plomos y léxico metrológico, todos los diccionarios.

Uso:  python3 t06_t07_significados.py     (salida: ../resultados/t06_t07_significados.json y un resumen en pantalla)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes, pruebas

def diccionarios():
    wik = fuentes.wikcionario(); wn = fuentes.wordnet(); ap_es = fuentes.apertium('es'); ap_en = fuentes.apertium('en')
    grupos = {
        'Wikcionario y diccionarios históricos': list(wik.values()) + [fuentes.azkue(), fuentes.trask_reconstruido()],
        'Diccionarios bilingües, puente castellano': [fuentes.opendata()] + list(ap_es.values()),
        'Diccionarios bilingües, puente inglés': list(ap_en.values()),
        'Concepto a concepto (WordNet)': list(wn.values()),
    }
    return grupos

if __name__ == '__main__':
    conj = {'30 unidades de los plomos': fuentes.unidades_plomos(), 'léxico metrológico (numerales)': fuentes.unidades_numerales()}
    res = {}
    for g, dics in diccionarios().items():
        for nombre, us in conj.items():
            # mínimo de unidades con candidatas: 40 % en el Wikcionario (como en el diseño original), 30 % en los demás grupos
            minimo = max(4, (0.4 if g.startswith('Wikcionario') else 0.3) * len(us))
            filas = [r for r in (pruebas.prueba_significados(us, d, nombre, minimo=minimo) for d in dics) if r]
            filas.sort(key=lambda r: r['z']); res[f'{g} | {nombre}'] = filas
            print(f'\n== {g} | {nombre} ({len(filas)} diccionarios)')
            for i, r in enumerate(filas, 1):
                if i <= 6 or 'uskera' in r['diccionario'] or r['diccionario'] in ('Basque', 'Latin'):
                    print(f"  {i:2d}. {r['diccionario']:44s} formas {r['formas']:6d} | unidades {r['unidades']:2d} | real {r['real']} azar {r['azar']} | z {r['z']:6.2f} p {r['p']}")
            sys.stdout.flush()
            json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't06_t07_significados.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
