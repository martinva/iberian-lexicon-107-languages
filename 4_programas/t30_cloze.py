"""Declaración 14: prueba de cloze con modelos primados como hablantes (segundo artículo; control de memoria).

Fase 1 (`preparar`): escribe las fichas del cloze (las 36 fichas despojadas de la declaración 13, sin candidatos, con
la indicación de que el término está tachado) en `2_criterios/jurado/cloze/FICHAS_cloze.md`, y los tres encargos
(primado euskera / primado gallego / sin primar) en `ENCARGO_cloze_{A,B,C}.md`.
Fase 2 (`puntuar`): lee las respuestas (`respuestas/<juez>_<condicion>.tsv`: codigo, forma) y puntúa: distancia del
estudio entre la forma propuesta (reducida con el normalizador de la lengua primada; en la condición C, el vasco) y la
forma ibérica real, frente a 1.000 palabras al azar de esa lengua y de la misma longitud (generador `cloze|azar|<id>`;
en C se usa también el diccionario vasco como referencia, decisión anotada: la declaración no fijaba referencia para C).
Se da el percentil por unidad y la proporción de unidades bajo la mediana del azar, con y sin numerales y sin las
unidades cuya nota del Wikcionario menciona el ibérico (entrada 11).
Uso / Usage:  python3 t30_cloze.py preparar | puntuar
"""
import csv, json, math, os, re, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import reducida
from ibcomp.distancia import dist
from ibcomp.pruebas import generador
from ibcomp.normalizadores import NORM
from t28_prediccion_prospectiva import fichas_unidades

AQUI = os.path.dirname(__file__); RAIZ = os.path.join(AQUI, '..'); SAL = os.path.join(RAIZ, '2_criterios', 'jurado', 'cloze')
MENCIONAN_IBERICO = {'A2', 'A19', 'A30', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N10', 'N20'}  # t27, nota del Wikcionario

PRIMADOS = {
 'A': "Eres un hablante nativo de euskera, historiador de la economía antigua. Una lengua antigua no descifrada, conservada en textos económicos breves, podría estar relacionada con la tuya.",
 'B': "Eres un hablante nativo de gallego, historiador de la economía antigua. Una lengua antigua no descifrada, conservada en textos económicos breves, podría estar relacionada con la tuya.",
 'C': "Eres un historiador de la economía antigua. Trabajas sobre una lengua antigua no descifrada, conservada en textos económicos breves.",
}
COMUN = """A continuación tienes 36 fichas. Cada una describe la distribución de un término de esa lengua antigua cuyo texto está tachado y no puede leerse. Para cada ficha, propón la forma más probable del término TAL COMO SONARÍA EN LA LENGUA ANTIGUA: una sola palabra, en letras latinas minúsculas, sin espacios. Guíate por lo que la distribución te sugiera del significado{y}.

Formato de la respuesta: una tabla con dos columnas (código, forma propuesta). No añadas nada más."""

def preparar():
    os.makedirs(SAL, exist_ok=True)
    F = fichas_unidades()
    with open(os.path.join(SAL, 'FICHAS_cloze.md'), 'w', encoding='utf-8') as g:
        g.write('# Fichas del cloze (declaración 14)\n\nLas 36 fichas despojadas de la declaración 13, sin candidatos. El término está tachado.\n\n| Código | Tipo | Distribución |\n|---|---|---|\n')
        for cod, tipo, texto, _ in F: g.write(f'| {cod} | {tipo} | {texto} |\n')
    for c, pr in PRIMADOS.items():
        extra = ' y, si te ayuda, por cómo nombra tu lengua esas realidades' if c in 'AB' else ''
        open(os.path.join(SAL, f'ENCARGO_cloze_{c}.md'), 'w', encoding='utf-8').write(f'# Encargo cloze, condición {c}\n\n{pr}\n\n{COMUN.replace("{y}", extra)}\n')
    print('fichas', len(F))

def puntuar():
    U = {u['id']: u for u in fuentes.unidades_plomos() + fuentes.unidades_numerales()}
    # la correspondencia código→unidad se toma de la clave de la entrada 7
    cl7 = {r['código']: r['unidad'] for r in csv.DictReader(open(os.path.join(RAIZ, '2_criterios', 'jurado', 'respuestas', 'CLAVE.tsv'), encoding='utf-8'), delimiter='\t')}
    W = fuentes.wikcionario(); DIC = {'A': ('Basque', W['Basque']), 'B': ('Galician', W['Galician']), 'C': ('Basque', W['Basque'])}
    res = {}
    for p in sorted(os.listdir(os.path.join(SAL, 'respuestas'))):
        if not p.endswith('.tsv'): continue
        juez, cond = p[:-4].rsplit('_', 1); lengua, d = DIC[cond]
        por_lon = defaultdict(list)
        for f in d.formas: por_lon[len(f)].append(f)
        filas = []; bajo = 0; n = 0
        for r in csv.DictReader(open(os.path.join(SAL, 'respuestas', p), encoding='utf-8'), delimiter='\t'):
            uid = cl7[r['codigo']]; real = reducida(U[uid]['formas'][0])
            prop = reducida(NORM[lengua](r['forma'].strip().lower()))
            if not prop: continue
            rnd = generador('cloze', 'azar', r['codigo']); cand = por_lon.get(len(prop)) or d.formas
            azar = sorted(dist(real, rnd.choice(cand)) for _ in range(1000))
            dd = dist(real, prop); perc = sum(a < dd for a in azar) / 10  # percentil en %
            med = azar[500]; n += 1; bajo += dd < med
            filas.append(dict(codigo=r['codigo'], unidad=uid, propuesta=r['forma'], reducida=prop, distancia=round(dd, 3), percentil=round(perc, 1), bajo_mediana=dd < med, numeral=uid.startswith('N'), menciona=uid in MENCIONAN_IBERICO))
        def prop_bajo(fs): fs = list(fs); return (sum(f['bajo_mediana'] for f in fs), len(fs))
        res[p[:-4]] = dict(filas=filas, bajo_mediana=prop_bajo(filas), sin_numerales=prop_bajo(f for f in filas if not f['numeral']), sin_mencion_iberico=prop_bajo(f for f in filas if not f['menciona']))
        print(p[:-4], 'bajo la mediana del azar:', res[p[:-4]]['bajo_mediana'], '| sin numerales:', res[p[:-4]]['sin_numerales'], '| sin mención del ibérico:', res[p[:-4]]['sin_mencion_iberico'])
    json.dump(res, open(os.path.join(RAIZ, 'resultados', 't30_cloze.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    {'preparar': preparar, 'puntuar': puntuar}[sys.argv[1]]()
