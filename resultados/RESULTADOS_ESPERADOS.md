# Resultados esperados

*English version: `EXPECTED_RESULTS_en.md`.*

Valores que da cada programa de `4_programas/` con los datos de `1_fuentes_lexicas/`, Python 3 y la semilla del paquete (20261120). El artículo (borrador v26) da estas mismas cifras. La salida completa de cada programa, línea a línea, es el archivo `.log` del mismo nombre en esta carpeta, y los valores sin redondear están en el `.json`; este documento resume lo que una réplica debe encontrar.

**Cambio del 21-11-2026 (tercera ejecución, tras la segunda revisión de la auditoría).** Los archivos guardan ahora los valores *z* sin redondear (en pantalla y aquí, con dos decimales); `t15` guarda los extremos del ensayo de significados cambiados; `t20` corrige los rótulos de sus extremos; se añade `ʜ` a la tabla de clases (mueve una centésima algunos valores de la tabla 14 y ningún puesto).

**Cambio del 21-11-2026 (segunda ejecución).** Todos los programas se han vuelto a ejecutar tras las correcciones de la auditoría del código, declaradas antes en `DECLARACIONES_PREVIAS.md` (entrada 2). Ningún puesto cambia; los valores *z* se mueven menos de una unidad. Se retira el diccionario histórico derivado de Trask y se añade la permutación condicionada por la longitud (`t16`, parte d).

## Cómo leer la comparación

- **Exacto:** valores que no dependen de sorteos (distancias reales, puestos de la serie numeral, perfil de sonidos, recuentos del corpus). Deben repetirse sin diferencia alguna.
- **Con sorteos:** valores *z*, ventajas y recuentos de permutaciones. Con los mismos programas y la misma semilla se repiten con exactitud. Con otra semilla u otra implementación varían: en 40 repeticiones de la prueba de la tabla 6, el *z* del euskera va de −11,6 a −13,3 y el de las demás lenguas se mueve en torno a media unidad (`t20`).
- Lo que una réplica debe reproducir es el **puesto** de cada lengua y la **separación** con la siguiente, no la segunda cifra decimal de un *z*.
- **Permutación de los significados (`t16`):** se permutan solo las unidades que tienen candidatas en la lengua; las demás se retiran antes.

## Tablas 1 y 2 (`t01_t02_corpus.py`) — exacto

| Soporte | Inscripciones | Palabras | Distintas | No onomástico distinto |
|---|---|---|---|---|
| Plomo | 143 | 1.171 | 1.020 | 388 |
| Cerámica | 1.217 | 1.237 | 848 | 164 |
| Piedra | 214 | 379 | 339 | 122 |
| Otros | 25 | 41 | 40 | 13 |
| Total | 1.599 | 2.828 | 2.095 (suma por soportes: 2.247) | 679 (suma: 687) |

Plomo / cerámica: palabras por inscripción 8,2 / 1,0; una palabra o menos 33 / 1.103; cinco o más 71 / 9; diez o más 39 / 2; completas 729 / 639; longitud media 7,7 / 5,3; de dos o tres letras 81 / 258; de seis o más 512 / 236; nombres 33 % / 60 %; palabras en formas repetidas 15 % / 32 %; palabras que repiten una forma ya presente 9,3 % / 20,3 %.

## Tablas 4 y 5 (`t04_t05_numerales.py`) — exacto

3.811 lenguas, 239 familias, 110 sin parientes. Euskera 0,317, puesto 1; segunda, 0,756 (wapa). Lenguas sin parientes: la más próxima a su vecino, 0,407. Vecino entre 0,2 y 0,3, de la misma familia en 53 de 54; entre 0,3 y 0,4, 63 de 63; entre 0,4 y 0,5, 46 de 48; entre 0,2 y 0,5, 162 de 165. Valores 1, 10 y 20: euskera 0,435; primera no vasca, 0,584 (falam chin).

## Tablas 6 y 7 (`t06_t07_significados.py`)

Euskera, 30 unidades (real y azar, exactos con la semilla; *z*):

| Diccionario | Formas | Unidades | Real | Azar | *z* |
|---|---|---|---|---|---|
| Wikcionario | 3.814 | 28 | 0,432 | 0,817 | −12,77 |
| Azkue (1905-1906) | 31.253 | 30 | 0,503 | 0,784 | −10,26 |
| Reconstruido (Trask 2008) | 391 | 15 | 0,557 | 0,928 | −7,20 |
| Open Data Euskadi | 41.940 | 30 | 0,452 | 0,740 | −10,88 |
| Apertium, puente castellano | 7.028 | 28 | 0,526 | 0,863 | −9,95 |
| Apertium, puente inglés | 6.885 | 28 | 0,501 | 0,786 | −9,67 |
| WordNet | 17.989 | 30 | 0,379 | 0,658 | −11,86 |

Lenguas siguientes: Wikcionario (34 diccionarios), gallego −4,27, tagalo −3,87, asturiano −3,29, latín −0,46 (puesto 22); puente castellano (10), gallego −4,77, italiano −2,91, aragonés −2,83; puente inglés (9), catalán −3,63, islandés −3,23, castellano −3,09; WordNet (4), gallego −3,25, catalán −2,37, castellano −1,70.

Léxico metrológico (10 unidades), euskera: Azkue −11,44; reconstruido −10,69; Wikcionario −10,55; Open Data −11,30; Apertium castellano −10,22; Apertium inglés −10,36; WordNet −10,48. Segunda lengua: turco −3,32 (Wikcionario) y −3,39 (Apertium inglés).

## Tabla 8 (`t08_perfil.py`) — exacto, salvo los remuestreos

Clases completas: la lengua más próxima es de la misma familia en 77 de 98; reducidas, 69 de 98. Ibérico, todo el corpus (2.229 formas): euskera 0,153, latín 0,174, finés 0,205; plomos (1.072): 0,158 y 0,179; primero en 500 de 500 remuestreos y en 500 de 500 mitades. Reducidas: euskera 0,070, yakuto 0,094. Wikcionario (35 lenguas): euskera 0,106, finés 0,131 (validación 17 de 24); reducidas 0,058 y 0,090 (15 de 24); 300 de 300. Controles: umbro, latín 0,166; gótico, lak 0,251 e islandés 0,254; córnico, galés 0,124 y bretón 0,141; dálmata, sueco 0,151 y rumano 0,168; umbro reducido, portugués 0,120, euskera 0,124, latín 0,133.

## Calibración del perfil (`t22_calibracion_perfil.py`) — exacto

Clases completas: ibérico–euskera 0,1533; percentil 6,5 de 1.053 parejas de la misma familia; 0,11 de 4.618 de familias distintas (5 a esa distancia o menos; mínimo 0,1345, sueco–vepsio). Reducidas: 0,0696; percentiles 2,4 y 0,02 (1 pareja: estonio–hindi 0,0681). Lenguas sin parientes en la base: 9.

## Tabla 9 (`t09_prestamos.py`)

26 unidades, euskera: Wikcionario −12,06; Azkue −9,63; reconstruido −7,28; Apertium castellano −10,33; Open Data −10,20; Apertium inglés −10,58; WordNet −10,83. Siguientes: gallego −2,57 (Wikcionario), −3,49 (Apertium), −1,43 (WordNet); islandés −3,13; catalán −2,89 (Apertium inglés); latín +0,37. Cuatro préstamos: gallego −4,62 / −4,50 / −4,96; tagalo −4,62; asturiano −4,59 / −3,89; aragonés −4,06; occitano −3,95; catalán −3,66; euskera −2,94 (Wikcionario), −2,62 (Azkue), −3,38 (Open Data), −1,95 y −1,45 (Apertium), −3,05 (WordNet).

## Apartado 8.2 (`s82_formas_y_sinonimos.py`)

24 lenguas. 30 unidades, euskera: cita −12,11 (gallego −4,32); con formas flexionadas −10,77 (tagalo −3,37); con sinónimos −12,10 (gallego −4,56); con ambas −11,08 (tagalo −2,88). Léxico metrológico: cita −10,11 (turco −3,64); con formas −11,85 (gallego −1,66).

## Tabla 10 (`t10_controles.py`) y potencia (`t19_potencia_controles.py`)

Cinco muestras: umbro 5 de 5 (−4,62 a −8,08); gótico 4 de 5 (−3,01 a −6,81); córnico 4 de 5 (−6,67 a −13,58); dálmata 5 de 5 (−12,07 a −15,48); etrusco, −2,39 a −4,76; sumerio, −1,61 a −2,76.

Cien muestras:

| Lengua | Pariente primero | *z* de la primera (mediana; mejor) | Separación (mediana; mayor) | Alcanza −9,3 | Alcanza 5,6 |
|---|---|---|---|---|---|
| Dálmata | 100 | −13,96; −18,01 | 1,21; 4,74 | 100 | 0 |
| Umbro | 95 | −6,17; −9,41 | 1,13; 5,77 | 1 | 1 |
| Córnico | 90 | −9,79; −15,12 | 2,96; 8,11 | 64 | 14 |
| Gótico | 79 | −4,56; −9,83 | 1,55; 6,36 | 1 | 2 |
| Etrusco | — | −3,44; −6,85 | 0,43; 2,64 | 0 | 0 |
| Sumerio | — | −2,17; −3,75 | 0,29; 1,69 | 0 | 0 |

Etrusco: la primera lengua es el latín en 39 muestras, el asturiano en 17, el rumano en 12 y el siciliano en 9.

## Tabla 10 bis y apartado 8.4 (`t15_solidez_unidades.py`)

32 lenguas. Lista completa: euskera −12,53; gallego −4,07. Quitando una unidad: primero en 30 de 30; de −11,75 a −12,97; menor separación 7,48. Al azar: 20 unidades, 2.000 de 2.000, mediana −10,14; 15, 1.999, −8,76; 10, 1.975, −7,16.

| Grupo | Unidades (comparables) | Euskera | Siguiente |
|---|---|---|---|
| Nivel I | 5 (4) | −5,75 | catalán −3,15 |
| Nivel II | 19 (18) | −8,06 | gallego −3,80 |
| Nivel III (toponimia) | 6 (6) | −8,29 | galés −2,35 |
| Niveles I y II | 24 (22) | −9,28 | gallego −3,97 |
| Nivel II con correspondencia señalada | 6 (6) | −7,27 | gallego −2,83 |
| Nivel II sin correspondencia | 13 (12) | −4,43 | tagalo −4,25 |
| Las mismas sin préstamos latinos | 9 (8) | −3,15 | albanés −2,41 |
| Sin las 5 con lectura alternativa (`t21`) | 25 | −11,84 | gallego −3,61 |

Retirada adversa: el euskera pierde el primer puesto al quitar 13 unidades; su valor sube de −3 al quitar 15. Significados cambiados (medianas; Open Data / Wikcionario / WordNet): ninguno −10,99 / −12,58 / −11,64; 5: −9,39 / −10,66 / −9,78; 10: −7,46 / −8,75 / −8,02; 15: −5,66 / −6,62 / −6,26; 20: −4,02 / −4,63 / −4,47; 30: −0,29 / −0,62 / −0,63. Con 15 cambiados, Open Data: percentil 5 −7,87, percentil 95 −3,58, caso más marcado −10,25, menos marcado −1,80 (el archivo guarda los cuatro valores para cada tamaño y diccionario).

## Apartado 8.4, tamaño de los diccionarios (`t23_tamano_diccionario.py`) — exacto

32 lenguas; Spearman(formas, *z*) −0,337 (−0,378 sin el euskera); euskera 3.814 formas, puesto 21 de 32 por tamaño; mediana 6.646.

## Tabla 10 bis con la clasificación del jurado (`t24_jurado_procedencia.py`) — exacto

| Clasificación | Niveles I y II (unidades; comparables) | Euskera | Siguiente | Nivel III | Nivel II solo |
|---|---|---|---|---|---|
| Autor | 24; 22 | −9,28 | gallego −3,97 | −8,29 (galés −2,35) | −8,06 (gallego −3,80) |
| Mistral | 17; 16 | −6,60 | tagalo −4,13 | −11,10 (gallego −2,34) | −6,24 (tagalo −4,05) |
| DeepSeek | 17; 16 | −6,60 | tagalo −4,13 | −11,10 (gallego −2,34) | −5,26 (tagalo −4,89) |
| Grok (crítico) | 12; 11 | −6,57 | albanés −2,23 | −10,81 (gallego −4,24) | −6,19 (albanés −2,31) |
| Menos favorable | 12; 11 | −6,57 | albanés −2,23 | −10,81 (gallego −4,24) | −6,19 (albanés −2,31) |

Segunda pregunta (suficiencia; `t24_jurado_procedencia.py suficiencia`): menos favorable, niveles I y II 12; 11, euskera −8,63, catalán −3,08; nivel II −8,24 (catalán −3,19); nivel III −9,24 (tagalo −4,23). Mistral I y II −9,32 (16; 15; gallego −3,72); DeepSeek −9,47 (13; 12; catalán −3,26); Grok −10,26 (19; 18; gallego −3,81).

El grupo «solo nivel I» se calcula únicamente con la clasificación del autor (−5,75; catalán −3,15); con las demás quedan menos de cuatro unidades comparables.

## Apartado 11.4, correspondencias (`t25_correspondencias.py`) — exacto

Euskera: 38 parejas, 195 columnas, 77 no idénticas; R 0,641; R′ 0,442. Permutación (1.000): R′ mediana 0,315, percentil 90 0,337, ninguna ≥ 0,442. Lenguas: 32; euskera 1.º por R′ (lituano 0,385). Tamaño igualado a 77: permutación mediana 0,378, p90 0,396, ninguna ≥ 0,442; lenguas: euskera 0,442, lituano 0,438, hausa 0,418.

## Apartado 11.5, prestabilidad (`t26_prestabilidad.py`) — exacto

ρ: Wikcionario −0,146 (34 unidades); Open Data Euskadi −0,039 (35). 33 lenguas: mediana −0,004, mínimo −0,452, máximo +0,305.

## Apartado 11.6, origen etimológico y fonotaxis (`t27_etimologia_vasca.py`) — exacto

Versión 2 (la vigente). Regla declarada: formas 423 préstamo, 540 heredado, 2.399 desconocido, 1.090 sin dato. Emparejadas: 38 con candidata, 31 con nota elegible; 2 préstamo (romance/latín 1), 18 heredado, 11 desconocido; proporción 0,065 frente a 0,125 (mismas unidades) y 0,126 (léxico); hipergeométrica p(≥2) 0,961 y p(≤2) 0,162; sorteo media 2,24, p(≥2) 0,7193. Control: *koŕta* préstamo (romance/latín), *bale* sin dato, *oŕtin* desconocido, *saltu* heredado. Fonotaxis: validación cruzada 0,839 / 0,804; fuera de muestra 11 de 38 como préstamo (con las candidatas en el entrenamiento, 8). Con `amplia`: 3/31 (romance 2) frente a 0,167 y 0,209; p(≥3) 0,959, p(≤3) 0,143; fonotaxis fuera de muestra 11 de 38. (Versión 1, conservada en `t27_etimologia_vasca_v1*`: 2/32 = 0,062; fonotaxis 8 de 38.)

## Tabla 10 ter y apartado 8.5 (`t16_contraste_principal.py`)

| Prueba | Lengua | *z* | Iguales o mejores de 100.000 | *p* corregida |
|---|---|---|---|---|
| (b) 30 unidades, 32 lenguas | Euskera | −10,09 | 0 | 0,00032 |
| | Gallego | −3,97 | 7 | 0,00256 |
| | Albanés | −3,12 | 118 | 0,038 |
| | Tagalo | −3,11 | 168 | 0,0541 |
| | Catalán | −2,69 | 473 | 0,152 |
| | Asturiano | −2,66 | 582 | 0,187 |
| (c) sin los cuatro préstamos, 31 lenguas | Euskera | −9,77 | 0 | 0,00031 |
| | Gallego | −2,64 | 603 | 0,187 |
| | Albanés | −2,38 | 1.019 | 0,316 |
| | Tagalo | −1,62 | 5.576 | 1 |
| (d) condicionada por la longitud | Euskera | −8,34 | 0 | 0,00032 |
| | Gallego | −4,17 | 5 | 0,0019 |
| | Tagalo | −3,58 | 33 | 0,011 |
| | Catalán | −2,82 | 299 | 0,096 |
| | Asturiano | −2,39 | 1.076 | 0,345 |
| | Albanés | −2,12 | 2.047 | 0,655 |
| (d) sin los cuatro préstamos, 31 lenguas | Euskera | −7,63 | 0 | 0,00031 |
| | Gallego | −2,99 | 240 | 0,075 |
| | Tagalo | −2,08 | 2.294 | 0,71 |
| | Catalán | −1,80 | 3.895 | 1 |

Otros diccionarios del euskera, (b): Open Data −9,10; Azkue −8,74; WordNet −9,32; 0 de 100.000 en los tres. WordNet castellano −1,59. (d), euskera: 9,04 × 10^15 permutaciones distintas posibles; 27 unidades pueden cambiar. (a) Sustitución con 20.000 sorteos: *z* −12,32; *p* 0,00005; corregida 0,0016.

## Tablas 11 a 13 (`t11_t13_estables.py`)

| Relación | Parejas | Estables | Poco estables | Estables mayor en |
|---|---|---|---|---|
| Emparentadas cercanas | 7 | 0,405 | 0,279 | 7 |
| Emparentadas lejanas | 12 | 0,133 | 0,060 | 11 |
| Parentesco lejano y préstamos | 2 | 0,148 | 0,055 | 2 |
| Solo contacto | 13 | 0,036 | 0,051 | 5 |
| Sin relación | 8 | −0,014 | −0,006 | 3 |

El valor de cada pareja está en `t11_t13_estables.log`. Ibérico frente al euskera: estables 0,533 (11); poco estables 0,445 (27); sin los numerales del dos al cinco 0,447; sin *saltu* 0,588. Segunda lengua en estables: galés 0,145. Por origen: dato externo 0,560 (7); numerales del dos al ocho 0,740 (7); casilla 0,307 (18); toponimia 0,548 (6); cuatro préstamos 0,238 (frente al gallego, 0,341).

## Tabla 14 (`t14_zonas.py`) — exacto, salvo las muestras igualadas

Solo plomos / todas las inscripciones (muestra completa de cada zona, campo `relativa`): Narbonense–Rosellón −2,16 / −2,25; Cataluña −2,52 / −2,37; Ebro–Castellón −2,39 / −2,37; Valencia −2,49 / −2,42; Sudeste −2,37 / −2,42. Narbonense, muestras igualadas: euskera primero en 197 de 300. Variación: misma zona 0,073; vecinas 0,083; no vecinas 0,092; extremos 0,101.

## Tabla 15 (`t18_perfil_contacto.py`) — exacto

Puesto de la donante (de 106): euskera–castellano 76, –latín 19, –catalán 65; húngaro–turco 21; rumano–búlgaro 7; albanés–latín 17, –griego 85; japonés–chino 73; coreano–chino 72; finés–sueco 27; inglés–francés 32; persa–árabe 105; turco–árabe 94, –persa 103; bretón–francés 5; armenio–persa 96; hindi–persa 87. Mediana, 72.

## Apartado 8.4, ensayo sobre la circularidad (`t17_techo_circularidad.py`) — no concluyente

Euskera con los significados propuestos: −13,68. Eligiendo los significados a conveniencia dentro del campo de cada unidad: malayo −12,11 (euskera −15,40). Eligiéndolos sin restricción: malayo −15,89 (euskera −14,98). Otras lenguas alcanzan, con esa libertad, valores como el del euskera: la prueba no sirve para acotar la circularidad, y así se dice en el artículo.

## Anexo A.3 (`a3_comprobacion_medida.py`) — exacto

106 lenguas, 5.565 parejas, 1.053 de la misma familia, 843 de parentesco antiguo. Área bajo la curva 0,816 (0,777 en los parentescos antiguos); entre 0,776 y 0,853 según el sorteo. Este programa conserva su semilla original (20261118).

## Anexo B.7, variación entre semillas (`t20_variacion_semillas.py`)

40 repeticiones de la prueba de la tabla 6 con claves de sorteo distintas. Euskera primero en 40; valor de −11,59 (menos marcado) a −13,33 (más marcado); mediana −12,38; desviación 0,41. Mejor de las demás: de −3,93 a −4,44; desviación 0,12. Separación: menor 7,31; mediana 8,28; mayor 9,06. Demás lenguas: amplitud mediana 0,28; mayor 0,57. Tarda en torno a tres horas en un solo proceso; puede repartirse por tramos (`python3 t20_variacion_semillas.py 1 20`).

## Observaciones

- Las cifras de la primera ejecución (antes de las correcciones del 21-11-2026) quedan en el historial del repositorio.
- La prueba (d) de `t16` sin los cuatro préstamos se calcula en la misma pasada que la (c) y se guarda en `c_permutacion_sin_prestamos[*].condicionada_por_longitud`.
- La variación entre semillas se ha medido en la prueba de la tabla 6; en las demás pruebas no.

## t32–t35 (declaraciones 17, 19 y 20; 22-11-2026)

| Programa | Cifra de referencia |
|---|---|
| t32_mapa_distancias.py | Léxico: 36 lenguas; vecino del ibérico, euskera 0,4513 (turco 0,8633); familia del vecino 21/24; ejes 0,1731 y 0,1037. Perfil: euskera 0,1065, finés 0,1313; 17/24 |
| t32c_vecino_remuestreos.py | Euskera vecino del ibérico en 200/200 remuestreos, recíproco 200/200; distancia 0,3332–0,5838 |
| t33_prestamo_conjunto_wold.py | Regla amplia: todos los numerales 3/41, mitad de los demás 7/41, ambos 0/41; estricta: 1/41, 3/41, 0/41 |
| t34_razon_verosimilitud.py | R1 18/19 vs 5/13, 2,35 [1,39; 5,69]; R2 2,1; R3 0,7; R4 77/98 vs 0/17, 28,18 |
| t35_perfil_suceso_equivalente.py | R4b 2/8 vs 0/10, 6,11 [0,73; 5292,27]; R4c 8/17 vs 0/10, 10,39 [1,98; 9485,36] |
