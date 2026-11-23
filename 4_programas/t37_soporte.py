"""Declaración 23: vocabulario por soporte (plomo frente a cerámica y piedra).

Palabras, soporte y criterio de nombre probable: los de t01_t02_corpus.py (tabla G1), importados sin cambios.
(1) Rarefacción a 1.000 palabras (1.000 repeticiones): formas distintas (variantes equivalentes unidas) en plomo y en cerámica.
(2) Proporción de palabras completas de 4 o más letras sin nombre probable, con la longitud controlada: de cada inscripción
    de plomo, una ventana aleatoria de tantas palabras como una inscripción de cerámica sorteada; permutación de la etiqueta
    plomo/cerámica entre inscripciones (10.000).
(3) Formas características por soporte: log-odds con prior de Dirichlet informativo (Monroe, Colaresi y Quinn 2008), descriptivo.
Uso / Usage:  python3 t37_soporte.py
"""
import csv, json, math, os, random, re, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.texto import limpia
import t01_t02_corpus as T

REP, PERM = 1000, 10000

def inscripciones():
    I = f'{fuentes.RAIZ}/iberico'; meta = {r['ref_hesperia']: r for r in csv.DictReader(open(f'{I}/hesperia_metadatos.csv', encoding='utf-8-sig'))}
    FOR = set(limpia(x['formante']) for x in json.load(open(f'{I}/formantes_onomasticos_rodriguez_ramos_2014.json', encoding='utf-8')))
    MLH = {limpia(r['forma']): r for r in csv.DictReader(open(f'{I}/lexico_mlh_v2_clasificacion.csv', encoding='utf-8-sig'))}
    def es_nombre(w):                                   # copia literal de t01_t02_corpus.es_nombre (allí es local a __main__)
        m = MLH.get(w)
        if m: return m['clase_segun_primera_frase'] in T.CLASES_NOMBRE or m['nombre_dudoso'] == 'sí'
        for s in [''] + T.SUFIJOS + ['ku', 'ḿ', 'i']:
            if s and not w.endswith(s): continue
            b = w[:-len(s)] if s else w
            if any(b[:k] in FOR and b[k:] in FOR for k in range(2, len(b) - 1)): return True
        return False
    out = []
    for r in csv.DictReader(open(f'{I}/hesperia_iberico_1599.csv', encoding='utf-8-sig')):
        g = T.grupo(meta[r['ref_hesperia']]); toks = []
        for linea in r['texto_crudo'].split('\n'):
            if re.search(r'[A-Z]{3,}', linea): continue
            for t in re.split(r'[·:|\s,;/]+', linea):
                w0 = limpia(re.sub(T.SIGNOS, '', t))
                if not re.fullmatch(T.LETRAS + '{2,}', w0): continue
                completa = not re.search(T.SIGNOS, t); w = limpia(t) if completa else w0
                eleg = completa and len(w) >= 4
                toks.append((T.equivalente(w0), eleg, (not es_nombre(w)) if eleg else None))
        out.append(dict(sigla=r['ref_hesperia'], soporte=g, toks=toks))
    return out

def proporcion(lista):
    e = [x for x in lista if x[1]]; return (sum(x[2] for x in e) / len(e), len(e)) if e else (float('nan'), 0)

def ventana(rnd, toks, L):
    if L >= len(toks): return toks
    i = rnd.randrange(len(toks) - L + 1); return toks[i:i + L]

def estadistico(rnd, plomo, ceram):
    largos = [len(c['toks']) for c in ceram if c['toks']]
    v = [x for p in plomo for x in ventana(rnd, p['toks'], rnd.choice(largos))]
    pc = [x for c in ceram for x in c['toks']]
    return proporcion(v)[0] - proporcion(pc)[0]

def logodds(cnt, tot, prior):
    a0 = sum(prior.values()); n_i = sum(cnt.values()); n_j = sum(tot.values()) - n_i; res = []
    for w, a in prior.items():
        yi = cnt.get(w, 0); yj = tot[w] - yi
        d = math.log((yi + a) / (n_i + a0 - yi - a)) - math.log((yj + a) / (n_j + a0 - yj - a))
        res.append((round(d / math.sqrt(1 / (yi + a) + 1 / (yj + a)), 2), w, yi))
    return sorted(res, reverse=True)

if __name__ == '__main__':
    INS = inscripciones(); rnd = random.Random('t37|soporte'); res = {}
    por = defaultdict(list); [por[i['soporte']].append(i) for i in INS]
    tok = {g: [x[0] for i in por[g] for x in i['toks']] for g in por}
    # (1) rarefacción
    rar = {}
    for g in ('Plomo', 'Cerámica'):
        vals = sorted(len(set(rnd.sample(tok[g], 1000))) for _ in range(REP))
        rar[g] = dict(palabras=len(tok[g]), media=round(sum(vals) / REP, 1), ic95=[vals[int(0.025 * REP)], vals[int(0.975 * REP) - 1]])
    rnd2 = random.Random('t37|rarefaccion-pareada'); gana = sum(len(set(rnd2.sample(tok['Plomo'], 1000))) > len(set(rnd2.sample(tok['Cerámica'], 1000))) for _ in range(REP))
    res['1_rarefaccion_1000_palabras'] = dict(rar, plomo_mayor_en=gana, de=REP, prevision_cumplida=rar['Plomo']['media'] > rar['Cerámica']['media'])
    print('1.', res['1_rarefaccion_1000_palabras'])
    # (2) proporción no onomástica con la longitud controlada
    plomo, ceram = por['Plomo'], por['Cerámica']
    bruto = proporcion([x for i in plomo for x in i['toks']])[0] - proporcion([x for i in ceram for x in i['toks']])[0]
    obs = sum(estadistico(rnd, plomo, ceram) for _ in range(REP)) / REP
    mezcla = plomo + ceram; k = len(plomo); rp = random.Random('t37|permutacion'); ge = 0
    for _ in range(PERM):
        rp.shuffle(mezcla); ge += estadistico(rp, mezcla[:k], mezcla[k:]) >= obs
    p = (ge + 1) / (PERM + 1)
    res['2_no_onomastico'] = dict(proporcion_plomo=round(proporcion([x for i in plomo for x in i['toks']])[0], 3), elegibles_plomo=proporcion([x for i in plomo for x in i['toks']])[1],
                                  proporcion_ceramica=round(proporcion([x for i in ceram for x in i['toks']])[0], 3), elegibles_ceramica=proporcion([x for i in ceram for x in i['toks']])[1],
                                  diferencia_bruta=round(bruto, 3), diferencia_con_longitud_controlada=round(obs, 3), p_permutacion=round(p, 5), permutaciones=PERM, prevision_cumplida=obs > 0 and p < 0.01)
    print('2.', res['2_no_onomastico'])
    # (3) log-odds descriptivo
    tot = Counter(x for g in tok for x in tok[g]); prior = dict(tot)
    res['3_formas_caracteristicas'] = {g: logodds(Counter(tok[g]), tot, prior)[:20] for g in ('Plomo', 'Cerámica', 'Piedra')}
    for g, l in res['3_formas_caracteristicas'].items(): print('3.', g, l[:10])
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't37_soporte.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
