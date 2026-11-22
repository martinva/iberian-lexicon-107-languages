"""Figuras complementarias del mapa de distancias (declaración 17), añadidas después de ver el resultado.
No calculan nada nuevo: leen la matriz de t32 y la dibujan de dos formas que no deforman las distancias:
(1) la matriz completa ordenada por el árbol (mapa de calor, valores exactos);
(2) la proyección en dos ejes con una línea entre cada lengua y su vecina más próxima en la matriz, con la distancia real.
Uso:  python3 t32b_figuras_mapa.py
"""
import json, os
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list
from scipy.spatial.distance import squareform
from t32_mapa_distancias import FAM

RES = os.path.join(os.path.dirname(__file__), '..', 'resultados')
ET = {'Iberian': 'IBÉRICO', 'Basque': 'EUSKERA'}

def calor(L, D, titulo, fich, vmax):
    Z = linkage(squareform(D, checks=False), 'average'); o = leaves_list(Z); Lo = [ET.get(L[i], L[i]) for i in o]; Do = D[np.ix_(o, o)]
    fig = plt.figure(figsize=(14, 12)); ax0 = fig.add_axes([0.02, 0.1, 0.13, 0.8]); ax = fig.add_axes([0.24, 0.1, 0.66, 0.8]); cax = fig.add_axes([0.92, 0.1, 0.02, 0.8])
    dendrogram(Z, orientation='left', ax=ax0, no_labels=True, color_threshold=0, link_color_func=lambda k: '#555'); ax0.invert_yaxis(); ax0.axis('off')
    M = Do.copy(); np.fill_diagonal(M, np.nan)
    im = ax.imshow(M, cmap='viridis', vmin=0, vmax=vmax, interpolation='nearest')
    ax.set_xticks(range(len(Lo))); ax.set_xticklabels(Lo, rotation=90, fontsize=8); ax.set_yticks(range(len(Lo))); ax.set_yticklabels(Lo, fontsize=8)
    for t in ax.get_xticklabels() + ax.get_yticklabels():
        if t.get_text() in ET.values(): t.set_fontweight('bold'); t.set_color('#c00000')
    ax.set_title(titulo, fontsize=11); fig.colorbar(im, cax=cax); fig.savefig(fich, dpi=150); plt.close(fig)

def vecinas(L, D, X, var, titulo, fich):
    fams = sorted(set(FAM.get(l, 'otra') for l in L)); cmap = plt.get_cmap('tab20'); col = {f: cmap(k % 20) for k, f in enumerate(fams)}; col['ibérica'] = 'black'; col['vasca'] = '#d62728'
    fig, ax = plt.subplots(figsize=(11, 9))
    for k in range(len(L)):
        m = min((D[k, j], j) for j in range(len(L)) if j != k)[1]
        ax.plot([X[k, 0], X[m, 0]], [X[k, 1], X[m, 1]], color='#888', lw=0.8, zorder=1)
        if (L[k], L[m]) in (('Iberian', 'Basque'), ('Basque', 'Iberian')) or D[k, m] < 0.5:
            ax.annotate(f'{D[k, m]:.2f}', ((X[k, 0] + X[m, 0]) / 2, (X[k, 1] + X[m, 1]) / 2), fontsize=7, color='#444')
    for k, l in enumerate(L):
        f = FAM.get(l, 'otra'); big = f in ('ibérica', 'vasca')
        ax.scatter(*X[k], s=110 if big else 40, color=col[f], edgecolor='k', zorder=3, marker='*' if f == 'ibérica' else 'o')
        ax.annotate(ET.get(l, l), X[k], fontsize=10 if big else 8, fontweight='bold' if big else 'normal', xytext=(4, 3), textcoords='offset points')
    for f in fams: ax.scatter([], [], color=col[f], label=f)
    ax.legend(fontsize=7, ncol=2); ax.set_title(titulo, fontsize=11); ax.grid(alpha=0.2)
    ax.set_xlabel(f'Eje 1 ({100 * var[0]:.0f} % de la variación)'); ax.set_ylabel(f'Eje 2 ({100 * var[1]:.0f} %)')
    fig.tight_layout(); fig.savefig(fich, dpi=150); plt.close(fig)

if __name__ == '__main__':
    r = json.load(open(os.path.join(RES, 't32_mapa_distancias.json'), encoding='utf-8'))
    A = r['lexico']; LA = A['lenguas']; DA = np.array(A['matriz_normalizada'])
    calor(LA, DA, 'Léxico de los plomos: distancia normalizada entre todas las lenguas (1 = azar), ordenada por el árbol', os.path.join(RES, 'figuras', 't32b_calor_lexico.png'), 1.0)
    vecinas(LA, DA, np.array(A['mds']), A['varianza_ejes'], 'Léxico de los plomos: cada lengua unida a su vecina más próxima en la matriz (distancia real)', os.path.join(RES, 'figuras', 't32b_vecinas_lexico.png'))
    B = r['perfil']; LB = B['lenguas']; DB = np.array(B['matriz'])
    calor(LB, DB, 'Perfil de combinaciones de sonidos: divergencia entre todas las lenguas, ordenada por el árbol', os.path.join(RES, 'figuras', 't32b_calor_perfil.png'), float(np.percentile(DB[DB > 0], 95)))
    vecinas(LB, DB, np.array(B['mds']), B['varianza_ejes'], 'Perfil de sonidos: cada lengua unida a su vecina más próxima en la matriz', os.path.join(RES, 'figuras', 't32b_vecinas_perfil.png'))
