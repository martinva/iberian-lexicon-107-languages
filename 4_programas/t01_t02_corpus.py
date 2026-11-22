"""Tablas 1 y 2: recuento descriptivo del corpus ibérico por soporte (palabras, extensión de los textos, tipo de palabras).

No interviene ninguna otra lengua. Reglas:
- Soporte: plomo si el material normalizado es PLOMO; piedra si es PIEDRA o el grupo de soporte es lápida o estela, parietal,
  monumental o arquitectónico; cerámica si el material es CERAMICA; otros, el resto.
- Las líneas del texto con tres o más mayúsculas seguidas (anotaciones editoriales) se omiten. Cada línea se parte por
  · : | espacios , ; /
- PALABRA: tramo que, quitados [ ] + * ? - ( ) < > cifras I V X Π . ' ’, y limpio, consta de dos o más letras ibéricas.
- PALABRA COMPLETA: palabra cuyo tramo original no contiene ninguno de esos signos (sin lagunas ni signos dudosos).
- Variantes gráficas equivalentes (b/p, t/d, k/g, s/ś, r/ŕ, m/n/ḿ) cuentan como una sola forma.
- NOMBRE PROBABLE: la palabra figura en el léxico de Moncunill y Velaza (2019) como nombre personal, nombre por formantes,
  leyenda monetal, marca o abreviatura o numeral, o como nombre dudoso; si no figura en ese léxico, la que, con alguno de los
  sufijos de la lista o sin sufijo, se divide en dos formantes de la lista de Rodríguez Ramos (2014).
Uso:  python3 t01_t02_corpus.py
"""
import csv, json, os, re, sys, statistics as st
from collections import defaultdict, Counter
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.texto import limpia

SIGNOS = r"[\[\]\+\*\?\-\(\)<>0-9IVXΠ\.\'’]"; LETRAS = '[aeioubtkdglnmrŕsśḿ]'
SUFIJOS = ['ka', 'te', 'en', 'ar', 'e', 'ban', 'sken', 'ḿi', 'ir', 'bi', 'ki', 'ite', 'ke']
CLASES_NOMBRE = ('nombre personal', 'nombre (formantes)', 'leyenda monetal', 'marca o abreviatura', 'numeral')
_EQ = {**{c: 'P' for c in 'pb'}, **{c: 'T' for c in 'td'}, **{c: 'K' for c in 'kg'}, **{c: 'S' for c in 'sś'}, **{c: 'N' for c in 'mnḿ'}, **{c: 'R' for c in 'rŕ'}, 'l': 'L'}
equivalente = lambda w: ''.join(_EQ.get(c, c) for c in w)

def grupo(m):
    if m['material_norm'] == 'PLOMO': return 'Plomo'
    if m['material_norm'] == 'PIEDRA' or m['soporte_grupo'] in ('LAPIDA_ESTELA', 'PARIETAL', 'MONUMENTAL', 'ARQUITECTONICO'): return 'Piedra'
    if m['material_norm'] == 'CERAMICA': return 'Cerámica'
    return 'Otros'

if __name__ == '__main__':
    I = f'{fuentes.RAIZ}/iberico'; meta = {r['ref_hesperia']: r for r in csv.DictReader(open(f'{I}/hesperia_metadatos.csv', encoding='utf-8-sig'))}
    FOR = set(limpia(x['formante']) for x in json.load(open(f'{I}/formantes_onomasticos_rodriguez_ramos_2014.json', encoding='utf-8')))
    MLH = {limpia(r['forma']): r for r in csv.DictReader(open(f'{I}/lexico_mlh_v2_clasificacion.csv', encoding='utf-8-sig'))}
    def es_nombre(w):
        m = MLH.get(w)
        if m: return m['clase_segun_primera_frase'] in CLASES_NOMBRE or m['nombre_dudoso'] == 'sí'
        for s in [''] + SUFIJOS + ['ku', 'ḿ', 'i']:
            if s and not w.endswith(s): continue
            b = w[:-len(s)] if s else w
            if any(b[:k] in FOR and b[k:] in FOR for k in range(2, len(b) - 1)): return True
        return False
    PAL = defaultdict(list); COMP = defaultdict(list); TXT = defaultdict(list)
    for r in csv.DictReader(open(f'{I}/hesperia_iberico_1599.csv', encoding='utf-8-sig')):
        g = grupo(meta[r['ref_hesperia']]); n = 0
        for linea in r['texto_crudo'].split('\n'):
            if re.search(r'[A-Z]{3,}', linea): continue
            for t in re.split(r'[·:|\s,;/]+', linea):
                w0 = limpia(re.sub(SIGNOS, '', t))
                if not re.fullmatch(LETRAS + '{2,}', w0): continue
                n += 1; PAL[g].append(w0)
                if not re.search(SIGNOS, t): COMP[g].append(limpia(t))
        TXT[g].append(n)
    G = ['Plomo', 'Cerámica', 'Piedra', 'Otros']; tp = sum(len(PAL[g]) for g in G); td = sum(len({equivalente(w) for w in PAL[g]}) for g in G); res = {}
    print('TABLA 1'); tot_no = 0; union_no = set(); union_d = set()
    for g in G:
        c3 = [w for w in COMP[g] if len(w) >= 3]; noon = {equivalente(w) for w in c3 if len(w) >= 4 and not es_nombre(w)}; tot_no += len(noon); union_no |= noon; union_d |= {equivalente(w) for w in PAL[g]}
        res[g] = dict(inscripciones=len(TXT[g]), palabras=len(PAL[g]), palabras_distintas=len({equivalente(w) for w in PAL[g]}), vocabulario_no_onomastico_distinto=len(noon))
    for g in G:
        r = res[g]; print(f"  {g:9s} inscripciones {r['inscripciones']:5d} | palabras {r['palabras']:5d} ({100 * r['palabras'] / tp:.0f} %) | distintas {r['palabras_distintas']:5d} ({100 * r['palabras_distintas'] / td:.0f} %) | no onomástico distinto {r['vocabulario_no_onomastico_distinto']:4d} ({100 * r['vocabulario_no_onomastico_distinto'] / tot_no:.0f} %)")
    res['Total'] = dict(inscripciones=sum(len(TXT[g]) for g in G), palabras=tp, suma_de_distintas_por_soporte=td, distintas_en_todo_el_corpus=len(union_d), suma_no_onomastico_por_soporte=tot_no, no_onomastico_distinto_en_todo_el_corpus=len(union_no))
    print(f"  Total     {res['Total']}")
    print('TABLA 2')
    for g in ('Plomo', 'Cerámica'):
        t = TXT[g]; ws = COMP[g]; L = [len(w) for w in ws]; c3 = [w for w in ws if len(w) >= 3]; c = Counter(equivalente(w) for w in c3); noon = [w for w in ws if len(w) >= 4 and not es_nombre(w)]
        suf = [w for w in noon if any(w.endswith(s) and len(w) - len(s) >= 3 for s in SUFIJOS)]
        d = dict(palabras_por_inscripcion=round(st.mean(t), 1), una_palabra_o_menos=sum(x <= 1 for x in t), cinco_o_mas=sum(x >= 5 for x in t), diez_o_mas=sum(x >= 10 for x in t), completas=len(ws), longitud_media=round(st.mean(L), 1),
                 de_dos_o_tres_letras=sum(x <= 3 for x in L), de_seis_o_mas=sum(x >= 6 for x in L), pct_nombres=round(100 * sum(es_nombre(w) for w in c3) / len(c3)), pct_en_formas_repetidas=round(100 * sum(v for v in c.values() if v > 1) / len(c3)), pct_repiten_forma_ya_presente=round(100 * sum(v - 1 for v in c.values()) / len(c3), 1), no_onomasticas_con_sufijo=len(suf))
        res[g].update(d); print(f'  {g}: {d}')
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't01_t02_corpus.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
