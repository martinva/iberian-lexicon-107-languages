"""Anexo B.7: variación de la prueba con significados entre semillas.

Repite la prueba de la tabla 6 (30 unidades de los plomos, lenguas del Wikcionario, 500 sorteos) con 40 secuencias de
sorteos distintas. Declarada antes de ejecutarse en resultados/DECLARACIONES_PREVIAS.md (entrada 3).

Uso:  python3 t20_variacion_semillas.py [desde hasta] [--regenerar]

Cada repetición se guarda en resultados/t20_repeticiones/NN.json con la huella (SHA-256) del paquete ibcomp y de este
programa; una repetición guardada con otra huella se calcula de nuevo. `--regenerar` las recalcula todas.
"""
import hashlib, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from ibcomp import fuentes, pruebas

REPETICIONES = 40
RES = os.path.join(os.path.dirname(__file__), '..', 'resultados')

def huella(us, wik):
    """SHA-256 de todo aquello de lo que depende cada repetición: el código (este programa y el paquete ibcomp) y las entradas ya leídas (unidades y diccionarios del Wikcionario, formas y candidatas incluidas). Si cambia cualquiera de las dos cosas, las repeticiones guardadas dejan de valer."""
    h = hashlib.sha256(); d = os.path.dirname(os.path.abspath(__file__))
    for f in [os.path.abspath(__file__)] + sorted(os.path.join(d, 'ibcomp', x) for x in os.listdir(os.path.join(d, 'ibcomp')) if x.endswith('.py')):
        h.update(open(f, 'rb').read())
    h.update(json.dumps(us, ensure_ascii=False, sort_keys=True, default=str).encode())
    for dic in wik: h.update(repr((dic.nombre, sorted((f, sorted(t)) for f, t in dic.entradas.items()))).encode())
    return h.hexdigest()[:16]

def una(us, wik, minimo, k):
    filas = [r for r in (pruebas.prueba_significados(us, d, f'variacion|{k}', minimo=minimo) for d in wik) if r]
    filas.sort(key=lambda r: r['z']); return dict(repeticion=k, tabla=[(r['diccionario'], round(r['z'], 3)) for r in filas])

if __name__ == '__main__':
    # Cada repetición tiene su propia clave de sorteo, de modo que pueden calcularse por tramos y en cualquier orden:
    #   python3 t20_variacion_semillas.py 1 20      calcula las repeticiones 1 a 20 (omite las ya guardadas)
    os.makedirs(os.path.join(RES, 't20_repeticiones'), exist_ok=True)
    regenerar = '--regenerar' in sys.argv; args = [x for x in sys.argv[1:] if x != '--regenerar']
    desde, hasta = (int(args[0]), int(args[1])) if len(args) == 2 else (1, REPETICIONES)
    us = fuentes.unidades_plomos(); wik = list(fuentes.wikcionario().values()); minimo = max(4, 0.4 * len(us)); H = huella(us, wik)
    for k in range(desde, hasta + 1):
        f = os.path.join(RES, 't20_repeticiones', f'{k:02d}.json')
        vigente = os.path.exists(f) and not regenerar and json.load(open(f, encoding='utf-8')).get('huella') == H
        if not vigente:
            r = una(us, wik, minimo, k); r['huella'] = H; json.dump(r, open(f, 'w', encoding='utf-8'), ensure_ascii=False); print(k, r['tabla'][:3], flush=True)
    R = [json.load(open(os.path.join(RES, 't20_repeticiones', f'{k:02d}.json'), encoding='utf-8')) for k in range(1, REPETICIONES + 1) if os.path.exists(os.path.join(RES, 't20_repeticiones', f'{k:02d}.json'))]
    R = [r for r in R if r.get('huella') == H]
    if len(R) < REPETICIONES: print('Faltan repeticiones:', REPETICIONES - len(R)); sys.exit(0)
    json.dump(R, open(os.path.join(RES, 't20_variacion_semillas_repeticiones.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    zs = {}
    for r in R:
        for l, z in r['tabla']: zs.setdefault(l, []).append(z)
    eus = np.array(zs['Basque']); seg = np.array([r['tabla'][1][1] if r['tabla'][0][0] == 'Basque' else r['tabla'][0][1] for r in R])
    out = dict(repeticiones=len(R), euskera_primero=sum(r['tabla'][0][0] == 'Basque' for r in R),
               euskera=dict(menos_marcado=float(eus.max()), mas_marcado=float(eus.min()), mediana=float(np.median(eus)), desviacion=round(float(eus.std()), 3), amplitud=round(float(eus.max() - eus.min()), 3)),
               mejor_de_las_demas=dict(menos_marcado=float(seg.max()), mas_marcado=float(seg.min()), mediana=float(np.median(seg)), desviacion=round(float(seg.std()), 3)),
               separacion=dict(menor=round(float((seg - eus).min()), 3), mediana=round(float(np.median(seg - eus)), 3), mayor=round(float((seg - eus).max()), 3)),
               por_lengua={l: dict(mediana=round(float(np.median(v)), 3), amplitud=round(float(max(v) - min(v)), 3), desviacion=round(float(np.std(v)), 3)) for l, v in sorted(zs.items(), key=lambda x: np.median(x[1]))})
    json.dump(out, open(os.path.join(RES, 't20_variacion_semillas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != 'por_lengua'}, ensure_ascii=False, indent=1))
    print('Amplitud por lengua (mediana de z; amplitud; desviación):')
    for l, v in list(out['por_lengua'].items())[:8]: print(f"  {l:14s} {v['mediana']:7.2f} {v['amplitud']:5.2f} {v['desviacion']:5.2f}")
    amp = [v['amplitud'] for v in out['por_lengua'].values()]; print('Amplitud mediana entre lenguas:', round(float(np.median(amp)), 2), '| mayor:', max(amp))
