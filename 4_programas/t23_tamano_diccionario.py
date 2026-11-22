"""Apartado 8.4: ¿depende el valor de una lengua del tamaño de su diccionario? Declarada antes de ejecutarse en
resultados/DECLARACIONES_PREVIAS.md (entrada 6).

Con las filas de la tabla 6 (30 unidades, lenguas del Wikcionario) se calcula la correlación de Spearman entre el número
de formas de cada diccionario y su valor z, con y sin el euskera; y el puesto del euskera por tamaño de diccionario.

Uso:  python3 t23_tamano_diccionario.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np

RES = os.path.join(os.path.dirname(__file__), '..', 'resultados')

def rangos(x):
    x = np.asarray(x, float); o = x.argsort(); r = np.empty(len(x)); r[o] = np.arange(1, len(x) + 1)
    for v in np.unique(x):
        m = x == v
        if m.sum() > 1: r[m] = r[m].mean()
    return r

def spearman(x, y):
    rx, ry = rangos(x), rangos(y); return float(np.corrcoef(rx, ry)[0, 1])

if __name__ == '__main__':
    d = json.load(open(os.path.join(RES, 't06_t07_significados.json'), encoding='utf-8'))
    filas = [r for r in d['Wikcionario y diccionarios históricos | 30 unidades de los plomos'] if r['diccionario'] not in ('Euskera, Azkue (1905-1906)', 'Euskera reconstruido (Trask 2008)')]
    n = [r['formas'] for r in filas]; z = [r['z'] for r in filas]; nom = [r['diccionario'] for r in filas]
    sin = [i for i, x in enumerate(nom) if x != 'Basque']
    out = dict(lenguas=len(filas), spearman_con_euskera=round(spearman(n, z), 3), spearman_sin_euskera=round(spearman([n[i] for i in sin], [z[i] for i in sin]), 3),
               formas_euskera=n[nom.index('Basque')], puesto_euskera_por_tamano=int(sorted(n, reverse=True).index(n[nom.index('Basque')]) + 1),
               mediana_formas=float(np.median(n)), por_lengua=sorted(((nom[i], n[i], round(z[i], 2)) for i in range(len(nom))), key=lambda t: t[2]))
    print(f"{len(filas)} lenguas del Wikcionario (30 unidades). Spearman(formas, z): con euskera {out['spearman_con_euskera']}; sin euskera {out['spearman_sin_euskera']}")
    print(f"Euskera: {out['formas_euskera']} formas, puesto {out['puesto_euskera_por_tamano']} de {len(filas)} por tamaño (mediana {out['mediana_formas']:.0f})")
    print('Mayores diccionarios:', sorted(((n[i], nom[i], round(z[i], 2)) for i in range(len(nom))), reverse=True)[:5])
    json.dump(out, open(os.path.join(RES, 't23_tamano_diccionario.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
