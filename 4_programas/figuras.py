"""Figuras 1, 2 y 3 del artículo. No calcula nada: dibuja los resultados que ya han escrito
t06_t07_significados.py, t08_perfil.py y t04_t05_numerales.py en la carpeta resultados/.

Figura 1: arriba, valor de cada lengua en la prueba con significados (30 unidades, Wikcionario);
          abajo, distancia de cada lengua al ibérico en el perfil de combinaciones de sonidos.
Figura 2: las dos pruebas a la vez, para las lenguas presentes en las dos bases.
Figura 3: serie numeral; distancia de cada lengua sin parientes a su vecino más próximo, y la del ibérico al euskera.

Requiere la biblioteca Matplotlib. La posición vertical de los puntos en la figura 1 es solo para
separarlos (semilla fija); no representa ningún dato.
Uso / Usage:  python3 figuras.py        (escribe en resultados/figuras/)
"""
import json, os, random
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

AQUI = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(AQUI, '..', 'resultados'); SAL = os.path.join(RES, 'figuras')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': '#8a8983',
                     'xtick.color': '#52514e', 'ytick.color': '#52514e', 'axes.labelcolor': '#52514e', 'figure.facecolor': '#fcfcfb',
                     'axes.facecolor': '#fcfcfb', 'savefig.facecolor': '#fcfcfb'})
AZUL, NARANJA, GRIS, TEXTO = '#2a78d6', '#eb6834', '#b9b8b0', '#0b0b0b'
NOMBRE = {'Basque': 'euskera', 'Latin': 'latín', 'Galician': 'gallego', 'Tagalog': 'tagalo', 'Turkish': 'turco', 'Finnish': 'finés', 'Icelandic': 'islandés'}
ROMANCES = {'Italian', 'Spanish', 'Catalan', 'Portuguese', 'French', 'Romanian', 'Latin', 'Galician', 'Asturian', 'Occitan', 'Sicilian', 'Sardinian', 'Aragonese'}
color = lambda n: AZUL if n == 'Basque' else (NARANJA if n in ROMANCES else GRIS)
coma = FuncFormatter(lambda v, _: f'{v:g}'.replace('.', ',').replace('-', '−'))

def leyenda(ax, donde):
    for c, t in ((AZUL, 'euskera'), (NARANJA, 'latín y lenguas romances'), (GRIS, 'otras lenguas')): ax.scatter([], [], s=40, color=c, label=t)
    ax.legend(frameon=False, loc=donde, fontsize=9, handletextpad=0.3)

def tira(ax, datos, rotulos, titulo, eje, franja):
    rnd = random.Random(7)
    if franja: ax.axvspan(-2, 2, color='#efeee9', zorder=0); ax.text(0, 1.02, 'valores próximos a cero (de −2 a +2)', ha='center', va='bottom', fontsize=8.5, color='#52514e', transform=ax.get_xaxis_transform())
    for n, v in datos:
        y = 0 if n == 'Basque' else rotulos.get(n, (None, rnd.uniform(-0.32, 0.32)))[1]
        ax.scatter(v, y, s=70 if n == 'Basque' else 34, color=color(n), edgecolor='#fcfcfb', linewidth=1.2, zorder=5 if n == 'Basque' else 3)
        if n in rotulos: ax.annotate(NOMBRE.get(n, n), (v, y), xytext=rotulos[n][0], textcoords='offset points', fontsize=9, color=TEXTO, ha='center')
    ax.set_yticks([]); ax.spines['left'].set_visible(False); ax.set_ylim(-0.6, 0.6); ax.set_xlabel(eje); ax.set_title(titulo, loc='left', fontsize=11, color=TEXTO, pad=18)
    ax.grid(axis='x', color='#e3e2dc', lw=0.6, zorder=1); ax.xaxis.set_major_formatter(coma)

if __name__ == '__main__':
    os.makedirs(SAL, exist_ok=True)
    sig = json.load(open(os.path.join(RES, 't06_t07_significados.json'), encoding='utf-8'))
    clave = next(k for k in sig if k.startswith('Wikcionario') and '30 unidades' in k)
    S = [(r['diccionario'], r['z']) for r in sig[clave] if not r['diccionario'].startswith('Euskera')]      # solo las lenguas del Wikcionario
    P = [(n, d) for n, d in json.load(open(os.path.join(RES, 't08_perfil.json'), encoding='utf-8'))['NorthEuraLex, clases completas']['iberico']['todo el corpus']['tabla']]
    # Figura 1
    fig, axs = plt.subplots(2, 1, figsize=(8.2, 5.8))
    tira(axs[0], S, {'Basque': ((0, 12), 0), 'Galician': ((8, 14), 0.2), 'Tagalog': ((-8, -18), -0.2)},
         f'Prueba con significados: {len(S)} lenguas (Wikcionario), azar igualado por longitud', 'valor (más a la izquierda = más lejos del azar)', True)
    leyenda(axs[0], 'lower left')
    tira(axs[1], P, {'Basque': ((0, 12), 0), 'Latin': ((0, -16), -0.08)}, f'Perfil de combinaciones de sonidos: {len(P)} lenguas (todo el corpus ibérico)',
         'distancia entre perfiles (más a la izquierda = más parecido)', False)
    fig.text(0.01, 0.005, 'El ibérico es la referencia: cada punto es una lengua comparada con él; el ibérico mismo no se representa.', fontsize=8.5, color='#52514e', ha='left', va='bottom')
    fig.tight_layout(h_pad=2.2, rect=(0, 0.025, 1, 1)); fig.savefig(os.path.join(SAL, 'figura_1_las_dos_pruebas.png'), dpi=220); plt.close(fig)
    # Figura 2
    pz, sz = dict(P), dict(S); comunes = [n for n in sz if n in pz]
    fig, ax = plt.subplots(figsize=(6.4, 5.6)); ax.axhspan(-2, 2, color='#efeee9', zorder=0)
    sitio = {'Basque': (10, -3), 'Latin': (8, -4), 'Turkish': (8, -4), 'Finnish': (8, 6), 'Icelandic': (8, -10)}
    for n in comunes:
        ax.scatter(pz[n], sz[n], s=80 if n == 'Basque' else 40, color=color(n), edgecolor='#fcfcfb', linewidth=1.2, zorder=4)
        if n in sitio: ax.annotate(NOMBRE.get(n, n), (pz[n], sz[n]), xytext=sitio[n], textcoords='offset points', fontsize=9, color=TEXTO)
    ax.set_xlabel('perfil de combinaciones de sonidos (distancia)'); ax.set_ylabel('prueba con significados')
    ax.set_title(f'Las dos pruebas a la vez: {len(comunes)} lenguas presentes en ambas bases', loc='left', fontsize=11, color=TEXTO, pad=10)
    ax.grid(color='#e3e2dc', lw=0.6, zorder=1); ax.text(0.99, 0.36, 'franja gris: valores entre −2 y +2\nen la prueba con significados', transform=ax.transAxes, ha='right', va='top', fontsize=8.5, color='#52514e')
    leyenda(ax, 'lower right'); ax.xaxis.set_major_formatter(coma); ax.yaxis.set_major_formatter(coma)
    fig.text(0.01, 0.005, 'El ibérico es la referencia: los dos ejes miden la distancia de cada lengua al ibérico; el ibérico mismo no se representa.', fontsize=8.5, color='#52514e', ha='left', va='bottom')
    fig.tight_layout(rect=(0, 0.025, 1, 1)); fig.savefig(os.path.join(SAL, 'figura_2_nube_dos_pruebas.png'), dpi=220); plt.close(fig)
    # Figura 3
    num = json.load(open(os.path.join(RES, 't04_t05_numerales.json'), encoding='utf-8'))['serie completa']
    d = num['sin_parientes']['distancias']; ib = num['iberico'][0][0]
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    ax.hist(d, bins=[x / 20 for x in range(4, 21)], color=GRIS, edgecolor='#fcfcfb', linewidth=1.2, zorder=3)
    ax.axvline(ib, color=AZUL, lw=2, zorder=4); ax.annotate(f'ibérico–euskera: {ib:.2f}'.replace('.', ','), (ib, 0.93), xycoords=('data', 'axes fraction'), xytext=(8, 0), textcoords='offset points', fontsize=9.5, color=TEXTO)
    ax.xaxis.set_major_formatter(coma); ax.set_xlabel('distancia a la lengua más próxima (serie numeral del 1 al 8 y 10)'); ax.set_ylabel('número de lenguas')
    ax.set_title(f'Serie numeral: las {len(d)} lenguas sin parientes y su vecino más próximo', loc='left', fontsize=11, color=TEXTO, pad=10); ax.grid(axis='y', color='#e3e2dc', lw=0.6, zorder=1)
    fig.tight_layout(); fig.savefig(os.path.join(SAL, 'figura_3_serie_numeral.png'), dpi=220); plt.close(fig)
    print('Figuras escritas en resultados/figuras/. Lenguas comunes a las dos pruebas:', len(comunes), '| ibérico–euskera', ib, '| mínimo sin parientes', min(d))
