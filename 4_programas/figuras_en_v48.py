"""English versions of figures 1 and 2 of the article (v48). They compute nothing: they draw the published results
(t06_t07_significados.json, t08_perfil.json, t32_mapa_distancias.json) with English labels.
Usage:  python3 figuras_en_v48.py
"""
import json, os
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import figuras as F
import t32b_figuras_mapa as M
ROJO = '#c0392b'
if __name__ == '__main__':
    F.NOMBRE.update({'Basque': 'Basque', 'Latin': 'Latin', 'Galician': 'Galician', 'Tagalog': 'Tagalog'})
    sig = json.load(open(os.path.join(F.RES, 't06_t07_significados.json'), encoding='utf-8'))
    clave = next(k for k in sig if k.startswith('Wikcionario') and '30 unidades' in k)
    S = [(r['diccionario'], r['z']) for r in sig[clave] if not r['diccionario'].startswith('Euskera')]
    P = [(n, d) for n, d in json.load(open(os.path.join(F.RES, 't08_perfil.json'), encoding='utf-8'))['NorthEuraLex, clases completas']['iberico']['todo el corpus']['tabla']]
    fig, axs = plt.subplots(2, 1, figsize=(8.2, 6.2))
    F.tira(axs[0], P, {'Basque': ((0, 12), 0), 'Latin': ((0, -16), -0.08)}, f'Without meanings, sounds only: profile of the whole Iberian corpus against {len(P)} languages',
           'distance between profiles (0 = Iberian itself; further left = more similar)', False)
    axs[0].scatter(0, 0, s=90, marker='D', color=ROJO, zorder=6); axs[0].annotate('Iberian\n(reference)', (0, 0), xytext=(0, 12), textcoords='offset points', ha='center', fontsize=9, color=ROJO)
    axs[0].set_xlim(-0.02, 0.45)
    F.tira(axs[1], S, {'Basque': ((0, 12), 0), 'Galician': ((8, 14), 0.2), 'Tagalog': ((-8, -18), -0.2)},
           f'With the proposed meanings: {len(S)} languages (Wiktionary), 30 words of the lead plaques', 'value against chance (further left = further from chance; 0 = chance)', True)
    for c, t in ((F.AZUL, 'Basque'), (F.NARANJA, 'Latin and Romance languages'), (F.GRIS, 'other languages')): axs[1].scatter([], [], s=40, color=c, label=t)
    axs[1].legend(frameon=False, loc='lower left', fontsize=9, handletextpad=0.3)
    for t in axs[1].texts:
        if t.get_text().startswith('valores próximos'): t.set_text('values close to zero (−2 to +2)')
    from matplotlib.ticker import FuncFormatter
    for a in axs: a.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:g}'.replace('-', '−')))
    fig.text(0.01, 0.005, 'Each point is a language compared with Iberian. Bottom: the value measures how far its resemblance to Iberian departs from chance.', fontsize=8, color='#52514e', ha='left', va='bottom')
    fig.tight_layout(h_pad=2.2, rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(F.SAL, 'figura_1_v48_dos_pruebas_en.png'), dpi=220); plt.close(fig)
    M.ET.update({'Iberian': 'IBERIAN', 'Basque': 'BASQUE'})
    r = json.load(open(os.path.join(M.RES, 't32_mapa_distancias.json'), encoding='utf-8'))['lexico']
    M.calor(r['lenguas'], np.array(r['matriz_normalizada']), 'Lexicon of the lead plaques: normalised distance between all languages (1 = chance), ordered by the tree',
            os.path.join(M.RES, 'figuras', 'figura_2_mapa_lexico_en.png'), 1.0)
