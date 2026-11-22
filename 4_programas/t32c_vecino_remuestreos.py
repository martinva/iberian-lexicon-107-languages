"""Comprobación posterior (no declarada; propuesta por la auditoría 4I): vecino más próximo del ibérico en cada uno de los
200 remuestreos de t32, leído en la matriz sin proyectar (t32 lo leía en la proyección en dos ejes).
Mismos remuestreos que t32 (misma semilla y mismo orden de sorteo).
Uso:  python3 t32c_vecino_remuestreos.py      Salida: ../resultados/t32c_vecino_remuestreos.json
"""
import json, os
from collections import Counter
import numpy as np
import t32_mapa_distancias as T

C, ids = T.candidatas(); L, por_u, azar, comp = T.matriz_lexica(C, ids); n = len(L)
rnd = np.random.default_rng(20261122); ib = L.index('Iberian'); eu = L.index('Basque')
vec, rec, dist_ie, segunda = [], 0, [], []
for b in range(T.NBOOT):
    mult = {}
    for u in rnd.choice(ids, len(ids), replace=True): mult[u] = mult.get(u, 0) + 1
    _, Nb = T.ensambla(n, por_u, azar, mult)
    Xb, _ = T.mds(Nb)                                   # se calcula igual que en t32 para no alterar la secuencia (no se usa)
    d = Nb[ib].copy(); d[ib] = np.inf; k = int(np.argmin(d)); vec.append(L[k])
    e = Nb[eu].copy(); e[eu] = np.inf; rec += int(np.argmin(e)) == ib
    dist_ie.append(float(Nb[ib, eu])); o = np.sort(d); segunda.append(float(o[1]))
res = dict(remuestreos=T.NBOOT, vecino_del_iberico=dict(Counter(vec)), reciprocos=rec,
           distancia_iberico_euskera=dict(mediana=round(float(np.median(dist_ie)), 4), p2_5=round(float(np.percentile(dist_ie, 2.5)), 4), p97_5=round(float(np.percentile(dist_ie, 97.5)), 4)),
           segunda_lengua_mas_proxima=dict(mediana=round(float(np.median(segunda)), 4), minimo=round(float(np.min(segunda)), 4)))
json.dump(res, open(os.path.join(T.RES, 't32c_vecino_remuestreos.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(res)
