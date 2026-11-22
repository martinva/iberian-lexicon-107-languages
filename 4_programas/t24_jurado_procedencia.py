"""Declaración 7: tabla 10 bis con la clasificación de la procedencia hecha por el jurado ciego.

Repite el apartado (c) de t15_solidez_unidades.py (mismos sorteos, misma semilla, mismos diccionarios del
Wikcionario) con los grupos que resultan de la segunda codificación: la de cada juez y la menos favorable
(el nivel más bajo que haya dado cualquiera de los tres a cada unidad). Las respuestas íntegras y la clave
están en 2_criterios/jurado/respuestas/.
Uso / Usage:  python3 t24_jurado_procedencia.py [suficiencia]
"""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from t15_solidez_unidades import tabla, z_de

AQUI = os.path.dirname(__file__)
# Sin argumento: primera pregunta (declaración 7, `respuestas/`). Con `suficiencia`: segunda pregunta (declaración 10, `respuestas_suficiencia/`).
RONDA = 'respuestas_suficiencia' if 'suficiencia' in sys.argv[1:] else 'respuestas'
CRUCE = os.path.join(AQUI, '..', '2_criterios', 'jurado', RONDA, 'cruce_con_la_clave.tsv')
SALIDA = 't24_jurado_procedencia_suficiencia.json' if RONDA == 'respuestas_suficiencia' else 't24_jurado_procedencia.json'

if __name__ == '__main__':
    filas = [r for r in csv.DictReader(open(CRUCE, encoding='utf-8'), delimiter='\t') if not r['control']]
    U = fuentes.unidades_plomos(); N = len(U); todas = [u['id'] for u in U]
    W = fuentes.wikcionario(); T = {}
    for l, d in W.items():
        ids, real, azar = tabla(U, d, 'plomos', 'terminos_en')
        if len(ids) >= 0.4 * N: T[l] = (ids, real, azar)
    ids_eu = T['Basque'][0]
    def puesto(G):
        zs = {}
        for l, (ids, real, azar) in T.items():
            sel = [i for i, x in enumerate(ids) if x in G]
            if len(sel) >= 4:
                z = z_de(real, azar, sel)
                if z is not None: zs[l] = z
        if 'Basque' not in zs or len(zs) < 2: return None   # sin euskera o sin otra lengua con z definido no hay comparación (guarda de la fase 4e)
        o = sorted(zs, key=zs.get); otra = next(l for l in o if l != 'Basque')
        return dict(z_euskera=round(zs['Basque'], 2), puesto=o.index('Basque') + 1, siguiente=otra, z_siguiente=round(zs[otra], 2), lenguas_comparadas=len(zs))
    res = {}
    for quien in ('autor', 'Mistral', 'DeepSeek', 'Grok', 'menos_favorable'):
        niv = {r['unidad']: r[quien] for r in filas if r['unidad'].startswith('A')}
        res[quien] = {}
        for nombre, G in (('nivel I', {u for u, n in niv.items() if n == 'I'}), ('niveles I y II', {u for u, n in niv.items() if n in ('I', 'II')}),
                          ('nivel II', {u for u, n in niv.items() if n == 'II'}), ('nivel III', {u for u, n in niv.items() if n == 'III'})):
            v = puesto(G); res[quien][nombre] = dict(unidades_del_grupo=len(G), comparables_con_el_euskera=len(G & set(ids_eu)), resultado=v)
            print(f'{quien:16s} {nombre:15s} n={len(G):2d} comparables={len(G & set(ids_eu)):2d}', v if v else 'menos de cuatro unidades comparables: no se calcula')
    json.dump(res, open(os.path.join(AQUI, '..', 'resultados', SALIDA), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
