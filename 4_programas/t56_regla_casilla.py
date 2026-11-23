"""Declaración 42: ¿cuánto acierta la regla de la casilla? Calibración en griego a tamaño ibérico.

Regla R: se selecciona toda forma escrita que aparezca al menos dos veces inmediatamente antes de un numeral.
Se aplica a 1.000 pseudocorpus griegos del tamaño de los plomos ibéricos con numerales y se mide qué proporción de las
formas seleccionadas son palabras de contabilidad según la tabla de la etapa 1 (t56_lexico_griego.py).
Uso / Usage:  python3 -I t56_regla_casilla.py RUTA/idp.data [ARCHIVO_CACHE.pkl]
"""
import csv, json, os, random, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from ibcomp import fuentes
from t52_estructura import corpus_iberico
from t54_genero import CLASES, clase_de, letras, n_numerales, ventana
from t55_genero_traslado import lee_ddbdp
from t56_lexico_griego import clasifica

SEMILLA = 42; N = 1000
RES = f'{fuentes.RAIZ}/../resultados'

def casillas(lineas, lado=-1):
    """Palabras inmediatamente antes (lado −1) o después (+1) de un numeral, en la misma línea y sin laguna en medio."""
    out = []
    for l in lineas:
        for j, it in enumerate(l):
            if it[0] != 'N': continue
            k = j + lado
            if 0 <= k < len(l) and l[k][0] == 'W': out.append(l[k])
    return out

def seleccion(textos, lado=-1, dos_textos=False, tope=None, rng=None):
    """Formas seleccionadas por la regla: {forma: (apariciones, textos, proporción con mayúscula)}.

    Con `tope`, se sortean como mucho ese número de casillas ocupadas antes de aplicar la regla (variante igualada en casillas)."""
    n = Counter(); t = defaultdict(set); may = Counter()
    todas = [(i, it) for i, lin in enumerate(textos) for it in casillas(lin, lado)]
    if tope is not None and len(todas) > tope: todas = rng.sample(todas, tope)
    for i, it in todas: n[it[1]] += 1; t[it[1]].add(i); may[it[1]] += bool(it[2])
    return {f: (c, len(t[f]), may[f] / c) for f, c in n.items() if c >= 2 and (not dos_textos or len(t[f]) >= 2)}

def acierto(sel, tabla):
    """Proporción de formas seleccionadas que son M o T (estricto) y M, T o F (amplio), con la tabla publicada y con las reglas."""
    if not sel: return None
    r = Counter()
    for f, (c, nt, may) in sel.items():
        cat_t = tabla.get(f)                                   # solo la tabla publicada (formas con 20 apariciones o más)
        cat_r = clasifica(f, may >= .5)[0]                     # las mismas reglas aplicadas a cualquier forma
        r['estricto_tabla'] += cat_t in ('M', 'T'); r['amplio_tabla'] += cat_t in ('M', 'T', 'F')
        r['estricto_reglas'] += cat_r in ('M', 'T'); r['amplio_reglas'] += cat_r in ('M', 'T', 'F')
        r['nombres'] += cat_r == 'N'
    return {k: r[k] / len(sel) for k in ('estricto_tabla', 'amplio_tabla', 'estricto_reglas', 'amplio_reglas', 'nombres')}

def pseudocorpus(textos, tamanos, rng):
    out = []; orden = rng.sample(range(len(textos)), len(textos)); i = 0
    for obj in tamanos:
        while i < len(orden):
            v = ventana(textos[orden[i]], obj, rng, intentos=3); i += 1
            if v: out.append(v); break
    return out

def resumen(v):
    v = [x for x in v if x is not None]
    if not v: return None
    return dict(mediana=round(float(np.median(v)), 3), p5=round(float(np.percentile(v, 5)), 3), p95=round(float(np.percentile(v, 95)), 3))

def simula(textos, tamanos, tabla, rng, lado=-1, dos_textos=False, tope=None):
    filas = []; ks = []; casi = []
    for _ in range(N):
        pc = pseudocorpus(textos, tamanos, rng); sel = seleccion(pc, lado, dos_textos, tope, rng)
        ks.append(len(sel)); casi.append(sum(len(casillas(l, lado)) for l in pc)); filas.append(acierto(sel, tabla))
    out = dict(formas_seleccionadas=resumen(ks), casillas_ocupadas=resumen(casi), sin_seleccion=sum(f is None for f in filas))
    for k in ('estricto_tabla', 'amplio_tabla', 'estricto_reglas', 'amplio_reglas', 'nombres'):
        out[k] = resumen([f[k] if f else None for f in filas])
    return out, ks, [f['estricto_tabla'] if f else None for f in filas]

def main(raiz, cache=None):
    tabla = {r['forma']: r['categoria'] for r in csv.DictReader(open(f'{RES}/t56_formas_griegas_clasificadas.csv', encoding='utf-8'))}
    IBT = [t for t in corpus_iberico() if n_numerales(t['lineas']) >= 1]
    IBP = [t for t in IBT if t['grupo'] == 'Plomo']
    tam = [letras(t['lineas']) for t in IBP]
    G = [[], [], []]
    for d in lee_ddbdp(raiz, cache):
        c = clase_de(d['terminos'])
        if c is not None and d['gr'] >= .9 and n_numerales(d['lineas']) >= 1: G[c].append(d['lineas'])
    R = dict(declaracion=42, semilla=SEMILLA, repeticiones=N, plomos_con_numeral=len(IBP), textos_ibericos_con_numeral=len(IBT),
             textos_griegos_con_numeral={CLASES[i]: len(G[i]) for i in range(3)})
    print(json.dumps({k: R[k] for k in ('plomos_con_numeral', 'textos_ibericos_con_numeral', 'textos_griegos_con_numeral')}, ensure_ascii=False))
    rng = random.Random(SEMILLA)
    R['prueba_1_cuentas_y_listas'], ks, ac = simula(G[0], tam, tabla, rng)
    print('1.', json.dumps(R['prueba_1_cuentas_y_listas'], ensure_ascii=False))
    sec = {}
    sec['cartas y peticiones'] = simula(G[1], tam, tabla, rng)[0]
    sec['contratos y recibos'] = simula(G[2], tam, tabla, rng)[0]
    sec['cuentas y listas, casilla +1'] = simula(G[0], tam, tabla, rng, lado=+1)[0]
    sec['cuentas y listas, regla de dos textos'] = simula(G[0], tam, tabla, rng, dos_textos=True)[0]
    R['secundaria_2'] = sec
    for k, v in sec.items(): print('2.', k, json.dumps(v, ensure_ascii=False))

    # ---- 3. aplicación al ibérico (descriptiva)
    U = json.load(open(f'{fuentes.RAIZ}/iberico/unidades_plomos.json', encoding='utf-8'))['unidades']
    eq = lambda w: w.replace('g', 'k').replace('d', 't')
    unidad = {eq(f): u['id'] for u in U for f in u['formas']}
    def marca(f):
        if f in ('a', 'o', 'ki'): return 'signo metrológico conocido'
        for u, i in unidad.items():
            if eq(f).startswith(u) or (len(eq(f)) >= 4 and u.startswith(eq(f))): return f'unidad {i}'
        return ''
    ib = {}
    for nombre, T in (('31 plomos', IBP), ('95 textos', IBT)):
        lin = [[[(it[0], it[1], False) if it[0] == 'W' else it for it in l] for l in t['lineas']] for t in T]
        fila = {}
        for lado in (-1, +1):
            sel = seleccion(lin, lado)
            fila[f'casilla {lado:+d}'] = dict(casillas_ocupadas=sum(len(casillas(l, lado)) for l in lin), formas_seleccionadas=len(sel),
                formas=[dict(forma=f, apariciones=c, textos=nt, marca=marca(f)) for f, (c, nt, _) in sorted(sel.items(), key=lambda x: -x[1][0])])
        ib[nombre] = fila
        print('3.', nombre, json.dumps(fila, ensure_ascii=False))
    k_ib = ib['31 plomos']['casilla -1']['formas_seleccionadas']
    ib['comparacion_de_tamano'] = dict(formas_seleccionadas_iberico=k_ib, percentil_en_los_pseudocorpus=round(float(np.mean(np.array(ks) <= k_ib)), 3),
        acierto_estricto_en_pseudocorpus_con_igual_o_menos_formas=resumen([a for a, k in zip(ac, ks) if k <= max(k_ib, 1)]))
    print('3.', json.dumps(ib['comparacion_de_tamano'], ensure_ascii=False))
    R['aplicacion_3_iberico'] = ib

    # ---- añadido no declarado: la comprobación de tamaño falla (el ibérico tiene la mitad de casillas ocupadas que los pseudocorpus),
    # así que se repite la calibración sorteando en cada pseudocorpus tantas casillas ocupadas como tienen los 31 plomos.
    tope = ib['31 plomos']['casilla -1']['casillas_ocupadas']; rng = random.Random(SEMILLA + 1); ig = {}
    for nombre, g, kw in (('cuentas y listas', G[0], {}), ('cuentas y listas, regla de dos textos', G[0], dict(dos_textos=True)),
                          ('cartas y peticiones', G[1], {}), ('contratos y recibos', G[2], {}),
                          ('contratos y recibos, regla de dos textos', G[2], dict(dos_textos=True))):
        ig[nombre] = simula(g, tam, tabla, rng, tope=tope, **kw)[0]
        print('igualada en casillas:', nombre, json.dumps(ig[nombre], ensure_ascii=False))
    R['no_declarado_igualada_en_casillas'] = dict(nota='Añadido después de ver que el ibérico queda fuera del rango de tamaño de los pseudocorpus.',
                                                  casillas_por_pseudocorpus=tope, resultados=ig)
    json.dump(R, open(f'{RES}/t56_regla_casilla.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
