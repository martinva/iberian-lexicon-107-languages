#!/usr/bin/env python3
"""Genera las páginas estáticas de la web por unidad léxica y por inscripción citada, a partir del CLDF.

Cada página existe en dos direcciones, una por idioma, con su título, su descripción y sus enlaces hreflang:
  inglés   docs/terminos/<forma>/        docs/terminos/        docs/inscripciones/
  español  docs/es/terminos/<forma>/     docs/es/terminos/     docs/es/inscripciones/

Una página por unidad (parameters.csv) con sus formas (forms.csv): significado propuesto, nivel de certeza,
inscripciones citadas por sigla, apoyo, fuente y unidades relacionadas (mismo campo; mismas inscripciones).
No reproduce textos de inscripciones. Escribe también docs/sitemap.xml (con las alternativas de idioma) y
completa la cabecera de las páginas de herramientas. La portada la genera web_portada.py.
Uso: python3 4_programas/web_paginas_terminos.py
"""
import csv, html, json, os, re, unicodedata
from collections import OrderedDict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLDF = os.path.join(RAIZ, '1_fuentes_lexicas', 'iberico', 'cldf')
DOCS = os.path.join(RAIZ, 'docs')
SITIO = 'https://iberico.martinva.org'
FECHA = '2026-11-25'
IDIOMAS = ('en', 'es')
PRE = {'en': '', 'es': '/es'}

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
CAMPO = {'predial y geográfico': 'land and geography', 'léxico con soporte metrológico': 'lexicon with metrological support',
         'personas y actos': 'persons and acts', 'contable y monetario': 'accounting and money',
         'predial; préstamo latino propuesto': 'land; proposed Latin loan', 'contable; préstamo latino propuesto': 'accounting; proposed Latin loan'}
# Prefijo de la sigla de Hesperia -> provincia o departamento (convención de Hesperia / MLH)
ZONA = {'V': ('Valencia', 'Valencia'), 'A': ('Alicante', 'Alicante'), 'B': ('Barcelona', 'Barcelona'), 'GI': ('Girona', 'Girona'),
        'T': ('Tarragona', 'Tarragona'), 'AUD': ('Aude (Francia)', 'Aude (France)'),
        'PYO': ('Pirineos Orientales (Francia)', 'Pyrénées-Orientales (France)'), 'SP': ('sin procedencia conocida', 'unknown provenance')}


def slug(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def e(s):
    return html.escape(s or '', quote=True)


def tr(L, en, es):
    return en if L == 'en' else es


def nivel_txt(n, L):
    return '; '.join(f'{p}: {NIVEL[p][1 if L == "en" else 0]}' for p in n.split('/') if p in NIVEL)


def fuentes_html(src, L):
    out = []
    for k in src.split(';'):
        es, en, doi = FUENTES.get(k, (k, k, None))
        t = en if L == 'en' else es
        out.append(f'<a href="https://doi.org/{doi}">{e(t)}</a>' if doi else e(t))
    return ', '.join(out)


def siglas(texto):
    """Siglas concretas citadas en el campo Inscripciones (las cuentas del tipo «10 inscripciones» no lo son)."""
    out = []
    for trozo in re.split(r'[;,]\s*', texto or ''):
        m = re.match(r'^([A-Z]{1,3})\.(\d{2})\.(\d{2,3})([a-z])?(?:[–-]([a-z]|\d{2,3}))?', trozo.strip())
        if not m:
            continue
        z, a, n, letra, fin = m.groups()
        if fin and fin.isdigit():
            out += [f'{z}.{a}.{str(k).zfill(len(n))}' for k in range(int(n), int(fin) + 1)]
        elif fin and letra:
            out += [f'{z}.{a}.{n}{chr(c)}' for c in range(ord(letra), ord(fin) + 1)]
        else:
            out.append(f'{z}.{a}.{n}{letra or ""}')
    return out


CSS = """:root{--bg:#fbfaf7;--panel:#f3f1eb;--fg:#17171a;--mut:#5d5c58;--line:#dcd9d0;--acc:#1b365d}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15161a;--panel:#1e2026;--fg:#ecebe7;--mut:#a6a49d;--line:#33353c;--acc:#9cb8e0;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#15161a;--panel:#1e2026;--fg:#ecebe7;--mut:#a6a49d;--line:#33353c;--acc:#9cb8e0;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 Inter,system-ui,sans-serif}
.wrap{max-width:820px;margin:0 auto;padding-block:24px 60px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
a{color:var(--acc)}.top{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:14px}
.series{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);font-weight:600;margin-top:18px}
h1{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:clamp(28px,5vw,40px);color:var(--acc);margin:4px 0 2px;text-wrap:balance}
h1 i{font-style:italic}h2{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:20px;color:var(--acc);border-bottom:1px solid var(--line);padding-bottom:4px;margin:30px 0 12px}
h3{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:15px;font-weight:400;margin:18px 0 4px;scroll-margin-top:12px}
.gl{font-size:18px;color:var(--mut);margin:0 0 14px}.box{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin:14px 0}
.box p{margin:4px 0}.tblwrap{overflow-x:auto;border:1px solid var(--line);border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--panel)}td.f{font-family:"Source Serif 4",Georgia,serif;font-style:italic;font-size:16px;white-space:nowrap}
code,.m{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:13px}.note{font-size:13px;color:var(--mut)}
ul.t{columns:3 170px;padding-left:18px}ul.t li{margin:3px 0;break-inside:avoid}
ul.r{padding-left:18px;margin:6px 0}ul.r li{margin:3px 0}
footer{margin-top:40px;font-size:13px;color:var(--mut);border-top:1px solid var(--line);padding-top:10px}
.lang a{display:inline-block;text-decoration:none;font-size:13px;border:1px solid var(--line);background:var(--panel);color:var(--fg);padding:3px 9px;border-radius:6px}
.lang a[aria-current="true"]{background:var(--acc);color:var(--bg);border-color:var(--acc)}"""

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400&display=swap">'


def alternativas(ruta):
    """Enlaces hreflang de una ruta común a los dos idiomas (ruta empieza por /)."""
    return (f'<link rel="alternate" hreflang="en" href="{SITIO}{ruta}">\n'
            f'<link rel="alternate" hreflang="es" href="{SITIO}/es{ruta}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{SITIO}{ruta}">\n')


def cabecera(L, title, desc, ruta, extra=''):
    canon = f'{SITIO}{PRE[L]}{ruta}'
    viejo = f"<script>if(location.hash==='#es')location.replace('{SITIO}/es{ruta}')</script>\n" if L == 'en' else ''
    return f"""<!doctype html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
{alternativas(ruta)}<meta name="author" content="David Martín Valladolid">
<meta property="og:type" content="article"><meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}">
<meta property="og:site_name" content="iberico.martinva.org"><meta property="og:locale" content="{tr(L, 'en_GB', 'es_ES')}">
{extra}{viejo}{FONTS}
<style>{CSS}</style>
</head>
<body><div class="wrap">
<div class="top"><a href="{SITIO}{PRE[L]}/">{tr(L, '← The Iberian lead-plaque lexicon and 107 languages', '← El léxico de los plomos ibéricos ante 107 lenguas')}</a>
<span class="lang" role="group" aria-label="{tr(L, 'Language', 'Idioma')}"><a href="{SITIO}{ruta}" hreflang="en" lang="en" aria-current="{'true' if L == 'en' else 'false'}">English</a> <a href="{SITIO}/es{ruta}" hreflang="es" lang="es" aria-current="{'true' if L == 'es' else 'false'}">Español</a></span></div>
"""


def pie(L):
    return f"""<footer><p>{tr(L, 'Proposed meanings are working hypotheses graded by certainty level, not established translations. Data:', 'Los significados propuestos son hipótesis de trabajo graduadas por nivel de certeza, no traducciones establecidas. Datos:')}
<a href="https://github.com/martinva/iberian-lexicon-107-languages/tree/main/1_fuentes_lexicas/iberico/cldf">CLDF</a> ·
<a href="https://doi.org/10.5281/zenodo.24443588">{tr(L, 'article', 'artículo')}</a> ·
<a href="{SITIO}{PRE[L]}/terminos/">{tr(L, 'all terms', 'todos los términos')}</a> ·
<a href="{SITIO}{PRE[L]}/inscripciones/">{tr(L, 'inscriptions cited', 'inscripciones citadas')}</a> ·
David Martín Valladolid · <a href="https://orcid.org/0009-0003-4884-2573">ORCID</a> · CC BY 4.0</p></footer>
</div>
</body>
</html>
"""


def escribe(L, ruta, texto):
    d = os.path.join(DOCS, (PRE[L] + ruta).strip('/'))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(texto)


def herramientas():
    """Completa la cabecera de las páginas de herramientas (título, descripción y dirección canónica). Idempotente."""
    datos = {
        'mapa-3d': ('Mapa en 3D del léxico de los plomos ibéricos: distancias entre 36 lenguas',
                    'Proyección en tres ejes de la matriz de distancias léxicas entre el ibérico de los plomos y 35 lenguas. El euskera es el vecino más próximo del ibérico.'),
        'proximidad': ('Proximidad léxica de los plomos ibéricos: diana y umbral entre 36 lenguas',
                       'Herramienta interactiva: pon cualquier lengua en el centro y mira las demás a su distancia léxica real. El ibérico de los plomos y el euskera son vecinos mutuos.'),
        'quitar-palabras': ('Iberian and Basque tested: remove words and watch the result',
                            'Interactive tool: remove any of the 40 Iberian units (for instance the proposed Latin loans) and see how the value of each of 32 languages changes. Basque stays first.'),
    }
    for carpeta, (titulo, desc) in datos.items():
        f = os.path.join(DOCS, 'herramientas', carpeta, 'index.html')
        s = open(f, encoding='utf-8').read()
        s = re.sub(r'\n<meta name="description"[^>]*>\n<link rel="canonical"[^>]*>', '', s, count=1)
        nuevo = (f'<title>{e(titulo)}</title>\n<meta name="description" content="{e(desc)}">\n'
                 f'<link rel="canonical" href="{SITIO}/herramientas/{carpeta}/">')
        s, n = re.subn(r'<title>[^<]*</title>', lambda m: nuevo, s, count=1)
        assert n == 1, carpeta
        open(f, 'w', encoding='utf-8').write(s)


def main():
    params = OrderedDict((r['ID'], r) for r in csv.DictReader(open(os.path.join(CLDF, 'parameters.csv'), encoding='utf-8')))
    formas = {}
    for r in csv.DictReader(open(os.path.join(CLDF, 'forms.csv'), encoding='utf-8')):
        formas.setdefault(r['Parameter_ID'], []).append(r)

    # primera pasada: datos de cada unidad
    U, usados = OrderedDict(), set()
    for pid, p in params.items():
        fs = formas.get(pid, [])
        if not fs:
            continue
        s = slug(fs[0]['Form'])
        if s in usados:
            s = f'{s}-{pid.lower()}'
        usados.add(s)
        ins = []
        for f in fs:
            for x in siglas(f['Inscripciones']):
                if x not in ins:
                    ins.append(x)
        U[pid] = dict(p=p, fs=fs, slug=s, nombre=fs[0]['Form'], formas=' / '.join(f['Form'] for f in fs), ins=ins,
                      niveles=sorted({f['Grado'] for f in fs}), grupo=fs[0]['Grupo'], campo=p['Campo'])
    INS = OrderedDict()
    for pid, u in U.items():
        for x in u['ins']:
            INS.setdefault(x, []).append(pid)

    def enlace(L, pid):
        u = U[pid]
        gl = u['p']['Terminos_en'] if L == 'en' else u['p']['Terminos_es']
        return f'<a href="{SITIO}{PRE[L]}/terminos/{u["slug"]}/"><i>{e(u["formas"])}</i></a> <span class="note">{tr(L, "‘" + e(gl) + "’", "«" + e(gl) + "»")}</span>'

    rutas = []
    for pid, u in U.items():
        p, fs, s = u['p'], u['fs'], u['slug']
        ruta = f'/terminos/{s}/'
        rutas.append(ruta)
        niv = ', '.join(u['niveles'])
        mismo_campo = [q for q in U if q != pid and U[q]['campo'] == u['campo']]
        mismas_ins = [q for q in U if q != pid and set(U[q]['ins']) & set(u['ins'])]
        for L in IDIOMAS:
            gl = p['Terminos_en'] if L == 'en' else p['Terminos_es']
            campo = CAMPO.get(u['campo'], u['campo']) if L == 'en' else u['campo']
            grupo = GRUPO.get(u['grupo'], u['grupo']) if L == 'en' else u['grupo']
            title = tr(L, f"Iberian {u['formas']}: proposed meaning ‘{gl}’ — lead-plaque lexicon",
                       f"Ibérico {u['formas']}: significado propuesto «{gl}» — léxico de los plomos")
            desc = tr(L, f"Iberian {u['formas']}: proposed meaning ‘{gl}’ (certainty level {niv}), inscriptions where it occurs, supporting evidence and sources. One of the 40 Iberian units compared with 107 languages.",
                      f"Ibérico {u['formas']}: significado propuesto «{gl}» (nivel de certeza {niv}), inscripciones en que aparece, apoyo y fuentes. Una de las 40 unidades ibéricas comparadas con 107 lenguas.")
            ld = {"@context": "https://schema.org", "@type": "DefinedTerm", "name": u['nombre'],
                  "alternateName": [f['Form'] for f in fs[1:]],
                  "description": tr(L, f"Proposed meaning: {gl}", f"Significado propuesto: {gl}"),
                  "inDefinedTermSet": {"@type": "DefinedTermSet", "name": "Iberian lead-plaque lexicon (CLDF)",
                                       "url": "https://github.com/martinva/iberian-lexicon-107-languages"},
                  "url": f'{SITIO}{PRE[L]}{ruta}', "inLanguage": "xib"}
            extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'

            def ins_html(txt):
                out = e(txt or '—')
                for x in sorted(set(siglas(txt)), key=len, reverse=True):
                    out = out.replace(e(x), f'<a href="{SITIO}{PRE[L]}/inscripciones/#{slug(x)}">{e(x)}</a>', 1)
                return out

            filas = ''.join(
                f"<tr><td class='f'>{e(f['Form'])}</td><td class='m'>{e(f['Segments'])}</td><td class='m'>{e(f['Grado'])}</td>"
                f"<td class='m'>{ins_html(f['Inscripciones'])}</td><td>{e(f['Apoyo'])}</td><td>{fuentes_html(f['Source'], L)}</td></tr>"
                for f in fs)
            rel = ''
            if mismas_ins:
                rel += f"<p><b>{tr(L, 'Cited in the same inscriptions', 'Citadas en las mismas inscripciones')}:</b></p><ul class='r'>" + ''.join(f'<li>{enlace(L, q)}</li>' for q in mismas_ins) + '</ul>'
            if mismo_campo:
                rel += f"<p><b>{tr(L, 'Same semantic field', 'Mismo campo')} ({e(campo)}):</b></p><ul class='r'>" + ''.join(f'<li>{enlace(L, q)}</li>' for q in mismo_campo) + '</ul>'
            apoyo_nota = '' if L == 'es' else '<p class="note">The supporting evidence is given in Spanish, as in the dataset.</p>'
            cuerpo = f"""<div class="series">{tr(L, 'Iberian', 'Ibérico')} · {e(grupo)}</div>
<h1><i>{e(u['formas'])}</i></h1>
<p class="gl">{tr(L, 'Proposed meaning: ‘' + e(gl) + '’', 'Significado propuesto: «' + e(gl) + '»')}</p>
<div class="box">
<p><b>{tr(L, 'Certainty level', 'Nivel de certeza')}:</b> <span class="m">{e(niv)}</span> — {e(nivel_txt('/'.join(u['niveles']), L))}</p>
<p><b>{tr(L, 'Semantic field', 'Campo')}:</b> {e(campo)} · <b>{tr(L, 'Unit', 'Unidad')}:</b> <span class="m">{e(pid)}</span></p>
</div>
<h2>{tr(L, 'Forms', 'Formas')}</h2>
<div class="tblwrap"><table><thead><tr><th>{tr(L, 'Form', 'Forma')}</th><th>{tr(L, 'Segments', 'Segmentos')}</th><th>{tr(L, 'Level', 'Nivel')}</th><th>{tr(L, 'Inscriptions', 'Inscripciones')}</th><th>{tr(L, 'Support', 'Apoyo')}</th><th>{tr(L, 'Source', 'Fuente')}</th></tr></thead>
<tbody>{filas}</tbody></table></div>
{apoyo_nota}<p class="note">{tr(L, 'Inscriptions are cited by their Hesperia / MLH reference; the texts can be consulted in the', 'Las inscripciones se citan por su sigla de Hesperia / MLH; los textos pueden consultarse en el')} <a href="https://hesperia.ucm.es/">Banco de datos Hesperia</a>.
{tr(L, 'Transcription: Hesperia system (dual script not distinguished in the forms).', 'Transcripción: sistema de Hesperia (sin distinguir la escritura dual en las formas).')}</p>
<h2>{tr(L, 'In the statistical comparison', 'En la comparación estadística')}</h2>
<p>{tr(L, 'This unit is one of the 40 Iberian units compared with 107 languages. See the article, the tool to remove words and the full inventory.', 'Esta unidad es una de las 40 unidades ibéricas comparadas con 107 lenguas. Véanse el artículo, la herramienta para quitar palabras y el inventario completo.')}</p>
<p><a href="https://doi.org/10.5281/zenodo.24443588">{tr(L, 'Article', 'Artículo')}</a> · <a href="{SITIO}/herramientas/quitar-palabras/">{tr(L, 'Remove words', 'Quitar palabras')}</a> · <a href="{SITIO}{PRE[L]}/#inventory">{tr(L, 'Inventory', 'Inventario')}</a> · <a href="{SITIO}{PRE[L]}/terminos/">{tr(L, 'All terms', 'Todos los términos')}</a></p>
<h2>{tr(L, 'Related terms', 'Términos relacionados')}</h2>
{rel}
"""
            escribe(L, ruta, cabecera(L, title, desc, ruta, extra) + cuerpo + pie(L))

    # índice de términos
    for L in IDIOMAS:
        items = OrderedDict()
        for pid, u in U.items():
            items.setdefault(u['grupo'], []).append(f"<li>{enlace(L, pid)} <span class='note'>· {e('/'.join(u['niveles']))}</span></li>")
        secc = ''.join(f"<h2>{e(GRUPO.get(g, g) if L == 'en' else g).capitalize()}</h2><ul class='t'>{''.join(v)}</ul>" for g, v in items.items())
        cuerpo = f"""<div class="series">{tr(L, 'Iberian lexicon · CLDF', 'Léxico ibérico · CLDF')}</div>
<h1>{tr(L, 'Iberian terms compared', 'Términos ibéricos comparados')}</h1>
<p class="gl">{tr(L, f'The {len(U)} units of the comparison, with their forms, proposed meaning and certainty level.', f'Las {len(U)} unidades de la comparación, con sus formas, significado propuesto y nivel de certeza.')}</p>
{secc}"""
        escribe(L, '/terminos/', cabecera(L, tr(L, 'Iberian terms compared: the lead-plaque lexicon (CLDF)', 'Términos ibéricos comparados: el léxico de los plomos (CLDF)'),
                                          tr(L, f'Index of the {len(U)} Iberian units of the lead-plaque lexicon compared with 107 languages: forms, proposed meanings and certainty levels.',
                                             f'Índice de las {len(U)} unidades ibéricas del léxico de los plomos comparadas con 107 lenguas: formas, significados propuestos y niveles de certeza.'),
                                          '/terminos/') + cuerpo + pie(L))

    # inscripciones citadas
    for L in IDIOMAS:
        bloques = []
        for x in sorted(INS, key=lambda s: (re.match(r'[A-Z]+', s).group(), s)):
            z = ZONA.get(re.match(r'[A-Z]+', x).group())
            zona = f" <span class='note'>· {e(z[1] if L == 'en' else z[0])}</span>" if z else ''
            bloques.append(f"<h3 id='{slug(x)}'>{e(x)}{zona}</h3><ul class='r'>" + ''.join(f'<li>{enlace(L, q)}</li>' for q in INS[x]) + '</ul>')
        cuerpo = f"""<div class="series">{tr(L, 'Iberian lexicon · CLDF', 'Léxico ibérico · CLDF')}</div>
<h1>{tr(L, 'Iberian inscriptions cited', 'Inscripciones ibéricas citadas')}</h1>
<p class="gl">{tr(L, f'The {len(INS)} inscriptions cited by reference in the inventory, each with the units of the comparison attested in it.', f'Las {len(INS)} inscripciones citadas por su sigla en el inventario, cada una con las unidades de la comparación que se documentan en ella.')}</p>
<p class="note">{tr(L, 'References follow the Hesperia database; the first letters of a reference indicate the province or département of the find. The texts are not reproduced here: they can be consulted in the', 'Las siglas son las del Banco de datos Hesperia; las letras iniciales indican la provincia o el departamento del hallazgo. Los textos no se reproducen aquí: pueden consultarse en el')} <a href="https://hesperia.ucm.es/">Banco de datos Hesperia</a>. {tr(L, 'Units whose attestations are given only as a count (for instance “10 inscriptions”) are not listed.', 'No figuran las unidades cuyas atestiguaciones se dan solo como recuento (por ejemplo, «10 inscripciones»).')}</p>
{''.join(bloques)}"""
        escribe(L, '/inscripciones/', cabecera(L, tr(L, 'Iberian inscriptions cited in the lead-plaque lexicon', 'Inscripciones ibéricas citadas en el léxico de los plomos'),
                                               tr(L, f'The {len(INS)} Iberian inscriptions (lead plaques and others) cited by their Hesperia reference, with the lexical units attested in each.',
                                                  f'Las {len(INS)} inscripciones ibéricas (plomos y otras) citadas por su sigla de Hesperia, con las unidades léxicas documentadas en cada una.'),
                                               '/inscripciones/') + cuerpo + pie(L))

    herramientas()

    # sitemap con alternativas de idioma
    dobles = [('/', '1.0'), ('/terminos/', '0.8'), ('/inscripciones/', '0.6')] + [(r, '0.6') for r in rutas]
    sueltas = [('/herramientas/quitar-palabras/', '0.7'), ('/herramientas/proximidad/', '0.6'), ('/herramientas/mapa-3d/', '0.5'), ('/herramientas/mapa-provincias/', '0.5')]
    lin = []
    for r, pr in dobles:
        alt = (f'<xhtml:link rel="alternate" hreflang="en" href="{SITIO}{r}"/><xhtml:link rel="alternate" hreflang="es" href="{SITIO}/es{r}"/>'
               f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITIO}{r}"/>')
        for L in IDIOMAS:
            lin.append(f' <url><loc>{SITIO}{PRE[L]}{r}</loc>{alt}<lastmod>{FECHA}</lastmod><priority>{pr}</priority></url>')
    lin += [f' <url><loc>{SITIO}{r}</loc><lastmod>{FECHA}</lastmod><priority>{pr}</priority></url>' for r, pr in sueltas]
    with open(os.path.join(DOCS, 'sitemap.xml'), 'w', encoding='utf-8') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                 + '\n'.join(lin) + '\n</urlset>\n')
    print(f'{len(U)} unidades x 2 idiomas; {len(INS)} inscripciones citadas; sitemap con {len(lin)} URL')


if __name__ == '__main__':
    main()
