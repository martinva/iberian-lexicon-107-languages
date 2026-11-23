"""Declaración 24: control con el celtibérico y triángulo ibérico–celtibérico–euskera en la prueba de perfil.

Datos: celtibérico de Hesperia en la extracción pública de Martínez-Fernández et al. (arXiv:2604.13070), archivo
src/celtiberian_raw.csv del repositorio gonmarfer2/palaeohispanic-dataset-generator, commit 789d03e (2-3-2026).
Se excluyen las fichas marcadas en la sigla como FALSA, SUSPECTA o LATINA. Tokenización y reducción idénticas a las
del ibérico (fuentes.hesperia y clases.red_ib); 107 lenguas de NorthEuraLex; mismas funciones que t08_perfil.py.

Uso / Usage:  python3 t38_celtiberico.py RUTA/celtiberian_raw.csv
"""
import csv, json, os, re, sys, unicodedata
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import red_ib, proyecta
from ibcomp.pruebas import perfil, divergencia, generador

CELTICAS = {'Welsh', 'Breton', 'Irish', 'Scottish Gaelic'}
LMIN, LMAX = 2, 12

def formas_celtibericas(ruta, z_a_s=False):
    csv.field_size_limit(10 ** 9)
    filas = list(csv.DictReader(open(ruta, encoding='utf-8'), delimiter=';'))
    autenticas = [r for r in filas if not re.search('FALSA|SUSPECTA|LATINA', r['refHesperia'])]
    formas = set(); palabras = 0
    for r in autenticas:
        texto = unicodedata.normalize('NFC', re.sub(r'[\[\]\(\)\+\-\?̲̱̣]', '', r['texto'])).lower()
        for t in re.split(r'[^\wśŕḿ]+', texto):                       # mismo corte que fuentes.hesperia()
            if not t or re.search(r'\d|[ivxlπ]{3,}', t): continue
            x = red_ib(t.replace('z', 's') if z_a_s else t)
            if LMIN <= len(x) <= LMAX: formas.add(x); palabras += 1
    return dict(fichas=len(filas), autenticas=len(autenticas), palabras=palabras, formas=formas)

def tabla(ws, P, nombres):
    q = perfil(ws)
    return sorted((round(divergencia(q, P[l]), 4), nombres[l]) for l in P)

def analiza(etiqueta, P, nombres, familia, cel, ib, remuestreos=500):
    o = tabla(cel, P, nombres); top5 = o[:5]
    fam = {nombres[l]: familia[l] for l in P}
    rnd = generador('t38', etiqueta); ws = sorted(cel); prim = Counter()
    for _ in range(remuestreos):
        p1 = perfil([rnd.choice(ws) for _ in ws]); prim[fam[min((divergencia(p1, P[m]), nombres[m]) for m in P)[1]]] += 1
    eus = [n for d, n in o].index('Basque') + 1
    d_cel_eus = next(d for d, n in o if n == 'Basque')
    oib = tabla(ib, P, nombres); d_ib_eus = next(d for d, n in oib if n == 'Basque')
    d_ib_cel = round(divergencia(perfil(ib), perfil(cel)), 4)
    puesto_cel_desde_ib = 1 + sum(d < d_ib_cel for d, n in oib)
    r = dict(formas_celtibericas=len(cel), primeras_10=[(n, d, fam[n]) for d, n in o[:10]],
             p1_mas_proxima_indoeuropea=fam[o[0][1]] == 'Indo-European',
             p1_celtica_entre_5=any(n in CELTICAS for d, n in top5),
             indoeuropea_entre_5=any(fam[n] == 'Indo-European' for d, n in top5),
             puesto_euskera_desde_celtiberico=eus, div_celtiberico_euskera=d_cel_eus, div_iberico_euskera=d_ib_eus,
             p3_euskera_fuera_de_5_y_mas_lejos=(eus > 5 and d_cel_eus > d_ib_eus),
             div_iberico_celtiberico=d_ib_cel, puesto_celtiberico_entre_107_desde_iberico=puesto_cel_desde_ib,
             primeras_5_desde_iberico=[(n, d) for d, n in oib[:5]],
             remuestreo_familia_de_la_primera=dict(prim), remuestreos=remuestreos)
    print(f'\n===== {etiqueta}: celtibérico ({len(cel)} formas)')
    for k, v in r.items(): print(f'  {k}: {v}')
    return r

if __name__ == '__main__':
    ruta = sys.argv[1]
    LEX, lang = fuentes.northeuralex(); nombres = {l: lang[l]['Name'] for l in LEX}; familia = {l: lang[l].get('Family') or '' for l in LEX}
    fichas = fuentes.hesperia(); IB = set().union(*[f['formas'] for f in fichas])
    C = formas_celtibericas(ruta); Cz = formas_celtibericas(ruta, z_a_s=True)
    print(f"Celtibérico: {C['fichas']} fichas, {C['autenticas']} auténticas, {C['palabras']} palabras, {len(C['formas'])} formas distintas")
    P = {l: perfil(ws) for l, ws in LEX.items()}
    Pr = {l: perfil(proyecta(ws)) for l, ws in LEX.items()}
    res = dict(datos={k: v for k, v in C.items() if k != 'formas'}, fuente='gonmarfer2/palaeohispanic-dataset-generator@789d03e src/celtiberian_raw.csv')
    res['clases completas'] = analiza('clases completas', P, nombres, familia, C['formas'], IB)
    res['reducidas'] = analiza('lenguas reducidas a lo que anota el signario', Pr, nombres, familia, proyecta(C['formas']), proyecta(IB))
    res['variante z->S, clases completas'] = analiza('variante z->S (sensibilidad)', P, nombres, familia, Cz['formas'], IB)
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't38_celtiberico.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
