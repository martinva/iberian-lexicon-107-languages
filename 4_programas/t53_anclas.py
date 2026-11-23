"""Declaración 39: anclas seguras (signos numerales, numerales léxicos y śalir) como referencia de las casillas.

Uso / Usage:  python3 t53_anclas.py
"""
import csv, json, os, re, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.pruebas import generador
from t52_estructura import corpus_iberico, _sin_marcas

EQ = lambda w: w.replace('g', 'k').replace('d', 't')
NUMS = ['ban', 'bin', 'bi', 'iŕur', 'irur', 'lauŕ', 'laur', 'borste', 'bors', 'śei', 'sisbi', 'sorse', 'abaŕ', 'oŕkei', 'okei']   # g = k
EXACTAS = {'abaŕ', 'lauŕ', 'laur', 'borste', 'sisbi', 'sorse', 'oŕkei', 'okei'}
PERM = 10000

def numeral_lexico(w):
    w = EQ(w)
    if w in EXACTAS: return True
    def comps(s):                                   # mayor número de formas numerales seguidas al principio de s
        mejor = 0
        for f in NUMS:
            if s.startswith(f):
                r = s[len(f):]; mejor = max(mejor, 1 + max(comps(r), comps(r[2:]) if r.startswith('ke') else 0))
        return mejor
    return comps(w) >= 2

def es_salir(w): return w.startswith('śalir') or w.endswith('śalir')

if __name__ == '__main__':
    U = fuentes.unidades_plomos(); QP = {'A2', 'A3', 'A5', 'A6', 'A16'}
    def unidades_de(w):
        out = set()
        for u in U:
            if u['id'] == 'A1': continue
            for f in u['formas']:
                f = _sin_marcas(f)
                if (w == f) if len(f) < 4 else (w.startswith(f) or w.endswith(f)): out.add(u['id'])
        return out
    IB = corpus_iberico()
    def tipo(it):                                   # 'S' signo numeral, 'L' numeral léxico, 'A' palabra con śalir, 'W' otra palabra
        if it[0] == 'N': return 'S'
        if numeral_lexico(it[1]): return 'L'
        return 'A' if es_salir(it[1]) else 'W'
    textos = []
    for t in IB:
        lin = [[None if it[0] == 'G' else (tipo(it), it[1] if it[0] == 'W' else None) for it in l] for l in t['lineas']]
        if any(x and x[0] in 'SLA' for l in lin for x in l): textos.append((t, lin))
    lex = Counter(x[1] for _, lin in textos for l in lin for x in l if x and x[0] == 'L')
    UD = {}
    def mide(lineas):
        """por unidad: apariciones y apariciones con otra ancla en la línea; además vecindad inmediata de las palabras con śalir."""
        n = Counter(); c = Counter(); sal = [0, 0]
        for l in lineas:
            anc = sum(1 for x in l if x and x[0] in 'SLA')
            for i, x in enumerate(l):
                if not x or x[1] is None: continue
                if x[1] not in UD: UD[x[1]] = unidades_de(x[1])
                propia = x[0] in 'LA'
                for u in UD[x[1]]:
                    n[u] += 1; c[u] += (anc - propia) > 0
                if x[0] == 'A':
                    sal[1] += 1
                    sal[0] += any(0 <= j < len(l) and l[j] and l[j][0] in 'SL' for j in (i - 1, i + 1))
        return n, c, sal
    N, C, SAL = Counter(), Counter(), [0, 0]
    for _, lin in textos:
        n, c, s = mide(lin); N += n; C += c; SAL[0] += s[0]; SAL[1] += s[1]
    grupo = lambda u: 'Q' if u in QP else 'R'
    def props(n, c):
        t = Counter(); k = Counter()
        for u in n: t[grupo(u)] += n[u]; k[grupo(u)] += c[u]
        return {g: (k[g] / t[g] if t[g] else 0.0) for g in 'QR'}, t, k
    po, to, ko = props(N, C); difobs = po['Q'] - po['R']
    rnd = generador('t53', 'anclas'); ge = 0; EC = Counter(); may = Counter(); nq = nr = 0.0; salge = 0; salesp = 0.0
    for _ in range(PERM):
        Np, Cp, Sp = Counter(), Counter(), [0, 0]
        for _, lin in textos:
            plano = [x for l in lin for x in l if x]; rnd.shuffle(plano); k = 0; nuevo = []
            for l in lin:
                fila = []
                for x in l:
                    if x is None: fila.append(None)
                    else: fila.append(plano[k]); k += 1
                nuevo.append(fila)
            n, c, s = mide(nuevo); Np += n; Cp += c; Sp[0] += s[0]; Sp[1] += s[1]
        pp, _, _ = props(Np, Cp); nq += pp['Q']; nr += pp['R']
        ge += (pp['Q'] - pp['R']) >= difobs - 1e-12
        for u in N: EC[u] += Cp[u]; may[u] += Cp[u] >= C[u]
        salesp += Sp[0]; salge += Sp[0] >= SAL[0]
    glosa = {u['id']: (u['formas'][0], u['glosa']) for u in U}
    tabla = sorted((dict(unidad=u, forma=glosa[u][0], grupo=grupo(u), apariciones=N[u], con_ancla_en_la_linea=C[u], esperadas=round(EC[u] / PERM, 2),
                         p=round((1 + may[u]) / (PERM + 1), 4)) for u in N), key=lambda x: x['p'])
    # 39.2c: puntuación de borde de la 38.C por grado
    grado = {}
    for r in csv.DictReader(open(f'{fuentes.RAIZ}/iberico/cldf/forms.csv', encoding='utf-8')): grado[r['Parameter_ID']] = r['Grado']
    t52 = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't52_estructura.json'), encoding='utf-8'))
    pu = t52['C_iberico']['unidades']['por_unidad']; porg = defaultdict(list)
    for u, d in pu.items(): porg['A' if grado.get(u) == 'A' else 'resto'].append((u, d['n'], d['diferencia_media']))
    res = dict(textos_con_ancla=len(textos), signos_numerales=sum(x[0] == 'S' for _, lin in textos for l in lin for x in l if x),
               numerales_lexicos=dict(apariciones=sum(lex.values()), palabras=sorted(lex.items())), palabras_con_salir=SAL[1],
               contraste=dict(Qp_apariciones=to['Q'], Qp_con_ancla=ko['Q'], Qp_prop=round(po['Q'], 3), R_apariciones=to['R'], R_con_ancla=ko['R'], R_prop=round(po['R'], 3),
                              Qp_prop_esperada=round(nq / PERM, 3), R_prop_esperada=round(nr / PERM, 3), p_diferencia=round((1 + ge) / (PERM + 1), 4)),
               por_unidad=tabla,
               control_positivo_salir=dict(palabras=SAL[1], junto_a_numeral=SAL[0], esperadas=round(salesp / PERM, 2), p=round((1 + salge) / (PERM + 1), 4)),
               borde_38C_por_grado={g: dict(unidades=v, media_ponderada=round(sum(n * d for _, n, d in v) / sum(n for _, n, _ in v), 3),
                                            con_diferencia_positiva=f"{sum(d > 0 for _, _, d in v)} de {len(v)}") for g, v in porg.items()})
    for k, v in res.items():
        if k != 'por_unidad': print(k, json.dumps(v, ensure_ascii=False))
    for r in tabla: print('  ', r)
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't53_anclas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
