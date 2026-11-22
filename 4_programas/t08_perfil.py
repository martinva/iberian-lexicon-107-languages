"""Tabla 8 y apartado 7.4: perfil de combinaciones de sonidos del ibérico frente a 107 lenguas (NorthEuraLex) y frente a 35 lenguas del Wikcionario.

Pasos: (1) validación: ¿la lengua más próxima a cada lengua es de su familia?; (2) lenguas de control; (3) ibérico, corpus completo
y plomos; (4) las mismas cuentas con todas las lenguas reducidas al inventario que el ibérico escribe; (5) remuestreo;
(6) lenguas de otras zonas del mundo (Wikcionario).
Uso:  python3 t08_perfil.py
"""
import json, os, sys, re
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes, pruebas
from ibcomp.clases import proyecta, reducida
from ibcomp.normalizadores import NORM, norm_control, red_control
from ibcomp.pruebas import perfil, divergencia, generador

FAM_WIK = {**{l: 'romance' for l in 'Latin Catalan Galician Asturian Occitan Romanian Sicilian Sardinian'.split()}, 'Welsh': 'céltica', 'Irish': 'céltica', **{l: 'urálica' for l in 'Finnish Estonian Hungarian'.split()},
           **{l: 'austronesia' for l in 'Tagalog Malagasy Indonesian Malay Hawaiian Samoan Tongan Fijian'.split()}, **{l: 'bantú' for l in 'Swahili Zulu Shona'.split()}}

def lexico_control_completo(lengua):
    """Todo el léxico elegible de una lengua de control, de 2 a 12 clases (para el perfil no se exige glosa)."""
    out = set()
    for linea in open(f'{fuentes.RAIZ}/wikcionario/kaikki_lenguas_de_control_2026-11-19.tsv', encoding='utf-8'):
        p = linea.rstrip('\n').split('\t')
        if len(p) != 6 or p[0] != lengua or p[4] != '0' or p[2] not in ('noun', 'verb', 'adj', 'adv', 'num', 'pron'): continue
        w = norm_control(lengua, (p[3].split('|')[0] if p[3] else p[1]).strip())
        if w and re.fullmatch(r'[a-zñð]+', w) and 2 <= len(red_control(w)) <= 12: out.add(red_control(w))
    return out

def vecinos(q, P, nombres, n=6):
    return sorted((round(divergencia(q, P[l]), 4), nombres[l]) for l in P)[:n]

def analiza(etiqueta, LEX, nombres, familia, ib, controles, res, remuestreos=500):
    P = {l: perfil(ws) for l, ws in LEX.items()}; fams = Counter(familia.get(l, '') for l in P); ok = tot = 0; par = []; nopar = []
    for l in P:
        if not familia.get(l) or fams[familia[l]] < 2: continue
        o = sorted((divergencia(P[l], P[m]), m) for m in P if m != l); tot += 1; ok += familia.get(o[0][1]) == familia[l]
        par.append(min(d for d, m in o if familia.get(m) == familia[l])); nopar.append(min(d for d, m in o if familia.get(m) != familia[l]))
    azar = sum((fams[familia[l]] - 1) / (len(P) - 1) for l in P if familia.get(l) and fams[familia[l]] >= 2) / tot
    r = dict(lenguas=len(P), validacion=dict(aciertos=ok, total=tot, azar=round(azar, 3), mediana_pariente=round(float(np.median(par)), 3), mediana_no_pariente=round(float(np.median(nopar)), 3)), controles={}, iberico={})
    print(f'\n===== {etiqueta}: {len(P)} lenguas | la más próxima es de la misma familia en {ok} de {tot} ({100 * ok / tot:.0f} %; por azar {100 * azar:.0f} %)')
    for l, ws in controles.items():
        r['controles'][l] = vecinos(perfil(ws), P, nombres); print(f'  control {l} ({len(ws)} formas): {r["controles"][l][:4]}')
    eus = next(l for l in P if nombres[l] == 'Basque'); r['euskera_vecinos'] = sorted((round(divergencia(P[eus], P[m]), 4), nombres[m]) for m in P if m != eus)[:4]
    for nombre, ws in ib.items():
        ws = sorted(ws); o = sorted((divergencia(perfil(ws), P[m]), nombres[m]) for m in P); pos = [n for d, n in o].index('Basque') + 1; rnd = generador('perfil', etiqueta, nombre); c1 = c2 = 0
        for _ in range(remuestreos):
            p1 = perfil([rnd.choice(ws) for _ in ws]); p2 = perfil(rnd.sample(ws, len(ws) // 2))          # una sola muestra por repetición, la misma frente a todas las lenguas
            c1 += min((divergencia(p1, P[m]), nombres[m]) for m in P)[1] == 'Basque'
            c2 += min((divergencia(p2, P[m]), nombres[m]) for m in P)[1] == 'Basque'
        r['iberico'][nombre] = dict(formas=len(ws), puesto_euskera=pos, tabla=[(n, round(d, 4)) for d, n in o], remuestreo=c1, mitades=c2, de=remuestreos)
        print(f'  IBÉRICO {nombre} ({len(ws)} formas): euskera en el puesto {pos} de {len(o)} | {[(n, round(d, 3)) for d, n in o[:5]]} | primero en {c1}/{remuestreos} remuestreos y {c2}/{remuestreos} mitades')
    res[etiqueta] = r; sys.stdout.flush()

if __name__ == '__main__':
    fichas = fuentes.hesperia(); TODAS = set().union(*[f['formas'] for f in fichas]); PLOMO = set().union(*[f['formas'] for f in fichas if f['plomo_amplio']])
    ib = {'todo el corpus': TODAS, 'plomos': PLOMO}; res = {}
    LEX, lang = fuentes.northeuralex(); nombres = {l: lang[l]['Name'] for l in LEX}; familia = {l: (lang[l].get('Family') or '') for l in LEX}
    ctrl = {fuentes.CONTROL[l]: lexico_control_completo(l) for l in fuentes.CONTROL}
    analiza('NorthEuraLex, clases completas', LEX, nombres, familia, ib, ctrl, res)
    analiza('NorthEuraLex, reducidas a lo que el ibérico escribe', {l: proyecta(ws) for l, ws in LEX.items()}, nombres, familia, {k: proyecta(v) for k, v in ib.items()}, {k: proyecta(v) for k, v in ctrl.items()}, res)
    W = {l: set(d.formas) for l, d in fuentes.wikcionario().items()}; nw = {l: l for l in W}
    analiza('Wikcionario (otras zonas), clases completas', W, nw, FAM_WIK, ib, {}, res, remuestreos=300)
    analiza('Wikcionario (otras zonas), reducidas', {l: proyecta(ws) for l, ws in W.items()}, nw, FAM_WIK, {k: proyecta(v) for k, v in ib.items()}, {}, res, remuestreos=300)
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't08_perfil.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
