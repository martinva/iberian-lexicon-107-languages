"""Apartado 8.3: potencia y falsos positivos de la prueba con significados, con las seis lenguas de control.

Como la tabla 10, con 100 muestras de 30 palabras por lengua en lugar de 5. Declarada antes de ejecutarse en
resultados/DECLARACIONES_PREVIAS.md (entrada 1).

Uso:  python3 t19_potencia_controles.py [lengua …]      (sin argumentos, las seis; con `resumen`, solo el resumen)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from ibcomp import fuentes, pruebas
from ibcomp.normalizadores import red_control
from t10_controles import PARIENTES

MUESTRAS = 100; UMBRAL_Z = -9.3; UMBRAL_SEPARACION = 5.6
RES = os.path.join(os.path.dirname(__file__), '..', 'resultados')

def resumen():
    out = {}
    for lengua in fuentes.CONTROL:
        f = os.path.join(RES, f't19_potencia_{lengua}.json')
        if not os.path.exists(f): continue
        M = json.load(open(f, encoding='utf-8'))
        if len(M) < MUESTRAS: print(f'AVISO: {lengua} tiene {len(M)} muestras de {MUESTRAS}; no se resume (ejecución incompleta)'); continue
        z1 = np.array([m['tabla'][0][1] for m in M]); sep = np.array([m['tabla'][1][1] - m['tabla'][0][1] for m in M])
        out[lengua] = dict(nombre=fuentes.CONTROL[lengua], muestras=len(M), con_parientes=bool(PARIENTES[lengua]), primera_es_pariente=sum(m['primera_es_pariente'] for m in M),
                           alcanza_z=int((z1 <= UMBRAL_Z).sum()), alcanza_separacion=int((sep >= UMBRAL_SEPARACION).sum()), alcanza_ambos=int(((z1 <= UMBRAL_Z) & (sep >= UMBRAL_SEPARACION)).sum()),
                           z_primera=dict(mediana=round(float(np.median(z1)), 3), mejor=round(float(z1.min()), 3), peor=round(float(z1.max()), 3)),
                           separacion=dict(mediana=round(float(np.median(sep)), 3), mayor=round(float(sep.max()), 3)))  # tres decimales: los registros ya van a tres; el artículo redondea una sola vez desde aquí
        print(out[lengua])
    json.dump(out, open(os.path.join(RES, 't19_potencia_controles.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    if sys.argv[1:] != ['resumen']:
        wik = list(fuentes.wikcionario().values())
        for lengua in (sys.argv[1:] or list(fuentes.CONTROL)):
            LEXT = fuentes.lexico_control(lengua); PAL = sorted(LEXT); rnd = pruebas.generador('potencia', lengua); M = []
            for k in range(1, MUESTRAS + 1):
                m = rnd.sample(PAL, 30); us = [dict(id=w, formas=[w], terminos_en=sorted(LEXT[w])) for w in m]
                filas = [r for r in (pruebas.prueba_significados(us, d, f'potencia|{lengua}|{k}', sorteos=150, minimo=12, reductor=red_control) for d in wik) if r]
                filas.sort(key=lambda r: r['z']); t = [(r['diccionario'], round(r['z'], 3)) for r in filas]
                M.append(dict(muestra=k, palabras=m, tabla=t[:6], primera_es_pariente=bool(t and t[0][0] in PARIENTES[lengua])))
                print(f'{lengua} {k}: {t[:3]}', flush=True)
                json.dump(M, open(os.path.join(RES, f't19_potencia_{lengua}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    resumen()
