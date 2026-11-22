"""Reglas de paso de la ortografía de cada lengua a una grafía común. Especificación: «Normalizadores por lengua».

Cada función recibe una palabra en la ortografía de su diccionario y devuelve una cadena en una grafía común
(letras latinas con valores aproximados: k, s, x, tx, ts, j = semiconsonante, etc.), que después se pasa a clases con
`clases.reducida`. Son reglas generales por lengua, aproximadas, fijadas antes de ejecutar las pruebas y aplicadas
por igual a todas las palabras de la lengua. No se usa transcripción fonética palabra a palabra.
"""
import re, unicodedata
from .texto import sin_acentos, dobles

def _de_una_vez(w, pares):
    """Aplica las sustituciones en una sola pasada de izquierda a derecha: lo ya sustituido no vuelve a transformarse. En cada posición vale el primer par de la lista que encaja."""
    d = dict(pares); return re.sub('|'.join(re.escape(a) for a, _ in pares), lambda m: d[m.group(0)], w)

def n_eu(w):
    """Euskera: la ortografía se toma tal cual (tx, tz, ts, rr, ll se resuelven en `reducida`)."""
    return w

def n_rom(w, lang):
    """Lenguas romances. `lang`: es, pt, gl, ca, oc, ast, an, fr, it, ro."""
    w = w.lower().replace('ç', 's').replace('ñ', 'n').replace('ț', 'ts').replace('ţ', 'ts').replace('ș', 'x').replace('ş', 'x')
    w = sin_acentos(w)
    w = w.replace('qu', 'k').replace('ph', 'f')
    w = re.sub(r'gu(?=[ei])', 'g', w)
    if lang in ('it', 'ro'):
        w = w.replace('ch', 'k').replace('gh', 'g'); w = re.sub(r'gl(?=i)', 'll', w); w = w.replace('gn', 'n'); w = re.sub(r'sc(?=[ei])', 'x', w)
    else:
        w = w.replace('ch', 'tx')
    w = re.sub(r'c(?=[ei])', 's', w).replace('c', 'k')
    if lang == 'es': w = re.sub(r'g(?=[ei])', 'k', w).replace('j', 'k')
    else: w = re.sub(r'g(?=[ei])', 'x', w).replace('j', 'x')
    w = w.replace('lh', 'll').replace('nh', 'n').replace('ny', 'n').replace('gn', 'n').replace('h', '').replace('v', 'b').replace('w', 'b')
    w = re.sub(r'y(?=[aeiou])', 'j', w).replace('y', 'i')
    return dobles(w)

def n_la(w):
    w = sin_acentos(w.lower()).replace('qu', 'k').replace('ph', 'f').replace('th', 't').replace('ch', 'k').replace('c', 'k').replace('x', 'ks').replace('v', 'b').replace('h', '')
    w = re.sub(r'^i(?=[aeou])', 'j', w).replace('y', 'i')
    return dobles(w)

def n_cy(w):
    w = sin_acentos(w.lower()).replace('dd', 'd').replace('ff', 'F').replace('f', 'b').replace('F', 'f').replace('ch', 'k').replace('th', 't').replace('rh', 'r').replace('ng', 'n').replace('ph', 'f').replace('c', 'k')
    w = re.sub(r'w(?=[aeiouy])', 'b', w).replace('w', 'u').replace('y', 'i')
    return re.sub(r'([^l])\1', r'\1', w)

def n_fi(w):
    """Finés y estonio."""
    return dobles(sin_acentos(w.lower()).replace('y', 'u').replace('v', 'b'))

def n_hbs(w):
    w = w.lower().replace('dž', 'tx').replace('đ', 'tx').replace('č', 'tx').replace('ć', 'tx').replace('š', 'x').replace('ž', 'x').replace('lj', 'll').replace('nj', 'n').replace('c', 'ts').replace('h', 'k').replace('v', 'b')
    return dobles(sin_acentos(w))

def n_ger(w):
    """Alemán, sueco e islandés (aproximado)."""
    w = w.lower().replace('ß', 's').replace('þ', 't').replace('ð', 'd')
    w = sin_acentos(w).replace('tsch', 'tx').replace('sch', 'x').replace('skj', 'x').replace('stj', 'x').replace('sj', 'x').replace('tj', 'tx').replace('kj', 'tx').replace('ch', 'k').replace('ck', 'k').replace('qu', 'k').replace('ph', 'f').replace('th', 't').replace('c', 'k').replace('w', 'b').replace('v', 'b').replace('y', 'u')
    w = re.sub(r'(?<=[aeiou])h', '', w)
    return dobles(w)

def n_hu(w):
    w = sin_acentos(w.lower()).replace('dzs', 'tx').replace('cs', 'tx').replace('zs', 'X').replace('sz', 'S').replace('gy', 'd').replace('ty', 't').replace('ny', 'n').replace('ly', 'j')
    w = w.replace('s', 'x').replace('S', 's').replace('X', 'x').replace('c', 'ts').replace('v', 'b')
    return dobles(w)

def n_tr(w):
    """Turco (diccionarios del Wikcionario)."""
    w = w.lower().replace('ç', 'tx').replace('ş', 'x').replace('ğ', '').replace('ı', 'i').replace('c', 'tx').replace('y', 'j').replace('v', 'b')
    return dobles(sin_acentos(w))

def n_tr_apertium(w):
    """Turco (diccionario de Apertium): las mismas sustituciones, en el orden usado en esa fuente."""
    return dobles(sin_acentos(w.lower().replace('ç', 'tx').replace('ş', 'x').replace('ğ', '').replace('ı', 'i').replace('c', 'tx').replace('v', 'b').replace('y', 'j')))

def n_sq(w):
    w = _de_una_vez(w.lower(), [('ç', 'tx'), ('xh', 'tx'), ('sh', 'x'), ('zh', 'x'), ('dh', 'd'), ('th', 't'), ('gj', 'g'), ('nj', 'n'), ('ll', 'l'), ('q', 'k'), ('x', 'ts'), ('c', 'ts'), ('ë', 'e'), ('y', 'u'), ('v', 'b')])
    return sin_acentos(w)

def n_ga(w):
    w = sin_acentos(w.lower()).replace('bh', 'b').replace('mh', 'b').replace('fh', '').replace('ph', 'f').replace('th', 'h').replace('sh', 'h').replace('dh', 'g').replace('gh', 'g').replace('ch', 'k').replace('c', 'k')
    return dobles(w)

def n_lt(w):
    w = w.lower().replace('č', 'tx').replace('š', 'x').replace('ž', 'x').replace('c', 'ts').replace('y', 'i').replace('v', 'b')
    return dobles(sin_acentos(w))

def n_mt(w):
    w = w.lower().replace('għ', '').replace('ċ', 'tx').replace('ġ', 'tx').replace('ħ', 'h').replace('ż', 's').replace('z', 'ts').replace('q', 'k').replace('w', 'b').replace('v', 'b')
    return dobles(sin_acentos(w))

def n_sw(w):
    return w.lower().replace("ng'", 'n').replace('ch', 'tx').replace('sh', 'x').replace('ny', 'n').replace('th', 't').replace('dh', 'd').replace('gh', 'g').replace('j', 'tx').replace('y', 'j').replace('w', 'b').replace('v', 'b')

def n_qu(w):
    return sin_acentos(w.lower().replace('ch', 'tx').replace('q', 'k').replace('w', 'b').replace('y', 'j'))

def _sa(w):
    return ''.join(c for c in unicodedata.normalize('NFD', w.lower()) if unicodedata.category(c) != 'Mn')

def n_poli(w):
    """Hawaiano, samoano y tongano."""
    return _sa(w).replace('ʻ', '').replace("'", '').replace('wh', 'f').replace('ng', 'n').replace('g', 'n').replace('w', 'b')

def n_fj(w):
    return _de_una_vez(_sa(w), [('c', 'd'), ('q', 'g'), ('g', 'n'), ('w', 'b'), ('y', 'j'), ('v', 'b')])

def n_indo(w):
    """Indonesio y malayo."""
    return dobles(_sa(w).replace('ng', 'n').replace('ny', 'n').replace('sy', 'x').replace('kh', 'k').replace('c', 'tx').replace('j', 'tx').replace('y', 'j').replace('w', 'b').replace('v', 'b').replace("'", ''))

def n_tl(w):
    return dobles(_sa(w).replace('ng', 'n').replace('ts', 'tx').replace('y', 'j').replace('w', 'b').replace('c', 'k').replace('-', ''))

def n_mg(w):
    return _sa(w).replace('tr', 't').replace('dr', 'd').replace('j', 'ts').replace('y', 'i').replace('v', 'b')

def n_bantu(w):
    """Zulú y shona."""
    return dobles(_de_una_vez(_sa(w), [('tsh', 'tx'), ('ch', 'tx'), ('sh', 'x'), ('hl', 'l'), ('dl', 'l'), ('ny', 'n'), ("ng'", 'n'), ('bh', 'b'), ('ph', 'p'), ('th', 't'), ('kh', 'k'), ('dh', 'd'), ('c', 'k'), ('q', 'k'), ('x', 'k'), ('y', 'j'), ('w', 'b'), ('v', 'b')]))

def n_ha(w):
    return dobles(_sa(w.lower().replace('ƙ', 'k').replace('ɗ', 'd').replace('ɓ', 'b').replace('ƴ', 'y')).replace('sh', 'x').replace('c', 'tx').replace('j', 'tx').replace('y', 'j').replace('w', 'b').replace("'", ''))

def n_yo(w):
    return _sa(w.lower().replace('ṣ', 'x').replace('ẹ', 'e').replace('ọ', 'o')).replace('gb', 'b').replace('j', 'tx').replace('y', 'j').replace('w', 'b')

def n_so(w):
    return dobles(_de_una_vez(_sa(w), [('dh', 'd'), ('sh', 'x'), ('kh', 'k'), ('c', ''), ('x', 'h'), ('q', 'k'), ('j', 'tx'), ('y', 'j'), ('w', 'b'), ("'", '')]))

def n_nah(w):
    w = _sa(w).replace('tl', 't').replace('tz', 'ts').replace('ch', 'tx').replace('qu', 'k').replace('hu', 'b').replace('uh', 'b').replace('cu', 'k').replace('uc', 'k').replace('z', 's')
    return dobles(re.sub(r'c(?=[ei])', 's', w).replace('c', 'k').replace('y', 'j').replace('h', ''))

#: Lenguas del Wikcionario (nombre en inglés, como en la extracción) y su normalizador.
NORM = {
    'Basque': n_eu, 'Galician': lambda w: n_rom(w, 'gl'), 'Catalan': lambda w: n_rom(w, 'ca'), 'Occitan': lambda w: n_rom(w, 'oc'), 'Asturian': lambda w: n_rom(w, 'ast'),
    'Romanian': lambda w: n_rom(w, 'ro'), 'Latin': n_la, 'Welsh': n_cy, 'Icelandic': n_ger, 'Finnish': n_fi, 'Estonian': n_fi, 'Hungarian': n_hu, 'Turkish': n_tr,
    'Albanian': n_sq, 'Irish': n_ga, 'Lithuanian': n_lt, 'Maltese': n_mt, 'Swahili': n_sw, 'Quechua': n_qu,
    'Hawaiian': n_poli, 'Samoan': n_poli, 'Tongan': n_poli, 'Fijian': n_fj, 'Indonesian': n_indo, 'Malay': n_indo, 'Tagalog': n_tl, 'Malagasy': n_mg,
    'Zulu': n_bantu, 'Shona': n_bantu, 'Hausa': n_ha, 'Yoruba': n_yo, 'Somali': n_so, 'Classical Nahuatl': n_nah,
    'Sardinian': lambda w: n_rom(w.replace('tz', 'ts'), 'it'), 'Sicilian': lambda w: n_rom(w, 'it'),
}

def _quita(w):
    return ''.join(c for c in unicodedata.normalize('NFD', w) if unicodedata.category(c) != 'Mn')

def norm_control(lengua, w):
    """Lenguas de control de filiación conocida o aisladas (umbro, gótico, córnico, dálmata, etrusco, sumerio)."""
    w = unicodedata.normalize('NFC', w.lower())
    if lengua == 'Umbrian':
        w = _quita(w.replace('ç', 's')); w = w.replace('c', 'k').replace('q', 'k').replace('x', 'ks').replace('v', 'w').replace('z', 'ts')
    elif lengua == 'Gothic':
        w = _quita(w.replace('þ', 'ð').replace('ƕ', 'hw')).replace('q', 'kw').replace('ei', 'i').replace('gg', 'ng').replace('gk', 'nk')
    elif lengua == 'Cornish':
        w = _quita(w); w = w.replace('dh', 'ð').replace('th', 'ð').replace('gh', 'h').replace('wh', 'w').replace('qw', 'kw')
        w = re.sub(r'c(?=[eiy])', 's', w).replace('ch', 'tx').replace('c', 'k').replace('j', 'tx'); w = w[0] + w[1:].replace('y', 'i') if w else w
    elif lengua == 'Dalmatian':
        w = _quita(w); w = w.replace('ch', 'k').replace('gh', 'g').replace('gn', 'ñ').replace('qu', 'kw'); w = re.sub(r'c(?=[ei])', 'tx', w).replace('c', 'k').replace('z', 'ts')
    elif lengua == 'Etruscan':
        w = _quita(w.replace('θ', 't').replace('φ', 'p').replace('χ', 'k').replace('ś', 's').replace('σ', 's')).replace('c', 'k').replace('z', 'ts').replace('v', 'w')
    elif lengua == 'Sumerian':
        w = _quita(w.replace('g̃', 'ng').replace('ĝ', 'ng').replace('ḫ', 'h')); w = re.sub(r'[^a-z]', '', w)
    return w

def red_control(w):
    """Reducción a clases de una palabra de lengua de control: la fricativa dental ð pasa a la clase D; el resto, con `clases.reducida`."""
    from .clases import reducida
    return 'D'.join(reducida(x) for x in w.split('ð'))
