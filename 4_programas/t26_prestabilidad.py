"""Declaración 9: gradiente de prestabilidad. Correlación de Spearman entre el valor z individual de cada unidad frente al
euskera (sorteos de t15, Wikcionario y Open Data Euskadi) y la puntuación de prestabilidad de su significado en la base
mundial de préstamos (WOLD, `Borrowed_score`; 35 unidades, `1_fuentes_lexicas/wold_prestabilidad_35_unidades.csv`).
Referencia: la misma correlación para las demás lenguas del Wikcionario con candidatas suficientes. Genera sus propios
500 sorteos (`tabla`, clave 'prestabilidad'), no reutiliza los de t15: desviación del plan anotada en la declaración 9.
Uso / Usage:  python3 t26_prestabilidad.py
"""
import csv, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.pruebas import _z
from t15_solidez_unidades import tabla

AQUI = os.path.dirname(__file__)

def spearman(x, y):
    def rangos(v):
        o = np.argsort(v, kind='mergesort'); r = np.empty(len(v)); s = np.array(v)[o]; i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and s[j + 1] == s[i]: j += 1
            r[o[i:j + 1]] = (i + j) / 2 + 1; i = j + 1
        return r
    if len(x) < 3: return None   # con menos de tres parejas la correlación no se calcula (guarda de la fase 4e)
    a, b = rangos(x), rangos(y)
    if np.std(a) == 0 or np.std(b) == 0: return None
    return float(np.corrcoef(a, b)[0, 1])

def z_por_unidad(ids, real, azar):
    """z individual de cada unidad con la guarda común `pruebas._z` (None si los sorteos de esa unidad son constantes)."""
    return {i: _z(real[k], azar[:, k]) for k, i in enumerate(ids)}

def agrega_referencia(ref):
    """Agregados de la referencia entre lenguas. Las lenguas cuya ρ no es calculable (None) se conservan en `por_lengua`,
    se cuentan en `sin_rho` y no entran en mediana ni extremos; sin ninguna ρ válida, los agregados son None (fase 4f)."""
    val = sorted(r['rho'] for r in ref.values() if r['rho'] is not None)
    return dict(lenguas=len(ref), por_lengua=ref, sin_rho=len(ref) - len(val), rho_mediana=float(np.median(val)) if val else None,
                rho_minima=val[0] if val else None, rho_maxima=val[-1] if val else None)

if __name__ == '__main__':
    W = fuentes.wold = {r['id']: float(r['borrowed_score']) for r in csv.DictReader(open(os.path.join(AQUI, '..', '1_fuentes_lexicas', 'wold_prestabilidad_35_unidades.csv'), encoding='utf-8'))}
    U = [u for u in fuentes.unidades_plomos() + fuentes.unidades_numerales() if u['id'] in W]; N = len(U); res = {}
    fuentes_eu = [('Wikcionario', fuentes.wikcionario()['Basque'], 'terminos_en'), ('Open Data Euskadi', fuentes.opendata(), 'terminos_es')]
    for nombre, d, campo in fuentes_eu:
        if d is None: continue
        ids, real, azar = tabla(U, d, 'prestabilidad', campo); z = z_por_unidad(ids, real, azar)
        pares = [(z[i], W[i]) for i in ids if z[i] is not None]
        rho = spearman([p[0] for p in pares], [p[1] for p in pares])
        res[nombre] = dict(unidades=len(pares), rho=rho, z_por_unidad={i: (None if z[i] is None else round(z[i], 3)) for i in ids}, prestabilidad={i: W[i] for i in ids})
        print(f'{nombre}: {len(pares)} unidades comparables, ρ de Spearman (z individual, prestabilidad) = ' + (f'{rho:+.3f}' if rho is not None else 'no calculable'))
    ref = {}
    for l, d in fuentes.wikcionario().items():
        ids, real, azar = tabla(U, d, 'prestabilidad', 'terminos_en')
        if len(ids) < 0.4 * N: continue
        z = z_por_unidad(ids, real, azar); pares = [(z[i], W[i]) for i in ids if z[i] is not None]
        ref[l] = dict(unidades=len(pares), rho=spearman([p[0] for p in pares], [p[1] for p in pares]))
    res['lenguas'] = L = agrega_referencia(ref)
    if L['rho_mediana'] is None: print(f"Referencia, {len(ref)} lenguas del Wikcionario: ninguna ρ calculable")
    else: print(f"Referencia, {len(ref)} lenguas del Wikcionario: ρ mediana {L['rho_mediana']:+.3f}, entre {L['rho_minima']:+.3f} y {L['rho_maxima']:+.3f}" + (f" ({L['sin_rho']} sin ρ calculable)" if L['sin_rho'] else ''))
    json.dump(res, open(os.path.join(AQUI, '..', 'resultados', 't26_prestabilidad.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
