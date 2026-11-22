"""Paso a clases de sonidos SCA. Especificación: «Clases de sonidos» y «Reducción de una forma».

Clases de consonante (List 2012): C africadas, B fricativas labiales, D fricativas dentales, G fricativas velares,
H laringales, K, J, M, L, N, P, S, R, T, W y ! (clics). Las seis clases de vocal de SCA se escriben en minúscula:
A→a, E→e, I→i, U→o, Y→u, O→o.
"""
import re, unicodedata, os
from .texto import limpia, VOCALES, limpia_grafia

_RUTA = os.path.join(os.path.dirname(__file__), '..', '..', '1_fuentes_lexicas', 'clases_sca', 'converter')
_conv = {}
for _l in open(_RUTA, encoding='utf-8'):
    if ' : ' in _l:
        _c, _t = _l.rstrip('\n').split(' : ', 1)
        for _x in _t.split(', '): _conv.setdefault(unicodedata.normalize('NFC', _x.strip()), _c)
_conv.setdefault('ʜ', 'H')   # fricativa epiglotal sorda, ausente de la tabla de LingPy; 112 apariciones en NorthEuraLex (se trata como h)
_VOC = {'A': 'a', 'E': 'e', 'I': 'i', 'U': 'o', 'O': 'o', 'Y': 'u'}

def clase_sca(simbolo):
    """Clase SCA de un símbolo fonético según la tabla de LingPy; None si no figura o es tono o marca."""
    c = _conv.get(unicodedata.normalize('NFC', simbolo))
    return None if c is None or c in '123456_9' else _VOC.get(c, c)

def red_afi(segmentos):
    """Lista de segmentos en alfabeto fonético internacional → cadena de clases (bases léxicas en AFI)."""
    out = ''
    for s in segmentos:
        s = s.replace('ː', '').replace('ˑ', '')
        c = clase_sca(s)
        if c is None:
            b = ''.join(ch for ch in unicodedata.normalize('NFD', s) if unicodedata.category(ch) in ('Ll', 'Lu', 'Lo'))
            if not b: continue
            c = clase_sca(b)
            if c is None:
                k = [clase_sca(ch) for ch in b]
                c = 'C' if (len(k) >= 2 and k[0] in ('T', 'P', 'K') and k[1] == 'S') else k[0]
        if c: out += c
    return out

_IB = {**{c: 'P' for c in 'pb'}, **{c: 'T' for c in 'td'}, **{c: 'K' for c in 'kg'}, **{c: 'S' for c in 'sś'}, **{c: 'R' for c in 'rŕ'}, 'l': 'L', 'm': 'M', 'ḿ': 'M', 'n': 'N'}

def red_ib(forma):
    """Forma ibérica en la transcripción de Hesperia → cadena de clases, signo a signo (se usa en el perfil de sonidos y en los numerales)."""
    out = ''
    for ch in limpia(forma): out += _IB.get(ch, unicodedata.normalize('NFD', ch)[0] if ch in VOCALES else '')
    return out

_DIG = {'tx': 'C', 'tz': 'C', 'ts': 'C', 'tś': 'C', 'ch': 'C', 'sh': 'S', 'll': 'L', 'rr': 'R', 'ng': 'N'}
_CL = {**{c: 'P' for c in 'pb'}, **{c: 'B' for c in 'fv'}, 'w': 'W', **{c: 'T' for c in 'td'}, **{c: 'K' for c in 'kgq'}, 'ʔ': 'H', 'h': 'H',
       **{c: 'S' for c in 'sśzxšç'}, 'c': 'C', **{c: 'M' for c in 'mḿ'}, **{c: 'N' for c in 'nñŋ'}, **{c: 'R' for c in 'rŕ'}, **{c: 'L' for c in 'lł'}, **{c: 'J' for c in 'yj'}}

def reducida(forma):
    """Forma en grafía común (salida de un normalizador) → cadena de clases.

    Se usa para los diccionarios y, en la prueba con significados, también para las formas ibéricas.
    Reglas: se limpia la forma; la h inicial no cuenta; i inicial ante a, e, o, u se trata como j; los dígrafos
    tx tz ts tś ch → C, sh → S, ll → L, rr → R, ng → N; el resto, letra a letra; lo que no tiene clase se omite.
    """
    f = limpia_grafia(forma); out = ''; i = 0
    if f.startswith('h'): f = f[1:]
    if len(f) > 1 and f[0] == 'i' and f[1] in 'aeou': f = 'j' + f[1:]
    while i < len(f):
        if f[i:i+2] in _DIG: out += _DIG[f[i:i+2]]; i += 2; continue
        ch = f[i]; out += _CL.get(ch, unicodedata.normalize('NFD', ch)[0] if ch in VOCALES else ''); i += 1
    return out

def red_chan(forma):
    """Numeral de la base de Chan (transcripción mixta) → cadena de clases, signo a signo; se simplifican las clases repetidas contiguas."""
    out = ''
    for ch in unicodedata.normalize('NFC', forma.lower()):
        c = clase_sca(ch)
        if c is None: c = clase_sca(unicodedata.normalize('NFD', ch)[0])
        if c: out += c
    return re.sub(r'(.)\1+', r'\1', out)

PROYECCION = str.maketrans({'B': 'P', 'D': 'T', 'G': 'K', 'C': 'S', 'M': 'N', 'H': None, 'W': 'o', 'J': 'i', '!': None})

def proyecta(formas):
    """Reduce un conjunto de formas al inventario que la escritura ibérica anota (B→P, D→T, G→K, C→S, M→N, W→o, J→i; H y clics se suprimen); descarta las de menos de dos símbolos."""
    return {w.translate(PROYECCION) for w in formas if len(w.translate(PROYECCION)) >= 2}
