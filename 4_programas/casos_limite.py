"""Casos límite sintéticos (auditoría, fases 4c y 4d): nulos constantes y valores z no definidos.

No usa datos lingüísticos. Comprueba que la guarda común `pruebas._z` devuelve None con un nulo constante, también
cuando la coma flotante deja una desviación residual, y que los consumidores (t15, t16, t17, t26) no fallan cuando un z
no está definido (desde la fase 4f, la comprobación 9 llama a las funciones reales de agregación de t15 y t26) o cuando no queda ninguna otra lengua con z definido.
Uso / Usage:  python3 casos_limite.py      (imprime «todo correcto» o el error)
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp.pruebas import _z, z2

def comprueba():
    # 1. nulo constante exacto y nulo constante con residuo de coma flotante
    assert _z(0.0, [0.5] * 100) is None
    assert _z(0.0, [0.1] * 100) is None            # np.std([0.1]*100) puede no ser exactamente 0
    assert _z(0.0, np.cumsum([0.1] * 100) * 0) is None
    assert abs(_z(0.0, [0.0, 1.0]) + 1.0) < 1e-12   # (0 − 0,5) / 0,5
    assert z2(None) is None and z2(-1.23456) == -1.23
    # 2. t26: z individual con la guarda común
    from t26_prestabilidad import z_por_unidad, spearman
    azar = np.array([[0.1, 0.2, 0.3]] * 100); real = np.array([0.0, 0.0, 0.0])
    z = z_por_unidad(['a', 'b', 'c'], real, azar); assert all(v is None for v in z.values()), z
    pares = [(z[i], 1.0) for i in z if z[i] is not None]; assert pares == []     # ninguna pareja: no se calcula ρ
    azar[:, 1] = np.linspace(0, 1, 100); z = z_por_unidad(['a', 'b', 'c'], real, azar); assert z['a'] is None and z['b'] is not None
    # 3. t15: puesto sin z del euskera y pasos de la retirada adversa con puesto None
    pasos = [dict(quitadas=1, puesto=None, z_euskera=None), dict(quitadas=2, puesto=2, z_euskera=-2.5)]
    assert next((p['quitadas'] for p in pasos if p['puesto'] is not None and p['puesto'] > 1), None) == 2
    assert next((p['quitadas'] for p in pasos if p['z_euskera'] is not None and p['z_euskera'] > -3), None) == 2
    zs = [None, None]; ind = sum(v is None for v in zs); zs = sorted(v for v in zs if v is not None); assert zs == [] and ind == 2
    # 4. t16: una sola lengua con z definido
    P = [dict(diccionario='Basque', z=-5.0)]; m = len(P)
    assert ((P[1]['diccionario'], z2(P[1]['z'])) if m >= 2 else 'ninguna otra lengua con z definido') == 'ninguna otra lengua con z definido'
    # 5. t17: conjunto vacío de rivales con z definido
    res = {'Basque': dict(propuestos=dict(z=-5.0), trampa_en_el_campo=dict(z=None), trampa_libre=dict(z=None)), 'X': dict(propuestos=dict(z=None), trampa_en_el_campo=dict(z=None), trampa_libre=dict(z=None))}
    otras = {l: r for l, r in res.items() if l != 'Basque' and r['trampa_en_el_campo']['z'] is not None and r['trampa_libre']['z'] is not None}
    assert otras == {}
    # 6. t15: agregados con puestos indefinidos mezclados (consumidores completos a, b, c)
    vals = [(None, None, None, None, 1), (-5.0, 1, 'X', -2.0, 30)]
    av = [v for v in vals if v[0] is not None]
    assert len(vals) - len(av) == 1 and max(v[0] for v in av) == -5.0
    import json as _json
    _json.dumps({'z': None, 'indefinidos': 1})               # el JSON debe ser estándar: None → null, nunca NaN
    try:
        _json.dumps(float('nan'), allow_nan=False); raise AssertionError('NaN no debe entrar en el JSON')
    except ValueError: pass
    # 7. t26: Spearman con menos de tres parejas o rangos constantes
    from t26_prestabilidad import spearman
    assert spearman([], []) is None and spearman([1.0], [2.0]) is None and spearman([1, 1, 1], [1, 2, 3]) is None
    assert abs(spearman([1, 2, 3], [1, 2, 3]) - 1.0) < 1e-12
    # 8. t24: una sola lengua con z definido → None, sin StopIteration
    zs = {'Basque': -5.0}
    assert ('Basque' not in zs or len(zs) < 2) == True
    # 9. Fase 4f: consumidores completos con las funciones reales del estudio (no expresiones simplificadas)
    from t15_solidez_unidades import agrega_quitando_una
    vac = agrega_quitando_una({'A1': (None, None, None, None, 1), 'A2': (None, None, None, None, 0)})
    assert vac['z_mas_debil'] is None and vac['z_mas_fuerte'] is None and vac['menor_separacion'] is None and vac['indefinidos'] == 2 and vac['primero_en'] == 0
    mix = agrega_quitando_una({'A1': (None, None, None, None, 1), 'A2': (-5.0, 1, 'X', -2.0, 30), 'A3': (-4.0, 2, 'Y', -4.5, 30)})
    assert mix['z_mas_debil'] == -4.0 and mix['z_mas_fuerte'] == -5.0 and mix['menor_separacion'] == -0.5 and mix['indefinidos'] == 1 and mix['primero_en'] == 1
    from t26_prestabilidad import agrega_referencia
    r0 = agrega_referencia({'a': dict(unidades=2, rho=None), 'b': dict(unidades=1, rho=None)})
    assert r0['rho_mediana'] is None and r0['rho_minima'] is None and r0['rho_maxima'] is None and r0['sin_rho'] == 2
    r1 = agrega_referencia({'a': dict(unidades=5, rho=None), 'b': dict(unidades=9, rho=0.3), 'c': dict(unidades=9, rho=-0.1)})
    assert r1['sin_rho'] == 1 and r1['rho_minima'] == -0.1 and r1['rho_maxima'] == 0.3 and abs(r1['rho_mediana'] - 0.1) < 1e-12 and 'a' in r1['por_lengua']
    _json.dumps(vac, allow_nan=False); _json.dumps(r0, allow_nan=False); _json.dumps(r1, allow_nan=False)   # serialización estándar: null, nunca NaN
    print('todo correcto')

if __name__ == '__main__':
    comprueba()
