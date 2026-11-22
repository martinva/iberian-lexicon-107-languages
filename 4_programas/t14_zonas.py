"""Tabla 14 (segunda parte): proximidad del perfil de combinaciones de sonidos al euskera por zonas, de norte a sur.

Para cada zona: perfil de sus formas (solo plomos; todas las inscripciones); distancia a las 107 lenguas de NorthEuraLex;
puesto del euskera y distancia relativa = (distancia al euskera − media de las 107) / desviación típica de las 107.
Muestras igualadas: 300 sorteos del tamaño de la zona menor. Se repite con todas las lenguas reducidas a lo que el ibérico escribe.
Variación dentro del ibérico: dos mitades disjuntas de la misma zona frente a muestras de zonas distintas, todas del mismo tamaño.
Uso:  python3 t14_zonas.py
"""
import json, os, sys
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import proyecta
from ibcomp.pruebas import perfil, divergencia, generador

if __name__ == '__main__':
    fichas = fuentes.hesperia(); LEX, lang = fuentes.northeuralex(); nombres = {l: lang[l]['Name'] for l in LEX}; eus = next(l for l in LEX if nombres[l] == 'Basque'); Z = [z for z, _ in fuentes.ZONAS]
    F = {z: {'solo plomos': set().union(*[f['formas'] for f in fichas if f['zona'] == z and f['plomo']]), 'todas las inscripciones': set().union(*[f['formas'] for f in fichas if f['zona'] == z])} for z in Z}
    info = {z: dict(inscripciones=sum(f['zona'] == z for f in fichas), plomos=sum(f['zona'] == z and f['plomo'] for f in fichas), signarios=dict(Counter(f['signario'] for f in fichas if f['zona'] == z).most_common(3))) for z in Z}
    def frente(ws, P):
        q = perfil(ws); d = {l: divergencia(q, P[l]) for l in P}; v = np.array(list(d.values())); o = sorted(d, key=d.get)
        return d[eus], o.index(eus) + 1, (d[eus] - float(v.mean())) / float(v.std()), [(nombres[l], round(d[l], 3)) for l in o[:3]]
    res = {'zonas': info}
    for conj in ('solo plomos', 'todas las inscripciones'):
        for variante, P, tr in (('clases completas', {l: perfil(ws) for l, ws in LEX.items()}, lambda ws: ws), ('reducidas a lo que el ibérico escribe', {l: perfil(proyecta(ws)) for l, ws in LEX.items()}, proyecta)):
            N = min(len(tr(F[z][conj])) for z in Z); rnd = generador('zonas', conj, variante); filas = []; print(f'\n===== {conj} · {variante} · muestra igualada de {N} formas')
            for z in Z:
                ws = sorted(tr(F[z][conj])); d, puesto, zrel, prim = frente(ws, P); S = [frente(rnd.sample(ws, N), P) for _ in range(300)]
                filas.append(dict(zona=z, formas=len(ws), distancia=round(d, 4), puesto_euskera=puesto, relativa=round(zrel, 2), primeras=prim, igualada=dict(distancia=round(float(np.mean([s[0] for s in S])), 4), puesto_medio=round(float(np.mean([s[1] for s in S])), 2), primero=sum(s[1] == 1 for s in S), relativa=round(float(np.mean([s[2] for s in S])), 2), relativa_dt=round(float(np.std([s[2] for s in S])), 2))))
                print(f"  {z:20s} inscripciones {info[z]['inscripciones']:4d} plomos {info[z]['plomos']:3d} formas {len(ws):4d} | euskera puesto {puesto}, relativa {zrel:+.2f} | igualada: relativa {filas[-1]['igualada']['relativa']:+.2f} ± {filas[-1]['igualada']['relativa_dt']:.2f}, primero {filas[-1]['igualada']['primero']}/300")
            res[f'{conj} | {variante}'] = dict(N=N, filas=filas); sys.stdout.flush()
        n = min(len(F[z][conj]) for z in Z) // 2; M = np.zeros((5, 5)); rnd = generador('zonas', conj, 'variación interna')
        for _ in range(300):
            A = []; B = []
            for z in Z: ws = rnd.sample(sorted(F[z][conj]), 2 * n); A.append(perfil(ws[:n])); B.append(perfil(ws[n:]))
            for i in range(5):
                for j in range(5): M[i, j] += divergencia(A[i], B[j]) / 300
        v = dict(n=n, misma_zona=round(float(np.mean(np.diag(M))), 3), vecinas=round(float(np.mean([M[i, j] for i in range(5) for j in range(5) if abs(i - j) == 1])), 3), no_vecinas=round(float(np.mean([M[i, j] for i in range(5) for j in range(5) if abs(i - j) >= 2])), 3), extremos=round(float((M[0, 4] + M[4, 0]) / 2), 3))
        res[f'{conj} | variación dentro del ibérico'] = v; print(f'  variación dentro del ibérico ({conj}; {n} formas por muestra): {v}')
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't14_zonas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
