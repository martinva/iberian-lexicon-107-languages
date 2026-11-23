"""Declaración 28 (exploratoria): alineamiento por géneros de texto entre ibérico y celtibérico.

Para cada género presente en los dos corpus, finales de palabra (1 a 3 clases, formas reducidas con red_ib) y su posición
en el texto (única, primera, interior, última); pares ibérico–celtibérico de finales con distribución posicional semejante.
Solo candidatos: ninguna salida es una traducción.
Uso / Usage:  python3 t42_generos.py RUTA/celtiberian_raw.csv
"""
import csv, json, math, os, re, sys, unicodedata
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import red_ib

POS = ('unica', 'primera', 'interior', 'ultima')

def palabras(texto):
    t = unicodedata.normalize('NFC', re.sub(r'[\[\]\(\)\+\-\?̲̱̣]', '', texto)).lower(); out = []
    for w in re.split(r'[^\wśŕḿ]+', t):
        if not w or re.search(r'\d|[ivxlπ]{3,}', w): continue
        x = red_ib(w)
        if 2 <= len(x) <= 12: out.append(x)
    return out

def genero_ib(m):
    g = m['soporte_grupo']
    if g == 'TESERA': return 'tesera'
    if g == 'RECIPIENTE': return 'recipiente'
    if g == 'LAPIDA_ESTELA': return 'estela_lapida'
    if g == 'PARIETAL': return 'rupestre_parietal'
    if g == 'LAMINA_PLACA': return 'lamina'
    return None

def genero_ce(s):
    s = (s or '').upper()
    if 'TESERA' in s or 'TÉSERA' in s: return 'tesera'
    if 'RECIPIENTE' in s: return 'recipiente'
    if 'ESTELA' in s or 'LAPIDA' in s: return 'estela_lapida'
    if 'PARIETAL' in s or 'RUPESTRE' in s: return 'rupestre_parietal'
    if 'LAMINA' in s or 'PLANCHA' in s or 'PLACA' in s: return 'lamina'
    return None

def perfil_finales(textos):
    d = defaultdict(Counter)
    for ws in textos:
        for i, w in enumerate(ws):
            p = 'unica' if len(ws) == 1 else ('primera' if i == 0 else ('ultima' if i == len(ws) - 1 else 'interior'))
            for k in (1, 2, 3):
                if len(w) > k: d[w[-k:]][p] += 1
    return d

def jsd(a, b):
    ta, tb = sum(a.values()), sum(b.values()); s = 0.0
    for k in POS:
        p = a.get(k, 0) / ta; q = b.get(k, 0) / tb; m = (p + q) / 2
        if p: s += 0.5 * p * math.log2(p / m)
        if q: s += 0.5 * q * math.log2(q / m)
    return s

if __name__ == '__main__':
    I = f'{fuentes.RAIZ}/iberico'
    meta = {r['ref_hesperia']: r for r in csv.DictReader(open(f'{I}/hesperia_metadatos.csv', encoding='utf-8-sig'))}
    IBT = defaultdict(list)
    for r in csv.DictReader(open(f'{I}/hesperia_iberico_1599.csv', encoding='utf-8-sig')):
        g = genero_ib(meta[r['ref_hesperia']]); ws = palabras(r['texto_crudo'])
        if g and ws: IBT[g].append(ws)
    csv.field_size_limit(10 ** 9); CET = defaultdict(list)
    for r in csv.DictReader(open(sys.argv[1], encoding='utf-8'), delimiter=';'):
        if re.search('FALSA|SUSPECTA|LATINA', r['refHesperia']) or 'LATINO' in (r['signario'] or '').upper(): continue
        g = genero_ce(r['soporte']); ws = palabras(r['texto'])
        if g and ws: CET[g].append(ws)
    res = {}
    for g in sorted(set(IBT) & set(CET)):
        fi, fc = perfil_finales(IBT[g]), perfil_finales(CET[g])
        ti = [k for k, v in sorted(fi.items(), key=lambda x: -sum(x[1].values())) if sum(v.values()) >= 3][:15]
        tc = [k for k, v in sorted(fc.items(), key=lambda x: -sum(x[1].values())) if sum(v.values()) >= 3][:15]
        pares = sorted((round(jsd(fi[a], fc[b]), 3), a, b, sum(fi[a].values()), sum(fc[b].values())) for a in ti for b in tc)[:12]
        res[g] = dict(textos_ib=len(IBT[g]), textos_ce=len(CET[g]),
                      palabras_por_texto_ib=round(sum(map(len, IBT[g])) / len(IBT[g]), 1), palabras_por_texto_ce=round(sum(map(len, CET[g])) / len(CET[g]), 1),
                      finales_ib=[(k, dict(fi[k])) for k in ti[:8]], finales_ce=[(k, dict(fc[k])) for k in tc[:8]],
                      pares_mas_semejantes=pares)
        print(f"\n== {g}: ib {len(IBT[g])} textos ({res[g]['palabras_por_texto_ib']} pal.), ce {len(CET[g])} ({res[g]['palabras_por_texto_ce']})")
        print('  finales ib:', res[g]['finales_ib'][:6]); print('  finales ce:', res[g]['finales_ce'][:6]); print('  pares:', pares[:8])
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't42_generos.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
