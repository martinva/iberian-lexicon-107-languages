"""Declaración 31: vía A, vecindad de las formas con numerales y signos metrológicos (permutación dentro de cada texto).

Uso / Usage:  python3 t45_vecindad_numerales.py
"""
import csv, json, os, re, sys, unicodedata
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.pruebas import generador

NUM = re.compile(r'^[a-zśŕḿ]{0,3}[IΠ]+[IΠ]*$|^\(\d+\)$')
PERM = 10000

def segmentos(texto):
    t = unicodedata.normalize('NFD', texto)
    t = ''.join(ch for ch in t if unicodedata.category(ch) != 'Mn')
    t = unicodedata.normalize('NFC', t.replace('ś', 'ś').replace('ŕ', 'ŕ'))
    t = re.sub(r'\[[^\]]*\]|[\[\]\+\?\-–‐…\.]', ' ', t)
    out = []
    for s in re.split(r'[:│·\s∙]+', t):
        s = re.sub(r'\((\d+)\)', r' (\1) ', s)
        for x in s.split():
            if NUM.match(x): out.append('#')
            elif re.fullmatch(r'[a-zśŕḿ]{2,}', x): out.append(x)
            else: out.append(None)
    return out

def vecinas(seq):
    v = Counter(); n = Counter()
    for i, w in enumerate(seq):
        if w and w != '#':
            n[w] += 1
            if (i > 0 and seq[i - 1] == '#') or (i + 1 < len(seq) and seq[i + 1] == '#'): v[w] += 1
    return v, n

if __name__ == '__main__':
    I = f'{fuentes.RAIZ}/iberico'
    textos = []
    for r in csv.DictReader(open(f'{I}/hesperia_iberico_1599.csv', encoding='utf-8-sig')):
        s = segmentos(r['texto_crudo'])
        if '#' in s: textos.append(s)
    V, N = Counter(), Counter()
    for s in textos: v, n = vecinas(s); V += v; N += n
    unidades = fuentes.unidades_plomos(); Q = {'A1', 'A2', 'A3', 'A5', 'A6', 'A16'}
    def grupo(w):
        for u in unidades:
            if any(w == f or w.startswith(f) for f in u['formas']): return 'Q' if u['id'] in Q else 'R'
        return None
    frec = [w for w in N if N[w] >= 3]
    rnd = generador('t45', 'permutacion'); mayor = Counter(); EV = Counter(); gq = {'Q': [0, 0], 'R': [0, 0]}
    for s in textos:
        for w in s:
            g = grupo(w) if w and w != '#' else None
            if g: gq[g][1] += 1
    obsQ = {g: sum(V[w] for w in N if grupo(w) == g) for g in 'QR'}
    difobs = obsQ['Q'] / max(1, gq['Q'][1]) - obsQ['R'] / max(1, gq['R'][1]); ge = 0; nullQ = []
    for k in range(PERM):
        Vp = Counter()
        for s in textos:
            p = s[:]; rnd.shuffle(p); v, _ = vecinas(p); Vp += v
        for w in frec:
            EV[w] += Vp[w]
            if Vp[w] >= V[w]: mayor[w] += 1
        pq = {g: sum(Vp[w] for w in N if grupo(w) == g) for g in 'QR'}
        d = pq['Q'] / max(1, gq['Q'][1]) - pq['R'] / max(1, gq['R'][1]); nullQ.append(pq['Q'] / max(1, gq['Q'][1]))
        if d >= difobs: ge += 1
    tabla = sorted(((w, N[w], V[w], round(EV[w] / PERM, 2), round(V[w] / max(EV[w] / PERM, 1e-9), 2), (1 + mayor[w]) / (PERM + 1)) for w in frec), key=lambda x: x[5])
    res = dict(textos_con_numerales=len(textos), elementos_numerales=sum(s.count('#') for s in textos), palabras=sum(N.values()),
               formas_frecuentes=len(frec), tabla=[dict(forma=a, apariciones=b, vecinas=c, esperadas=d, razon=e, p=f) for a, b, c, d, e, f in tabla],
               contraste=dict(Q_apariciones=gq['Q'][1], Q_vecinas=obsQ['Q'], R_apariciones=gq['R'][1], R_vecinas=obsQ['R'],
                              Q_prop=round(obsQ['Q'] / max(1, gq['Q'][1]), 3), R_prop=round(obsQ['R'] / max(1, gq['R'][1]), 3),
                              Q_prop_esperada=round(sum(nullQ) / PERM, 3), p_diferencia=(1 + ge) / (PERM + 1)))
    print({k: v for k, v in res.items() if k != 'tabla'})
    for row in res['tabla'][:25]: print(row)
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't45_vecindad_numerales.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
