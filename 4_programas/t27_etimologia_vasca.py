"""Declaración 11: origen etimológico y fonotaxis de las palabras vascas emparejadas con las unidades ibéricas.

(1) Clasificación de cada lema vasco del Wikcionario inglés por su nota etimológica (préstamo / heredado / desconocido /
    sin dato), con reglas fijas publicadas aquí.
(2) Para cada unidad (30 de los plomos y 10 numerales) con candidatas en el Wikcionario vasco, la candidata a menor
    distancia (como t25) y su clase etimológica.
(3) Proporción de préstamos entre esas candidatas frente a dos referencias: todas las candidatas vascas de los mismos
    significados, y todos los lemas con nota. Hipergeométrica y 10.000 sorteos de una candidata al azar por unidad.
(4) Control positivo: las cuatro unidades propuestas como préstamos latinos deben emparejar con préstamos.
(5) Fonotaxis (Miller y otros 2020, variante mínima): trigramas de clases con Kneser–Ney sobre heredados y sobre
    préstamos; diferencia de entropía por segmento; validación cruzada de 10 pliegues; clasificación de las candidatas.
Versión 2 (21-11-2026, tras la auditoría de la fase 4e): (a) la etimología se enlaza por LEMA cuya glosa hace
elegible la candidata para la unidad, no por la forma reducida (que puede mezclar lemas distintos, p. ej. *biga* y
*pika*); (b) el préstamo se desglosa por donante (romance/latín frente a árabe u otro), porque la pregunta es la
fuente latina o romance común; (c) la hipergeométrica y los sorteos usan las mismas unidades que el observado;
(d) la fonotaxis añade la clasificación FUERA DE MUESTRA (modelos entrenados sin las formas candidatas). Las salidas
de la versión 1 se conservan como `t27_etimologia_vasca_v1_*.json/.log`.
Uso / Usage:  python3 t27_etimologia_vasca.py [amplia]

Con `amplia` (comprobación POSTERIOR a la declaración, añadida tras ver el resultado y señalada como tal): la regla de
«préstamo» admite además cualquier nota que contenga «borrowed from» en cualquier posición, o «Derived/Adapted from»
seguido de una lengua donante, o «Probably/Possibly/Ultimately/Perhaps from» seguido de una lengua donante. Con la
regla declarada, 406 notas de ese tipo quedaban en «desconocido». Salida: t27_etimologia_vasca_amplia.json.
"""
import csv, json, math, os, re, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import reducida
from ibcomp.distancia import dist
from ibcomp.pruebas import generador
from ibcomp.normalizadores import NORM

AQUI = os.path.dirname(__file__); RAIZ = os.path.join(AQUI, '..', '1_fuentes_lexicas')
SORTEOS = 10000
AMPLIA = 'amplia' in sys.argv[1:]
DONANTES = r'(Spanish|Old Spanish|Latin|Late Latin|Vulgar Latin|Medieval Latin|French|Old French|Occitan|Old Occitan|Gascon|Aragonese|Navarro-Aragonese|Romance|Arabic|English|Italian|Catalan|Galician|Portuguese)'

def clase_etimologica(nota):
    """Regla fija: préstamo / heredado / desconocido / sin dato (véase la declaración 11)."""
    n = nota.strip()
    if not n: return 'sin dato'
    if re.match(r'^(Borrowed from|Borrowing from|Loanword from)\b', n) or re.match(r'^From ' + DONANTES + r'\b', n) or re.match(r'^(Derived|Adapted) from ' + DONANTES + r'\b', n): return 'préstamo'
    if AMPLIA and (re.search(r'\b[Bb]orrowed from\b', n) or re.search(r'(Derived|Adapted) from ' + DONANTES, n) or re.match(r'^(Probably|Possibly|Ultimately|Perhaps) from ' + DONANTES, n)): return 'préstamo'
    if 'Proto-Basque' in n or re.match(r'^Inherited from', n): return 'heredado'
    return 'desconocido'

DONANTE_ROMANCE = re.compile(r'(Spanish|Latin|French|Occitan|Gascon|Aragonese|Romance|Catalan|Galician|Portuguese|Italian)')

def donante(nota):
    """Para una nota clasificada como préstamo: 'romance/latín' si nombra una lengua romance o el latín; 'otro' si no (árabe, inglés…)."""
    return 'romance/latín' if DONANTE_ROMANCE.search(nota) else 'otro'

def lemas_con_nota():
    """forma reducida → lista de (lema, clase, menciona_iberico, términos de la glosa, donante)."""
    from ibcomp.fuentes import terminos_de_glosa
    out = defaultdict(list)
    for r in csv.DictReader(open(os.path.join(RAIZ, 'wikcionario', 'wikcionario_eu_en_v1.csv'), encoding='utf-8')):
        w = r['lema'].lower()
        if ' ' in w or not w.isalpha(): continue
        f = reducida(NORM['Basque'](w))
        if not f: continue
        c = clase_etimologica(r['etimologia'])
        out[f].append((w, c, 'Iberian' in r['etimologia'], frozenset(terminos_de_glosa(r['glosa_en'])), donante(r['etimologia']) if c == 'préstamo' else ''))
    return out

def clase_de_forma(ls):
    """Clase de una lista de entradas (lema, clase, …): préstamo si alguna lo es y ninguna es heredada; heredado si alguna lo es; si hay conflicto, 'mixto'."""
    cs = {e[1] for e in ls}
    if 'heredado' in cs and 'préstamo' in cs: return 'mixto'
    for c in ('heredado', 'préstamo', 'desconocido'):
        if c in cs: return c
    return 'sin dato'

# ---- fonotaxis: trigramas con Kneser–Ney (interpolado, un solo descuento) sobre clases de sonidos
class KN:
    def __init__(self, formas, d=0.75):
        self.d = d; self.tri = Counter(); self.bi = Counter(); self.uni = Counter(); self.cont = defaultdict(set); self.cont1 = defaultdict(set); self.ctx = Counter(); self.tipos = defaultdict(set)
        for f in formas:
            s = ['<', '<'] + list(f) + ['>']
            for i in range(2, len(s)):
                a, b, c = s[i - 2], s[i - 1], s[i]
                self.tri[(a, b, c)] += 1; self.ctx[(a, b)] += 1; self.tipos[(a, b)].add(c)
                self.cont[(b, c)].add(a); self.cont1[c].add(b); self.uni[c] += 1
        self.bi_cont = Counter({k: len(v) for k, v in self.cont.items()}); self.bictx = Counter()
        for (b, c), n in self.bi_cont.items(): self.bictx[b] += n
        self.tipos_bi = Counter(b for (b, c) in self.bi_cont)
        self.uni_cont = Counter({c: len(v) for c, v in self.cont1.items()}); self.total_cont = sum(self.uni_cont.values()); self.V = len(self.uni) + 1
    def p_uni(self, c): return (self.uni_cont.get(c, 0) + 0.5) / (self.total_cont + 0.5 * self.V)
    def p_bi(self, b, c):
        n = self.bictx.get(b, 0)
        if n == 0: return self.p_uni(c)
        t = self.tipos_bi.get(b, 0)
        return max(self.bi_cont.get((b, c), 0) - self.d, 0) / n + self.d * t / n * self.p_uni(c)
    def p(self, a, b, c):
        n = self.ctx.get((a, b), 0)
        if n == 0: return self.p_bi(b, c)
        return max(self.tri.get((a, b, c), 0) - self.d, 0) / n + self.d * len(self.tipos[(a, b)]) / n * self.p_bi(b, c)
    def entropia(self, f):
        s = ['<', '<'] + list(f) + ['>']; return -sum(math.log2(self.p(s[i - 2], s[i - 1], s[i])) for i in range(2, len(s))) / (len(s) - 2)

if __name__ == '__main__':
    L = lemas_con_nota(); res = {'regla': 'amplia (posterior)' if AMPLIA else 'declarada'}
    print('Regla de clasificación:', res['regla'])
    # (1) recuento
    todas = [(f, clase_de_forma(ls)) for f, ls in L.items()]
    rec = Counter(c for _, c in todas); res['recuento_formas'] = dict(rec); print('Formas vascas con nota, por clase:', dict(rec)); print('(5.513 registros con nota en el archivo; los lemas distintos en minúsculas son menos: véase LEEME_fuentes)')
    # (2) candidatas emparejadas: la clase se decide SOLO con los lemas elegibles (su glosa contiene un término de la unidad)
    U = fuentes.unidades_plomos() + fuentes.unidades_numerales(); B = fuentes.wikcionario()['Basque']
    PREST_LAT = set(fuentes.PRESTAMOS_LATINOS)   # bale, koŕta, saltu, oŕtin
    def elegibles(forma, T):
        return [e for e in L.get(forma, []) if e[3] & T]
    filas = []; cands_ref = []
    for u in U:
        c = B.candidatas(u, 'terminos_en')
        if not c: continue
        T = frozenset(u.get('terminos_en') or [])
        f = reducida(u['formas'][0]); mejor = min(sorted(c), key=lambda x: dist(f, x))
        clases_c = [clase_de_forma(elegibles(x, T)) if elegibles(x, T) else 'sin dato' for x in sorted(c)]
        ls = elegibles(mejor, T)
        don = sorted({e[4] for e in ls if e[1] == 'préstamo' and e[4]})
        filas.append(dict(id=u['id'], iberico=u['formas'][0], candidata=mejor, lemas=sorted({e[0] for e in ls}), clase=clase_de_forma(ls) if ls else 'sin dato', donante=' y '.join(don), menciona_iberico=any(e[2] for e in ls), distancia=round(dist(f, mejor), 3), candidatas=len(c), prestamos_entre_candidatas=sum(x == 'préstamo' for x in clases_c), candidatas_con_dato=sum(x not in ('sin dato',) for x in clases_c), clases_candidatas=clases_c))
    res['emparejadas'] = [dict((k2, v2) for k2, v2 in r.items() if k2 != 'clases_candidatas') for r in filas]
    con_dato = [r for r in filas if r['clase'] != 'sin dato']; k = sum(r['clase'] == 'préstamo' for r in con_dato); n = len(con_dato)
    k_rom = sum(r['clase'] == 'préstamo' and 'romance/latín' in r['donante'] for r in con_dato)
    print(f"\nUnidades con candidata: {len(filas)}; con nota etimológica (lemas elegibles): {n}; emparejadas con préstamo: {k} (romance/latín: {k_rom}); heredado: {sum(r['clase'] == 'heredado' for r in con_dato)}; desconocido: {sum(r['clase'] == 'desconocido' for r in con_dato)}; mixto: {sum(r['clase'] == 'mixto' for r in con_dato)}; con mención del ibérico en la nota: {sum(r['menciona_iberico'] for r in filas)}")
    for r in filas: print(f"   {r['id']:4s} {r['iberico']:10s} → {r['candidata']:10s} {','.join(r['lemas'])[:28]:28s} {r['clase']:12s}{(' ['+r['donante']+']') if r['donante'] else '':16s} d={r['distancia']} candidatas {r['candidatas']} (préstamos {r['prestamos_entre_candidatas']}/{r['candidatas_con_dato']})")
    # (3) referencias, sobre las MISMAS unidades que el observado (las de candidata con nota)
    ref_sig = sum(r['prestamos_entre_candidatas'] for r in con_dato) / max(1, sum(r['candidatas_con_dato'] for r in con_dato))
    ref_lex = rec.get('préstamo', 0) / max(1, sum(v for c, v in rec.items() if c != 'sin dato'))
    K = sum(r['prestamos_entre_candidatas'] for r in con_dato); N = sum(r['candidatas_con_dato'] for r in con_dato)
    from math import comb
    p_hip = sum(comb(K, i) * comb(N - K, n - i) for i in range(k, min(K, n) + 1)) / comb(N, n) if N >= n and K <= N else None
    p_hip_menor = sum(comb(K, i) * comb(N - K, n - i) for i in range(0, k + 1)) / comb(N, n) if N >= n and K <= N else None
    rnd = generador('etimologia', 'sorteo'); S = []
    for _ in range(SORTEOS):
        tot = 0
        for r in con_dato:
            cl = [x for x in r['clases_candidatas'] if x != 'sin dato']
            if cl and rnd.choice(cl) == 'préstamo': tot += 1
        S.append(tot)
    p_sorteo = sum(x >= k for x in S) / SORTEOS
    res['referencia'] = dict(prestamos_emparejadas=k, prestamos_romance_latin=k_rom, emparejadas_con_dato=n, proporcion=k / n if n else None, proporcion_candidatas_mismos_significados=ref_sig, proporcion_lexico_con_nota=ref_lex, p_hipergeometrica_mayor_o_igual=p_hip, p_hipergeometrica_menor_o_igual=p_hip_menor, sorteos=SORTEOS, p_sorteo_mayor_o_igual=p_sorteo, media_sorteo=float(np.mean(S)))
    print(f"\nProporción de préstamos: emparejadas {k}/{n} = {k / n if n else float('nan'):.3f} (romance/latín {k_rom}/{n}); candidatas de los mismos significados (mismas unidades) {ref_sig:.3f}; léxico con nota {ref_lex:.3f}; hipergeométrica p(≥k) {p_hip} y p(≤k) {p_hip_menor}; sorteo de una candidata por unidad (mismas unidades): media {np.mean(S):.2f}, p(≥k) {p_sorteo:.4f}")
    # (4) control
    res['control_latinos'] = {r['iberico']: dict(candidata=r['candidata'], lemas=r['lemas'], clase=r['clase'], donante=r['donante']) for r in filas if r['iberico'] in PREST_LAT}; print('Control, unidades propuestas como préstamos latinos:', res['control_latinos'])
    # (5) fonotaxis
    her = [f for f, c in todas if c == 'heredado']; pre = [f for f, c in todas if c == 'préstamo']
    rnd2 = generador('etimologia', 'pliegues'); idx_h = list(range(len(her))); idx_p = list(range(len(pre))); rnd2.shuffle(idx_h); rnd2.shuffle(idx_p)
    ok_h = ok_p = 0
    for pl in range(10):
        th = {her[i] for j, i in enumerate(idx_h) if j % 10 == pl}; tp = {pre[i] for j, i in enumerate(idx_p) if j % 10 == pl}
        mh = KN([f for f in her if f not in th]); mp = KN([f for f in pre if f not in tp])
        ok_h += sum(mh.entropia(f) <= mp.entropia(f) for f in th); ok_p += sum(mp.entropia(f) < mh.entropia(f) for f in tp)
    objetivo = {r['candidata'] for r in filas}
    mh = KN([f for f in her if f not in objetivo]); mp = KN([f for f in pre if f not in objetivo])   # FUERA DE MUESTRA: sin las formas candidatas
    clasif = {r['id']: ('préstamo' if mp.entropia(r['candidata']) < mh.entropia(r['candidata']) else 'heredado') for r in filas}
    mh_t = KN(her); mp_t = KN(pre)                                                                  # con todo (versión 1, se publica como comparación)
    clasif_t = {r['id']: ('préstamo' if mp_t.entropia(r['candidata']) < mh_t.entropia(r['candidata']) else 'heredado') for r in filas}
    res['fonotaxis'] = dict(heredados=len(her), prestamos=len(pre), acierto_heredados_cv=ok_h / len(her), acierto_prestamos_cv=ok_p / len(pre),
                            clasificacion_emparejadas_fuera_de_muestra=clasif, emparejadas_como_prestamo_fuera_de_muestra=sum(v == 'préstamo' for v in clasif.values()),
                            emparejadas_como_prestamo_con_todo=sum(v == 'préstamo' for v in clasif_t.values()), emparejadas=len(clasif))
    print(f"\nFonotaxis: modelos sobre {len(her)} heredados y {len(pre)} préstamos; validación cruzada: acierto heredados {ok_h / len(her):.3f}, préstamos {ok_p / len(pre):.3f}; emparejadas como préstamo FUERA DE MUESTRA: {res['fonotaxis']['emparejadas_como_prestamo_fuera_de_muestra']} de {len(clasif)} (con las candidatas en el entrenamiento, versión 1: {res['fonotaxis']['emparejadas_como_prestamo_con_todo']})")
    json.dump(res, open(os.path.join(AQUI, '..', 'resultados', 't27_etimologia_vasca_amplia.json' if AMPLIA else 't27_etimologia_vasca.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
