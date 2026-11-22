# Fuentes léxicas

Todos los datos que usan los programas están en esta carpeta. Para cada fuente se indica de dónde procede, qué archivo se usa y si es una copia de la fuente pública o un archivo derivado de ella. **Para una réplica independiente se recomienda empezar por las fuentes públicas**, obtenidas de su origen, y usar los archivos derivados solo como comprobación.

El tratamiento de cada archivo (qué líneas se usan y cómo) está en `5_especificacion/ESPECIFICACION_FUNCIONAL_es.md`, apartado 1.

## Ibérico (`iberico/`)

| Archivo | Contenido | Origen | Tipo |
|---|---|---|---|
| `unidades_plomos.json` | 30 unidades de los plomos: formas, significado propuesto, términos | Monografías I–IV del autor | Propio |
| `unidades_numerales.json` | Serie numeral: 10 unidades | Orduña (2005); Ferrer i Jané (2009, 2022) | Propio, sobre la bibliografía |
| `cldf/` | Las 40 unidades (serie numeral y plomos) en formato CLDF, módulo Wordlist: formas, segmentos, clases de sonidos, grado, fuente | Los dos archivos anteriores | Propio; mismo contenido que los dos archivos JSON, en el formato de intercambio de la lingüística comparada |
| `hesperia_iberico_1599.csv` | Texto de las 1.599 inscripciones ibéricas auténticas | Hesperia, Banco de datos de lenguas paleohispánicas (hesperia.ucm.es), consulta del 7-11-2026 | **No se redistribuye.** Lo genera `descargar_hesperia.py` (abajo) |
| `hesperia_metadatos.csv` | Soporte, material, signario, yacimiento y datación de cada ficha | Hesperia, consulta del 12-11-2026 | **No se redistribuye.** Lo genera `descargar_hesperia.py`, con las columnas normalizadas |
| `hesperia_formas_reducidas.json` | Edición pública: formas reducidas a clases de sonidos de cada ficha, con sigla, zona, plomo y signario; sin el texto | Derivado de los dos archivos anteriores con `ibcomp.fuentes.hesperia()` | Lista mínima; los programas la usan si faltan los archivos de Hesperia |
| `descargar_hesperia.py` | Programa que descarga de Hesperia los dos archivos anteriores y comprueba que coinciden, byte a byte (SHA-256), con los usados en el artículo | Propio | Solo biblioteca estándar de Python 3; unos 40 minutos con pausas de cortesía. `python3 descargar_hesperia.py` desde esta carpeta; `--solo-listado` para el primer archivo; `--cache DIR` guarda el HTML crudo; `--verificar` comprueba las sumas de archivos ya presentes |
| `lexico_mlh_v2_clasificacion.csv` | Clase de cada forma (nombre personal, marca, leyenda monetal, etc.) | Moncunill y Velaza (2019), *Monumenta Linguarum Hispanicarum* V.2 | Derivado: forma y clasificación; solo se usa en las tablas 1 y 2 |
| `formantes_onomasticos_rodriguez_ramos_2014.json` | Lista de formantes de nombres personales | Rodríguez Ramos (2014), *ArqueoWeb* 15 | Derivado: lista de formantes |

## Clases de sonidos (`clases_sca/`)

| Archivo | Contenido | Origen | Tipo |
|---|---|---|---|
| `converter`, `INFO` | Tabla símbolo fonético → clase del modelo SCA | LingPy (List 2012) | Copia sin modificar |

## Wikcionario (`wikcionario/`)

Entradas del Wikcionario inglés, obtenidas de la extracción pública de kaikki.org. Licencia de origen: CC BY-SA.

| Archivo | Contenido | Fecha de extracción |
|---|---|---|
| `kaikki_control_20lenguas_2026-11-17.tsv` | Lengua, palabra, categoría y glosa de 20 lenguas | 17-11-2026 |
| `kaikki_control_silaba_simple_16lenguas_2026-11-18.tsv` | Lo mismo, 16 lenguas más | 18-11-2026 |
| `kaikki_formas_26lenguas_2026-11-18.tsv.gz` | Formas flexionadas de cada lema (comprimido; los programas lo leen directamente) | 18-11-2026 |
| `kaikki_lenguas_de_control_2026-11-19.tsv` | Umbro, gótico, córnico, dálmata, etrusco y sumerio, con romanización y glosas | 19-11-2026 |
| `wikcionario_eu_en_v1.csv`, `wikcionario_eu_formas_verbales_v1.csv` | Entradas vascas con etimología; formas verbales vascas | 17 y 18-11-2026 |

La columna `etimologia` de `wikcionario_eu_en_v1.csv` (nota etimológica del Wikcionario inglés, 5.513 lemas con nota) la usa solo `t27_etimologia_vasca.py` (entrada 11 de las declaraciones), con la regla de clasificación fijada en la especificación 4.24. Las notas son de calidad desigual y algunas mencionan el ibérico; esa mención no se usa.

Tipo: derivado. De cada entrada de kaikki.org se conservan solo los campos indicados.

## Otras fuentes del euskera (`euskera/`)

| Archivo | Contenido | Origen | Tipo |
|---|---|---|---|
| `azkue_lemas_equivalentes.csv` (edición pública; en el repositorio de trabajo, `azkue_abbyy_v2.csv`) | Lema y equivalentes castellanos (lista mínima) | Azkue (1905-1906), *Diccionario vasco-español-francés*; reimpresión de Euskaltzaindia (1984), edición digital | Derivado: obtenido del texto reconocido automáticamente; puede contener errores de lectura |
| `trask_formas_glosas.json` (edición pública; en el repositorio de trabajo, `trask_lexico_nativo_derivado.json`) | Formas reconstruidas y glosas (lista mínima) | Trask (2008), «The Native Lexicon» | Derivado. Se usan las formas sin vocal ni consonante indeterminada (`V`, `C`): 391. El resto de notaciones del derivado (corchetes, variantes) no se ha cotejado de nuevo con la obra |
| `opendata_euskadi_eu_es_v1.tsv` | Léxico euskera–castellano | Open Data Euskadi (Gobierno Vasco), descarga del 18-11-2026; CC BY 4.0 | Derivado: dos columnas del archivo original |

## WordNet (`wordnet_mcr/`)

Multilingual Central Repository 3.0 (Gonzalez-Agirre, Laparra y Rigau 2012), en la distribución de Open Multilingual WordNet. Archivos del euskera, castellano, catalán y gallego. CC BY 3.0. Copia sin modificar.

## Apertium (`apertium/`)

Diccionarios bilingües de 19 pares de lenguas, del repositorio público de Apertium (github.com/apertium). Licencia GPL. Copia sin modificar de cada archivo `.dix`. La lista de archivos usados está en `_archivos_usados.json`.

## NorthEuraLex (`northeuralex/`)

Dellert y otros (2020), edición de Lexibank (github.com/lexibank/northeuralex). CC BY 4.0. Archivos `forms.csv` y `languages.csv`, sin modificar.

## Numerales (`numerales_chan/`)

Chan (2019), *Numeral Systems of the World's Languages*, edición CLDF de Numeralbank (github.com/numeralbank/channumerals). CC BY 4.0. Archivos `forms.csv` y `languages.csv`, sin modificar.

## Prestabilidad de los significados (`wold_prestabilidad_35_unidades.csv`)

Haspelmath y Tadmor (eds.) (2009), *World Loanword Database* (WOLD), edición CLDF de Lexibank (github.com/lexibank/wold), archivo `cldf/parameters.csv`, columna `Borrowed_score`. CC BY 4.0. Archivo derivado: 35 filas (unidad, identificador y nombre del significado en WOLD, puntuación), copiadas a mano el 21-11-2026 para los significados de la lista central que corresponden a las unidades; la correspondencia unidad–significado se fijó y publicó antes de calcular (`resultados/DECLARACIONES_PREVIAS.md`, entrada 9).
