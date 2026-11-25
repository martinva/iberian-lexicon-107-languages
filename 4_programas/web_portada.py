#!/usr/bin/env python3
"""Genera la portada de la web en sus dos direcciones, una por idioma, desde una sola plantilla.

  inglés   docs/index.html      https://iberico.martinva.org/
  español  docs/es/index.html   https://iberico.martinva.org/es/

La plantilla (4_programas/web_portada_plantilla.html) lleva los dos idiomas marcados con data-l="en" y
data-l="es". Aquí se deja en cada página solo su idioma, con su título, su descripción, su dirección
canónica y los enlaces hreflang entre las dos. Uso: python3 4_programas/web_portada.py
"""
import os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(RAIZ, 'docs')
SITIO = 'https://iberico.martinva.org'
PRE = {'en': '', 'es': '/es'}

TXT = {
    'en': dict(
        title='The Iberian lead-plaque lexicon and 107 languages: Basque ranks first',
        desc='Statistical comparison of Iberian with 107 languages: by sound profile and by proposed meanings, Basque is the closest. Article, open data (CLDF) and tools.',
        ogtitle='The Lexicon of the Iberian Lead Plaques Compared with 107 Languages',
        ogdesc='Blind to any proposed translation, the language whose sound profile is closest to the Iberian corpus among 107 is Basque. Open data, programs and audits.',
        ogimg='figura_1_v48_dos_pruebas_en.png', loc='en_GB', alt='es_ES'),
    'es': dict(
        title='El léxico de los plomos ibéricos ante 107 lenguas: el euskera, primero',
        desc='Comparación estadística del ibérico con 107 lenguas: por perfil de sonidos y por significados propuestos, la más próxima es el euskera. Artículo, datos abiertos y herramientas.',
        ogtitle='El léxico de los plomos ibéricos ante 107 lenguas',
        ogdesc='A ciegas respecto a cualquier traducción propuesta, la lengua de perfil de sonidos más próximo al corpus ibérico entre 107 es el euskera. Datos abiertos, programas y auditorías.',
        ogimg='figura_1_v48_dos_pruebas.png', loc='es_ES', alt='en_GB'),
}
CITA_ES = '''<meta name="citation_title" content="El léxico de los plomos ibéricos ante 107 lenguas: una comparación estadística en la que el euskera ocupa el primer lugar">
<meta name="citation_author" content="Martín Valladolid, David">
<meta name="citation_author_orcid" content="0009-0003-4884-2573">
<meta name="citation_publication_date" content="2026/11/22">
<meta name="citation_publisher" content="Zenodo">
<meta name="citation_doi" content="10.5281/zenodo.24443588">
<meta name="citation_language" content="es">
<meta name="citation_abstract_html_url" content="https://doi.org/10.5281/zenodo.24443588">
'''


def cambia(s, viejo, nuevo, n=1):
    assert s.count(viejo) == n, (viejo[:60], s.count(viejo))
    return s.replace(viejo, nuevo)


def re_cambia(s, patron, nuevo, flags=0):
    s2, k = re.subn(patron, lambda m: nuevo, s, count=1, flags=flags)
    assert k == 1, patron[:60]
    return s2


def pagina(P, L):
    t = TXT[L]; otro = 'es' if L == 'en' else 'en'; canon = f'{SITIO}{PRE[L]}/'
    s = P
    s = cambia(s, '<html lang="en">', f'<html lang="{L}">')
    s = re_cambia(s, r'<title>[^<]*</title>', f'<title>{t["title"]}</title>')
    s = re_cambia(s, r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{t["desc"]}">')
    s = cambia(s, '<link rel="canonical" href="https://iberico.martinva.org/">', f'<link rel="canonical" href="{canon}">')
    if L == 'es':
        s = re_cambia(s, r'<meta name="citation_title".*?<meta name="citation_abstract_html_url"[^>]*>\n', CITA_ES, re.S)
    s = re_cambia(s, r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{t["ogtitle"]}">')
    s = re_cambia(s, r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{t["ogdesc"]}">')
    s = cambia(s, '<meta property="og:url" content="https://iberico.martinva.org/">', f'<meta property="og:url" content="{canon}">')
    s = re_cambia(s, r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{SITIO}/img/{t["ogimg"]}">')
    s = cambia(s, '<meta property="og:locale" content="en_GB">', f'<meta property="og:locale" content="{t["loc"]}">')
    s = cambia(s, '<meta property="og:locale:alternate" content="es_ES">', f'<meta property="og:locale:alternate" content="{t["alt"]}">')
    s = cambia(s, '<link rel="alternate" hreflang="en" href="https://iberico.martinva.org/#en">\n<link rel="alternate" hreflang="es" href="https://iberico.martinva.org/#es">',
               f'<link rel="alternate" hreflang="en" href="{SITIO}/">\n<link rel="alternate" hreflang="es" href="{SITIO}/es/">\n<link rel="alternate" hreflang="x-default" href="{SITIO}/">')
    # selector de idioma: enlaces en lugar de botones
    s = cambia(s, '.lang button{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--panel);color:var(--fg);padding:4px 10px;border-radius:6px;cursor:pointer}',
               '.lang a{display:inline-block;text-decoration:none;font-size:13px;border:1px solid var(--line);background:var(--panel);color:var(--fg);padding:4px 10px;border-radius:6px}')
    s = cambia(s, '.lang button[aria-pressed="true"]{', '.lang a[aria-current="true"]{')
    s = re_cambia(s, r' <div class="lang" role="group" aria-label="Language">.*?</div>\n',
                  f' <div class="lang" role="group" aria-label="{"Language" if L == "en" else "Idioma"}">\n'
                  f'  <a href="/" hreflang="en" lang="en" aria-current="{"true" if L == "en" else "false"}">English</a>\n'
                  f'  <a href="/es/" hreflang="es" lang="es" aria-current="{"true" if L == "es" else "false"}">Español</a>\n </div>\n', re.S)
    # cuerpo estático: solo el idioma de la página
    i = s.index('<body>'); j = s.index('<script>\n(function(){')
    cuerpo = s[i:j]
    cuerpo = re.sub(r'<(span|p|th)\b[^>]*\sdata-l="%s"[^>]*>.*?</\1>' % otro, '', cuerpo, flags=re.S)
    cuerpo = re.sub(r'\s*<img data-l="%s"[^>]*>' % otro, '', cuerpo)
    assert f'data-l="{otro}"' not in cuerpo
    cuerpo = cuerpo.replace('href="herramientas/', 'href="/herramientas/').replace('src="img/', 'src="/img/')
    cuerpo = cambia(cuerpo, '<a href="terminos/">', f'<a href="{PRE[L]}/terminos/">')
    cuerpo = cambia(cuerpo, '</a></p>\n\n<h2 id="check">',
                    f'</a> · <a href="{PRE[L]}/inscripciones/">{"inscriptions cited" if L == "en" else "inscripciones citadas"}</a></p>\n\n<h2 id="check">')
    cuerpo = cuerpo.replace('placeholder="Search form, meaning or inscription…" aria-label="Search"',
                            'placeholder="Search form, meaning or inscription…" aria-label="Search"' if L == 'en' else 'placeholder="Buscar forma, significado o inscripción…" aria-label="Buscar"')
    guion = s[j:]
    guion = cambia(guion, "fetch('data/inventory.json')", "fetch('/data/inventory.json')")
    guion = cambia(guion, "<a href=\"'+esc(d.page)+'\">", "<a href=\"'+esc('%s/'+d.page)+'\">" % PRE[L])
    guion = re_cambia(guion, r" function set\(l\)\{.*?\n btns\.forEach\(function\(b\)\{b\.addEventListener\('click',function\(\)\{set\(b\.dataset\.set\)\}\)\}\);\n",
                      " labels();\n" + (" if(location.hash==='#es')location.replace('/es/');\n" if L == 'en' else ''), re.S)
    guion = cambia(guion, "var html=document.documentElement,btns=document.querySelectorAll('.lang button');", "var html=document.documentElement;")
    return s[:i] + cuerpo + guion


if __name__ == '__main__':
    P = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web_portada_plantilla.html'), encoding='utf-8').read()
    for L in ('en', 'es'):
        d = os.path.join(DOCS, PRE[L].strip('/')); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(pagina(P, L))
        print(L, os.path.join(d, 'index.html'))
