"""Declaración 27: efecto de la escritura en la prueba de perfil (cuatro controles).

(1) celtibérico en alfabeto latino frente a signario; (2) ibérico grecoibérico frente a levantino; (3) canal de escritura
simulado aplicado a las 107 lenguas (supresión / vocal de apoyo); (4) pseudocorpus de solo escritura.
Oclusivas (clases SCA): P, T, K. El signario no escribe oclusiva + consonante ni oclusiva final.
Uso / Usage:  python3 t41_escritura.py RUTA/celtiberian_raw.csv
"""
import csv, json, os, re, sys, unicodedata
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import red_ib
from ibcomp.pruebas import perfil, divergencia, generador

OCL = set('PTK'); VOC = set('aeiou')

def formas_cel_por_escritura(ruta):
    csv.field_size_limit(10 ** 9); lat, sig = set(), set()
    for r in csv.DictReader(open(ruta, encoding='utf-8'), delimiter=';'):
        if re.search('FALSA|SUSPECTA|LATINA', r['refHesperia']): continue
        destino = lat if 'LATINO' in (r['signario'] or '').upper() else sig
        texto = unicodedata.normalize('NFC', re.sub(r'[\[\]\(\)\+\-\?̲̱̣]', '', r['texto'])).lower()
        for t in re.split(r'[^\wśŕḿ]+', texto):
            if not t or re.search(r'\d|[ivxlπ]{3,}', t): continue
            x = red_ib(t)
            if 2 <= len(x) <= 12: destino.add(x)
    return lat, sig

def canal(w, modo):
    out = []
    for i, ch in enumerate(w):
        sig = w[i + 1] if i + 1 < len(w) else None
        if ch in OCL and (sig is None or sig not in VOC):
            if modo == 'supresion': continue
            out.append(ch)
            v = next((c for c in w[i + 1:] if c in VOC), None) or next((c for c in reversed(w[:i]) if c in VOC), 'a')
            out.append(v); continue
        out.append(ch)
    s = ''.join(out); return s if len(s) >= 2 else None

def signos(w):
    """Parte una forma ibérica en signos: oclusiva + vocal es un signo; el resto, uno por letra."""
    out, i = [], 0
    while i < len(w):
        if w[i] in OCL and i + 1 < len(w) and w[i + 1] in VOC: out.append(w[i:i + 2]); i += 2
        else: out.append(w[i]); i += 1
    return out

def ranking(ws, P, nombres, n=5):
    q = perfil(ws); o = sorted((divergencia(q, P[l]), nombres[l]) for l in P)
    return [(nm, round(d, 4)) for d, nm in o[:n]], [nm for d, nm in o].index('Basque') + 1, round(next(d for d, nm in o if nm == 'Basque'), 4)

def remuestreo(ws, P, nombres, clave, rep=500):
    rnd = generador('t41', clave); ws = sorted(ws); top5 = 0; prim = 0
    for _ in range(rep):
        q = perfil([rnd.choice(ws) for _ in ws]); o = sorted((divergencia(q, P[l]), nombres[l]) for l in P)
        nm = [x for _, x in o]; prim += nm[0] == 'Basque'; top5 += 'Basque' in nm[:5]
    return dict(euskera_primero=prim, euskera_entre_5=top5, de=rep)

if __name__ == '__main__':
    LEX, lang = fuentes.northeuralex(); nombres = {l: lang[l]['Name'] for l in LEX}
    P = {l: perfil(ws) for l, ws in LEX.items()}
    fichas = fuentes.hesperia(); IB = set().union(*[f['formas'] for f in fichas]); res = {}
    # (1) celtibérico por escritura
    lat, sig = formas_cel_por_escritura(sys.argv[1])
    r1 = {}
    for nombre, ws in (('alfabeto latino', lat), ('signario', sig)):
        top, pos, d = ranking(ws, P, nombres)
        r1[nombre] = dict(formas=len(ws), primeras_5=top, puesto_euskera=pos, div_euskera=d, familia_primera=next(lang[l]['Family'] for l in P if nombres[l] == top[0][0]))
    r1['prevision_cumplida'] = r1['alfabeto latino']['div_euskera'] > r1['signario']['div_euskera'] and r1['alfabeto latino']['familia_primera'] == 'Indo-European'
    res['1_celtiberico_por_escritura'] = r1; print('1.', r1)
    # (2) ibérico grecoibérico frente a levantino
    gr = set().union(*[f['formas'] for f in fichas if f['signario'] == 'GRECOIBERICO'])
    lv = set().union(*[f['formas'] for f in fichas if f['signario'] == 'LEVANTINO'])
    r2 = {}
    for nombre, ws in (('grecoibérico', gr), ('levantino', lv)):
        top, pos, d = ranking(ws, P, nombres); r2[nombre] = dict(formas=len(ws), primeras_5=top, puesto_euskera=pos, div_euskera=d)
    r2['grecoibérico']['remuestreo'] = remuestreo(gr, P, nombres, 'grecoiberico')
    r2['prevision_cumplida'] = r2['grecoibérico']['puesto_euskera'] <= 5
    res['2_iberico_por_escritura'] = r2; print('2.', r2)
    # (3) canal de escritura simulado
    r3 = {}
    for modo in ('supresion', 'vocal_de_apoyo'):
        Pc = {l: perfil({x for x in (canal(w, modo) for w in ws) if x}) for l, ws in LEX.items()}
        top, pos, d = ranking(IB, Pc, nombres, n=8); r3[modo] = dict(primeras_8=top, puesto_euskera=pos, div_euskera=d)
    r3['prevision_cumplida'] = all(r3[m]['puesto_euskera'] == 1 for m in ('supresion', 'vocal_de_apoyo'))
    res['3_canal_simulado'] = r3; print('3.', r3)
    # (4) pseudocorpus de solo escritura
    ss = [signos(w) for w in IB]; freq = Counter(s for x in ss for s in x); largos = [len(x) for x in ss]
    pob, pesos = zip(*sorted(freq.items())); rnd = generador('t41', 'pseudocorpus'); cnt = Counter(); primeros = Counter()
    for _ in range(200):
        ws = {''.join(rnd.choices(pob, weights=pesos, k=rnd.choice(largos))) for _ in range(len(IB))}
        top, pos, d = ranking(ws, P, nombres, n=1); cnt[pos == 1] += 1; primeros[top[0][0]] += 1
    res['4_pseudocorpus'] = dict(euskera_primero=cnt[True], de=200, lengua_primera=dict(primeros.most_common(6)), prevision_cumplida=cnt[True] < 100)
    print('4.', res['4_pseudocorpus'])
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't41_escritura.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
