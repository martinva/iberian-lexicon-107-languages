"""Declaración 36: lenguas no indoeuropeas y preindoeuropeas de Eurasia occidental y central (Wikcionario, kaikki.org).

Uso / Usage:  python3 t50_preindoeuropeas.py RUTA/kaikki_preindoeuropeas.tsv
"""
import json, os, re, sys, unicodedata
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes, pruebas
from ibcomp.fuentes import Diccionario, terminos_de_glosa
from ibcomp.clases import reducida
from ibcomp.normalizadores import norm_control
from ibcomp.pruebas import perfil, divergencia, generador

FAMILIA = {**{l: 'kartvélica' for l in ('Georgian', 'Mingrelian', 'Laz', 'Svan')},
           **{l: 'caucásica NO' for l in ('Abkhaz', 'Adyghe', 'Kabardian')},
           **{l: 'caucásica NE' for l in ('Chechen', 'Ingush', 'Avar')},
           **{l: 'bereber' for l in ('Tashelhit', 'Central Atlas Tamazight')},
           **{l: 'semítica' for l in ('Arabic', 'Hebrew', 'Akkadian')}, 'Egyptian': 'egipcia',
           'Etruscan': 'tirsénica', 'Sumerian': 'aislada (sumerio)',
           **{l: 'túrquica' for l in ('Azerbaijani', 'Kazakh', 'Uzbek', 'Tatar', 'Bashkir', 'Chuvash', 'Yakut')},
           **{l: 'mongólica' for l in ('Mongolian', 'Kalmyk', 'Buryat')}, 'Tamil': 'drávida', 'Ket': 'yeniseica'}

def norm_general(w):
    """Romanización o grafía latina → grafía común (regla general fijada en la declaración 36)."""
    w = unicodedata.normalize('NFC', w.lower().split('|')[0].strip())
    for a, b in (('č', 'tx'), ('ç', 'tx'), ('ǯ', 'tx'), ('ǰ', 'tx'), ('dž', 'tx'), ('š', 's'), ('ş', 's'), ('ž', 's'), ('ʒ', 's'), ('ğ', 'g'), ('ǧ', 'g'),
                 ('ḫ', 'h'), ('χ', 'h'), ('x', 'h'), ('ı', 'i'), ('ə', 'e'), ('ɣ', 'g'), ('ŋ', 'ng'), ('ꜣ', ''), ('ꜥ', ''), ('ʼ', ''), ('ʿ', ''), ('ʾ', ''), ("'", ''), ('ʻ', '')):
        w = w.replace(a, b)
    w = ''.join(c for c in unicodedata.normalize('NFD', w) if unicodedata.category(c) != 'Mn')
    w = re.sub(r'[\-\.·₀-₉0-9]', '', w)
    return w if re.fullmatch(r'[a-zñ]+', w) else None

def lexico(ruta):
    L = defaultdict(lambda: defaultdict(set))
    for linea in open(ruta, encoding='utf-8'):
        p = linea.rstrip('\n').split('\t')
        if len(p) != 6 or p[4] != '0' or p[0] not in FAMILIA: continue
        bruto = p[3] if p[3] else p[1]
        w = norm_control(p[0], bruto.split('|')[-1] if p[0] == 'Sumerian' else bruto) if p[0] in ('Etruscan', 'Sumerian') else norm_general(bruto)
        if not w: continue
        x = reducida(w)
        if not 2 <= len(x) <= 12: continue
        T = set()
        for g in p[5].split(' || '):
            if re.match(r'(?i)(see |the meaning|alternative|romanization|obsolete|misspelling|the name of)', g) or 'uncertain' in g.lower(): continue
            T |= {t for t in terminos_de_glosa(g) if t and re.fullmatch(r'[a-z]+( [a-z]+)?', t)}
        if T: L[p[0]][x] |= T
    return L

if __name__ == '__main__':
    LX = lexico(sys.argv[1]); res = {'lenguas_datos': {l: len(v) for l, v in LX.items()}}
    dics = {l: Diccionario(l, v) for l, v in LX.items()}
    W = fuentes.wikcionario()
    conj = {'plomos': fuentes.unidades_plomos(), 'numerales': fuentes.unidades_numerales()}
    for nombre, us in conj.items():
        filas = []
        for l, d in list(W.items()) + list(dics.items()):
            r = pruebas.prueba_significados(us, d, nombre, minimo=0.4 * len(us))
            if r: r['familia'] = FAMILIA.get(l, 'estudio (35)'); r.pop('detalle', None); filas.append(r)
        filas.sort(key=lambda r: r['z'])
        fam = defaultdict(list)
        for r in filas:
            if r['familia'] != 'estudio (35)': fam[r['familia']].append(r['z'])
        res[nombre] = dict(orden=[(r['diccionario'], r['familia'], r['unidades'], round(r['z'], 2)) for r in filas],
                           puesto_euskera=[r['diccionario'] for r in filas].index('Basque') + 1,
                           mediana_z_familia={f: round(float(np.median(z)), 2) for f, z in fam.items()},
                           mejor_nueva=next(((r['diccionario'], round(r['z'], 2)) for r in filas if r['familia'] != 'estudio (35)'), None))
        print(f"\n== {nombre}: euskera {res[nombre]['puesto_euskera']}.º de {len(filas)}; mejor nueva {res[nombre]['mejor_nueva']}")
        for x in res[nombre]['orden'][:12]: print('  ', x)
        print('  familias:', res[nombre]['mediana_z_familia'])
    # perfil a igual tamaño (fuente común: Wikcionario)
    IB = set().union(*[f['formas'] for f in fuentes.hesperia()]); q = perfil(IB)
    conjuntos = {l: sorted(d.formas) for l, d in dics.items() if len(d.formas) >= 300}
    for l, d in W.items():
        if len(d.formas) >= 300: conjuntos[l] = sorted(d.formas)
    N = min(len(v) for v in conjuntos.values()); rnd = generador('t50', 'perfil')
    medias = {l: float(np.mean([divergencia(q, perfil(rnd.sample(v, N))) for _ in range(100)])) for l, v in conjuntos.items()}
    orden = sorted(medias, key=medias.get)
    res['perfil'] = dict(tamano=N, orden=[(l, FAMILIA.get(l, 'estudio (35)'), round(medias[l], 4)) for l in orden], puesto_euskera=orden.index('Basque') + 1)
    print('\n== perfil a igual tamaño', N, ':', res['perfil']['orden'][:12], 'euskera', res['perfil']['puesto_euskera'])
    res['previsiones'] = {'1': res['plomos']['puesto_euskera'] == 1 and res['numerales']['puesto_euskera'] == 1,
                          '2': all(v >= -2 for k in ('plomos', 'numerales') for v in res[k]['mediana_z_familia'].values()),
                          '3': res['perfil']['puesto_euskera'] == 1 or all(FAMILIA.get(l) is None for l in orden[:orden.index('Basque')])}
    print(res['previsiones'])
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't50_preindoeuropeas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
