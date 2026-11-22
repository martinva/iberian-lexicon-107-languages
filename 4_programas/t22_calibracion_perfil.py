"""Apartado 7.4: calibración de la distancia entre perfiles. ¿Es 0,153 (ibérico–euskera) una distancia pequeña
entre lenguas sin relación conocida? Declarada antes de ejecutarse en resultados/DECLARACIONES_PREVIAS.md (entrada 5).

Para las 107 lenguas de NorthEuraLex (clases completas y reducidas a lo que el ibérico escribe) se calculan las
distancias de todas las parejas y se separan en parejas de la misma familia y de familias distintas. Se da en qué
percentil de cada grupo cae la distancia ibérico–euskera, cuántas parejas de familias distintas están a esa
distancia o menos, y qué lenguas sin parientes en la base tienen un vecino a esa distancia o menos.

Uso:  python3 t22_calibracion_perfil.py
"""
import itertools, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from ibcomp import fuentes
from ibcomp.clases import proyecta
from ibcomp.pruebas import perfil, divergencia

def calibra(etiqueta, LEX, nombres, familia, ib):
    P = {l: perfil(ws) for l, ws in LEX.items()}; pib = perfil(ib); L = sorted(P)
    d_ib = {l: divergencia(pib, P[l]) for l in L}; eu = next(l for l in L if nombres[l] == 'Basque'); d_eu = d_ib[eu]
    pares = [(a, b, divergencia(P[a], P[b])) for a, b in itertools.combinations(L, 2)]
    misma = np.array([d for a, b, d in pares if familia[a] and familia[a] == familia[b]])
    dist = np.array([d for a, b, d in pares if not (familia[a] and familia[a] == familia[b])])
    fams = {}
    for l in L: fams.setdefault(familia[l], []).append(l)
    sin = [l for l in L if len(fams[familia[l]]) == 1 or not familia[l]]
    vecino = {l: min((divergencia(P[l], P[m]), nombres[m]) for m in L if m != l) for l in sin}
    out = dict(iberico_euskera=round(d_eu, 4), parejas_misma_familia=len(misma), parejas_familias_distintas=len(dist),
               percentil_misma_familia=round(100 * float((misma <= d_eu).mean()), 1), percentil_familias_distintas=round(100 * float((dist <= d_eu).mean()), 2),
               familias_distintas_a_esa_distancia_o_menos=int((dist <= d_eu).sum()), minimo_familias_distintas=round(float(dist.min()), 4), mediana_familias_distintas=round(float(np.median(dist)), 4),
               minimo_misma_familia=round(float(misma.min()), 4), mediana_misma_familia=round(float(np.median(misma)), 4),
               lenguas_sin_parientes=len(sin), sin_parientes_con_vecino_a_esa_distancia_o_menos=sorted((nombres[l], round(v[0], 4), v[1]) for l, v in vecino.items() if v[0] <= d_eu),
               vecinos_de_las_sin_parientes=sorted((nombres[l], round(v[0], 4), v[1]) for l, v in vecino.items()),
               parejas_familias_distintas_mas_proximas=sorted(((round(d, 4), nombres[a], nombres[b]) for a, b, d in pares if not (familia[a] and familia[a] == familia[b])))[:10])
    print(f'== {etiqueta}: ibérico–euskera {d_eu:.4f} | misma familia: percentil {out["percentil_misma_familia"]} de {len(misma)} parejas | familias distintas: percentil {out["percentil_familias_distintas"]} de {len(dist)} ({out["familias_distintas_a_esa_distancia_o_menos"]} a esa distancia o menos; mínimo {out["minimo_familias_distintas"]})')
    print(f'   lenguas sin parientes en la base: {len(sin)}; con vecino a ≤ {d_eu:.3f}: {out["sin_parientes_con_vecino_a_esa_distancia_o_menos"]}')
    print(f'   parejas de familias distintas más próximas: {out["parejas_familias_distintas_mas_proximas"][:5]}')
    return out

if __name__ == '__main__':
    fichas = fuentes.hesperia(); TODAS = set().union(*[f['formas'] for f in fichas])
    LEX, lang = fuentes.northeuralex(); nombres = {l: lang[l]['Name'] for l in LEX}; familia = {l: (lang[l].get('Family') or '') for l in LEX}
    res = {'clases completas': calibra('clases completas', LEX, nombres, familia, TODAS),
           'reducidas a lo que el ibérico escribe': calibra('reducidas', {l: proyecta(ws) for l, ws in LEX.items()}, nombres, familia, proyecta(TODAS))}
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't22_calibracion_perfil.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
