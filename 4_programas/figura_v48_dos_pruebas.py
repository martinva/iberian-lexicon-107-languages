"""Figura 1 del artículo (v48): las dos pruebas, primero la que no usa significados, con el ibérico dibujado
como punto de referencia en la distancia 0. No calcula nada: dibuja t08_perfil.json y t06_t07_significados.json.
Uso / Usage:  python3 figura_v48_dos_pruebas.py
"""
import json, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from figuras import tira, leyenda, RES, SAL, TEXTO
ROJO = '#c0392b'
if __name__ == '__main__':
    sig = json.load(open(os.path.join(RES, 't06_t07_significados.json'), encoding='utf-8'))
    clave = next(k for k in sig if k.startswith('Wikcionario') and '30 unidades' in k)
    S = [(r['diccionario'], r['z']) for r in sig[clave] if not r['diccionario'].startswith('Euskera')]
    P = [(n, d) for n, d in json.load(open(os.path.join(RES, 't08_perfil.json'), encoding='utf-8'))['NorthEuraLex, clases completas']['iberico']['todo el corpus']['tabla']]
    fig, axs = plt.subplots(2, 1, figsize=(8.2, 6.2))
    tira(axs[0], P, {'Basque': ((0, 12), 0), 'Latin': ((0, -16), -0.08)}, f'Sin significados, solo sonidos: perfil de todo el corpus ibérico frente a {len(P)} lenguas',
         'distancia entre perfiles (0 = el propio ibérico; más a la izquierda = más parecido)', False)
    axs[0].scatter(0, 0, s=90, marker='D', color=ROJO, zorder=6); axs[0].annotate('ibérico\n(referencia)', (0, 0), xytext=(0, 12), textcoords='offset points', ha='center', fontsize=9, color=ROJO)
    axs[0].set_xlim(-0.02, 0.45)
    tira(axs[1], S, {'Basque': ((0, 12), 0), 'Galician': ((8, 14), 0.2), 'Tagalog': ((-8, -18), -0.2)},
         f'Con los significados propuestos: {len(S)} lenguas (Wikcionario), 30 palabras de los plomos', 'valor frente al azar (más a la izquierda = más lejos del azar; 0 = azar)', True)
    leyenda(axs[1], 'lower left')
    fig.text(0.01, 0.005, 'Cada punto es una lengua comparada con el ibérico. Abajo, el valor mide cuánto se aparta del azar su parecido con el ibérico.', fontsize=8, color='#52514e', ha='left', va='bottom')
    fig.tight_layout(h_pad=2.2, rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(SAL, 'figura_1_v48_dos_pruebas.png'), dpi=220); plt.close(fig)
