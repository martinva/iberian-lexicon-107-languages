"""Declaración 19: razón de verosimilitud de los resultados de la segunda parte frente a parejas emparentadas y de contacto.
Lee solo resultados publicados (t11_t13_estables.json, t08_perfil.json, t18_perfil_contacto.json).
Uso:  python3 t34_razon_verosimilitud.py     Salida: ../resultados/t34_razon_verosimilitud.json
"""
import json, os
import numpy as np
RES = os.path.join(os.path.dirname(__file__), '..', 'resultados')
PRIOR = (0.10, 0.25, 0.50, 0.75, 0.90)

def razon(kr, nr, kc, nc, clave):
    pr, pc = (kr + 0.5) / (nr + 1), (kc + 0.5) / (nc + 1)
    rng = np.random.default_rng(20261122 + sum(map(ord, clave)))
    s = rng.beta(kr + 0.5, nr - kr + 0.5, 100000) / rng.beta(kc + 0.5, nc - kc + 0.5, 100000)
    R = pr / pc
    return dict(emparentadas=[kr, nr], contacto=[kc, nc], p_emparentadas=round(pr, 4), p_contacto=round(pc, 4), razon=round(R, 2),
                ic95=[round(float(np.percentile(s, 2.5)), 2), round(float(np.percentile(s, 97.5)), 2)],
                posterior={str(p): round(R * p / (R * p + 1 - p), 3) for p in PRIOR})

t11 = json.load(open(os.path.join(RES, 't11_t13_estables.json'), encoding='utf-8'))
ib = t11['iberico']['Basque']; v_e = ib['estables']['ventaja']; v_s = ib['estables sin los numerales del dos al cinco']['ventaja']
emp = [p for p in t11['parejas'] if isinstance(p[3], dict) and p[0] in ('emparentadas cercanas', 'emparentadas lejanas')]
con = [p for p in t11['parejas'] if isinstance(p[3], dict) and p[0] == 'solo contacto']   # se omiten las parejas sin resultado (Zulu–Shona: sin cobertura suficiente)
def cuenta(G, f): return sum(1 for p in G if f(p[3])), len(G)
res = dict(valores_iberico=dict(estables=v_e, poco_estables=ib['poco estables']['ventaja'], estables_sin_2_5=v_s))
R1 = lambda d: d['estables']['ventaja'] > d['poco estables']['ventaja']
R2 = lambda d: d['estables']['ventaja'] >= v_e
R3 = lambda d: d['estables sin los numerales del dos al cinco']['ventaja'] >= v_s
for nombre, f in (('R1', R1), ('R2', R2), ('R3', R3)):
    kr, nr = cuenta(emp, f); kc, nc = cuenta(con, f); res[nombre] = razon(kr, nr, kc, nc, nombre)
    res[nombre]['parejas_que_cumplen'] = dict(emparentadas=[f'{p[1]}–{p[2]}' for p in emp if f(p[3])], contacto=[f'{p[1]}–{p[2]}' for p in con if f(p[3])])
v = json.load(open(os.path.join(RES, 't08_perfil.json'), encoding='utf-8'))['NorthEuraLex, clases completas']['validacion']
c = json.load(open(os.path.join(RES, 't18_perfil_contacto.json'), encoding='utf-8'))['resumen']
res['R4'] = razon(v['aciertos'], v['total'], c['donante_primera'], c['parejas'], 'R4')
orden = sorted(['R1', 'R2', 'R3', 'R4'], key=lambda k: -res[k]['ic95'][0]); res['orden_por_limite_inferior'] = orden
json.dump(res, open(os.path.join(RES, 't34_razon_verosimilitud.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k in ('R1', 'R2', 'R3', 'R4'): print(k, {x: res[k][x] for x in ('emparentadas', 'contacto', 'razon', 'ic95', 'posterior')})
print('orden', orden); print(res['R2']['parejas_que_cumplen'], res['R3']['parejas_que_cumplen'])
