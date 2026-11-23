"""Declaración 35: prueba de perfil con las cabeceras del EHHE-200 como capa vasca.

Uso / Usage:  python3 t49_perfil_ehhe.py RUTA/ehhe_extraccion.json RUTA/celtiberian_raw.csv
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import reducida
from ibcomp.pruebas import perfil, divergencia
from ehhe_parse import entradas
from t41_escritura import formas_cel_por_escritura

if __name__ == '__main__':
    E = entradas(sys.argv[1])
    def formas(es):
        out = set()
        for e in es:
            for c in e['cabeceras']:
                c = re.sub(r'[()\-\s]', '', c)
                if len(c) >= 2:
                    x = reducida(c)
                    if len(x) >= 2: out.add(x)
        return out
    todas = formas(E); patr = formas([e for e in E if not e['prestamo']])
    LEX, lang = fuentes.northeuralex(); nombres = {l: lang[l]['Name'] for l in LEX}; P = {l: perfil(ws) for l, ws in LEX.items()}
    IB = set().union(*[f['formas'] for f in fuentes.hesperia()]); q = perfil(IB)
    _, sig = formas_cel_por_escritura(sys.argv[2]); qc = perfil(sig); res = {}
    for nombre, fs in (('EHHE todas', todas), ('EHHE sin préstamos', patr)):
        pe = perfil(fs); d = divergencia(q, pe)
        orden = sorted([(divergencia(q, P[l]), nombres[l]) for l in P] + [(d, nombre)])
        pos = [n for _, n in orden].index(nombre) + 1
        res[nombre] = dict(formas=len(fs), div_iberico=round(d, 4), puesto_entre_108=pos, primeras=[(n, round(x, 4)) for x, n in orden[:5]],
                           div_celtiberico_signario=round(divergencia(qc, pe), 4))
    res['previsiones'] = {'1': all(res[k]['puesto_entre_108'] <= 2 for k in ('EHHE todas', 'EHHE sin préstamos')),
                          '2': all(res[k]['div_iberico'] < res[k]['div_celtiberico_signario'] for k in ('EHHE todas', 'EHHE sin préstamos'))}
    print(json.dumps(res, ensure_ascii=False, indent=1))
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't49_perfil_ehhe.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
