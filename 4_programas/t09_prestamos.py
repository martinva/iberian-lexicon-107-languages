"""Tabla 9: prueba con significados con los cuatro préstamos latinos propuestos y sin ellos.

Uso:  python3 t09_prestamos.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes, pruebas
from t06_t07_significados import diccionarios

if __name__ == '__main__':
    u30 = fuentes.unidades_plomos(); lat = [u for u in u30 if u['formas'][0] in fuentes.PRESTAMOS_LATINOS]; assert len(lat) == 4
    conj = {'26 unidades sin préstamos latinos': [u for u in u30 if u not in lat], '4 préstamos latinos propuestos': lat}; res = {}
    for g, dics in diccionarios().items():
        for nombre, us in conj.items():
            filas = [r for r in (pruebas.prueba_significados(us, d, nombre, minimo=max(3, 0.3 * len(us))) for d in dics) if r]
            filas.sort(key=lambda r: r['z']); res[f'{g} | {nombre}'] = filas; print(f'\n== {g} | {nombre} ({len(filas)} diccionarios)')
            for i, r in enumerate(filas, 1):
                if i <= 7 or 'uskera' in r['diccionario'] or r['diccionario'] in ('Basque', 'Latin'): print(f"  {i:2d}. {r['diccionario']:44s} unidades {r['unidades']:2d} | real {r['real']} azar {r['azar']} | z {r['z']:6.2f} p {r['p']}")
            sys.stdout.flush(); json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't09_prestamos.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
