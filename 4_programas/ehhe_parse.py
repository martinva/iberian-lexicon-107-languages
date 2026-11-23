"""Analiza la extracción del EHHE-200 (Euskaltzaindia; uso privado, no se redistribuye) y devuelve sus entradas principales.

Cada entrada: id, cabeceras (las formas separadas por «/»), atestiguaciones fechadas [(forma, año)], texto de Etimología y marca de préstamo.
"""
import json, re
from bs4 import BeautifulSoup

ROM = {'i': 1, 'v': 5, 'x': 10}
def _rom(s):
    t = 0; p = 0
    for ch in reversed(s):
        v = ROM[ch]; t = t - v if v < p else t + v; p = max(p, v)
    return t

def _parentesis(t):
    i = t.find('(')
    if i < 0: return '', t
    n = 0
    for j in range(i, len(t)):
        if t[j] == '(': n += 1
        elif t[j] == ')':
            n -= 1
            if n == 0: return t[i + 1:j], t[:i]
    return t[i + 1:], t[:i]

def _atestiguaciones(par, cab):
    out = []
    for seg in re.split(r';', re.sub(r'\[[^\]]*\]', '', par)):
        seg = seg.strip()
        m = re.match(r'^(?:([^\d~:]+?)\s+)?(~?\s?\d{3,4}|[ivx]+\.\s*m\.)', seg)
        if not m: continue
        forma = (m.group(1) or cab).strip().strip(',').strip()
        y = m.group(2)
        anio = int(re.sub(r'\D', '', y)) if re.search(r'\d', y) else _rom(y.split('.')[0]) * 100 - 50
        if re.fullmatch(r"[a-zñçü()'\-]+", forma.lower()): out.append((forma.lower(), anio))
    return out

def entradas(ruta):
    d = json.load(open(ruta, encoding='utf-8')); res = []
    for fam, html in d['familias'].items():
        s = BeautifulSoup(html, 'html.parser')
        for p in s.find_all('p'):
            pid = p.get('id') or ''
            if not (pid.startswith('pfamilia-') or pid.startswith('psarrera-')): continue
            t = p.get_text(' ', strip=True).lstrip('!♦ ').strip()
            par, antes = _parentesis(t)
            cabs = [c.strip().lower() for c in re.split(r'/', antes) if c.strip()]
            cabs = [re.sub(r'\d+$', '', c).strip('* ') for c in cabs if re.fullmatch(r"[*a-zñçü()\-\s\d]+", c)]
            if not cabs: continue
            # etimología: hasta el siguiente párrafo de entrada
            ety = []; q = p.find_next_sibling()
            while q is not None and not ((q.get('id') or '').startswith(('psarrera-', 'pfamilia-'))):
                ety.append(q.get_text(' ', strip=True)); q = q.find_next_sibling()
            todo = t + ' ' + ' '.join(ety)
            i = todo.find('►'); etim = todo[i:i + 1200] if i >= 0 else ''
            prest = bool(re.search(r'mailegu|<\s*lat\.|< ?gazt\.|erromantzetik|latinetik|gaztelaniatik|frantsesetik', etim))
            res.append(dict(id=pid.split('-', 1)[1], familia=fam, cabeceras=cabs, atestiguaciones=_atestiguaciones(par, cabs[0]), etimologia=etim[:600], prestamo=prest))
    return res

if __name__ == '__main__':
    import sys
    E = entradas(sys.argv[1]); print(len(E)); import collections
    print(sum(1 for e in E if e['atestiguaciones']), sum(e['prestamo'] for e in E))
    for e in E[:5] + [x for x in E if x['cabeceras'][0] in ('bortz', 'lau', 'hiru', 'hogei', 'zilar', 'bat')]: print(e['id'], e['cabeceras'], e['atestiguaciones'][:5], e['prestamo'])
