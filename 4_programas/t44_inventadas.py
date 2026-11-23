"""Declaración 30: prueba con significados frente a palabras inventadas con la fonotaxis del ibérico.

Uso / Usage:  python3 t44_inventadas.py
"""
import json, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import reducida
from ibcomp.distancia import dist
from ibcomp.pruebas import generador

REP = 1000

class Trigramas:
    def __init__(self, formas):
        self.t = defaultdict(Counter)
        for w in formas:
            z = '^^' + w + '$'
            for i in range(2, len(z)): self.t[z[i - 2:i]][z[i]] += 1
    def genera(self, n, rnd, prohibidas, intentos=2000):
        for _ in range(intentos):
            ctx, out = '^^', ''
            while len(out) < n:
                c = {k: v for k, v in self.t[ctx].items() if k != '$'}
                if not c: break
                ks = sorted(c); x = rnd.choices(ks, weights=[c[k] for k in ks])[0]
                out += x; ctx = ctx[1] + x
            if len(out) == n and out not in prohibidas: return out
        raise RuntimeError(f'no se pudo generar una forma de longitud {n}')

def preparar(unidades, dic):
    reg = []
    for u in unidades:
        c = dic.candidatas(u, None)
        if c: reg.append(([reducida(x) for x in u['formas']], sorted(c)))
    return reg

def valor(reg, formas=None):
    fs = formas or [r[0] for r in reg]
    return float(np.mean([min(dist(a, b) for a in f for b in c) for f, (_, c) in zip(fs, reg)]))

if __name__ == '__main__':
    IB = set().union(*[f['formas'] for f in fuentes.hesperia()]); M = Trigramas(sorted(IB))
    conj = {'plomos': fuentes.unidades_plomos(), 'numerales': fuentes.unidades_numerales()}
    dics = fuentes.wikcionario(); res = {}
    for nombre, us in conj.items():
        prohib = {reducida(x) for u in us for x in u['formas']}
        rnd = generador('t44', nombre)
        inventadas = [[[M.genera(len(reducida(x)), rnd, prohib) for x in u['formas']] for u in us] for _ in range(REP)]
        filas = {}
        for lg, d in dics.items():
            idx = [i for i, u in enumerate(us) if d.candidatas(u, None)]
            if len(idx) < max(4, 0.4 * len(us)): continue
            reg = preparar(us, d); real = valor(reg)
            nul = np.array([valor(reg, [inv[i] for i in idx]) for inv in inventadas])
            filas[lg] = dict(unidades=len(idx), real=round(real, 4), inventadas_mediana=round(float(np.median(nul)), 4),
                             ventaja=round(float(np.median(nul) - real), 4), frac_inventadas_menor_o_igual=float((nul <= real).mean()), _nul=nul)
        orden = sorted(filas, key=lambda l: -filas[l]['ventaja'])
        puestos_brutos = [sorted(filas, key=lambda l: filas[l]['_nul'][k]).index('Basque') + 1 for k in range(REP)] if 'Basque' in filas else []
        for l in filas: del filas[l]['_nul']
        res[nombre] = dict(lenguas=len(filas), por_ventaja=[(l, filas[l]) for l in orden], puesto_euskera_por_ventaja=orden.index('Basque') + 1,
                           puesto_euskera_bruto_inventadas=dict(mediana=int(np.median(puestos_brutos)), primero=sum(p == 1 for p in puestos_brutos), de=REP),
                           ejemplo_inventadas=inventadas[0][:8])
        print(f"\n== {nombre}: {len(filas)} lenguas; euskera puesto por ventaja {res[nombre]['puesto_euskera_por_ventaja']}")
        for l in orden[:6]: print(' ', l, filas[l])
        print('  euskera:', filas['Basque']); print('  bruto con inventadas:', res[nombre]['puesto_euskera_bruto_inventadas'])
    e = res['plomos']['por_ventaja']; eu = dict(e)['Basque']; en = dict(res['numerales']['por_ventaja'])['Basque']
    res['previsiones'] = {'1': eu['frac_inventadas_menor_o_igual'] <= 0.01, '2': res['plomos']['puesto_euskera_por_ventaja'] == 1,
                          '3': en['frac_inventadas_menor_o_igual'] <= 0.01}
    print(res['previsiones'])
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't44_inventadas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
