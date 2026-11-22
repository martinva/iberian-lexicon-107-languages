"""Tablas 11 a 13 (segunda parte): ventaja sobre el azar en significados estables y poco estables.

Un significado es ESTABLE si su glosa principal figura en la lista Leipzig–Yakarta (100) o en la de Swadesh (207):
uno, dos, tres, cuatro, cinco, dar, hacer, tierra, hierba, camino, monte. Los demás, poco estables.
Tabla 11: 42 parejas de lenguas de relación conocida (20 repeticiones por pareja, 120 sorteos cada una).
Tabla 12: ibérico frente a cada diccionario del Wikcionario (500 sorteos). Tabla 13: ibérico frente al euskera por origen del significado (y los cuatro préstamos latinos frente al gallego).
Uso:  python3 t11_t13_estables.py
"""
import json, os, sys
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import reducida
from ibcomp.pruebas import ventaja_por_grupos, generador, GRUPOS_ESTABLES as EST

PAREJAS = [('emparentadas cercanas', a, b) for a, b in [('Catalan', 'Occitan'), ('Galician', 'Asturian'), ('Malay', 'Indonesian'), ('Estonian', 'Finnish'), ('Romanian', 'Latin'), ('Catalan', 'Latin'), ('Sardinian', 'Latin'), ('Zulu', 'Shona')]] + \
          [('emparentadas lejanas', a, b) for a, b in [('Irish', 'Welsh'), ('Hungarian', 'Finnish'), ('Irish', 'Latin'), ('Icelandic', 'Latin'), ('Lithuanian', 'Latin'), ('Icelandic', 'Lithuanian'), ('Tagalog', 'Malay'), ('Malagasy', 'Malay'), ('Hawaiian', 'Malay'), ('Fijian', 'Malay'), ('Swahili', 'Zulu'), ('Hausa', 'Somali')]] + \
          [('parentesco lejano y préstamos', a, b) for a, b in [('Albanian', 'Latin'), ('Welsh', 'Latin')]] + \
          [('solo contacto', a, b) for a, b in [('Tagalog', 'Galician'), ('Tagalog', 'Catalan'), ('Quechua', 'Galician'), ('Basque', 'Latin'), ('Basque', 'Galician'), ('Basque', 'Catalan'), ('Maltese', 'Sicilian'), ('Hungarian', 'Turkish'), ('Finnish', 'Icelandic'), ('Romanian', 'Hungarian'), ('Romanian', 'Turkish'), ('Albanian', 'Turkish'), ('Malagasy', 'Swahili')]] + \
          [('sin relación', a, b) for a, b in [('Basque', 'Finnish'), ('Quechua', 'Hungarian'), ('Hawaiian', 'Irish'), ('Zulu', 'Icelandic'), ('Yoruba', 'Lithuanian'), ('Classical Nahuatl', 'Welsh'), ('Hausa', 'Estonian'), ('Fijian', 'Latin')]]
UN = fuentes.unidades_numerales() + fuentes.unidades_plomos(); CONC = [(u['id'], u) for u in UN]; IDS = {u['id'] for u in UN}
GRUPOS = {'estables': EST, 'poco estables': IDS - EST, 'estables sin los numerales del dos al cinco': EST - {'N2', 'N3', 'N4', 'N5'}, 'estables sin saltu': EST - {'A13'}, 'todos': IDS}
ORIGEN = {'dato externo (grado A): uno, diez, veinte, plata, mitad, hacer, escrito': {'N1', 'N10', 'N20', 'A1', 'A2', 'A30', 'A17'}, 'numerales del dos al ocho (valor por posición)': {'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8'},
          'por la casilla que ocupa en los documentos': {f'A{i}' for i in range(3, 24)} - {'A17'}, 'con apoyo de la toponimia': {f'A{i}' for i in range(24, 30)}, 'los cuatro préstamos latinos propuestos': {'A6', 'A9', 'A11', 'A13'}}
WIK = None
def _wik():
    global WIK
    if WIK is None: WIK = fuentes.wikcionario()
    return WIK

def pareja(arg):
    cat, lx, ly = arg; W = _wik(); rnd = generador('estables', lx, ly)
    fx = {cid: W[lx].candidatas(u, 'terminos_en') for cid, u in CONC}; fx = {k: v for k, v in fx.items() if v}
    ne = sum(1 for cid, u in CONC if cid in fx and cid in EST and W[ly].candidatas(u, 'terminos_en')); npo = sum(1 for cid, u in CONC if cid in fx and cid not in EST and W[ly].candidatas(u, 'terminos_en'))
    if ne < 5 or npo < 8: return (cat, lx, ly, f'cobertura insuficiente (estables {ne}, poco estables {npo})')
    R = [ventaja_por_grupos({k: [rnd.choice(v)] for k, v in fx.items()}, CONC, W[ly], rnd, GRUPOS, sorteos=120) for _ in range(20)]; out = {}
    for g in GRUPOS:
        v = [r[g] for r in R if r[g]]
        if v: out[g] = dict(n=round(float(np.mean([x['n'] for x in v])), 1), ventaja=round(float(np.mean([x['ventaja'] for x in v])), 3), z=round(float(np.mean([x['z'] for x in v])), 2))
    return (cat, lx, ly, out)

if __name__ == '__main__':
    W = _wik(); res = {'iberico': {}, 'iberico por origen': {}, 'parejas': []}; ruta = os.path.join(os.path.dirname(__file__), '..', 'resultados', 't11_t13_estables.json')
    xs = {u['id']: [reducida(f) for f in u['formas']] for u in UN}
    for ly in sorted(W):
        m = ventaja_por_grupos(xs, CONC, W[ly], generador('estables', 'ibérico', ly), GRUPOS, sorteos=500)
        if m['estables'] and m['poco estables']: res['iberico'][ly] = m
    print('== Tabla 12. Ibérico frente a cada lengua (ordenado por la ventaja en estables):')
    for l, m in sorted(res['iberico'].items(), key=lambda kv: -kv[1]['estables']['ventaja'])[:6]: print(f"  {l:16s} estables {m['estables']['ventaja']:.3f} (n {m['estables']['n']}) | poco estables {m['poco estables']['ventaja']:.3f} (n {m['poco estables']['n']}) | sin 2–5 {m['estables sin los numerales del dos al cinco']['ventaja']:.3f} | sin saltu {m['estables sin saltu']['ventaja']:.3f}")
    res['iberico por origen'] = ventaja_por_grupos(xs, CONC, W['Basque'], generador('estables', 'ibérico', 'origen'), ORIGEN, sorteos=500)
    res['prestamos frente al gallego'] = ventaja_por_grupos(xs, CONC, W['Galician'], generador('estables', 'ibérico', 'origen', 'gallego'), ORIGEN, sorteos=500)['los cuatro préstamos latinos propuestos']  # los cuatro préstamos, frente al gallego
    print('== Tabla 13. Ibérico frente al euskera, por origen del significado:'); [print(f'  {k}: n {v["n"]} ventaja {v["ventaja"]:.3f}') for k, v in res['iberico por origen'].items() if v]; print(f"  los cuatro préstamos latinos, frente al gallego: ventaja {res['prestamos frente al gallego']['ventaja']:.3f}"); sys.stdout.flush()
    with Pool(2) as p:
        for r in p.imap(pareja, PAREJAS):
            res['parejas'].append(r); cat, lx, ly, v = r
            print(f'  [{cat}] {lx}–{ly}: ' + (v if isinstance(v, str) else f"estables {v['estables']['ventaja']:.3f} | poco estables {v['poco estables']['ventaja']:.3f}"), flush=True)
            json.dump(res, open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('== Tabla 11. Resumen por tipo de relación')
    for cat in dict.fromkeys(c for c, _, _ in PAREJAS):
        v = [x[3] for x in res['parejas'] if x[0] == cat and not isinstance(x[3], str)]
        print(f"  {cat:32s} parejas {len(v):2d} | estables {np.mean([x['estables']['ventaja'] for x in v]):.3f} | poco estables {np.mean([x['poco estables']['ventaja'] for x in v]):.3f} | estables > poco en {sum(x['estables']['ventaja'] > x['poco estables']['ventaja'] for x in v)}")
