"""Declaración 16: efecto de la reclasificación de A7, A17 y A18 (Monografía IV, edición final) en los grupos de 8.4.

Reproduce el apartado (c) de t15_solidez_unidades.py para los grupos que dependen de qué unidades tienen una
correspondencia vasca señalada después de obtenido el significado, con la clasificación original (comprobación:
debe dar los valores del artículo v38) y con la reclasificada (A7 y A18 pasan al grupo con correspondencia; A17 es
de nivel I y no entra en estos grupos). Importa t15 sin modificarlo; mismos sorteos y lenguas.
Uso / Usage:  python3 t31_reclasificacion_m4.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from t15_solidez_unidades import tabla, z_de, EXTERNO, TOPONIMIA, PARALELO

RECLASIFICADAS = {'A7', 'A18'}          # nivel II; A17 (kutu) es de nivel I
PARALELO2 = PARALELO | RECLASIFICADAS
LAT = {'A6', 'A9', 'A11', 'A13'}

if __name__ == '__main__':
    U = fuentes.unidades_plomos(); N = len(U); W = fuentes.wikcionario(); T = {}
    for l, d in W.items():
        ids, real, azar = tabla(U, d, 'plomos', 'terminos_en')
        if len(ids) >= 0.4 * N: T[l] = (ids, real, azar)
    todas = [u['id'] for u in U]; ids_eu = set(T['Basque'][0]); casilla = set(todas) - EXTERNO - TOPONIMIA
    def puesto(G):
        zs = {}
        for l, (ids, real, azar) in T.items():
            sel = [i for i, x in enumerate(ids) if x in G]
            if len(sel) >= 4:
                z = z_de(real, azar, sel)
                if z is not None: zs[l] = z
        if 'Basque' not in zs or len(zs) < 2: return dict(z_euskera=None)
        o = sorted(zs, key=zs.get); otra = next(l for l in o if l != 'Basque')
        return dict(unidades_del_grupo=len(G), comparables_con_el_euskera=len(G & ids_eu), z_euskera=round(zs['Basque'], 2),
                    puesto=o.index('Basque') + 1, siguiente=otra, z_siguiente=round(zs[otra], 2), lenguas_comparadas=len(zs))
    res = {}
    for etiqueta, P in (('original_v38', PARALELO), ('reclasificada_m4_final', PARALELO2)):
        res[etiqueta] = {'nivel II con correspondencia vasca señalada después': puesto(P),
                         'nivel II sin correspondencia señalada': puesto(casilla - P),
                         'nivel II sin correspondencia señalada y sin los préstamos latinos': puesto(casilla - P - LAT)}
        for k, v in res[etiqueta].items(): print(etiqueta, '|', k, '|', v)
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't31_reclasificacion_m4.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
