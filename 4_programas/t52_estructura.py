"""Declaración 38: estructura distribucional sin euskera (exploratoria).

38.A vecindad con numerales (repite la 31 con la lectura corregida) · 38.B ¿predice el contexto la clase de una palabra?
38.C segmentación por entropía de ramificación y entidad de palabra de las unidades · 38.D hapax y Zipf por soporte.

No usa ninguna lengua de comparación. El celtibérico (archivo de la declaración 24) sirve de calibración.
Uso / Usage:  python3 t52_estructura.py RUTA/celtiberian_raw.csv [A B C D]
"""
import csv, json, math, os, re, sys, unicodedata
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.texto import limpia
from ibcomp.pruebas import generador
from t01_t02_corpus import SUFIJOS, CLASES_NOMBRE, grupo

SEP = r'[:·│|.∙\s]+'
ELEM = re.compile(r'[IVXLΠΙ<>S]+-?|\d+|[a-zśŕḿ]+')
SIGNO = re.compile(r'[btdkg][aeiou]|.')

# ------------------------------------------------------------------ lectura común
def _sin_marcas(t):
    t = unicodedata.normalize('NFD', t).replace('ś', '\x01').replace('ŕ', '\x02').replace('ḿ', '\x03')
    t = ''.join(ch for ch in t if unicodedata.category(ch) != 'Mn')
    return t.replace('\x01', 'ś').replace('\x02', 'ŕ').replace('\x03', 'ḿ')

def lee(texto):
    """Devuelve la lista de líneas; cada línea es una lista de elementos ('W', palabra, pegada) | ('N',) | ('G',).

    `pegada` es True si la palabra sigue a la anterior con un separador escrito y sin nada más en medio (se usa en 38.C)."""
    lineas = []
    for linea in _sin_marcas(texto).split('\n'):
        linea = linea.strip()
        if not linea: continue
        m = re.search(r'(\d+)$', linea)
        if m and int(m.group(1)) % 5 == 0 and int(m.group(1)) > 0: linea = linea[:m.start()]
        linea = re.sub(r'\[[^\]]*\]', ' \x04 ', linea)
        linea = re.sub(r'[\[\]\+]|--+', ' \x04 ', linea)
        linea = re.sub(r'[\?\(\)\'’]', '', linea)
        items = []; previo_sep = False
        for tramo in re.split(f'({SEP})', linea):
            if not tramo: continue
            if re.fullmatch(SEP, tramo): previo_sep = True; continue
            if '\x04' in tramo or re.search(r'S\d', tramo) or ELEM.sub('', tramo) != '':
                items.append(('G',)); previo_sep = False; continue
            partes = ELEM.findall(tramo)
            for j, p in enumerate(partes):
                if re.fullmatch(r'[a-zśŕḿ]+', p):
                    pegada = j == 0 and previo_sep and bool(items) and items[-1][0] == 'W'
                    items.append(('W', p, pegada))
                else: items.append(('N',))
            previo_sep = False
        if items: lineas.append(items)
    return lineas

def corpus_iberico():
    I = f'{fuentes.RAIZ}/iberico'
    meta = {r['ref_hesperia']: r for r in csv.DictReader(open(f'{I}/hesperia_metadatos.csv', encoding='utf-8-sig'))}
    out = []
    for r in csv.DictReader(open(f'{I}/hesperia_iberico_1599.csv', encoding='utf-8-sig')):
        m = meta[r['ref_hesperia']]
        if 'LATINO' in (m.get('signario') or '').upper(): continue
        out.append(dict(sigla=r['ref_hesperia'], grupo=grupo(m), lineas=lee(r['texto_crudo'])))
    return out

def prepara_celtiberico(t):
    """El archivo trae cada texto en una sola línea, con los rótulos de la edición (Título:, Columna I:, Cara A:, I-1., 01.).
    Se convierten en saltos de línea y se quitan «(sic)» y los desarrollos entre paréntesis, que no están en el original."""
    t = re.sub(r'(Título|Columna\s+[IVX]+|Cara\s+[A-D]|\b[A-D]):', '\n', t)
    t = re.sub(r'(?<![\w\[])(?:[IVX]+-)?\d+\.(?=\s|$)', '\n', t)
    return re.sub(r'\([^)]*\)', '', t)

def corpus_celtiberico(ruta):
    csv.field_size_limit(10 ** 9); out = []
    for r in csv.DictReader(open(ruta, encoding='utf-8'), delimiter=';'):
        if re.search('FALSA|SUSPECTA|LATINA', r['refHesperia']) or 'LATIN' in (r.get('signario') or '').upper(): continue
        out.append(dict(sigla=r['refHesperia'], grupo='Celtibérico', lineas=lee(prepara_celtiberico(r['texto']))))
    return out

def palabras(t): return [it[1] for l in t['lineas'] for it in l if it[0] == 'W']

def criterio_nombre():
    I = f'{fuentes.RAIZ}/iberico'
    FOR = set(limpia(x['formante']) for x in json.load(open(f'{I}/formantes_onomasticos_rodriguez_ramos_2014.json', encoding='utf-8')))
    MLH = {limpia(r['forma']): r for r in csv.DictReader(open(f'{I}/lexico_mlh_v2_clasificacion.csv', encoding='utf-8-sig'))}
    def es_nombre(w):                                   # copia literal del criterio de t01_t02_corpus.py (tabla G1)
        m = MLH.get(w)
        if m: return m['clase_segun_primera_frase'] in CLASES_NOMBRE or m['nombre_dudoso'] == 'sí'
        for s in [''] + SUFIJOS + ['ku', 'ḿ', 'i']:
            if s and not w.endswith(s): continue
            b = w[:-len(s)] if s else w
            if any(b[:k] in FOR and b[k:] in FOR for k in range(2, len(b) - 1)): return True
        return False
    return es_nombre

def auc(pos, neg):
    if not pos or not neg: return None
    todos = sorted([(x, 1) for x in pos] + [(x, 0) for x in neg]); n = len(todos); suma = 0.0; i = 0
    while i < n:
        j = i
        while j < n and todos[j][0] == todos[i][0]: j += 1
        r = (i + j + 1) / 2
        suma += r * sum(c for _, c in todos[i:j]); i = j
    return (suma - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))

# ------------------------------------------------------------------ 38.A
def parte_A(IB, PERM=10000):
    U = fuentes.unidades_plomos(); Q = {'A1', 'A2', 'A3', 'A5', 'A6', 'A16'}
    def grupos(w):
        g = set()
        for u in U:
            for f in u['formas']:
                f = _sin_marcas(f)
                if (w == f) if len(f) < 4 else (w.startswith(f) or w.endswith(f)): g.add('Q' if u['id'] in Q else 'R')
        return g
    def ultimo(w): return SIGNO.findall(w)[-1]
    textos = [t for t in IB if any(it[0] == 'N' for l in t['lineas'] for it in l)]
    def recuento(t, orden=None):
        """vecinas y totales por forma; `orden` es la lista permutada de los elementos W/N del texto."""
        k = 0; V = Counter(); N = Counter(); P = Counter(); PN = Counter()
        for l in t['lineas']:
            seq = []
            for it in l:
                if it[0] == 'G': seq.append(None)
                else:
                    seq.append(orden[k] if orden else it); k += 1
            for i, it in enumerate(seq):
                if it and it[0] == 'W':
                    w = it[1]; N[w] += 1; PN[ultimo(w)] += 1
                    antes = i > 0 and seq[i - 1] and seq[i - 1][0] == 'N'; desp = i + 1 < len(seq) and seq[i + 1] and seq[i + 1][0] == 'N'
                    if antes or desp: V[w] += 1
                    if desp: P[ultimo(w)] += 1
        return V, N, P, PN
    V, N, P, PN = Counter(), Counter(), Counter(), Counter()
    for t in textos:
        v, n, p, pn = recuento(t); V += v; N += n; P += p; PN += pn
    G = {w: grupos(w) for w in N}
    tot = {g: sum(N[w] for w in N if g in G[w]) for g in 'QR'}
    obs = {g: sum(V[w] for w in N if g in G[w]) for g in 'QR'}
    prop = lambda v, g: v[g] / tot[g] if tot[g] else 0.0
    difobs = prop(obs, 'Q') - prop(obs, 'R')
    frec = [w for w in N if N[w] >= 3]; fins = [s for s in PN if PN[s] >= 10]
    rnd = generador('t52', 'A'); ge = 0; EV = Counter(); mayor = Counter(); EP = Counter(); mayorP = Counter(); nulQ = 0.0; nulR = 0.0
    planos = [[it for l in t['lineas'] for it in l if it[0] != 'G'] for t in textos]
    for _ in range(PERM):
        Vp = Counter(); Pp = Counter()
        for t, pl in zip(textos, planos):
            o = pl[:]; rnd.shuffle(o); v, _, p, _ = recuento(t, o); Vp += v; Pp += p
        pq = {g: sum(Vp[w] for w in Vp if g in G[w]) for g in 'QR'}
        d = prop(pq, 'Q') - prop(pq, 'R'); nulQ += prop(pq, 'Q'); nulR += prop(pq, 'R')
        if d >= difobs - 1e-12: ge += 1
        for w in frec:
            EV[w] += Vp[w]; mayor[w] += Vp[w] >= V[w]
        for s in fins:
            EP[s] += Pp[s]; mayorP[s] += Pp[s] >= P[s]
    tabla = sorted((dict(forma=w, apariciones=N[w], vecinas=V[w], esperadas=round(EV[w] / PERM, 2),
                         razon=round(V[w] / max(EV[w] / PERM, 1e-9), 2), p=round((1 + mayor[w]) / (PERM + 1), 4)) for w in frec), key=lambda x: (x['p'], -x['vecinas']))
    tablaP = sorted((dict(signo_final=s, palabras=PN[s], ante_numeral=P[s], esperadas=round(EP[s] / PERM, 2),
                          razon=round(P[s] / max(EP[s] / PERM, 1e-9), 2), p=round((1 + mayorP[s]) / (PERM + 1), 4)) for s in fins), key=lambda x: x['p'])
    return dict(textos_con_numerales=len(textos), de_ellos_plomo=sum(t['grupo'] == 'Plomo' for t in textos),
                elementos_numerales=sum(it[0] == 'N' for t in textos for l in t['lineas'] for it in l), palabras=sum(N.values()),
                contraste=dict(Q_apariciones=tot['Q'], Q_vecinas=obs['Q'], Q_prop=round(prop(obs, 'Q'), 3), R_apariciones=tot['R'], R_vecinas=obs['R'],
                               R_prop=round(prop(obs, 'R'), 3), Q_prop_esperada=round(nulQ / PERM, 3), R_prop_esperada=round(nulR / PERM, 3),
                               p_diferencia=round((1 + ge) / (PERM + 1), 4), palabras_en_los_dos_grupos=sum(N[w] for w in N if len(G[w]) == 2),
                               formas_Q=sorted((w, N[w], V[w]) for w in N if 'Q' in G[w]), formas_R=sorted((w, N[w], V[w]) for w in N if 'R' in G[w])),
                formas=tabla, signo_final_ante_numeral=tablaP)

# ------------------------------------------------------------------ 38.B
def parte_B(textos, es_clase, etiqueta, PERM=1000, lmin=3, sin_lagunas=False):
    """Clasificador bayesiano ingenuo: clase de la palabra a partir de la clase del elemento anterior y del siguiente."""
    T = []
    for t in textos:
        if len(palabras(t)) < 4: continue
        lin = []
        for l in t['lineas']:
            lin.append([('G' if it[0] == 'G' else 'N' if it[0] == 'N' else ('C' if len(it[1]) < lmin else None), it[1] if it[0] == 'W' else None) for it in l])
        T.append(lin)
    # objetivos: palabras de lmin letras o más; su etiqueta real
    real = [[es_clase(w) for l in lin for c, w in l if c is None] for lin in T]
    def filas(lin, etiquetas):
        """(clase, contexto anterior, contexto siguiente) de cada objetivo del texto, con las etiquetas dadas."""
        k = 0; out = []; marc = []
        for l in lin:
            fila = []
            for c, w in l:
                if c is None: fila.append('1' if etiquetas[k] else '0'); k += 1
                else: fila.append(c)
            marc.append(fila)
        k = 0
        for l, fila in zip(lin, marc):
            for i, (c, w) in enumerate(l):
                if c is None:
                    out.append((etiquetas[k], fila[i - 1] if i > 0 else 'INI', fila[i + 1] if i + 1 < len(fila) else 'FIN')); k += 1
        return [x for x in out if not (sin_lagunas and 'G' in x[1:])]
    CTX = ['1', '0', 'N', 'G', 'C', 'INI', 'FIN']
    def puntua(etqs):
        F = [filas(lin, e) for lin, e in zip(T, etqs)]
        tot = Counter(); A = Counter(); S = Counter()
        for f in F:
            for y, a, s in f: tot[y] += 1; A[(y, a)] += 1; S[(y, s)] += 1
        pos, neg = [], []
        for f in F:
            lt = Counter(); la = Counter(); ls = Counter()
            for y, a, s in f: lt[y] += 1; la[(y, a)] += 1; ls[(y, s)] += 1
            n1 = tot[True] - lt[True]; n0 = tot[False] - lt[False]
            if n1 == 0 or n0 == 0: continue
            for y, a, s in f:
                lo = math.log(n1 / n0)
                for cnt, loc, x in ((A, la, a), (S, ls, s)):
                    p1 = (cnt[(True, x)] - loc[(True, x)] + 1) / (n1 + len(CTX)); p0 = (cnt[(False, x)] - loc[(False, x)] + 1) / (n0 + len(CTX))
                    lo += math.log(p1 / p0)
                (pos if y else neg).append(lo)
        return auc(pos, neg), len(pos), len(neg)
    a_obs, n1, n0 = puntua(real)
    rnd = generador('t52', 'B', etiqueta); nul = []
    for _ in range(PERM):
        e = []
        for r in real:
            x = r[:]; rnd.shuffle(x); e.append(x)
        nul.append(puntua(e)[0])
    nul = [x for x in nul if x is not None]
    # tabla descriptiva: P(clase positiva | contexto)
    F = [x for lin, e in zip(T, real) for x in filas(lin, e)]
    desc = {}
    for lado, idx in (('anterior', 1), ('siguiente', 2)):
        c = Counter((x[idx], x[0]) for x in F)
        desc[lado] = {k: dict(n=c[(k, True)] + c[(k, False)], prop_clase=round(c[(k, True)] / max(1, c[(k, True)] + c[(k, False)]), 3)) for k in CTX if c[(k, True)] + c[(k, False)]}
    return dict(textos=len(T), objetivos=n1 + n0, de_la_clase=n1, AUC=round(a_obs, 4), AUC_azar_media=round(sum(nul) / len(nul), 4),
                AUC_azar_p95=round(sorted(nul)[int(0.95 * len(nul))], 4), p=round((1 + sum(x >= a_obs for x in nul)) / (len(nul) + 1), 4), contexto=desc)

# ------------------------------------------------------------------ 38.C
def tramos(t):
    """Tramos continuos de palabras unidas por separador escrito: lista de listas de palabras."""
    out = []
    for l in t['lineas']:
        act = []
        for it in l:
            if it[0] == 'W':
                if act and not it[2]: out.append(act); act = []
                act.append(it[1])
            elif act: out.append(act); act = []
        if act: out.append(act)
    return out

def parte_C(textos, etiqueta, unidades=None, K=3, PART=10, BOOT=1000, SORT=10000):
    rnd = generador('t52', 'C', etiqueta)
    TR = [[[SIGNO.findall(w) for w in tr] for tr in tramos(t)] for t in textos]
    idx = list(range(len(textos))); rnd.shuffle(idx); parte = {i: n % PART for n, i in enumerate(idx)}
    def cuenta(ids):
        Fw = [defaultdict(Counter) for _ in range(K + 1)]; Bw = [defaultdict(Counter) for _ in range(K + 1)]
        for i in ids:
            for tr in TR[i]:
                s = [x for w in tr for x in w]
                for p in range(1, len(s)):
                    for k in range(1, K + 1):
                        if p - k >= 0: Fw[k][tuple(s[p - k:p])][s[p]] += 1
                        if p + k <= len(s): Bw[k][tuple(s[p:p + k])][s[p - 1]] += 1
        return Fw, Bw
    def H(c):
        n = sum(c.values()); return -sum(v / n * math.log2(v / n) for v in c.values())
    crudo = []                                           # (texto, tramo, posición, es_frontera, [entropías 2K])
    for f in range(PART):
        Fw, Bw = cuenta([i for i in idx if parte[i] != f])
        for i in idx:
            if parte[i] != f: continue
            for j, tr in enumerate(TR[i]):
                s = [x for w in tr for x in w]; cortes = set(); a = 0
                for w in tr[:-1]: a += len(w); cortes.add(a)
                for p in range(1, len(s)):
                    hs = []
                    for k in range(1, K + 1):
                        c = Fw[k].get(tuple(s[p - k:p])) if p - k >= 0 else None; hs.append(H(c) if c else None)
                    for k in range(1, K + 1):
                        c = Bw[k].get(tuple(s[p:p + k])) if p + k <= len(s) else None; hs.append(H(c) if c else None)
                    crudo.append((i, j, p, p in cortes, hs))
    med = []; des = []
    for d in range(2 * K):
        xs = [r[4][d] for r in crudo if r[4][d] is not None]; m = sum(xs) / len(xs); med.append(m)
        des.append((sum((x - m) ** 2 for x in xs) / len(xs)) ** 0.5 or 1.0)
    punt = {}
    for i, j, p, c, hs in crudo:
        z = [(h - med[d]) / des[d] for d, h in enumerate(hs) if h is not None]
        punt[(i, j, p)] = (sum(z) / len(z) if z else 0.0, c)
    # 1. calibración con los separadores escritos
    por_texto = defaultdict(lambda: ([], []))
    for (i, j, p), (z, c) in punt.items(): por_texto[i][0 if c else 1].append(z)
    con_sep = [i for i in por_texto if por_texto[i][0]]
    pos = [z for i in con_sep for z in por_texto[i][0]]; neg = [z for i in con_sep for z in por_texto[i][1]]
    a = auc(pos, neg); bs = []
    for _ in range(BOOT):
        m = [rnd.choice(con_sep) for _ in con_sep]
        bs.append(auc([z for i in m for z in por_texto[i][0]], [z for i in m for z in por_texto[i][1]]))
    bs = sorted(x for x in bs if x is not None)
    res = dict(textos_con_separadores=len(con_sep), fronteras_con_separador=len(pos), posiciones_interiores=len(neg), AUC=round(a, 4),
               IC95=[round(bs[int(0.025 * len(bs))], 4), round(bs[int(0.975 * len(bs)) - 1], 4)])
    # 2. entidad de palabra de las unidades
    if unidades:
        casos = []                                      # (unidad, palabra, [puntuaciones en bordes], [puntuaciones en todas las interiores])
        for i in idx:
            for j, tr in enumerate(TR[i]):
                base = 0
                for w in tr:
                    for uid, fs in unidades:
                        if len(w) <= len(fs): continue
                        for ini in range(len(w) - len(fs) + 1):
                            if w[ini:ini + len(fs)] != fs: continue
                            bordes = [b for b in (ini, ini + len(fs)) if 0 < b < len(w)]
                            inter = list(range(1, len(w)))
                            if not bordes or len(inter) <= len(bordes): continue
                            casos.append((uid, ''.join(w), [punt[(i, j, base + b)][0] for b in bordes], [punt[(i, j, base + b)][0] for b in inter], tuple(fs)))
                    base += len(w)
        if casos:
            obs = sum(sum(c[2]) / len(c[2]) for c in casos) / len(casos)
            medint = sum(sum(c[3]) / len(c[3]) for c in casos) / len(casos); ge = 0
            for _ in range(SORT):
                v = sum(sum(rnd.sample(c[3], len(c[2]))) / len(c[2]) for c in casos) / len(casos)
                ge += v >= obs - 1e-12
            por_u = defaultdict(list)
            for c in casos: por_u[c[0]].append(sum(c[2]) / len(c[2]) - sum(c[3]) / len(c[3]))
            res['unidades'] = dict(apariciones_dentro_de_palabra=len(casos), unidades_distintas=len(por_u), media_en_bordes=round(obs, 3),
                                   media_en_interiores=round(medint, 3), p=round((1 + ge) / (SORT + 1), 4),
                                   unidades_con_borde_mayor=sum(sum(v) / len(v) > 0 for v in por_u.values()),
                                   por_unidad={u: dict(n=len(v), diferencia_media=round(sum(v) / len(v), 2)) for u, v in sorted(por_u.items())},
                                   ejemplos=sorted({c[1] for c in casos})[:60])
            # --- análisis posterior (no declarado): ¿más que otras cadenas recurrentes de igual longitud y frecuencia?
            formas_u = {tuple(fs) for _, fs in unidades}; CAD = defaultdict(list)
            for i in idx:
                for j, tr in enumerate(TR[i]):
                    base = 0
                    for w in tr:
                        for L in range(2, 6):
                            for ini in range(len(w) - L + 1):
                                if L == len(w): continue
                                bordes = [b for b in (ini, ini + L) if 0 < b < len(w)]; inter = list(range(1, len(w)))
                                if not bordes or len(inter) <= len(bordes): continue
                                CAD[tuple(w[ini:ini + L])].append(sum(punt[(i, j, base + b)][0] for b in bordes) / len(bordes) - sum(punt[(i, j, base + b)][0] for b in inter) / len(inter))
                        base += len(w)
            dif = lambda v: sum(v) / len(v)
            pares = []
            for f in sorted(formas_u):
                if f not in CAD: continue
                n = len(CAD[f]); ctr = [dif(v) for g, v in CAD.items() if g not in formas_u and len(g) == len(f) and n / 1.5 <= len(v) <= n * 1.5 and len(v) >= 2]
                if n >= 2 and len(ctr) >= 5: pares.append((''.join(f), n, dif(CAD[f]), ctr))
            if pares:
                mu = sum(p[2] for p in pares) / len(pares); ge = 0
                for _ in range(SORT):
                    ge += sum(rnd.choice(p[3]) for p in pares) / len(pares) >= mu - 1e-12
                res['unidades']['posterior_frente_a_cadenas_emparejadas'] = dict(
                    formas_con_control=len(pares), media_unidades=round(mu, 3), media_controles=round(sum(dif(p[3]) for p in pares) / len(pares), 3),
                    p=round((1 + ge) / (SORT + 1), 4), unidades_sobre_la_mediana_de_sus_controles=sum(p[2] > sorted(p[3])[len(p[3]) // 2] for p in pares),
                    detalle=[dict(forma=p[0], n=p[1], diferencia=round(p[2], 2), controles=len(p[3]), percentil=round(100 * sum(c < p[2] for c in p[3]) / len(p[3]))) for p in pares])
    return res

# ------------------------------------------------------------------ 38.D
def parte_D(grupos, N=500, BOOT=1000):
    out = {}
    for g, textos in grupos.items():
        W = [[w for w in palabras(t) if len(w) >= 2] for t in textos]; W = [w for w in W if w]
        total = sum(len(w) for w in W)
        if total < N: out[g] = dict(palabras=total, nota='menos de 500 palabras'); continue
        rnd = generador('t52', 'D', g); hap, ttr, pen = [], [], []
        for _ in range(BOOT):
            m = []
            while len(m) < N: m += rnd.choice(W)
            c = Counter(m[:N]); fr = sorted(c.values(), reverse=True)
            hap.append(sum(v == 1 for v in fr) / len(fr)); ttr.append(len(fr) / N)
            xs = [math.log(r + 1) for r in range(len(fr))]; ys = [math.log(v) for v in fr]; mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
            pen.append(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs))
        q = lambda v: [round(sorted(v)[int(p * len(v))], 3) for p in (0.025, 0.5, 0.975)]
        out[g] = dict(inscripciones=len(W), palabras=total, distintas_por_500=q(ttr), hapax_entre_distintas=q(hap), pendiente_zipf=q(pen))
    return out

if __name__ == '__main__':
    ruta = sys.argv[1]; partes = sys.argv[2:] or list('ABCD')
    IB = corpus_iberico(); CE = corpus_celtiberico(ruta)
    sal = os.path.join(os.path.dirname(__file__), '..', 'resultados', 't52_estructura.json')
    res = json.load(open(sal, encoding='utf-8')) if os.path.exists(sal) else {}
    res['lectura'] = dict(iberico_textos=len(IB), iberico_palabras=sum(len(palabras(t)) for t in IB), plomos=sum(t['grupo'] == 'Plomo' for t in IB),
                          plomos_palabras=sum(len(palabras(t)) for t in IB if t['grupo'] == 'Plomo'), celtiberico_textos=len(CE), celtiberico_palabras=sum(len(palabras(t)) for t in CE))
    print(res['lectura'])
    if 'A' in partes:
        res['A'] = parte_A(IB); print('A', {k: v for k, v in res['A'].items() if k not in ('formas', 'signo_final_ante_numeral')})
        for r in res['A']['formas'][:20]: print('  ', r)
        for r in res['A']['signo_final_ante_numeral'][:12]: print('  ', r)
    if 'B' in partes:
        es_nombre = criterio_nombre()
        res['B_iberico_plomos'] = parte_B([t for t in IB if t['grupo'] == 'Plomo'], es_nombre, 'ib'); print('B ib', res['B_iberico_plomos'])
        res['B_celtiberico_kum'] = parte_B(CE, lambda w: len(w) >= 4 and w.endswith('kum'), 'ce', lmin=3); print('B ce', res['B_celtiberico_kum'])
        res['B_posterior_iberico_sin_lagunas'] = parte_B([t for t in IB if t['grupo'] == 'Plomo'], es_nombre, 'ib2', sin_lagunas=True); print('B ib sin lagunas', res['B_posterior_iberico_sin_lagunas'])
    if 'C' in partes:
        U = [(u['id'], SIGNO.findall(_sin_marcas(f))) for u in fuentes.unidades_plomos() for f in u['formas'] if len(_sin_marcas(f)) >= 4]
        U += [(u['id'], SIGNO.findall(_sin_marcas(f))) for u in fuentes.unidades_numerales() for f in u['formas'] if len(_sin_marcas(f)) >= 4]
        res['C_iberico'] = parte_C(IB, 'ib', U); print('C ib', res['C_iberico'])
        res['C_celtiberico'] = parte_C(CE, 'ce'); print('C ce', res['C_celtiberico'])
    if 'D' in partes:
        G = {g: [t for t in IB if t['grupo'] == g] for g in ('Plomo', 'Cerámica', 'Piedra')}; G['Celtibérico'] = CE
        res['D'] = parte_D(G); print('D', json.dumps(res['D'], ensure_ascii=False))
    json.dump(res, open(sal, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
