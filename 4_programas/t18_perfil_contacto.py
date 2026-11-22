"""Apartado 11.3: el perfil de combinaciones de sonidos en parejas de lenguas con préstamo léxico intenso.

Para cada pareja (lengua que toma, lengua que da) se anota el puesto de la donante entre las otras 106 lenguas de
NorthEuraLex, por distancia de perfil, y la lengua de perfil más próximo. Si el préstamo de vocabulario acercara la
manera de combinar sonidos, las donantes ocuparían los primeros puestos.

Uso:  python3 t18_perfil_contacto.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from ibcomp import fuentes
from ibcomp.pruebas import perfil, divergencia

# Parejas fijadas antes de ejecutar: (lengua que toma, lengua que da)
PAREJAS = [('Basque', 'Spanish'), ('Basque', 'Latin'), ('Basque', 'Catalan'), ('Hungarian', 'Turkish'), ('Romanian', 'Bulgarian'), ('Standard Albanian', 'Latin'), ('Standard Albanian', 'Modern Greek'),
           ('Japanese', 'Mandarin Chinese'), ('Korean', 'Mandarin Chinese'), ('Finnish', 'Swedish'), ('English', 'French'), ('Western Farsi', 'Standard Arabic'), ('Turkish', 'Standard Arabic'),
           ('Turkish', 'Western Farsi'), ('Breton', 'French'), ('Armenian', 'Western Farsi'), ('Hindi', 'Western Farsi')]

if __name__ == '__main__':
    LEX, L = fuentes.northeuralex(); nom = {l: L[l]['Name'] for l in LEX}; P = {l: perfil(ws) for l, ws in LEX.items()}; inv = {v: k for k, v in nom.items()}; res = {'parejas': []}
    for x, y in PAREJAS:
        o = sorted((divergencia(P[inv[x]], P[m]), nom[m]) for m in P if m != inv[x]); pos = [n for d, n in o].index(y) + 1; dxy = next(d for d, n in o if n == y)
        res['parejas'].append(dict(toma=x, da=y, puesto=pos, distancia=round(dxy, 3), mas_proxima=o[0][1], distancia_mas_proxima=round(o[0][0], 3)))
        print(f'{x:18s} – {y:18s} puesto {pos:3d} de {len(o)} | {dxy:.3f} | más próxima: {o[0][1]} ({o[0][0]:.3f})')
    ps = [r['puesto'] for r in res['parejas']]
    res['resumen'] = dict(parejas=len(ps), donante_primera=sum(p == 1 for p in ps), entre_las_cinco_primeras=sum(p <= 5 for p in ps), puesto_mediano=float(np.median(ps)))
    print('resumen:', res['resumen'])
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't18_perfil_contacto.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
