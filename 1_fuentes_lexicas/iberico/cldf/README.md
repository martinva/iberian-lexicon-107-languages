# Léxico ibérico con significado propuesto (formato CLDF)

Conjunto de datos del artículo «El léxico de los plomos ibéricos ante 107 lenguas: una comparación estadística en la que el euskera ocupa el primer lugar». Módulo CLDF: Wordlist.

| Archivo | Contenido |
|---|---|
| `languages.csv` | Una lengua: ibérico |
| `parameters.csv` | Significados propuestos, con los términos de búsqueda en castellano e inglés usados en la prueba con significados |
| `forms.csv` | Formas ibéricas, con segmentos, clases de sonidos SCA, grupo, grado de certeza, procedencia del significado (según el autor y según el jurado ciego), fuente, inscripciones y apoyo |
| `orthography_iberico.tsv` | Paso de la transcripción a segmentos y a clases SCA |
| `sources.bib` | Fuentes |

Avisos:
- Los significados son propuestas. El grado indica su firmeza: A, valor asegurado por la metrología o por la bibliografía; B, regularidad documentada en un texto o grupo de textos; C, hipótesis de trabajo.
- Los segmentos siguen una convención: el valor fonético exacto de *ś*, *ŕ*, *r* y *ḿ* se discute.
- No se incluyen textos de inscripciones. Las formas proceden de la transcripción de Hesperia, Banco de datos de lenguas paleohispánicas, que debe consultarse para el contexto.
- Procedencia del significado (diseño contra la circularidad): `Procedencia_autor` sigue la tabla 5 de la Monografía IV y el anexo D.3 del artículo (I, propuesta anterior de terceros o valor con apoyo externo; II, propuesta de las monografías por la casilla documental; III, convergente, o en los numerales valor asignado por la posición en la serie). `Procedencia_jurado` es la clasificación menos favorable del jurado ciego (artículo, apartado 8.4; `2_criterios/jurado/respuestas/cruce_con_la_clave.tsv`): I, prueba material externa o contexto sin otra lectura; II, distribución documental; III, requiere un parecido con otra lengua; vacío en los cuatro numerales no sometidos al jurado. Las dos codificaciones se publican tal como se registraron; la reclasificación posterior de A7, A17 y A18 (declaración 16) afecta a la señal de paralelo vasco, no al nivel.
- Estado: validado con la herramienta oficial de CLDF (`cldf validate`, pycldf) en cada cambio, mediante el flujo de GitHub Actions `.github/workflows/cldf.yml`.
