"""Declaración 43: la prueba de perfil del primer estudio con la escritura igualada, y variación por lengua al quitar el signario.

(a) cambio relativo de la divergencia de cada lengua con el ibérico al pasar la lengua por el canal del signario;
(b) remuestreo (500 con reemplazo y 500 mitades) frente a las lenguas pasadas por el canal;
(c) ibérico: grecoibérico (106 formas) frente a 500 submuestras levantinas del mismo tamaño, lengua a lengua;
(d) celtibérico: alfabeto latino (109) frente a 500 submuestras en signario, lengua a lengua;
(e) cabeceras y formas reconstruidas del EHHE pasadas por el canal.
Uso / Usage:  python3 t57_perfil_escritura_igualada.py RUTA/celtiberian_raw.csv RUTA/ehhe_extraccion.json
"""
import json, os, re, statistics, sys
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import reducida
from ibcomp.pruebas import perfil, divergencia, generador
from t41_escritura import formas_cel_por_escritura, canal
from t51_perfil_ehhe_reconstruido import reconstruidas
from ehhe_parse import entradas

MODOS = ('supresion', 'vocal_de_apoyo')


def pasa(ws, modo):
    return {x for x in (canal(w, modo) for w in ws) if x}


def cuartil_superior(x, xs):
    return sum(v <= x for v in xs) / len(xs)


def cambios(base, nuevo, nombres):
    """base, nuevo: dict lengua -> divergencia. Devuelve resumen de los cambios relativos."""
    c = {l: (nuevo[l] - base[l]) / base[l] for l in base}
    orden = sorted(c.items(), key=lambda kv: kv[1])
    eus = next(l for l in c if nombres[l] == 'Basque'); absd = sorted(abs(v) for v in c.values())
    return dict(euskera=round(c[eus], 4), mediana=round(statistics.median(c.values()), 4), mediana_abs=round(statistics.median(absd), 4),
                se_acercan=sum(v < 0 for v in c.values()), se_alejan=sum(v > 0 for v in c.values()), de=len(c),
                puesto_euskera_de_menor_a_mayor=[l for l, _ in orden].index(eus) + 1,
                puesto_euskera_por_cambio_absoluto=sorted(c, key=lambda l: abs(c[l])).index(eus) + 1,
                fraccion_con_cambio_menor_o_igual_que_euskera=round(cuartil_superior(c[eus], list(c.values())), 3),
                menores=[(nombres[l], round(v, 4)) for l, v in orden[:6]], mayores=[(nombres[l], round(v, 4)) for l, v in orden[-6:]],
                todas={nombres[l]: round(v, 4) for l, v in orden})


def primeras(q, P, nombres, n=6):
    return [(nm, round(d, 4)) for d, nm in sorted((divergencia(q, P[l]), nombres[l]) for l in P)[:n]]


def remuestreo(ws, P, nombres, clave, rep=500):
    rnd = generador('t57', clave); ws = sorted(ws); c1 = c2 = 0; m1 = []
    for _ in range(rep):
        for k, muestra in enumerate(([rnd.choice(ws) for _ in ws], rnd.sample(ws, len(ws) // 2))):
            pm = perfil(muestra); o = sorted((divergencia(pm, P[l]), nombres[l]) for l in P)
            if k == 0:
                c1 += o[0][1] == 'Basque'; d_e = next(d for d, nm in o if nm == 'Basque'); m1.append(min(d for d, nm in o if nm != 'Basque') - d_e)
            else:
                c2 += o[0][1] == 'Basque'
    return dict(remuestreo=c1, mitades=c2, de=rep, ventaja_mediana_sobre_la_mejor_otra=round(statistics.median(m1), 4))


def submuestras(ws, n, P, clave, rep=500):
    """Mediana, lengua a lengua, de la divergencia de rep submuestras de n formas."""
    rnd = generador('t57', clave); ws = sorted(ws); acc = {l: [] for l in P}
    for _ in range(rep):
        q = perfil(rnd.sample(ws, n))
        for l in P: acc[l].append(divergencia(q, P[l]))
    return {l: statistics.median(v) for l, v in acc.items()}


if __name__ == '__main__':
    LEX, lang = fuentes.northeuralex(); nombres = {l: lang[l]['Name'] for l in LEX}
    P0 = {l: perfil(ws) for l, ws in LEX.items()}; PC = {m: {l: perfil(pasa(ws, m)) for l, ws in LEX.items()} for m in MODOS}
    fichas = fuentes.hesperia()
    IB = {'todo el corpus': set().union(*[f['formas'] for f in fichas]), 'plomos': set().union(*[f['formas'] for f in fichas if f['plomo_amplio']])}
    res = {}
    # (a) y (b)
    for nombre, ws in IB.items():
        q = perfil(ws); d0 = {l: divergencia(q, P0[l]) for l in P0}; r = dict(formas=len(ws), original=primeras(q, P0, nombres))
        for m in MODOS:
            dm = {l: divergencia(q, PC[m][l]) for l in P0}
            r[m] = dict(primeras=primeras(q, PC[m], nombres), cambio=cambios(d0, dm, nombres), **remuestreo(ws, PC[m], nombres, nombre + m))
            print(nombre, m, r[m]['primeras'][:3], {k: v for k, v in r[m]['cambio'].items() if k != 'todas' and not isinstance(v, list)}, r[m]['remuestreo'], r[m]['mitades'], r[m]['ventaja_mediana_sobre_la_mejor_otra']); sys.stdout.flush()
        res['igualar: ' + nombre] = r
    # (c) ibérico
    gr = set().union(*[f['formas'] for f in fichas if f['signario'] == 'GRECOIBERICO']); lv = set().union(*[f['formas'] for f in fichas if f['signario'] == 'LEVANTINO'])
    qg = perfil(gr); dg = {l: divergencia(qg, P0[l]) for l in P0}; dl = submuestras(lv, len(gr), P0, 'levantino')
    res['quitar: ibérico'] = dict(formas=len(gr), primeras_grecoiberico=primeras(qg, P0, nombres), primeras_levantino_mediana=[(nombres[l], round(d, 4)) for d, l in sorted((d, l) for l, d in dl.items())[:6]], cambio=cambios(dl, dg, nombres))
    print('ibérico', {k: v for k, v in res['quitar: ibérico']['cambio'].items() if k != 'todas'}); sys.stdout.flush()
    # (d) celtibérico
    lat, sig = formas_cel_por_escritura(sys.argv[1]); ql = perfil(lat); dla = {l: divergencia(ql, P0[l]) for l in P0}; ds = submuestras(sig, len(lat), P0, 'signario')
    res['quitar: celtibérico'] = dict(formas=len(lat), primeras_latino=primeras(ql, P0, nombres), primeras_signario_mediana=[(nombres[l], round(d, 4)) for d, l in sorted((d, l) for l, d in ds.items())[:6]], cambio=cambios(ds, dla, nombres))
    print('celtibérico', {k: v for k, v in res['quitar: celtibérico']['cambio'].items() if k != 'todas'}); sys.stdout.flush()
    # (e) EHHE
    E = entradas(sys.argv[2]); cab = set()
    for e in E:
        for c in e['cabeceras']:
            c = re.sub(r'[()\-\s]', '', c)
            if len(c) >= 2:
                x = reducida(c)
                if len(x) >= 2: cab.add(x)
    rec = {x for x in (reducida(w) for w in reconstruidas(sys.argv[2])) if len(x) >= 2}
    q = perfil(IB['todo el corpus']); r = {}
    for nombre, fs in (('EHHE cabeceras', cab), ('EHHE reconstruido', rec)):
        r[nombre] = dict(formas=len(fs), original=round(divergencia(q, perfil(fs)), 4))
        for m in MODOS:
            d = divergencia(q, perfil(pasa(fs, m))); orden = sorted([(divergencia(q, PC[m][l]), nombres[l]) for l in P0] + [(d, nombre)])
            r[nombre][m] = dict(div=round(d, 4), puesto=[n for _, n in orden].index(nombre) + 1, de=len(orden), primera_lengua=[(n, round(x, 4)) for x, n in orden if n != nombre][0])
    res['EHHE con el canal'] = r; print(r)
    c = res['igualar: todo el corpus']
    res['previsiones'] = {'1': c['supresion']['remuestreo'] >= 475, '2': 250 < c['vocal_de_apoyo']['remuestreo'] < 475,
                          '3': all(c[m]['cambio']['se_acercan'] >= 0.6 * 107 and abs(c[m]['cambio']['euskera']) < c[m]['cambio']['mediana_abs'] for m in MODOS),
                          '4': 0.08 <= res['quitar: ibérico']['cambio']['euskera'] <= 0.11 and res['quitar: ibérico']['primeras_grecoiberico'][0][0] == 'Basque' and res['quitar: ibérico']['cambio']['puesto_euskera_de_menor_a_mayor'] > 1,
                          '5': 0.45 <= res['quitar: celtibérico']['cambio']['euskera'] <= 0.55 and res['quitar: celtibérico']['cambio']['fraccion_con_cambio_menor_o_igual_que_euskera'] >= 0.75,
                          '6': all(r[k][m]['puesto'] == 1 for k in r for m in MODOS)}
    print(res['previsiones'])
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't57_perfil_escritura_igualada.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
