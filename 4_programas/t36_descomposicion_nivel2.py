"""Declaración 21: descomposición por unidades del grupo de nivel II sin correspondencia vasca señalada (t15, 8.4).

Para las 13 unidades del grupo y para euskera, tagalo, gallego y albanés (Wikcionario; mismas tablas y semilla que t15):
distancia real, candidata más próxima y contribución de la unidad (media de los sorteos menos distancia real; positiva =
más próxima que el azar). Después, valor del grupo sin las unidades cuya candidata tagala más próxima es préstamo del
castellano según la nota etimológica del Wikcionario inglés (regla de la declaración 11), leída de
`1_fuentes_lexicas/wikcionario/t36_etimologia_tagalo.csv` (consulta del 22-11-2026).
Uso / Usage:  python3 t36_descomposicion_nivel2.py
"""
import csv, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import reducida
from ibcomp.distancia import dist
from t15_solidez_unidades import tabla, z_de, EXTERNO, TOPONIMIA, PARALELO

LENGUAS = ('Basque', 'Tagalog', 'Galician', 'Albanian')
if __name__ == '__main__':
    U = fuentes.unidades_plomos(); W = fuentes.wikcionario(); L = fuentes.wikcionario_lemas()
    G = sorted(set(u['id'] for u in U) - EXTERNO - TOPONIMIA - PARALELO, key=lambda x: int(x[1:]))
    porid = {u['id']: u for u in U}; res = dict(unidades=G, lenguas={})
    for l in LENGUAS:
        d = W[l]; ids, real, azar = tabla(U, d, 'plomos', 'terminos_en')
        sel = [i for i, x in enumerate(ids) if x in G]
        lem = {}
        for w in L[l]:
            lem.setdefault(reducida(fuentes.NORM[l](w)), []).append(w)
        filas = []
        for i in sel:
            u = porid[ids[i]]; ri = [reducida(x) for x in u['formas']]; c = sorted(d.candidatas(u, 'terminos_en'))
            best = min(c, key=lambda b: min(dist(a, b) for a in ri))
            filas.append(dict(unidad=ids[i], formas=u['formas'], significado=u.get('glosa', ''), candidata_reducida=best,
                              lemas=sorted(lem.get(best, [])), distancia=round(float(real[i]), 3),
                              contribucion=round(float(azar[:, i].mean() - real[i]), 3)))
        z = z_de(real, azar, sel)
        res['lenguas'][l] = dict(z_grupo=None if z is None else round(z, 2), comparables=len(sel), filas=filas, _ids=ids, _sel=sel)
        print(l, res['lenguas'][l]['z_grupo'], len(sel))
        for f in sorted(filas, key=lambda f: -f['contribucion']): print('   ', f['unidad'], f['formas'], f['lemas'][:3], f['distancia'], f['contribucion'])
    # sin hispanismos del tagalo
    ruta = os.path.join(os.path.dirname(__file__), '..', '1_fuentes_lexicas', 'wikcionario', 't36_etimologia_tagalo.csv')
    if os.path.exists(ruta):
        esp = {r['unidad'] for r in csv.DictReader(open(ruta, encoding='utf-8')) if r['clase'] == 'préstamo del castellano'}
        res['unidades_con_hispanismo_tagalo'] = sorted(esp, key=lambda x: int(x[1:])); res['sin_hispanismos'] = {}
        for l in LENGUAS:
            d = W[l]; ids, real, azar = tabla(U, d, 'plomos', 'terminos_en')
            sel = [i for i, x in enumerate(ids) if x in G and x not in esp]
            z = z_de(real, azar, sel) if len(sel) >= 4 else None
            res['sin_hispanismos'][l] = dict(z=None if z is None else round(z, 2), comparables=len(sel))
        print('sin hispanismos', res['unidades_con_hispanismo_tagalo'], res['sin_hispanismos'])
    for v in res['lenguas'].values(): v.pop('_ids'); v.pop('_sel')
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't36_descomposicion_nivel2.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
