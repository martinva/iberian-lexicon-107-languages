"""Declaración 20: primer puesto por perfil con suceso equivalente (una lengua designada) en emparentadas y en préstamo.
Uso:  python3 t35_perfil_suceso_equivalente.py     Salida: ../resultados/t35_perfil_suceso_equivalente.json
"""
import json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.pruebas import perfil, divergencia
from t18_perfil_contacto import PAREJAS
from t34_razon_verosimilitud import razon

LEX, L = fuentes.northeuralex(); nom = {l: L[l]['Name'] for l in LEX}; inv = {v: k for k, v in nom.items()}
fam = {l: (L[l].get('Family') or '') for l in LEX}; P = {l: perfil(ws) for l, ws in LEX.items()}; tam = Counter(fam.values())
def orden(l): return [m for d, m in sorted((divergencia(P[l], P[m]), m) for m in P if m != l)]
emp_b = []; emp_c = []
for l in sorted(LEX):
    if tam[fam[l]] == 2:
        otro = next(m for m in LEX if m != l and fam[m] == fam[l]); o = orden(l)
        emp_b.append(dict(lengua=nom[l], designada=nom[otro], familia=fam[l], puesto=o.index(otro) + 1))
    if tam[fam[l]] in (2, 3):
        o = orden(l); emp_c.append(dict(lengua=nom[l], familia=fam[l], mas_proxima=nom[o[0]], acierto=fam[o[0]] == fam[l]))
con = []
for x, y in PAREJAS:
    a, b = inv[x], inv[y]
    if fam[a] != fam[b]: o = orden(a); con.append(dict(toma=x, da=y, puesto=o.index(b) + 1))
kb = sum(e['puesto'] == 1 for e in emp_b); kc_ = sum(e['acierto'] for e in emp_c); k0 = sum(c['puesto'] == 1 for c in con)
res = dict(R4b=razon(kb, len(emp_b), k0, len(con), 'R4b'), R4c=razon(kc_, len(emp_c), k0, len(con), 'R4c'),
           emparentadas_R4b=emp_b, emparentadas_R4c=emp_c, contacto=con)
json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't35_perfil_suceso_equivalente.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k in ('R4b', 'R4c'): print(k, {x: res[k][x] for x in ('emparentadas', 'contacto', 'razon', 'ic95', 'posterior')})
print(emp_b); print([ (c['toma'],c['da'],c['puesto']) for c in con])
