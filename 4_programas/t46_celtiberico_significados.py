"""Declaración 32: control celtibérico de la prueba con significados (piloto; lista fijada en la declaración).

Uso / Usage:  python3 t46_celtiberico_significados.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes, pruebas

LISTA = [  # forma, términos ingleses (búsqueda en el Wikcionario), glosa
    ('dekam', ['ten'], 'diez'), ('sues', ['six'], 'seis'), ('novan', ['nine'], 'nueve'), ('ekuo', ['horse'], 'caballo'),
    ('ku', ['dog', 'hound'], 'perro'), ('duatir', ['daughter'], 'hija'), ('arganto', ['silver'], 'plata'),
    ('gentis', ['son', 'offspring', 'descendant'], 'hijo, descendencia'), ('kamanom', ['path', 'way', 'road'], 'camino'),
    ('okris', ['mountain', 'hill'], 'monte'), ('treba', ['settlement', 'village', 'town'], 'poblado'),
    ('briga', ['hill', 'town', 'fortress'], 'colina, ciudad'), ('teiuo', ['god'], 'dios'), ('boustom', ['cowshed', 'stable', 'byre'], 'establo'),
    ('eni', ['in', 'into'], 'en'), ('uta', ['and'], 'y'), ('as', ['we', 'us'], 'nosotros'), ('loutu', ['load', 'burden'], 'carga'),
    ('monima', ['memory'], 'memoria'), ('veizos', ['witness'], 'testigo'), ('ozas', ['foot', 'feet'], 'pies'),
    ('togias', ['roof', 'house'], 'techos, casas'), ('olokas', ['garden', 'orchard'], 'huertos'), ('erekaias', ['furrow', 'field'], 'surcos'),
    ('ablu', ['strong'], 'fuerte'), ('silabur', ['money', 'silver'], 'dinero'), ('kar', ['friendship', 'friend'], 'amistad'),
    ('dekez', ['do', 'make', 'did'], 'hizo'), ('datuz', ['give'], 'debe dar'), ('melmu', ['intelligence', 'mind'], 'inteligencia'),
]

if __name__ == '__main__':
    us = [dict(id=f'C{i + 1}', formas=[f], terminos_en=t, glosa=g) for i, (f, t, g) in enumerate(LISTA)]
    filas = [r for r in (pruebas.prueba_significados(us, d, 'celtibérico 30', minimo=0.4 * len(us)) for d in fuentes.wikcionario().values()) if r]
    filas.sort(key=lambda r: r['z'])
    for i, r in enumerate(filas, 1):
        print(f"{i:2d}. {r['diccionario']:20s} unidades {r['unidades']:2d} real {r['real']} azar {r['azar']} z {r['z']:6.2f} p {r['p']:.4f}")
    eus = next((i for i, r in enumerate(filas, 1) if r['diccionario'] == 'Basque'), None)
    zb = next((r['z'] for r in filas if r['diccionario'] == 'Basque'), None)
    prev = {'1': filas[0]['diccionario'] != 'Basque', '2': any(r['diccionario'] in ('Welsh', 'Irish', 'Latin') for r in filas[:3]), '3': zb is None or zb >= -2}
    print('puesto euskera', eus, 'z', zb, prev)
    json.dump(dict(lista=LISTA, filas=filas, puesto_euskera=eus, z_euskera=zb, previsiones=prev),
              open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't46_celtiberico_significados.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
