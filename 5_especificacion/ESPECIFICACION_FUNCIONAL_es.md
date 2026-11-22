# Especificación funcional detallada

**Comparación matemática del léxico de los plomos ibéricos con el de otras lenguas. Modelo final.**

Este documento describe, sin recurrir al código, todo lo necesario para rehacer los cálculos del estudio: qué datos se usan, cómo se preparan, qué reglas se aplican y qué hace cada programa. Quien lo siga con cualquier lenguaje de programación debe obtener los mismos resultados, con la salvedad indicada en el apartado 0.4.

Cada apartado remite al archivo de `4_programas/` que lo implementa. Los nombres de funciones entre paréntesis son los del paquete `ibcomp`.

---

## 0. Convenciones generales

### 0.1 Vocabulario

- **Forma:** una palabra tal como aparece en una fuente.
- **Forma reducida:** la misma palabra convertida en una cadena de *clases de sonidos* (apartado 2). Todas las comparaciones se hacen entre formas reducidas.
- **Unidad:** un significado propuesto para el ibérico, con una o varias formas ibéricas que lo expresan y una lista de *términos* (palabras castellanas e inglesas que lo traducen).
- **Diccionario:** una fuente de otra lengua, convertida en una tabla «forma reducida → conjunto de significados».
- **Candidatas** de una unidad en un diccionario: las formas del diccionario cuyo significado coincide con alguno de los términos de la unidad.

### 0.2 Codificación

Todos los archivos de texto están en UTF-8. Antes de comparar caracteres se aplica la normalización Unicode que se indica en cada regla (NFC o NFD).

### 0.3 Longitud admitida

Salvo que se diga otra cosa, una forma reducida se admite si tiene entre 2 y 12 símbolos. Las más cortas o más largas se descartan. La excepción son los numerales de Chan (apartado 1.8), que no llevan este límite.

### 0.4 Azar y reproducibilidad

Varias pruebas comparan un valor observado con los obtenidos en *sorteos*. Cada cálculo usa su propio generador de números al azar, cuya semilla es el texto `20261120|<prueba>|<conjunto>|<diccionario>` (`pruebas.generador`). Así el resultado no depende del orden en que se ejecuten los programas.

Con el generador *Mersenne Twister* de Python y esa semilla, los resultados son idénticos de una ejecución a otra. Con otro generador, los valores que dependen de sorteos (los valores *z*) variarán en torno a media unidad; los que no dependen de sorteos (distancias reales, puestos en el perfil de sonidos, serie numeral) deben coincidir exactamente.

Hay tres excepciones, en las que se conserva la semilla numérica del cálculo original para obtener las mismas muestras: la muestra de 400 lenguas de la tabla 5 (semilla 20261118), las muestras de palabras de las lenguas de control (apartado 4.6) y los sorteos de conceptos del Anexo A.3 (apartado 4.15). Y hay un segundo generador: las permutaciones de 4.11 usan el generador de NumPy (`default_rng`, PCG64), sembrado con 63 bits tomados del generador de texto; la variante condicionada por la longitud consume el mismo generador a continuación de las 100.000 permutaciones libres, sin semilla propia.

Los valores *z* se calculan y se ordenan sin redondear; en pantalla y en el artículo se dan con dos decimales. Excepciones en los archivos de resultados: 4.10 (`t15`) guarda sus resúmenes con dos decimales; 4.13 (`t19`), 4.17 (`t20`) y 4.18 (`t21`) guardan las tablas por lengua con tres decimales, y el resumen de 4.13 (medianas y extremos) también con tres, calculados desde los valores de tres decimales de los registros, de modo que el artículo redondea una sola vez desde ahí. En 4.13 y 4.17 las ordenaciones y los recuentos de «primera lengua» se hacen a precisión completa, antes de redondear; los archivos conservan tres decimales. Programas añadidos: 4.20 (`t24`) guarda sus valores con dos decimales; 4.23 (`t26`) guarda los z individuales con tres y la correlación sin redondear; 4.24 (`t27`) guarda las distancias con tres. Un nulo se considera constante cuando su recorrido (máximo − mínimo) no supera 10⁻¹² · max(1, max|nulo|): el suelo 1 evita que un vector de valores minúsculos pase por variable. Los casos límite (nulo constante, z no definido y sus consumidores, incluidos los agregados de `t15`, la correlación de `t26` con menos de tres parejas y la segunda lengua de `t24`) se comprueban con `4_programas/casos_limite.py`; los archivos JSON solo contienen números finitos o null. Las probabilidades se guardan sin redondear; en el artículo se dan con los decimales necesarios para que la comparación con 0,05 no dependa del redondeo.

La prueba 3.2 se detiene con un error si, en algún sorteo, el diccionario no tiene palabras suficientes de una longitud para sustituir sin repetición. El valor *z* no se calcula (queda vacío) si los sorteos son constantes: desviación típica cero o recorrido (máximo menos mínimo) no mayor que 10⁻¹² × max(1, mayor valor absoluto del nulo) —la misma regla con suelo 1 que se da arriba—, para que un vector de valores iguales con residuo de coma flotante no produzca un *z* espurio. Un *z* vacío se trata así en cada programa: en 4.10 (`t15`) la lengua sin *z* no entra en la ordenación y, si es el euskera, el puesto queda vacío; en 4.11 (`t16`) el diccionario sin *z* se excluye de la ordenación y del resumen; en 4.16 (`t17`) se imprime «None» y la lengua no entra en los techos; en 4.23 (`t26`) la lengua sin ρ calculable se conserva en la tabla, se cuenta en `sin_rho` y no entra en mediana ni extremos; en los agregados de 4.10 (a), si ningún caso tiene *z* definido, los agregados quedan vacíos (null). Las probabilidades se guardan sin redondear, junto con el número de sorteos iguales o menores que el valor real.

### 0.5 Convenciones de detalle

Fijadas a raíz de una réplica independiente hecha a ciegas, que las señaló como ambiguas. Ninguna cambia un puesto; algunas cambian recuentos.

| Punto | Convención |
|---|---|
| Semillas | El texto de la semilla es `20261120` seguido de las claves del cálculo, unidas por `\|`. Prueba con significados: `20261120\|significados\|<conjunto>\|<nombre del diccionario>`. Las claves literales de cada cálculo constan en su programa. Una réplica con otras claves u otro orden de sorteo dará valores *z* distintos dentro del margen (apartado 5), no idénticos |
| Orden | Unidades, en el orden del archivo. Candidatas y formas reducidas, deduplicadas y en orden alfabético de sus caracteres (orden Unicode) |
| Desviación típica | Poblacional (divisor *n*), sobre los valores de los sorteos |
| Empates | Las ordenaciones de lenguas por valor se hacen por el par (valor, nombre de la lengua): a igual valor, orden alfabético del nombre (4.3, 4.12 y, en 4.4, los vecinos del ibérico, del euskera y de los controles). Dos excepciones en 4.4: la validación por familias (vecino más próximo de cada lengua) ordena por el par (valor, identificador de la lengua en la base), no por el nombre; y las listas de vecinos del ibérico y del euskera redondean la divergencia a cuatro decimales antes de ordenar, de modo que dos lenguas se ordenan por el nombre cuando sus divergencias redondeadas coinciden (lo que puede ocurrir también con diferencias algo mayores de 0,00005, según caigan los redondeos). En la prueba con significados y en 4.10 se ordena solo por el valor, y a igual valor se conserva el orden de la base (orden estable). En los tramos de distancia, el extremo inferior se incluye y el superior no |
| Mínimos de cobertura | El número de unidades con candidatas se compara con el umbral sin redondear: el 30 % de 26 exige 8 |
| Lenguas del Wikcionario | Los archivos contienen 37 etiquetas de lengua; se usan las 35 que tienen normalizador. Armenio y georgiano no lo tienen y quedan fuera |
| Glosas con paréntesis | Se suprime desde cada paréntesis de apertura hasta el primer cierre que le sigue (expresión regular `\(.*?\)`); los anidados no reciben tratamiento aparte. De cada trozo se quita una sola partícula inicial (`to`, `a`, `an`, `the`) y se exige coincidencia completa con el término |
| Open Data Euskadi | El equivalente castellano se usa entero, en minúsculas, sin trocearlo |
| Numerales de Chan | No se aplica el límite de 2 a 12 símbolos del apartado 0.3: se conservan todas las formas no vacías. Las variedades con el campo `Glottocode` vacío se excluyen de la selección del apartado 4.3, paso 1. En el paso 5 entran todas las variedades que tienen los tres valores, sin los filtros del paso 1 |
| Formas ibéricas de los numerales | Las del archivo `unidades_numerales.json` en todas las pruebas (diez: *abaŕ*, *baŕ*; veinte: *oŕkei*, *ogei*) |
| Tope de candidatas (3.5 y 4.5) | Se aplica una sola vez, antes de los sorteos; el mismo subconjunto sirve para el valor real y para el azar. En esos dos cálculos el valor real puede depender de la semilla |
| Grupos por origen (tabla 13) | Los cuatro préstamos latinos propuestos forman también parte del grupo de la casilla documental: es una subcomprobación, no un quinto grupo de una partición |

---

## 1. Fuentes léxicas y su tratamiento

Archivos en `1_fuentes_lexicas/`. Implementación: `ibcomp/fuentes.py`.

### 1.1 Unidades ibéricas

`iberico/unidades_plomos.json` (30 unidades) e `iberico/unidades_numerales.json` (10 unidades). Cada unidad tiene:

| Campo | Contenido |
|---|---|
| `id` | Identificador (A1 a A30; N1 a N8, N10, N20) |
| `formas` | Lista de formas ibéricas en la transcripción de Hesperia |
| `glosa` | Significado propuesto |
| `terminos_es`, `terminos_en` | Términos castellanos e ingleses del significado |
| `terminos_es_v2`, `terminos_en_v2` | Lista ampliada con sinónimos (solo para el apartado 4.5) |
| `tipo` | Origen del significado: `a` por la casilla documental; `c` convergente con apoyo toponímico |

Las cuatro unidades propuestas como préstamos latinos son las que empiezan por *bale*, *koŕta*, *saltu* y *oŕtin*.

### 1.2 Corpus ibérico (Hesperia)

`iberico/hesperia_iberico_1599.csv` (columnas `ref_hesperia`, `texto_crudo` y otras) e `iberico/hesperia_metadatos.csv` (columnas `ref_hesperia`, `material`, `signario` y otras). Se enlazan por `ref_hesperia`. Los dos archivos no se redistribuyen: los genera `iberico/descargar_hesperia.py` a partir del buscador de Hesperia (listado completo, zona TODO, con el filtro de lengua IBERICO; se excluyen las referencias marcadas FALSA, SUSPECTA o LATINA, que son 16 de 1.615) y de las pestañas Generalidades, Epigrafía y Contexto de cada ficha; el programa comprueba al final que el resultado coincide, por su suma SHA-256, con los archivos usados en el artículo (consultas del 7 y del 12-11-2026).

Extracción de las palabras de una ficha (`fuentes.hesperia`):

1. Del texto se eliminan los caracteres `[ ] ( ) + - ?` y los signos combinantes de subrayado y de punto inferior (U+0332, U+0331, U+0323).
2. Se normaliza a NFC y se pasa a minúsculas.
3. Se parte por cualquier secuencia de caracteres que no sean letras, cifras, guion bajo, `ś`, `ŕ` o `ḿ`.
4. Se descarta el tramo vacío, el que contiene alguna cifra y el que contiene tres o más caracteres seguidos del conjunto `i v x l π` (notaciones numerales).
5. Cada tramo se reduce con la regla del apartado 2.3 y se admite si tiene de 2 a 12 símbolos.

De cada ficha se guarda el conjunto de formas reducidas distintas, y:

- **Zona**, por las letras iniciales de la sigla: Narbonense–Rosellón (AUD, HER, PYO, HGA); Cataluña (GI, B, L); Ebro–Castellón (T, TE, Z, HU, CS); Valencia (V); Sudeste (A, MU, AB). Las demás siglas no tienen zona.
- **Plomo (criterio estricto):** el campo `material` contiene «PLOMO». Se usa en la tabla 14.
- **Plomo (criterio amplio):** la palabra «plomo» aparece en cualquier campo de los metadatos. Se usa en la tabla 8.

### 1.3 Wikcionario inglés (extracción de kaikki.org)

`wikcionario/kaikki_control_20lenguas_2026-11-17.tsv` y `wikcionario/kaikki_control_silaba_simple_16lenguas_2026-11-18.tsv`. Cuatro columnas separadas por tabulador: lengua (nombre en inglés), palabra, categoría, glosa.

Una línea se usa si (`fuentes.wikcionario_lemas`):

- tiene exactamente cuatro columnas;
- la lengua tiene normalizador (apartado 2.2);
- la categoría no es `name`, `character`, `suffix`, `prefix` ni `romanization`;
- la palabra, en minúsculas, no contiene espacios y consta solo de letras.

**Términos de una glosa** (`fuentes.terminos_de_glosa`): se suprime lo que va entre paréntesis; se corta por comas y puntos y coma; cada trozo se pasa a minúsculas, se le quitan los espacios de los extremos, la palabra inicial `to`, `a`, `an` o `the`, y los puntos y espacios finales.

Para cada lengua se forma el diccionario: forma reducida (normalizador de la lengua y regla del apartado 2.4) → unión de los términos de todas las palabras que dan esa forma.

### 1.4 Otras fuentes del euskera

| Fuente | Archivo | Tratamiento | Términos |
|---|---|---|---|
| Azkue (1905-1906) | `euskera/azkue_lemas_equivalentes.csv` (`azkue_abbyy_v2.csv` en el repositorio de trabajo), columnas `lema`, `equivalentes` | Lema en minúsculas, sin espacios y solo letras. Significados: `equivalentes` cortado por comas y puntos y coma, en minúsculas | Castellanos |
| Trask (2008), léxico reconstruido | `euskera/trask_formas_glosas.json` (`trask_lexico_nativo_derivado.json` en el repositorio de trabajo): entradas con `proto` y `glosas` | Se descartan las formas reconstruidas que contienen una vocal o una consonante sin determinar (`V` o `C` mayúsculas). De las demás se conservan solo las letras a–z, `ñ` y los corchetes; minúsculas | Ingleses |
| Open Data Euskadi | `euskera/opendata_euskadi_eu_es_v1.tsv`, columnas `eu`, `es` (primera línea, cabecera) | Palabra vasca sin espacios y solo letras; equivalente castellano en minúsculas | Castellanos |

En todas se aplica el normalizador del euskera y la regla del apartado 2.4.

### 1.5 WordNet multilingüe (MCR 3.0)

`wordnet_mcr/wn-data-{eus,spa,cat,glg}.tab`. Tres columnas: concepto, tipo, palabra. Se usan las líneas cuyo tipo termina en `lemma`. La palabra se pasa a minúsculas y los guiones bajos a espacios.

Cada diccionario es «forma reducida → conjunto de conceptos». Las candidatas de una unidad son las formas que comparten algún concepto con los conceptos en que figura alguno de sus términos castellanos (se busca en el archivo `spa`).

### 1.6 Apertium (diccionarios bilingües)

`apertium/*.dix`. De cada archivo se extraen los pares `<l>…</l><r>…</r>`. Antes de extraer los pares se eliminan los comentarios XML (`<!-- … -->`). De cada lado, `<b/>` pasa primero a espacio y después se quitan las demás etiquetas; se pasa a minúsculas y los guiones bajos a espacios. La lista de archivos, el lado en que está la lengua comparada y su normalizador figuran en `fuentes.APERTIUM_ES` (puente castellano, 9 lenguas) y `fuentes.APERTIUM_EN` (puente inglés, 10 lenguas). El significado de cada palabra es su equivalente en la lengua puente.

### 1.7 NorthEuraLex

`northeuralex/forms.csv` (columnas `Language_ID`, `Segments`) y `languages.csv` (`ID`, `Name`, `Family`). Cada forma viene en alfabeto fonético internacional, con los segmentos separados por espacios; se reduce con la regla del apartado 2.5.

### 1.8 Numerales de Chan (2019)

`numerales_chan/forms.csv` (columnas `Language_ID`, `Parameter_ID` = valor numérico, `Form`) y `languages.csv` (`ID`, `Name`, `Family`, `Glottocode`). Cada forma se reduce con la regla del apartado 2.6. Se conservan todas las formas no vacías de cada valor, en el orden del archivo.

### 1.9 Lenguas de control

`wikcionario/kaikki_lenguas_de_control_2026-11-19.tsv`. Seis columnas: lengua, palabra, categoría, romanización, marca de remisión, glosas (separadas por ` || `).

Una palabra es elegible (`fuentes.lexico_control`) si: la marca de remisión es `0`; la categoría es `noun`, `verb`, `adj`, `adv`, `num` o `pron`; la forma (primera romanización si existe; si no, la palabra), una vez normalizada (apartado 2.2), consta solo de letras a–z, `ñ` y `ð`; su forma reducida tiene de 3 a 10 símbolos; y tiene al menos un término de glosa formado por una o dos palabras de letras a–z. Se ignoran las glosas que empiezan por *see*, *the meaning*, *alternative*, *romanization*, *obsolete* o *misspelling*, y las que contienen *uncertain*.

### 1.10 Formas flexionadas

`wikcionario/kaikki_formas_26lenguas_2026-11-18.tsv.gz` (comprimido con gzip; solo se lee el archivo `.gz`): tres columnas (lengua, marca, forma). La marca `L` indica un lema; las líneas siguientes, sus formas flexionadas. `wikcionario/wikcionario_eu_formas_verbales_v1.csv` (columnas `lema`, `forma`) añade formas verbales vascas. Solo se usan las formas de lemas presentes en el diccionario de la lengua, sin espacios y solo con letras. El lema vigente es el de la última línea `L` leída, con su lengua; una línea de forma se admite solo si su lengua es la del lema vigente y ese lema está en el diccionario de esa lengua. (Una auditoría externa contó, en los 8.233.273 renglones del archivo, 557 formas cuya lengua no es la del último lema; con la comprobación de lengua ninguna puede admitirse, y en estos datos tampoco lo era antes de añadirla.) Las formas verbales vascas añadidas no pasan por ese filtro, salvo el de pertenecer a un lema del diccionario.

---

## 2. Criterios: de la grafía a las clases de sonidos

Implementación: `ibcomp/texto.py`, `ibcomp/normalizadores.py`, `ibcomp/clases.py`.

### 2.1 Limpieza de una forma (`texto.limpia` y `texto.limpia_grafia`)

`texto.limpia`, para las formas ibéricas:

1. NFC y minúsculas.
2. Se eliminan los caracteres combinantes (categoría Unicode `Mn`), salvo el acento agudo U+0301.
3. NFC de nuevo.
4. Se eliminan `* [ ] { } ( ) - ? ’ ‘ '`, los espacios y los puntos.

`texto.limpia_grafia`, para las palabras de los diccionarios (salida de un normalizador) y para las formas de las unidades en la prueba con significados. No llama a `limpia`; sus pasos son:

1. NFC y minúsculas.
2. Cada carácter que no esté en la lista de conservados se descompone (NFD) y pierde sus signos combinantes (categoría `Mn`): `ê` → `e`, `ö` → `o`, `ǵ` → `g`. Se conservan tal cual `ś ŕ ḿ ñ š ç ł ŋ` (tienen clase propia en 2.4) y las vocales con acento agudo o con macrón (`á é í ó ú ā ē ī ō ū`), que en 2.4 reciben la clase de su vocal base.
3. NFC de nuevo.
4. Se eliminan `* [ ] { } ( ) - ? ’ ‘ '`, los espacios y los puntos.

Las formas del corpus ibérico (4.14, 4.4 y 4.8) siguen usando `limpia`, que no toca los caracteres precompuestos: la grafía de Hesperia no los emplea fuera de los signos dudosos, que se excluyen.

Simplificación de letras dobles (`texto.dobles`): toda repetición contigua de una misma letra, de cualquier longitud, se reduce a una, salvo `rr` y `ll`.

### 2.2 Normalizadores por lengua

Cada lengua tiene una función que pasa su ortografía a una grafía común, con sustituciones aplicadas en un orden fijo. En el albanés, el fiyiano, el zulú y el shona, y el somalí, las sustituciones se aplican en una sola pasada de izquierda a derecha, probando en cada posición las secuencias en el orden de la lista, de modo que lo ya sustituido no vuelve a transformarse. Son reglas generales, aproximadas, iguales para todas las palabras de la lengua. La tabla completa, sustitución por sustitución, es el archivo `ibcomp/normalizadores.py`, que debe leerse como parte de esta especificación: cada función es una lista ordenada de sustituciones de texto. Lenguas y función:

| Lenguas | Función |
|---|---|
| Euskera | `n_eu` (sin cambios) |
| Gallego, catalán, occitano, asturiano, rumano, aragonés, portugués, francés, italiano, castellano, siciliano, sardo | `n_rom`, con el código de lengua |
| Latín | `n_la` |
| Galés | `n_cy` |
| Islandés, alemán, sueco | `n_ger` |
| Finés, estonio | `n_fi` |
| Húngaro | `n_hu` |
| Turco | `n_tr` (Wikcionario), `n_tr_apertium` (Apertium) |
| Albanés, irlandés, lituano, maltés, suajili, quechua | `n_sq`, `n_ga`, `n_lt`, `n_mt`, `n_sw`, `n_qu` |
| Serbocroata | `n_hbs` |
| Hawaiano, samoano, tongano | `n_poli` |
| Fiyiano; indonesio y malayo; tagalo; malgache | `n_fj`; `n_indo`; `n_tl`; `n_mg` |
| Zulú y shona; hausa; yoruba; somalí; náhuatl clásico | `n_bantu`; `n_ha`; `n_yo`; `n_so`; `n_nah` |
| Umbro, gótico, córnico, dálmata, etrusco, sumerio | `norm_control` |

Criterios comunes a casi todas: se quitan los acentos; las letras dobles se simplifican (salvo `rr` y `ll`); las africadas se escriben `tx` o `ts`; la fricativa palatal, `x`; la semiconsonante palatal, `j`. La `v` y la `w` no reciben un tratamiento común: los normalizadores de las lenguas en que `v` o `w` representan [b] o [β] las convierten en `b` (romances, griego, turco, albanés, entre otras; cada función lo indica); el del euskera no cambia nada, y en las lenguas sin esa regla `v` pasa a la clase B (con `f`) y `w` a la clase W en 2.4.

### 2.3 Forma ibérica, signo a signo (`clases.red_ib`)

Se limpia la forma (2.1) y cada letra se sustituye así: `p b` → P; `t d` → T; `k g` → K; `s ś` → S; `r ŕ` → R; `l` → L; `m ḿ` → M; `n` → N; cada vocal, por su letra base en minúscula. Lo demás se omite. Se usa para el corpus (perfil de sonidos) y para los numerales.

### 2.4 Forma en grafía común (`clases.reducida`)

Se usa para los diccionarios y, en la prueba con significados, también para las formas de las unidades ibéricas.

1. Se limpia la forma con `limpia_grafia` (2.1).
2. Si empieza por `h`, se quita esa `h`.
3. Si empieza por `i` seguida de `a`, `e`, `o` o `u`, esa `i` se sustituye por `j`.
4. Se recorre de izquierda a derecha. Si los dos caracteres siguientes forman un dígrafo, se emite su clase y se avanzan dos: `tx tz ts tś ch` → C; `sh` → S; `ll` → L; `rr` → R; `ng` → N.
5. Si no, se emite la clase del carácter: `p b` → P; `f v` → B (la `v` de las lenguas cuyo normalizador no la ha convertido en `b`); `w` → W; `t d` → T; `k g q` → K; `ʔ h` → H; `s ś z x š ç` → S; `c` → C; `m ḿ` → M; `n ñ ŋ` → N; `r ŕ` → R; `l ł` → L; `y j` → J; una vocal, su letra base en minúscula. Lo demás se omite.

### 2.5 Transcripción fonética (`clases.red_afi`)

Para cada segmento: se quitan las marcas de longitud `ː` y `ˑ`; se busca su clase en la tabla SCA de LingPy (`clases_sca/converter`). Si no figura, se reduce a sus letras base (descomposición NFD, solo letras) y se busca de nuevo. Si tampoco figura, se toma la clase de su primera letra, salvo que las dos primeras sean una oclusiva (clase T, P o K) seguida de una sibilante (S), en cuyo caso la clase es C.

Las clases de tono y de marca (`1` a `6`, `_`, `9`) se descartan. Las seis clases de vocal de SCA se escriben en minúscula: A → a, E → e, I → i, U → o, O → o, Y → u. A la tabla de LingPy se añade `ʜ` → H (fricativa epiglotal sorda, 112 apariciones en NorthEuraLex, que la tabla no recoge). Inventario de lo que se omite en NorthEuraLex con estas reglas: el separador de morfemas `+` (7.074 apariciones) y las marcas de tono `² ⁴ ⁵¹` (1.542); ningún otro segmento.

### 2.6 Numerales de Chan (`clases.red_chan`)

La forma se pasa a minúsculas y NFC. Cada carácter se sustituye por su clase SCA; si no figura, por la de su letra base. Lo que no tiene clase se omite. Al final toda repetición contigua de una misma clase, de cualquier longitud, se reduce a una.

### 2.7 Lenguas de control (`normalizadores.red_control`)

La palabra normalizada se parte por `ð`; cada parte se reduce con 2.4 y las partes se unen con la clase D.

### 2.8 Reducción al inventario que el ibérico escribe (`clases.proyecta`)

B → P; D → T; G → K; C → S; M → N; W → o; J → i; H y `!` se suprimen. Se descartan las formas que quedan con menos de dos símbolos.

---

## 3. Algoritmos

### 3.1 Medida de distancia (`distancia.dist`)

Los resultados de la función se guardan en una caché de hasta cuatro millones de pares (`functools.lru_cache`); la caché solo afecta al tiempo y a la memoria, no a los valores. Entre dos formas reducidas *a* y *b*:

- Si alguna está vacía, la distancia es 1. Si son iguales, 0.
- Peso de un símbolo: 0,5 si es vocal (minúscula); 1 si es consonante.
- Costes: insertar o borrar un símbolo cuesta su peso; sustituir una vocal por otra vocal distinta cuesta 0,5; cualquier otra sustitución de símbolos distintos cuesta 1.
- Se calcula el coste mínimo de transformar *a* en *b* (programación dinámica, como en la distancia de edición).
- Ese coste se divide por la media de los pesos totales de *a* y de *b*.

Ejemplo: *śalir* se reduce a `SaLiR` (peso 4) y *zilar* a `SiLaR` (peso 4). Hay dos sustituciones de vocal por vocal: coste 1. Distancia: 1 / 4 = 0,25.

### 3.2 Prueba con significados (`pruebas.prueba_significados`)

Entrada: un conjunto de unidades, un diccionario y el campo de términos que corresponde al diccionario (castellanos o ingleses).

1. Para cada unidad se obtienen sus candidatas. Si no tiene ninguna, la unidad no cuenta.
2. Distancia de la unidad: la menor entre cualquiera de sus formas (reducidas con 2.4) y cualquiera de sus candidatas.
3. Si las unidades con candidatas son menos que el mínimo exigido, el diccionario se descarta. El mínimo es el mayor de 4 y el 30 % del número de unidades (40 % en el Wikcionario y sus capas históricas; en la tabla 9, el mayor de 3 y el 30 %).
4. **Valor real:** media de las distancias de las unidades con candidatas.
5. **Azar:** se repite 500 veces. En cada repetición se reúnen todas las candidatas distintas de todas las unidades y se agrupan por su longitud en símbolos. Para cada longitud se toman al azar, sin repetir ninguna, tantas formas del mismo diccionario y de esa longitud como candidatas distintas hay, y se asignan una a una a las candidatas (ordenadas alfabéticamente). Cada candidata queda así sustituida por una forma de su misma longitud; una candidata que comparten varias unidades recibe la misma sustituta en todas. Se recalcula la distancia de cada unidad (la menor entre cualquiera de sus formas y las sustitutas de sus candidatas) y la media. Si para una longitud hubiera menos formas en el diccionario que candidatas, se sortea con repetición.

   Si se fija un tope de candidatas por unidad (solo en 4.5), las candidatas de la unidad que lo supera se reducen una sola vez, al azar, a ese número; el mismo subconjunto sirve para el valor real y para los sorteos.
6. **Resultado:** *z* = (valor real − media de las 500 repeticiones) / desviación típica de las 500 repeticiones. *p* = (1 + número de repeticiones con valor menor o igual que el real) / 501. **Ventaja** = media de las repeticiones − valor real.

Los diccionarios se ordenan por *z*, de menor a mayor. Un *z* más negativo indica mayor proximidad.

### 3.3 Perfil de combinaciones de sonidos (`pruebas.perfil`, `pruebas.divergencia`)

- **Perfil** de un conjunto de formas reducidas distintas: a cada forma se le antepone `^` y se le pospone `$`; se cuentan todos los pares de símbolos consecutivos; cada cuenta se divide por el total.
- **Distancia** entre dos perfiles *P* y *Q*: divergencia de Jensen-Shannon en bits. Con *M* = (*P* + *Q*) / 2, es ½ Σ *P* log₂(*P* / *M*) + ½ Σ *Q* log₂(*Q* / *M*), sumando sobre todos los pares presentes en alguno de los dos. Vale 0 si son idénticos y 1 si no comparten ningún par.

### 3.4 Serie numeral

Distancia entre dos series: media de las distancias (3.1) entre los numerales del mismo valor. Cuando el ibérico tiene dos formas para un valor, se toma la menor. Las formas ibéricas se reducen con 2.3.

### 3.5 Ventaja por grupos de significados (`pruebas.ventaja_por_grupos`)

Para una lengua examinada *X* (con una o varias formas reducidas por significado) y un diccionario *Y*:

1. Para cada significado con formas en *X* y candidatas en *Y*: si las candidatas son más de 40, se toman 40 al azar. Distancia real: la menor entre las formas y las candidatas. Azar: lo mismo, sustituyendo las candidatas como en 3.2 (sin repetir forma y conservando las candidatas compartidas), tantas veces como sorteos.
2. Para cada grupo de significados con al menos tres: ventaja = media del azar − media real.

**Grupos.** Estables: N1 a N5, A13, A21, A24, A27, A28, A30 (uno a cinco, monte, dar, tierra, hierba, camino, hacer). Poco estables: los otros 29. Criterio: la glosa principal figura en la lista Leipzig–Yakarta de 100 significados o en la de Swadesh de 207.

---

## 4. Programas

Cada programa se ejecuta sin argumentos desde `4_programas/` y escribe en `resultados/` un archivo JSON con el mismo nombre.

### 4.1 `t06_t07_significados.py` — tablas 6 y 7

Aplica la prueba 3.2 a dos conjuntos (las 30 unidades de los plomos; las 10 de la serie numeral) frente a cuatro grupos de diccionarios:

| Grupo | Diccionarios | Términos | Mínimo |
|---|---|---|---|
| Wikcionario y diccionarios históricos | 35 lenguas del Wikcionario; Azkue; Trask, reconstruido (el diccionario etimológico de Trask se excluyó por estar contaminado por la propia comparación y no lo lee el programa) | Ingleses (castellanos en Azkue) | 40 % |
| Bilingües, puente castellano | Open Data Euskadi; Apertium, 9 lenguas | Castellanos | 30 % |
| Bilingües, puente inglés | Apertium, 10 lenguas | Ingleses | 30 % |
| Concepto a concepto | WordNet: euskera, catalán, gallego, castellano | Castellanos, vía conceptos | 30 % |

### 4.2 `t09_prestamos.py` — tabla 9

La misma prueba y los mismos diccionarios, con las 30 unidades separadas en dos conjuntos: las 4 propuestas como préstamos latinos y las otras 26. Mínimo: el mayor de 3 y el 30 %.

### 4.3 `t04_t05_numerales.py` — tablas 4 y 5, figura 3

1. **Selección de lenguas.** De cada variedad se toma la primera forma de cada valor 1, 2, 3, 4, 5, 6, 7, 8 y 10. Se recorren las variedades en el orden de la base y se conserva la primera de cada código de Glottolog que tenga los nueve valores, cuyo código no esté vacío ni empiece por `xxxx` y cuya familia no sea *Bookkeeping*, *Unattested*, *Unclassifiable*, *Pidgin*, *Mixed Language*, *Artificial Language*, *Speech Register* ni *Sign Language*. Familia de una lengua: el campo `Family`; si está vacío, la lengua forma familia propia.
2. **Ibérico.** Distancia de la serie ibérica (*ban*; *bi*, *bin*; *iŕur*; *lauŕ*; *borste*, *bors*; *śei*; *sisbi*; *sorse*; *abaŕ*, *baŕ*) a cada lengua; se ordenan. Las formas se leen del archivo de unidades.
3. **Lenguas sin parientes en la base.** Para cada lengua cuya familia tiene un solo miembro en la selección (lo que no equivale a que sea una lengua aislada: puede deberse a la cobertura de la base), se busca la lengua más próxima y se anota su distancia.
4. **Lenguas con parientes.** Se toma una muestra de 400 lenguas de familias de cinco o más miembros (semilla 20261118, sobre la lista en el orden de la selección). Para cada una se busca la lengua más próxima y se anota su distancia y si es de la misma familia. Se cuenta por tramos de distancia.
5. **Valores con apoyo externo.** Con los valores 1, 10 y 20 (*ban*; *abaŕ*, *baŕ*; *oŕkei*, *ogei*), todas las variedades que los tienen, primera forma de cada valor. Se anota el puesto del euskera (código `basq1248`) y la primera variedad que no es euskera.
6. **Valores barajados.** Con los diez valores, para las cuatro variedades más próximas: 2.000 veces se reordenan al azar los valores de la variedad y se recalcula la distancia.

### 4.4 `t08_perfil.py` — tabla 8 y apartado 7.4

Para una base de lenguas (léxico → perfil por lengua):

1. **Validación.** Para cada lengua con algún pariente en la base, se busca la lengua de perfil más próximo y se anota si es de su familia. Se da también el acierto esperable por azar: media, sobre esas lenguas, de (miembros de su familia − 1) / (lenguas − 1).
2. **Controles.** Perfil de todo el léxico elegible de cada lengua de control (formas de 2 a 12 símbolos, sin exigir glosa) y sus lenguas más próximas.
3. **Ibérico.** Perfil de todas las formas del corpus y, aparte, de las formas de los plomos (criterio amplio). Lenguas ordenadas por distancia; puesto del euskera.
4. **Remuestreo.** 500 veces se sacan con reposición tantas formas como tiene el conjunto, y 500 veces la mitad sin reposición; se cuenta en cuántas el euskera es la lengua más próxima. En cada repetición se saca una sola muestra ibérica, que se compara con todas las lenguas.

Se ejecuta cuatro veces: con NorthEuraLex (107 lenguas), con las formas tal cual y con todas reducidas según 2.8; y con las 35 lenguas del Wikcionario (300 remuestreos), del mismo modo. Familias en el Wikcionario: romance (latín, catalán, gallego, asturiano, occitano, rumano, siciliano, sardo); céltica (galés, irlandés); urálica (finés, estonio, húngaro); austronesia (tagalo, malgache, indonesio, malayo, hawaiano, samoano, tongano, fiyiano); bantú (suajili, zulú, shona).

### 4.5 `s82_formas_y_sinonimos.py` — apartado 8.2

Solo las lenguas del Wikcionario con más de 200 lemas con formas flexionadas. Para cada una se forman dos diccionarios: con los lemas, y con los lemas más sus formas flexionadas (cada forma hereda los significados de su lema). Se aplica la prueba 3.2 con 300 sorteos, mínimo del 40 % y, si una unidad tiene más de 400 candidatas, un tope de 400 (véase 3.2). Variantes: lemas; lemas y formas; lemas con la lista ampliada de términos; lemas y formas con la lista ampliada. Para la serie numeral, las dos primeras.

### 4.6 `t10_controles.py` — tabla 10

Para cada lengua de control: se ordenan alfabéticamente sus palabras elegibles (1.9); con la semilla 20261119 más la suma de los códigos Unicode de las letras del nombre inglés de la lengua, se sacan ocho muestras sucesivas de 30 palabras sin reposición y se usan las cinco primeras. Cada muestra se trata como un conjunto de unidades: cada palabra es una unidad, su forma se reduce con 2.7 y sus términos son los de su glosa. Se aplica la prueba 3.2 frente a los 35 diccionarios del Wikcionario, con 150 sorteos y un mínimo de 12 palabras con candidatas.

Parientes esperados: umbro y dálmata, el latín y las lenguas romances; córnico, el galés y el irlandés; gótico, el islandés; etrusco y sumerio, ninguno.

### 4.7 `t11_t13_estables.py` — tablas 11 a 13

- **Tabla 12.** Algoritmo 3.5 con las formas ibéricas de las 40 unidades (reducidas con 2.4) frente a cada diccionario del Wikcionario, 500 sorteos.
- **Tabla 13.** Lo mismo frente al euskera, con estos grupos: dato externo (N1, N10, N20, A1, A2, A17, A30); numerales por posición (N2 a N8); casilla documental (A3 a A23, salvo A17); apoyo toponímico (A24 a A29); préstamos latinos propuestos (A6, A9, A11, A13). Este último grupo se calcula además frente al gallego.
- **Tabla 11.** Para cada pareja (lengua *X*, lengua *Y*) de la lista fijada: las formas de *X* para cada significado son las de su diccionario cuyo significado coincide con algún término inglés de la unidad. Se exige que al menos 5 significados estables y 8 poco estables tengan formas en *X* y candidatas en *Y*. Se repite 20 veces: se elige al azar una forma de *X* por significado y se aplica 3.5 con 120 sorteos. Se promedian las 20 repeticiones. La lista de parejas y su tipo de relación está en el programa.

Lista de parejas (lengua *X* – lengua *Y*), fijada antes de ejecutar. Son 43; zulú–shona queda fuera por no alcanzar la cobertura mínima de significados, y quedan 42.

| Tipo de relación | Parejas |
|---|---|
| Emparentadas cercanas | catalán–occitano; gallego–asturiano; malayo–indonesio; estonio–finés; rumano–latín; catalán–latín; sardo–latín; zulú–shona |
| Emparentadas lejanas | irlandés–galés; húngaro–finés; irlandés–latín; islandés–latín; lituano–latín; islandés–lituano; tagalo–malayo; malgache–malayo; hawaiano–malayo; fiyiano–malayo; suajili–zulú; hausa–somalí |
| Parentesco lejano y préstamos | albanés–latín; galés–latín |
| Solo contacto | tagalo–gallego; tagalo–catalán; quechua–gallego; euskera–latín; euskera–gallego; euskera–catalán; maltés–siciliano; húngaro–turco; finés–islandés; rumano–húngaro; rumano–turco; albanés–turco; malgache–suajili |
| Sin relación | euskera–finés; quechua–húngaro; hawaiano–irlandés; zulú–islandés; yoruba–lituano; náhuatl clásico–galés; hausa–estonio; fiyiano–latín |

Las parejas comparten lenguas y no son observaciones independientes entre sí; las medias por tipo se dan como descripción.

### 4.8 `t14_zonas.py` — tabla 14

Para cada zona (1.2), con las formas de sus plomos (criterio estricto) y con las de todas sus inscripciones:

1. Perfil de la zona y distancia a cada una de las 107 lenguas de NorthEuraLex. Puesto del euskera. Distancia relativa = (distancia al euskera − media de las 107 distancias) / desviación típica de las 107.
2. Muestras igualadas: 300 veces se sacan sin reposición tantas formas como tiene la zona con menos formas; se promedian la distancia relativa y el puesto.
3. Se repite con todas las lenguas y las formas ibéricas reducidas según 2.8.
4. Variación dentro del ibérico: 300 veces, de cada zona se sacan dos muestras disjuntas de *n* formas (*n* = mitad del tamaño de la zona menor); se calcula la distancia entre la primera muestra de cada zona y la segunda de cada zona. Se dan la media para la misma zona, para zonas vecinas, para zonas no vecinas y para las dos extremas.

---

### 4.9 `figuras.py` — figuras 1 a 3

No calcula nada. Dibuja, a partir de los archivos de resultados: los valores *z* de las lenguas del Wikcionario con las 30 unidades (figura 1, arriba); la distancia de cada una de las 107 lenguas al perfil de todo el corpus ibérico (figura 1, abajo); los dos valores a la vez para las lenguas presentes en las dos bases (figura 2); y el histograma de las distancias de las lenguas sin parientes a su vecino más próximo en la serie numeral, con la distancia entre el ibérico y el euskera (figura 3). La posición vertical de los puntos de la figura 1 solo sirve para separarlos.

### 4.10 `t15_solidez_unidades.py` — tabla 10 bis y apartado 8.4

Con las 30 unidades de los plomos. Para cada diccionario se calcula, unidad por unidad, la distancia real (como en 3.2) y la del azar en cada uno de 500 sorteos; el valor *z* de un subconjunto de unidades se obtiene promediando sus columnas. Lenguas: las del Wikcionario con candidatas para al menos el 40 % de las unidades.

1. **Quitando una unidad cada vez:** valor y puesto del euskera en los 30 casos.
2. **Subconjuntos al azar** de 20, 15 y 10 unidades, 2.000 de cada tamaño: número de veces que el euskera es la primera lengua y valor mediano. En todos los pasos de este apartado, una lengua entra en la comparación de un subconjunto si conserva al menos cuatro unidades con candidatas; el número de lenguas comparadas se guarda en cada resultado por grupo (`lenguas_comparadas`). El ensayo de significados cambiados (paso 5) guarda la mediana, los percentiles 5 y 95 y los dos extremos de las 300 repeticiones.
3. **Por origen del significado:** dato externo, que es el nivel I (A1, A2, A3, A17, A30; A3 no tiene candidatas en euskera y se cuenta en el grupo aunque no sea comparable); apoyo de la toponimia (A24 a A29); casilla documental (las demás). Y por niveles de procedencia según el inventario cerrado de la Monografía IV (apartado 5.1, tabla 5): niveles I y II juntos (todas menos A24 a A29); nivel II con correspondencia vasca señalada después de fijado el significado (A8, A10, A14, A15, A19, A20); nivel II sin correspondencia señalada (las demás de la casilla documental); estas últimas sin los cuatro préstamos latinos propuestos (A6, A9, A11, A13).
4. **Retirada adversa:** las unidades se ordenan por su distancia real al euskera, de menor a mayor, y se quitan una a una; se anota cuántas hay que quitar para que el euskera deje de ser la primera lengua.
5. **Significados cambiados:** con Open Data Euskadi, el Wikcionario y WordNet. Para cada pareja (unidad, significado de otra unidad) se calculan la distancia real y la del azar (200 sorteos). A *k* unidades elegidas al azar (*k* = 5, 10, 15, 20, 30) se les asigna el significado de otra de ellas por rotación; 300 repeticiones por *k*; se da la mediana del valor *z* y los percentiles 5 y 95.

### 4.11 `t16_contraste_principal.py` — apartado 8.5

Análisis principal: las 30 unidades de los plomos frente a las lenguas del Wikcionario con candidatas para al menos el 40 % de las unidades.

1. **Sustitución con 20.000 sorteos.** La prueba 3.2 para el euskera con 20.000 sorteos. La probabilidad se multiplica por el número de lenguas comparadas (corrección de Bonferroni), con máximo 1.
2. **Permutación de los significados.** Para cada lengua, con las unidades que tienen candidatas (mínimo 12): se forma la tabla de distancias entre cada unidad *i* y las candidatas del significado de cada unidad *j* (la menor distancia entre las formas de *i* y esas candidatas). Valor real: media de la diagonal. Se generan 100.000 permutaciones al azar de las columnas y, para cada una, la media de las distancias entre cada unidad y el significado que le toca. *p* = (1 + número de permutaciones con valor menor o igual que el real) / 100.001; *z* respecto de las permutaciones. No se sortea ninguna palabra del diccionario. Se aplica también a Open Data Euskadi, Azkue y WordNet (euskera y castellano).
3. **Lo mismo sin las cuatro unidades propuestas como préstamos latinos.**
4. **Permutación condicionada por la longitud.** Como el paso 2, pero las unidades se agrupan por la longitud (número de símbolos) de su primera forma reducida, y los significados solo se permutan dentro de cada grupo; las unidades solas en su grupo conservan el suyo. Se da además el número de permutaciones distintas posibles (producto de los factoriales de los tamaños de los grupos) y el número de unidades que pueden cambiar. Declarada antes de ejecutarse (`resultados/DECLARACIONES_PREVIAS.md`, entrada 2).

Semilla de las permutaciones: generador NumPy `default_rng` sembrado con los 63 bits que da `pruebas.generador('permutacion', <clave del cálculo>, <nombre del diccionario>)`; cada cálculo y cada diccionario tienen así su propia secuencia. Al contar las permutaciones iguales o mejores que el valor real se admite una tolerancia numérica de 10⁻¹² (una permutación cuenta si su valor es ≤ real + 10⁻¹²), en las dos variantes. La variante condicionada se calcula, y se informa, también en el paso 3 (sin los cuatro préstamos).

### 4.12 `t18_perfil_contacto.py` — tabla 15 y apartado 11.3

Con NorthEuraLex y los perfiles del apartado 3.3 (formas tal cual, sin la reducción de 2.8). Para cada pareja (lengua que toma, lengua que da) se ordenan las otras 106 lenguas por su distancia de perfil a la primera y se anota el puesto de la segunda, su distancia y la lengua más próxima. Sin sorteos. Parejas, fijadas antes de ejecutar (nombres de la base): Basque–Spanish; Basque–Latin; Basque–Catalan; Hungarian–Turkish; Romanian–Bulgarian; Standard Albanian–Latin; Standard Albanian–Modern Greek; Japanese–Mandarin Chinese; Korean–Mandarin Chinese; Finnish–Swedish; English–French; Western Farsi–Standard Arabic; Turkish–Standard Arabic; Turkish–Western Farsi; Breton–French; Armenian–Western Farsi; Hindi–Western Farsi.

### 4.13 `t19_potencia_controles.py` — apartado 8.3 (potencia y falsos positivos)

Como 4.6, con 100 muestras de 30 palabras por lengua de control. Las muestras se toman, una tras otra, de un generador sembrado con `20261120|potencia|<lengua>` sobre la lista de palabras elegibles en orden alfabético; la prueba de cada muestra usa la clave `potencia|<lengua>|<número de muestra>`. Se anota, por lengua: en cuántas muestras la primera lengua es pariente; el valor de la primera lengua; la separación con la segunda; y en cuántas muestras se alcanzan los umbrales −9,3 (valor) y 5,6 (separación). Declarado antes de ejecutarse en `resultados/DECLARACIONES_PREVIAS.md`.

### 4.14 `t01_t02_corpus.py` — tablas 1 y 2

Con el corpus del apartado 1.2, pero con una segmentación propia, más estricta que la de `fuentes.hesperia`:

- *Palabras.* De cada línea de `texto_crudo` se descartan las que contienen tres o más mayúsculas seguidas (texto latino). Cada línea se parte por `· : | , ; /` y espacios. De cada tramo se quitan los signos `[ ] + * ? - ( ) < >`, los dígitos, los numerales `I V X Π`, el punto y los apóstrofos, y se limpia (2.1, `limpia`). Cuenta como palabra lo que queda si tiene dos o más caracteres y todos son letras del alfabeto `a e i o u b t k d g l n m r ŕ s ś ḿ` (sin `p`, que la escritura ibérica no distingue, y sin `h`).
- *Palabras completas.* Las que proceden de un tramo sin ninguno de los signos anteriores (sin corchetes, cruces ni interrogaciones).
- *Formas distintas.* Dos palabras son la misma forma si coinciden tras igualar `p b` → P, `t d` → T, `k g` → K, `s ś` → S, `m n ḿ` → N, `r ŕ` → R, `l` → L (`equivalente`).
- *Vocabulario no onomástico.* Sobre las palabras completas de cuatro o más letras: se excluyen las que la clasificación de MLH V.2 (1.2) da como nombre personal, formante, leyenda monetal, marca o abreviatura, o numeral, o como nombre dudoso; y las que, quitando opcionalmente uno de los sufijos `ka te en ar e ban sken ḿi ir bi ki ite ke ku ḿ i`, se descomponen en dos formantes onomásticos de la lista de Rodríguez Ramos (2014) (cada parte de dos o más letras).
- *Tabla 1.* Por soporte: inscripciones, palabras, formas distintas y formas distintas no onomásticas. La fila de totales da, además de la suma por soportes, el número de formas distintas en todo el corpus (unión), que es menor porque una forma puede aparecer en más de un soporte.
- *Tabla 2.* Los porcentajes de nombres y de repetición se calculan sobre las palabras completas de tres o más letras; el de nombres aplica el clasificador anterior a esas palabras. Repetición: dos medidas, el porcentaje de palabras cuya forma aparece más de una vez en el soporte y el porcentaje de palabras que repiten una forma ya presente (palabras menos formas distintas, dividido por palabras). «Formas no onomásticas con sufijo reconocible» cuenta apariciones (no formas distintas) de palabras completas no onomásticas de cuatro o más letras que terminan en uno de los trece primeros sufijos de la lista y dejan al menos tres letras delante.

Sin sorteos.

### 4.15 `a3_comprobacion_medida.py` — Anexo A.3

Con NorthEuraLex sin el euskera (106 lenguas). De cada lengua y concepto se toma la primera forma del archivo que tenga alguna clase tras 2.5 (sin aplicar el filtro de longitud de 0.3). Doce sorteos de 40 conceptos, tomados de la lista de conceptos en orden alfabético con un generador sembrado con el número 20261118 (se conserva la semilla del cálculo original; es la tercera excepción a 0.4). En cada sorteo, la distancia entre dos lenguas es la media de las distancias (3.1) entre sus formas de un mismo concepto, sobre los conceptos del sorteo que tienen forma en las dos lenguas; si no comparten ninguno, la distancia es 1. Se calcula el área bajo la curva con que esa distancia separa las parejas de la misma familia (campo `Family` de `languages.csv`) de las demás, por rangos, con rango medio en los empates; y lo mismo solo para los parentescos antiguos: parejas de la misma familia, indoeuropea o urálica, con campo `Subfamily` no vacío y distinto en las dos lenguas. Se da la media de los doce sorteos, el mínimo y el máximo.

### 4.16 `t17_techo_circularidad.py` — apartado 8.4, ensayo sobre la circularidad

Con las 30 unidades de los plomos y las lenguas del Wikcionario con candidatas para al menos el 40 % de ellas. Tabla de distancias entre cada unidad y las candidatas del significado de cada otra, y su azar con 200 sorteos (como en 4.10, paso 5; clave `techo|<lengua>`). Para cada lengua se calculan tres valores *z*: con los significados propuestos; asignando a cada unidad el significado que más la acerca a esa lengua dentro de su campo (contable, predial o personas, según `parameters.csv`); y asignándolo entre los 30 sin restricción. Precisiones: la asignación optimizada no es una permutación (un mismo significado puede asignarse a varias unidades); se elige por distancia mínima, no por *z*; la asignación propuesta y las optimizadas pueden usar distinto número de unidades (solo las que tienen candidatas para el significado asignado); y la optimización no se repite sobre cada sorteo nulo, por lo que el *z* resultante no es una probabilidad calibrada que incorpore el proceso de elegir significados. El resultado es no concluyente y así consta en el artículo: con esa libertad, otras lenguas alcanzan valores como el del euskera.

### 4.17 `t20_variacion_semillas.py` — Anexo B.7

Cada repetición se guarda en `resultados/t20_repeticiones/NN.json` junto con una huella (SHA-256, 16 caracteres) de este programa, del paquete `ibcomp` y de las entradas ya leídas (las 30 unidades y los diccionarios del Wikcionario con sus formas y términos); el resumen solo cuenta las repeticiones cuya huella coincide con la del código y los datos vigentes, de modo que un cambio en los datos de entrada invalida las repeticiones guardadas igual que un cambio en el código, y `--regenerar` las recalcula todas. El resumen de 4.13 (`t19`) no resume una lengua cuyo archivo tenga menos de 100 muestras.

La prueba de 4.1 con las 30 unidades de los plomos y las lenguas del Wikcionario (mismo mínimo de unidades, 500 sorteos), repetida 40 veces con la clave de sorteo `variacion|k` (k de 1 a 40) en lugar de la clave habitual. De cada repetición se guarda el valor *z* de cada lengua. Se dan, para el euskera y para la mejor de las demás lenguas, mediana, extremos y desviación típica poblacional; la menor separación; y la amplitud por lengua. Las repeticiones son independientes entre sí y pueden calcularse por tramos.

### 4.18 `t21_lecturas_alternativas.py` — tabla 10 bis, fila sin lecturas alternativas

Con las tablas de 4.10 (mismas claves y sorteos), valor *z* de cada lengua sin las unidades A11, A12, A13, A16 y A19 (las que tienen, en alguna aparición, una lectura alternativa documentada en las monografías), con el mínimo de cuatro unidades comparables; puesto del euskera y lenguas siguientes. Declarada antes de ejecutarse (entrada 4).

### 4.19 `t22_calibracion_perfil.py` — tabla 8, calibración

Perfiles de 4.4 (clases completas y reducidas). Para las 5.671 parejas de las 107 lenguas, distancia (3.3) y tipo: misma familia si las dos tienen el mismo campo `Family` no vacío; familias distintas en otro caso. Percentil de la distancia ibérico–euskera en cada grupo (proporción de parejas con distancia menor o igual), número de parejas de familias distintas a esa distancia o menos y las diez más próximas; para las lenguas cuya familia no tiene otra lengua en la base, distancia a su vecino más próximo. Sin sorteos. Declarada antes de ejecutarse (entrada 5).

### 4.20 `t23_tamano_diccionario.py` — apartado 8.4, tamaño de los diccionarios

Sobre las filas del Wikcionario de la tabla 6 (sin Azkue ni el léxico reconstruido): correlación de Spearman (rangos medios en los empates) entre el número de formas y el valor *z*, con y sin el euskera; puesto del euskera por tamaño; mediana de tamaños. Sin sorteos. Declarada antes de ejecutarse (entrada 6).

### 4.21 `t24_jurado_procedencia.py` — tabla 10 bis con la clasificación del jurado ciego

Repite el apartado (c) de 4.12 (`t15`: misma tabla real/azar por unidad, mismos 500 sorteos y semilla, Wikcionario con candidatas para al menos el 40 % de las unidades, mínimo de cuatro unidades comparables por lengua) con los grupos de nivel I, I y II, II y III que resultan de la clasificación de cada juez y de la menos favorable (nivel más bajo dado por cualquiera), leídas de `2_criterios/jurado/respuestas/cruce_con_la_clave.tsv` (columnas `autor`, `Mistral`, `DeepSeek`, `Grok`, `menos_favorable`; se excluyen las filas de control). Un grupo con menos de cuatro unidades comparables con el euskera no se calcula. Declarada antes de enviar las fichas (entrada 7). Con el argumento `suficiencia` lee `respuestas_suficiencia/cruce_con_la_clave.tsv` (segunda pregunta, entrada 10) y escribe `t24_jurado_procedencia_suficiencia.json`.

### 4.22 `t25_correspondencias.py` — apartado 11.4, regularidad de las correspondencias

Unidades: las 30 de los plomos y los 10 numerales. Para cada lengua del Wikcionario con candidatas para al menos el 40 % de ellas, pareja de cada unidad con su candidata a menor distancia (3.1; empates, orden alfabético). Alineación de la primera forma ibérica reducida con la candidata por Needleman–Wunsch con los costes de 3.1 (vocal 0,5, consonante 1; sustitución vocal–vocal 0,5, otra 1; identidad 0), trazado con preferencia diagonal a igual coste; hueco «−». R: proporción de columnas cuyo par es el más frecuente para su clase (por clase ibérica, por clase vasca y media); R′: lo mismo sobre las columnas no idénticas. Permutación: 1.000 reasignaciones de candidatas entre unidades, generador `correspondencias|permutacion`. Comprobación de tamaño igualado: submuestras al azar de tantas columnas no idénticas como tiene el euskera (200 por lengua, 20 por permutación), generador `correspondencias|submuestra`. Declarada antes de ejecutarse (entrada 8); la comprobación de tamaño se añadió después.

### 4.23 `t26_prestabilidad.py` — apartado 11.5, gradiente de prestabilidad

Unidades: las 35 de `1_fuentes_lexicas/wold_prestabilidad_35_unidades.csv` (puntuación *Borrowed score* de WOLD, copiada a mano y publicada antes de calcular). Para cada unidad, *z* individual = (distancia real − media de los 500 sorteos) / desviación de los sorteos, con la tabla de 4.10 (`t15.tabla`, clave `prestabilidad`); Spearman (rangos medios en los empates) entre ese *z* y la puntuación, con el Wikcionario vasco y Open Data Euskadi, y para cada lengua del Wikcionario con candidatas para al menos el 40 % de las 35. Declarada antes de ejecutarse (entrada 9).

### 4.24 `t27_etimologia_vasca.py` — apartado 11.6, origen etimológico y fonotaxis de las candidatas vascas

Fuente: columna `etimologia` de `1_fuentes_lexicas/wikcionario/wikcionario_eu_en_v1.csv` (nota etimológica del Wikcionario inglés; 5.513 registros con nota). Regla declarada (entrada 11): *préstamo* si la nota empieza por «Borrowed from», «Borrowing from» o «Loanword from», o por «From» (o «Derived/Adapted from») seguido del nombre de una lengua donante (español, latín clásico, tardío, vulgar o medieval, francés, occitano, gascón, aragonés, romance, árabe, inglés, italiano, catalán, gallego, portugués); *heredado* si contiene «Proto-Basque» o empieza por «Inherited from»; *desconocido* en otro caso; *sin dato* si no hay nota. Los lemas se reducen con `NORM['Basque']` y `reducida`; una forma con varios lemas toma la clase heredado > préstamo > desconocido, y «mixto» si hay heredado y préstamo a la vez. Para cada unidad con candidatas en el Wikcionario vasco (`terminos_en`), la candidata a menor distancia (como en 4.22) y su clase. Proporción de préstamos entre las candidatas con nota frente a (a) todas las candidatas con nota de los mismos significados y (b) todo el léxico con nota; hipergeométrica (K préstamos entre las N candidatas con nota, n emparejadas con nota, k observadas) y 10.000 sorteos de una candidata con nota al azar por unidad (generador `etimologia|sorteo`). Control: las cuatro unidades de `PRESTAMOS_LATINOS`. Fonotaxis: modelo de trigramas de clases (con dos marcas iniciales y una final) con suavizado de Kneser–Ney interpolado (descuento 0,75, continuación en bigramas y unigramas, unigrama con suma de 0,5) sobre las formas heredadas y otro sobre las préstamo; una forma se clasifica como préstamo si su entropía por segmento es menor con el modelo de préstamos; validación cruzada de 10 pliegues (reparto con el generador `etimologia|pliegues`). Con el argumento `amplia`, regla posterior no declarada (véase la entrada 11) que admite «borrowed from» en cualquier posición; salida `t27_etimologia_vasca_amplia.json`. Versión 2 (tras la auditoría de la fase 4e; corrección documentada en la entrada 11): la clase de una candidata se decide solo con los lemas cuya glosa la hace elegible para la unidad; el préstamo se desglosa por donante (romance/latín frente a otro); la hipergeométrica y los sorteos usan las mismas unidades que el observado y se publican las dos colas; la fonotaxis clasifica además con las formas candidatas excluidas del entrenamiento. Las salidas de la versión 1 se conservan como `t27_etimologia_vasca_v1*`.

### 4.25 `t28_prediccion_prospectiva.py` — segundo artículo, predicción prospectiva (declaración 13)

`preparar`: fichas despojadas (regla mecánica en el programa) de las 36 unidades y fichas mecánicas de las 11 palabras de Hesperia declaradas; para cada una, cuatro significados candidatos (lema más próximo del Wikcionario vasco, gallego y latino sobre todo el diccionario, con la distancia del estudio y empate alfabético, más un lema vasco al azar con el generador `prospectiva|azar|<código>`), barajados con `prospectiva|orden|<código>`; clave con SHA-256 publicado antes de enviar. `puntuar`: recuento por juez y por mayoría frente a la binomial (p = 1/5 al admitirse «ninguno»), con el desglose sin U10.

### 4.26 `t29_sufijos.py` — segundo artículo, sufijos (declaración 12)

`preparar`: recuento mecánico de los sufijos del inventario declarado en todo el corpus (tema = antropónimo de dos formantes, unidad, u otra palabra atestiguada dos veces), y clave con SHA-256. `puntuar`: funciones fijadas por mayoría del jurado (≥2 de 3, sin «indeterminable»); distancia del estudio entre cada sufijo ibérico (primera variante, reducida) y el exponente vasco de su función (ergativo *-k*, genitivo *-(r)en*, gentilicio *-(t)ar*, determinante *-a*, «mitad» *erdi*; Trask 1997; Hualde y Ortiz de Urbina 2003); media real frente a 10.000 permutaciones de los exponentes entre las funciones (generador `sufijos|permutacion`). La comparación con las lenguas de referencia queda pendiente (desviación anotada en la declaración 12).

### 4.27 `t30_cloze.py` — segundo artículo, cloze como control de memoria (declaración 14)

`preparar`: fichas despojadas sin candidatos y tres encargos (primado euskera / gallego / sin primar). `puntuar`: forma propuesta reducida con el normalizador de la lengua primada (en la condición C, el vasco: decisión anotada, la declaración no fijaba referencia para C); distancia a la forma ibérica real frente a 1.000 palabras al azar de esa lengua e igual longitud (generador `cloze|azar|<código>`); proporción de unidades bajo la mediana del azar, también sin numerales y sin las unidades cuya nota del Wikcionario menciona el ibérico.

### 4.28 `t31_reclasificacion_m4.py` — apartado 8.4, reclasificación de la Monografía IV (declaración 16)

Importa `tabla`, `z_de` y los grupos de `t15_solidez_unidades.py` sin modificarlos (mismos 500 sorteos, mismas lenguas del Wikcionario con candidatas para al menos el 40 % de las unidades). Calcula el valor z del euskera, su puesto y la lengua siguiente en tres grupos del nivel II (con correspondencia vasca señalada después; sin ella; sin ella y sin los cuatro préstamos latinos), con la clasificación original (comprobación frente a la v38) y con la reclasificada (A7 y A18 pasan al grupo con correspondencia). Salida: `resultados/t31_reclasificacion_m4.json`.

## 5. Resultados esperados

El archivo `resultados/RESULTADOS_ESPERADOS.md` recoge, tabla por tabla, los valores que deben obtenerse y su comparación con los del artículo.
