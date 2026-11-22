"""Limpieza de formas. Especificación: 5_especificacion, apartado «Limpieza de una forma»."""
import re, unicodedata

VOCALES = set('aeiouáéíóúāēīōū')
CONSERVA = VOCALES | set('śŕḿñšçłŋ')          # caracteres con signo diacrítico que tienen clase propia o que distinguen signos ibéricos

def limpia(forma):
    """Limpieza de una forma ibérica de Hesperia: minúsculas; se quitan marcas editoriales y signos combinantes sueltos, salvo el acento agudo (que distingue ś, ŕ, ḿ).

    Pasos: (1) normalización Unicode NFC y minúsculas; (2) se eliminan los caracteres combinantes (categoría Mn)
    distintos del acento agudo U+0301; (3) NFC de nuevo; (4) se eliminan * [ ] { } ( ) - ? ’ ‘ ' espacios y puntos.
    Las letras que Hesperia marca como de lectura dudosa con un signo precompuesto (ṯ, ḵ…) se conservan tal cual: la
    palabra que las contiene no supera después el filtro de letras y queda fuera del corpus.
    """
    f = unicodedata.normalize('NFC', forma).lower()
    f = ''.join(ch for ch in f if unicodedata.category(ch) != 'Mn' or ch == '́')
    f = unicodedata.normalize('NFC', f)
    return re.sub(r"[\*\[\]\{\}\(\)\-\?’‘'\s\.]", '', f)

def limpia_grafia(forma):
    """Limpieza de una palabra de diccionario (salida de un normalizador) o de una forma ibérica ya escogida.

    Como `limpia`, pero además cada carácter que no esté en la lista de conservados (ś ŕ ḿ ñ š ç ł ŋ y las vocales con
    acento agudo o macron) se descompone (NFD) y pierde sus signos diacríticos: ê → e, ö → o, ǵ → g.
    """
    f = unicodedata.normalize('NFC', forma).lower()
    f = ''.join(ch if ch in CONSERVA else ''.join(c for c in unicodedata.normalize('NFD', ch) if unicodedata.category(c) != 'Mn') for ch in f)
    f = unicodedata.normalize('NFC', f)
    return re.sub(r"[\*\[\]\{\}\(\)\-\?’‘'\s\.]", '', f)

def sin_acentos(w, conserva=''):
    """Quita todos los signos combinantes (tras descomposición NFD), salvo los indicados en `conserva`."""
    return ''.join(ch for ch in unicodedata.normalize('NFD', w) if unicodedata.category(ch) != 'Mn' or ch in conserva)

def dobles(w):
    """Simplifica las letras dobles, salvo rr y ll."""
    return re.sub(r'([^rl])\1+', r'\1', w)
