"""Declaración 37: perfil con las formas con asterisco del EHHE (capa reconstruida).

Uso / Usage:  python3 t51_perfil_ehhe_reconstruido.py RUTA/ehhe_extraccion.json
"""
import json, os, re, sys
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import reducida
from ibcomp.pruebas import perfil, divergencia

def reconstruidas(ruta):
    d = json.load(open(ruta, encoding='utf-8')); out = set()
    for h in d['familias'].values():
        t = BeautifulSoup(h, 'html.parser').get_text(' ').lower()
        for m in re.finditer(r'\*\s?([a-zñçü]{2,12})(?![a-z])', t):
            w = m.group(1)
            if re.search(r'(us|um|are|ere|ire|ari|iu)$', w) or (w.endswith('ia') and len(w) > 5) or re.search(r'[vyw]|c(?!ç)', w.replace('ç', '')): continue
            out.add(w)
    return out

if __name__ == '__main__':
    R = reconstruidas(sys.argv[1]); F = {x for x in (reducida(w) for w in R) if len(x) >= 2}
    LEX, lang = fuentes.northeuralex(); nombres = {l: lang[l]['Name'] for l in LEX}
    IB = set().union(*[f['formas'] for f in fuentes.hesperia()]); q = perfil(IB); d = divergencia(q, perfil(F))
    orden = sorted([(divergencia(q, perfil(ws)), nombres[l]) for l, ws in LEX.items()] + [(d, 'EHHE reconstruido')])
    res = dict(formas_asterisco=len(R), formas_reducidas=len(F), div_iberico=round(d, 4), puesto=[n for _, n in orden].index('EHHE reconstruido') + 1,
               primeras=[(n, round(x, 4)) for x, n in orden[:5]], ejemplos=sorted(R)[:40])
    res['prevision'] = res['puesto'] <= 2 and d < next(x for x, n in orden if n == 'Basque')
    print(json.dumps(res, ensure_ascii=False, indent=1))
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't51_perfil_ehhe_reconstruido.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
