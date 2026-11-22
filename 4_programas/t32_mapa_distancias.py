"""Declaración 17: mapa de distancias entre lenguas (todas contra todas) para el léxico de los plomos y para el perfil de sonidos.

Uso:  python3 t32_mapa_distancias.py
Salidas: ../resultados/t32_mapa_distancias.json, ../resultados/figuras/t32_mapa_lexico.png, ../resultados/figuras/t32_mapa_perfil.png
"""
import json, os, sys, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import reducida
from ibcomp.distancia import dist
from ibcomp.pruebas import generador, perfil, divergencia
from t08_perfil import FAM_WIK

RES = os.path.join(os.path.dirname(__file__), '..', 'resultados')
FAM = {**FAM_WIK, 'Basque': 'vasca', 'Iberian': 'ibérica', 'Albanian': 'albanesa', 'Icelandic': 'germánica', 'Lithuanian': 'báltica',
       'Turkish': 'túrquica', 'Maltese': 'semítica', 'Hausa': 'chádica', 'Somali': 'cusítica', 'Quechua': 'quechua',
       'Classical Nahuatl': 'yutoazteca', 'Yoruba': 'yoruboide'}
TOPE, MINIMO, NAZAR, NBOOT = 15, 12, 200, 200

def candidatas():
    W = fuentes.wikcionario(); U = fuentes.unidades_plomos() + fuentes.unidades_numerales(); C = {}
    for l, d in W.items():
        c = {}
        for u in U:
            x = sorted(d.candidatas(u))
            if not x: continue
            if len(x) > TOPE: x = sorted(generador('mapa', l, u['id']).sample(x, TOPE))
            c[u['id']] = x
        if len(c) >= MINIMO: C[l] = c
    C['Iberian'] = {u['id']: sorted({reducida(f) for f in u['formas']}) for u in U}
    return C, [u['id'] for u in U]

def dmin(A, B): return min(dist(a, b) for a in A for b in B)

def matriz_lexica(C, ids):
    L = sorted(C); n = len(L); por_u = {}; azar = np.zeros((n, n)); compartidos = {}
    for i, j in itertools.combinations(range(n), 2):
        X, Y = C[L[i]], C[L[j]]; sh = [u for u in ids if u in X and u in Y]
        por_u[(i, j)] = {u: dmin(X[u], Y[u]) for u in sh}; compartidos[(i, j)] = len(sh)
        pares = [(u, v) for u in ids if u in X for v in ids if v in Y and v != u]
        rnd = generador('mapa-azar', L[i], L[j]); muestra = rnd.sample(pares, min(NAZAR, len(pares)))
        azar[i, j] = azar[j, i] = np.mean([dmin(X[u], Y[v]) for u, v in muestra])
    return L, por_u, azar, compartidos

def ensambla(n, por_u, azar, pesos=None):
    B = np.zeros((n, n))
    for (i, j), d in por_u.items():
        if pesos is None: v = np.mean(list(d.values()))
        else:
            w = np.array([pesos.get(u, 0) for u in d]); v = float(np.dot(w, list(d.values())) / w.sum()) if w.sum() else np.mean(list(d.values()))
        B[i, j] = B[j, i] = v
    N = np.divide(B, azar, out=np.zeros_like(B), where=azar > 0)
    return B, N

def mds(D, k=2):
    n = len(D); J = np.eye(n) - np.ones((n, n)) / n; Bm = -0.5 * J @ (D ** 2) @ J
    w, V = np.linalg.eigh(Bm); o = np.argsort(w)[::-1]; w, V = w[o], V[:, o]
    X = V[:, :k] * np.sqrt(np.maximum(w[:k], 0)); var = (np.maximum(w[:k], 0) / np.maximum(w, 0).sum()).tolist()
    return X, var

def procrustes(X, Y):
    """Alinea Y con X (rotación/reflexión y traslación, sin cambio de escala)."""
    mx, my = X.mean(0), Y.mean(0); U, _, Vt = np.linalg.svd((X - mx).T @ (Y - my)); R = (U @ Vt).T
    return (Y - my) @ R + mx

def upgma(D, L):
    from scipy.cluster.hierarchy import linkage, dendrogram
    from scipy.spatial.distance import squareform
    Z = linkage(squareform(D, checks=False), 'average'); return Z

def dibuja(X, L, var, titulo, fich, nubes=None, Z=None):
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    from scipy.cluster.hierarchy import dendrogram
    fams = sorted(set(FAM.get(l, 'otra') for l in L)); cmap = plt.get_cmap('tab20')
    col = {f: cmap(k % 20) for k, f in enumerate(fams)}; col['ibérica'] = 'black'; col['vasca'] = '#d62728'
    fig, axs = plt.subplots(1, 2 if Z is not None else 1, figsize=(16, 8) if Z is not None else (9, 8), gridspec_kw={'width_ratios': [3, 2]} if Z is not None else None)
    ax = axs[0] if Z is not None else axs
    if nubes is not None:
        for k, l in enumerate(L): ax.scatter(nubes[:, k, 0], nubes[:, k, 1], s=2, alpha=0.08, color=col[FAM.get(l, 'otra')])
    for k, l in enumerate(L):
        f = FAM.get(l, 'otra'); ax.scatter(X[k, 0], X[k, 1], s=90 if f in ('ibérica', 'vasca') else 40, color=col[f], edgecolor='k', zorder=3,
                                          marker='*' if f == 'ibérica' else 'o')
        ax.annotate({'Iberian': 'IBÉRICO (plomos)', 'Basque': 'EUSKERA'}.get(l, l), X[k], fontsize=8 if f not in ('ibérica', 'vasca') else 10,
                    fontweight='bold' if f in ('ibérica', 'vasca') else 'normal', xytext=(4, 3), textcoords='offset points')
    for f in fams: ax.scatter([], [], color=col[f], label=f)
    ax.legend(fontsize=7, loc='best', ncol=2); ax.set_title(titulo, fontsize=11)
    ax.set_xlabel(f'Eje 1 ({100 * var[0]:.0f} % de la variación)'); ax.set_ylabel(f'Eje 2 ({100 * var[1]:.0f} %)'); ax.grid(alpha=0.2)
    if Z is not None:
        dendrogram(Z, labels=[{'Iberian': 'IBÉRICO', 'Basque': 'EUSKERA'}.get(l, l) for l in L], orientation='right', ax=axs[1], leaf_font_size=8, color_threshold=0)
        axs[1].set_title('Árbol (UPGMA) de la misma matriz', fontsize=10)
    fig.tight_layout(); fig.savefig(fich, dpi=150); plt.close(fig)

def vecinos(D, L, l, n=5):
    k = L.index(l); return [(L[m], round(float(D[k, m]), 4)) for m in np.argsort(D[k]) if m != k][:n]

def agrupamiento(D, L):
    """Comprobación (1): ¿el vecino más próximo de cada lengua con parientes en la muestra es de su familia?"""
    from collections import Counter
    c = Counter(FAM.get(l) for l in L); ok = tot = 0
    for k, l in enumerate(L):
        if c[FAM.get(l)] < 2: continue
        m = min((D[k, j], j) for j in range(len(L)) if j != k)[1]; tot += 1; ok += FAM.get(L[m]) == FAM.get(l)
    return ok, tot

if __name__ == '__main__':
    res = {}
    C, ids = candidatas(); L, por_u, azar, comp = matriz_lexica(C, ids); n = len(L)
    B, N = ensambla(n, por_u, azar); X, var = mds(N); Z = upgma(N, L)
    rnd = np.random.default_rng(20261122); nubes = np.zeros((NBOOT, n, 2))
    for b in range(NBOOT):
        mult = {}
        for u in rnd.choice(ids, len(ids), replace=True): mult[u] = mult.get(u, 0) + 1
        _, Nb = ensambla(n, por_u, azar, mult); Xb, _ = mds(Nb); nubes[b] = procrustes(X, Xb)
    ok, tot = agrupamiento(N, L)
    vib = []
    for b in range(NBOOT):
        k = L.index('Iberian'); d = ((nubes[b] - nubes[b][k]) ** 2).sum(1); d[k] = np.inf; vib.append(L[int(np.argmin(d))])
    from collections import Counter
    res['lexico'] = dict(lenguas=L, familias={l: FAM.get(l) for l in L}, significados=len(ids), significados_por_lengua={l: len(C[l]) for l in L},
                         compartidos_min=int(min(comp.values())), matriz_normalizada=np.round(N, 4).tolist(), matriz_bruta=np.round(B, 4).tolist(),
                         azar=np.round(azar, 4).tolist(), mds=np.round(X, 4).tolist(), varianza_ejes=[round(v, 4) for v in var],
                         vecinos_iberico=vecinos(N, L, 'Iberian'), vecinos_euskera=vecinos(N, L, 'Basque'),
                         familia_del_vecino=dict(aciertos=ok, total=tot),
                         vecino_iberico_en_el_mapa_remuestreos=dict(Counter(vib)))
    dibuja(X, L, var, 'Mapa A. Distancia en el léxico de los plomos (normalizada; 1 = azar)', os.path.join(RES, 'figuras', 't32_mapa_lexico.png'), nubes, Z)
    print('A lenguas', n, 'vecinos ibérico', res['lexico']['vecinos_iberico']); print('  vecinos euskera', res['lexico']['vecinos_euskera'])
    print('  familia del vecino', ok, '/', tot, ' var', var, ' remuestreos', res['lexico']['vecino_iberico_en_el_mapa_remuestreos'])
    # Mapa B: perfil
    W = {l: set(d.formas) for l, d in fuentes.wikcionario().items()}
    W['Iberian'] = set().union(*[f['formas'] for f in fuentes.hesperia()])
    LB = sorted(W); P = {l: perfil(W[l]) for l in LB}; m = len(LB); DB = np.zeros((m, m))
    for i, j in itertools.combinations(range(m), 2): DB[i, j] = DB[j, i] = divergencia(P[LB[i]], P[LB[j]])
    XB, varB = mds(DB); okB, totB = agrupamiento(DB, LB)
    res['perfil'] = dict(lenguas=LB, matriz=np.round(DB, 5).tolist(), mds=np.round(XB, 4).tolist(), varianza_ejes=[round(v, 4) for v in varB],
                         vecinos_iberico=vecinos(DB, LB, 'Iberian'), vecinos_euskera=vecinos(DB, LB, 'Basque'), familia_del_vecino=dict(aciertos=okB, total=totB))
    dibuja(XB, LB, varB, 'Mapa B. Distancia entre perfiles de combinaciones de sonidos (Jensen-Shannon)', os.path.join(RES, 'figuras', 't32_mapa_perfil.png'), None, upgma(DB, LB))
    print('B vecinos ibérico', res['perfil']['vecinos_iberico'], ' familia', okB, '/', totB, varB)
    json.dump(res, open(os.path.join(RES, 't32_mapa_distancias.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
