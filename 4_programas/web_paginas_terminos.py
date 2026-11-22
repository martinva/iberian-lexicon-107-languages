#!/usr/bin/env python3
"""Genera las páginas estáticas por unidad léxica de la web (docs/terminos/) a partir del CLDF.

Una página por unidad (parameters.csv) con sus formas (forms.csv): significado propuesto,
nivel de certeza, inscripciones citadas por sigla, apoyo y fuente. No reproduce textos de
inscripciones. Actualiza también docs/sitemap.xml. Uso: python3 4_programas/web_paginas_terminos.py
"""
import csv, html, json, os, re, unicodedata
from collections import OrderedDict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLDF = os.path.join(RAIZ, '1_fuentes_lexicas', 'iberico', 'cldf')
DOCS = os.path.join(RAIZ, 'docs')
SITIO = 'https://iberico.martinva.org'
FECHA = '2026-11-22'

FUENTES = {
    'MartinValladolid2026a': ('Monografía I', 'Monograph I', '10.5281/zenodo.23610039'),
    'MartinValladolid2026b': ('Monografía II', 'Monograph II', '10.5281/zenodo.23612741'),
    'MartinValladolid2026c': ('Monografía III', 'Monograph III', '10.5281/zenodo.23614005'),
    'MartinValladolid2026d': ('Monografía IV', 'Monograph IV', '10.5281/zenodo.23617694'),
    'Ferrer2022': ('Ferrer i Jané 2022', 'Ferrer i Jané 2022', '10.21001/rap.2022.32.1'),
    'Orduna2005': ('Orduña 2005', 'Orduña 2005', None),
    'Ferrer2014': ('Ferrer i Jané 2014', 'Ferrer i Jané 2014', None),
}
NIVEL = {
    'A': ('base epigráfica, metrológica o numismática directa', 'direct epigraphic, metrological or numismatic basis'),
    'B': ('regularidad posicional, tabular o aritmética', 'positional, tabular or arithmetical regularity'),
    'C': ('hipótesis funcional, semántica o de préstamo', 'functional, semantic or loanword hypothesis'),
}
GRUPO = {'léxico de los plomos': 'lead-plaque lexicon', 'metrológico': 'metrological'}


def slug(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def e(s):
    return html.escape(s or '', quote=True)


def nivel_txt(n, i):
    return '; '.join(f'{p}: {NIVEL[p][i]}' for p in n.split('/') if p in NIVEL)


def fuentes_html(src, i):
    out = []
    for k in src.split(';'):
        es, en, doi = FUENTES.get(k, (k, k, None))
        t = es if i == 0 else en
        out.append(f'<a href="https://doi.org/{doi}">{e(t)}</a>' if doi else e(t))
    return ', '.join(out)


CSS = """:root{--bg:#fbfaf7;--panel:#f3f1eb;--fg:#17171a;--mut:#5d5c58;--line:#dcd9d0;--acc:#1b365d}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15161a;--panel:#1e2026;--fg:#ecebe7;--mut:#a6a49d;--line:#33353c;--acc:#9cb8e0;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#15161a;--panel:#1e2026;--fg:#ecebe7;--mut:#a6a49d;--line:#33353c;--acc:#9cb8e0;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 Inter,system-ui,sans-serif}
.wrap{max-width:820px;margin:0 auto;padding-block:24px 60px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
a{color:var(--acc)}.top{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:14px}
.series{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);font-weight:600;margin-top:18px}
h1{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:clamp(28px,5vw,40px);color:var(--acc);margin:4px 0 2px}
h1 i{font-style:italic}h2{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:20px;color:var(--acc);border-bottom:1px solid var(--line);padding-bottom:4px;margin:30px 0 12px}
.gl{font-size:18px;color:var(--mut);margin:0 0 14px}.box{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin:14px 0}
.box p{margin:4px 0}.tblwrap{overflow-x:auto;border:1px solid var(--line);border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--panel)}td.f{font-family:"Source Serif 4",Georgia,serif;font-style:italic;font-size:16px;white-space:nowrap}
code,.m{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:13px}.note{font-size:13px;color:var(--mut)}
ul.t{columns:3 170px;padding-left:18px}ul.t li{margin:3px 0;break-inside:avoid}
footer{margin-top:40px;font-size:13px;color:var(--mut);border-top:1px solid var(--line);padding-top:10px}
.lang button{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--panel);color:var(--fg);padding:3px 9px;border-radius:6px;cursor:pointer}
.lang button[aria-pressed="true"]{background:var(--acc);color:var(--bg)}
[data-l]{display:none}html[lang="en"] [data-l="en"],html[lang="es"] [data-l="es"]{display:revert}"""

JS = """<script>(function(){var h=document.documentElement,b=document.querySelectorAll('.lang button');
function s(l){h.lang=l;b.forEach(function(x){x.setAttribute('aria-pressed',x.dataset.set===l?'true':'false')});try{localStorage.setItem('lang',l)}catch(e){}}
var v=null;try{v=localStorage.getItem('lang')}catch(e){}var q=(location.hash||'').slice(1);
s(q==='es'||q==='en'?q:(v||((navigator.language||'en').slice(0,2)==='es'?'es':'en')));
b.forEach(function(x){x.addEventListener('click',function(){s(x.dataset.set)})})})();</script>"""

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400&display=swap">'


def cabecera(title, desc, canon, extra=''):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="article"><meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}">
<meta property="og:site_name" content="iberico.martinva.org">
{extra}{FONTS}
<style>{CSS}</style>
</head>
<body><div class="wrap">
<div class="top"><a href="{SITIO}/"><span data-l="en">← Iberian lead-plaque lexicon and 107 languages</span><span data-l="es">← El léxico de los plomos ibéricos ante 107 lenguas</span></a>
<span class="lang" role="group" aria-label="Language"><button type="button" data-set="en" aria-pressed="true">EN</button> <button type="button" data-set="es" aria-pressed="false">ES</button></span></div>
"""


PIE = """<footer><p><span data-l="en">Proposed meanings are working hypotheses graded by certainty level, not established translations. Data:</span><span data-l="es">Los significados propuestos son hipótesis de trabajo graduadas por nivel de certeza, no traducciones establecidas. Datos:</span>
<a href="https://github.com/martinva/iberian-lexicon-107-languages/tree/main/1_fuentes_lexicas/iberico/cldf">CLDF</a> ·
<a href="https://doi.org/10.5281/zenodo.24443589"><span data-l="en">article</span><span data-l="es">artículo</span></a> ·
David Martín Valladolid · <a href="https://orcid.org/0009-0003-4884-2573">ORCID</a> · CC BY 4.0</p></footer>
</div>""" + JS + "\n</body>\n</html>\n"


def main():
    params = OrderedDict((r['ID'], r) for r in csv.DictReader(open(os.path.join(CLDF, 'parameters.csv'), encoding='utf-8')))
    formas = {}
    for r in csv.DictReader(open(os.path.join(CLDF, 'forms.csv'), encoding='utf-8')):
        formas.setdefault(r['Parameter_ID'], []).append(r)
    base = os.path.join(DOCS, 'terminos')
    os.makedirs(base, exist_ok=True)
    indice, urls, usados = [], [], set()
    for pid, p in params.items():
        fs = formas.get(pid, [])
        if not fs:
            continue
        nombre = fs[0]['Form']
        s = slug(nombre)
        if s in usados:
            s = f'{s}-{pid.lower()}'
        usados.add(s)
        titulo_formas = ' / '.join(f['Form'] for f in fs)
        url = f'{SITIO}/terminos/{s}/'
        urls.append(url)
        gl_en, gl_es = p['Terminos_en'], p['Terminos_es']
        niveles = sorted({f['Grado'] for f in fs})
        grupo = fs[0]['Grupo']
        title = f'Iberian {titulo_formas} — proposed meaning, inscriptions and certainty level'
        desc = (f"Iberian {titulo_formas}: proposed meaning '{gl_en}' (level {', '.join(niveles)}), "
                f"inscriptions and support. Significado propuesto: «{gl_es}».")
        ld = {"@context": "https://schema.org", "@type": "DefinedTerm", "name": nombre,
              "alternateName": [f['Form'] for f in fs[1:]], "description": f"Proposed meaning: {gl_en} / {gl_es}",
              "inDefinedTermSet": {"@type": "DefinedTermSet", "name": "Iberian lead-plaque lexicon (CLDF)",
                                   "url": "https://github.com/martinva/iberian-lexicon-107-languages"},
              "url": url, "inLanguage": "xib"}
        extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
        filas = ''.join(
            f"<tr><td class='f'>{e(f['Form'])}</td><td class='m'>{e(f['Segments'])}</td><td class='m'>{e(f['Grado'])}</td>"
            f"<td class='m'>{e(f['Inscripciones'] or '—')}</td><td>{e(f['Apoyo'])}</td>"
            f"<td><span data-l='es'>{fuentes_html(f['Source'], 0)}</span><span data-l='en'>{fuentes_html(f['Source'], 1)}</span></td></tr>"
            for f in fs)
        cuerpo = f"""<div class="series"><span data-l="en">Iberian · {e(GRUPO.get(grupo, grupo))}</span><span data-l="es">Ibérico · {e(grupo)}</span></div>
<h1><i>{e(titulo_formas)}</i></h1>
<p class="gl"><span data-l="en">Proposed meaning: ‘{e(gl_en)}’</span><span data-l="es">Significado propuesto: «{e(gl_es)}»</span></p>
<div class="box">
<p><b><span data-l="en">Certainty level</span><span data-l="es">Nivel de certeza</span>:</b> <span class="m">{e(', '.join(niveles))}</span> —
<span data-l="en">{e(nivel_txt('/'.join(niveles), 1))}</span><span data-l="es">{e(nivel_txt('/'.join(niveles), 0))}</span></p>
<p><b><span data-l="en">Semantic field</span><span data-l="es">Campo</span>:</b> {e(p['Campo'])} · <b><span data-l="en">Unit</span><span data-l="es">Unidad</span>:</b> <span class="m">{e(pid)}</span></p>
</div>
<h2><span data-l="en">Forms</span><span data-l="es">Formas</span></h2>
<div class="tblwrap"><table><thead><tr><th><span data-l="en">Form</span><span data-l="es">Forma</span></th><th><span data-l="en">Segments</span><span data-l="es">Segmentos</span></th><th><span data-l="en">Level</span><span data-l="es">Nivel</span></th><th><span data-l="en">Inscriptions</span><span data-l="es">Inscripciones</span></th><th><span data-l="en">Support</span><span data-l="es">Apoyo</span></th><th><span data-l="en">Source</span><span data-l="es">Fuente</span></th></tr></thead>
<tbody>{filas}</tbody></table></div>
<p class="note"><span data-l="en">Inscriptions are cited by their Hesperia / MLH reference; the texts can be consulted in the</span><span data-l="es">Las inscripciones se citan por su sigla de Hesperia / MLH; los textos pueden consultarse en el</span> <a href="https://hesperia.ucm.es/">Banco de datos Hesperia</a>.
<span data-l="en">Transcription: Hesperia system (dual script not distinguished in the forms).</span><span data-l="es">Transcripción: sistema de Hesperia (sin distinguir la escritura dual en las formas).</span></p>
<h2><span data-l="en">In the statistical comparison</span><span data-l="es">En la comparación estadística</span></h2>
<p><span data-l="en">This unit is one of the 40 Iberian units compared with 107 languages. See the article, the tool to remove words and the full inventory.</span><span data-l="es">Esta unidad es una de las 40 unidades ibéricas comparadas con 107 lenguas. Véanse el artículo, la herramienta para quitar palabras y el inventario completo.</span></p>
<p><a href="https://doi.org/10.5281/zenodo.24443589"><span data-l="en">Article</span><span data-l="es">Artículo</span></a> · <a href="{SITIO}/herramientas/quitar-palabras/"><span data-l="en">Remove words</span><span data-l="es">Quitar palabras</span></a> · <a href="{SITIO}/#inventory"><span data-l="en">Inventory</span><span data-l="es">Inventario</span></a> · <a href="{SITIO}/terminos/"><span data-l="en">All terms</span><span data-l="es">Todos los términos</span></a></p>
"""
        d = os.path.join(base, s)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as fh:
            fh.write(cabecera(title, desc, url, extra) + cuerpo + PIE)
        indice.append((grupo, s, titulo_formas, gl_en, gl_es, '/'.join(niveles)))

    # índice
    items = {}
    for g, s, t, en, es, n in indice:
        items.setdefault(g, []).append(
            f"<li><a href='{s}/'><i>{e(t)}</i></a> <span class='note'><span data-l='en'>‘{e(en)}’</span><span data-l='es'>«{e(es)}»</span> · {e(n)}</span></li>")
    secc = ''.join(
        f"<h2><span data-l='en'>{e(GRUPO.get(g, g)).capitalize()}</span><span data-l='es'>{e(g).capitalize()}</span></h2><ul class='t'>{''.join(v)}</ul>"
        for g, v in items.items())
    url_i = f'{SITIO}/terminos/'
    cuerpo_i = f"""<div class="series"><span data-l="en">Iberian lexicon · CLDF</span><span data-l="es">Léxico ibérico · CLDF</span></div>
<h1><span data-l="en">Iberian terms compared</span><span data-l="es">Términos ibéricos comparados</span></h1>
<p class="gl"><span data-l="en">The {len(indice)} units of the comparison, with their forms, proposed meaning and certainty level.</span><span data-l="es">Las {len(indice)} unidades de la comparación, con sus formas, significado propuesto y nivel de certeza.</span></p>
{secc}"""
    with open(os.path.join(base, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(cabecera('Iberian terms compared — lead-plaque lexicon (CLDF)',
                          'Index of the Iberian units of the lead-plaque lexicon compared with 107 languages: forms, proposed meanings and certainty levels.',
                          url_i) + cuerpo_i + PIE)

    # sitemap
    fijas = [(f'{SITIO}/', '1.0'), (f'{SITIO}/terminos/', '0.8'),
             (f'{SITIO}/herramientas/quitar-palabras/', '0.7'), (f'{SITIO}/herramientas/proximidad/', '0.6'),
             (f'{SITIO}/herramientas/mapa-3d/', '0.5'), (f'{SITIO}/herramientas/mapa-provincias/', '0.5')]
    lin = [f' <url><loc>{u}</loc><lastmod>{FECHA}</lastmod><priority>{p}</priority></url>' for u, p in fijas]
    lin += [f' <url><loc>{u}</loc><lastmod>{FECHA}</lastmod><priority>0.6</priority></url>' for u in urls]
    with open(os.path.join(DOCS, 'sitemap.xml'), 'w', encoding='utf-8') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + '\n'.join(lin) + '\n</urlset>\n')
    print(f'{len(indice)} páginas de términos; sitemap con {len(lin)} URL')


if __name__ == '__main__':
    main()
