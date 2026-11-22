# Criterios del estudio y su justificación

Cada criterio se enuncia, se justifica y, cuando lo hay, se remite al uso equivalente en la bibliografía. La aplicación exacta de cada uno está en `5_especificacion/ESPECIFICACION_FUNCIONAL_es.md`.

Estado de las referencias: **[V]** comprobada en la fuente o en su registro editorial; **[P]** comprobada en parte (se indica qué falta); **[C]** citada a través de otra obra.

## 1. Qué léxico ibérico se compara

**Criterio.** Dos conjuntos cerrados: la serie numeral y las unidades de medida (léxico con soporte metrológico), y las 30 unidades léxicas de los plomos de contenido económico.

**Justificación.**
- El soporte se elige por una razón objetiva: los plomos son el 9 % de las inscripciones y reúnen el 41 % de las palabras y más de la mitad del vocabulario que no es nombre propio; solo en ellos las palabras aparecen de forma regular dentro de un texto, junto a cifras y en posiciones que se repiten (tablas 1 y 2).
- Dentro de los plomos no se seleccionan palabras para este estudio: se toman las unidades que resultan del análisis de esos documentos en las monografías I–IV.
- Los significados se propusieron antes de la comparación, por la posición de cada término en las casillas de los documentos y por su relación con cifras y unidades de medida.

**Uso equivalente.** Listas cerradas, no limitadas al vocabulario básico y con varios términos por significado: Kilani (2015) **[V]**.

## 2. Cómo se expresa un significado

**Criterio.** Cada unidad lleva una lista de términos castellanos e ingleses, fijada antes de consultar ningún diccionario. Una palabra de un diccionario es candidata si su glosa coincide exactamente con uno de esos términos, quitados artículos y aclaraciones entre paréntesis. No se admiten coincidencias parciales.

**Justificación.** La coincidencia exacta impide ampliar a voluntad el número de candidatas. La lista de términos es pública y forma parte de los datos.

## 3. Grado de certeza y origen de cada significado

**Criterio.** Cada unidad lleva un grado (A, valor asegurado por la metrología o por la bibliografía; B, regularidad documentada en un texto o grupo de textos; C, hipótesis de trabajo) y un origen (por dato externo; por posición en la serie numeral; por la casilla documental; con apoyo de la toponimia).

**Justificación.** Permite dar los resultados por separado para los significados obtenidos sin intervención del euskera y para los demás (tabla 13), y así medir cuánto del resultado podría deberse a la manera de asignar los significados.

## 4. Clases de sonidos

**Criterio.** Las comparaciones se hacen entre formas reducidas a clases de sonidos, con el modelo SCA y su tabla tal como la distribuye LingPy, sin modificar.

**Justificación y uso equivalente.** Agrupar las consonantes según su tendencia a sustituirse unas por otras en la evolución de las lenguas es un procedimiento establecido: Dolgopolsky (1986) **[C]**; Turchin, Peiros y Gell-Mann (2010) **[V]**, que lo aplican al indoeuropeo, al semítico y al altaico; List (2012) **[V]**, que lo amplía en el modelo SCA. Es la agrupación de referencia de la comparación léxica automática actual.

**Comprobación propia.** Con las 106 lenguas de NorthEuraLex clasificadas por familias y listas de 40 conceptos, la distancia separa las parejas de la misma familia de las demás con un área bajo la curva de 0,816 (0,777 en los parentescos antiguos). Programa `a3_comprobacion_medida.py`.

## 5. De la ortografía a los sonidos

**Criterio.** NorthEuraLex ofrece transcripción fonética y se reduce directamente. Los diccionarios se toman en su ortografía y se pasan a una grafía común con reglas generales por lengua, fijadas antes de ejecutar las pruebas y aplicadas a todas las palabras de la lengua.

**Justificación.** No hay transcripción fonética de los diccionarios completos. Las reglas son aproximadas, pero son las mismas para todas las palabras de una lengua, de modo que no pueden favorecer a unas unidades frente a otras. Su efecto se contrasta con las lenguas de control, tratadas con el mismo procedimiento.

**Límite.** Una ortografía opaca (irlandés, francés) queda peor representada que una transparente (euskera, finés). Esto puede perjudicar a esas lenguas; no puede explicar el resultado del euskera frente a otras lenguas de ortografía igualmente transparente.

## 6. Escritura ibérica

**Criterio.** Las formas ibéricas se toman en la transcripción de Hesperia. La escritura no distingue de forma general sordas y sonoras: *b*/*p*, *t*/*d* y *k*/*g* caen en la misma clase en los dos lados de la comparación, porque el modelo SCA agrupa cada pareja.

**Comprobación.** El perfil de combinaciones de sonidos se repite reduciendo todas las lenguas al inventario que el ibérico escribe; el resultado no cambia (tabla 8).

## 7. Descuento del azar

**Criterio.** El valor observado se compara con el que se obtiene sustituyendo las palabras de significado coincidente por palabras tomadas al azar del mismo diccionario y de la misma longitud, sin repetir ninguna dentro de un sorteo y dando la misma sustituta a una candidata que comparten varias unidades. En el contraste principal se añaden la permutación de los significados entre las unidades y la corrección por el número de lenguas comparadas (Bonferroni).

**Justificación y uso equivalente.** Las pruebas de permutación son el procedimiento habitual para valorar el parecido entre listas de palabras: Oswalt (1970) **[C]**; Ringe (1992) **[C]**; Baxter y Manaster Ramer (2000) **[V]**; Kessler (2001) **[V]**; Kilani (2015) **[V]**; Ceolin (2019) **[V]**; Kassian y otros (2021) **[V]**. Corregir la distancia entre palabras del mismo significado con la distancia entre palabras de significado distinto, dentro de la misma pareja de lenguas, es lo que proponen Wichmann y otros (2010) **[V]**; el sorteo dentro del propio diccionario cumple esa función.

**Igualar la longitud.** En la bibliografía de comparación entre lenguas no se ha localizado un precedente de igualar la longitud de las palabras sorteadas. El principio sí está en uso en un problema vecino: Dautriche, Mahowald, Gibson y Piantadosi (2017) **[V]**, al medir en 100 lenguas si las palabras de significado próximo se parecen más en la forma, obtienen el nivel de azar permutando la correspondencia entre forma y significado solo entre palabras de la misma longitud, por la misma razón: la longitud condiciona por sí sola la distancia entre formas. Aquí se adoptó porque las lenguas de control mostraron que, sin ello, lenguas sin parentesco obtenían valores de −4 a −6: las palabras de significado común son más cortas que una palabra cualquiera del diccionario. Con la corrección, una lengua aislada no pasa de −2,5.

## 8. Lenguas de control

**Criterio.** Las mismas pruebas, sin cambiar nada, se aplican a lenguas cuya filiación se conoce (umbro, gótico, córnico, dálmata) y a lenguas aisladas (etrusco, sumerio); y, en la segunda parte, a 42 parejas de lenguas emparentadas, en contacto o sin relación.

**Justificación y uso equivalente.** Validar un método de comparación con parejas de relación conocida: Blevins y Sproat (2021) **[V]**, con cien pares de lenguas.

## 9. Significados estables y poco estables

**Criterio.** Un significado es estable si su glosa principal figura en la lista Leipzig–Yakarta de 100 significados o en la lista de Swadesh de 207.

**Justificación y uso equivalente.** Los significados difieren en su resistencia al préstamo: Tadmor, Haspelmath y Taylor (2010) **[V: resumen]**, sobre 41 lenguas, de donde procede la lista Leipzig–Yakarta. Comparar la semejanza en un rango básico y en otro menos básico para separar herencia y contacto es el análisis por rangos de Chen Baoya, expuesto en Wang y Minett (2005: 123-124) **[V]**, que advierten de que su fiabilidad no estaba establecida. Sublistas de significados muy estables y poco estables, aplicadas al quechua y al aimara: McMahon y otros (2005) **[V: resumen y extracto]**; en ese caso el resultado apuntó al contacto.

**Adaptación propia.** Las listas se aplican a los 40 significados disponibles, y la medida es la ventaja sobre el azar, no la proporción de cognados. Por la advertencia citada, su capacidad de distinguir se comprueba con las 42 parejas de control.

## 10. Zonas

**Criterio.** Cinco zonas de norte a sur, definidas por la sigla de procedencia de Hesperia. Se comparan con muestras del mismo tamaño.

**Justificación y uso equivalente.** La relación entre distancia lingüística y distancia geográfica es el objeto de la dialectometría: Nerbonne (2010) **[V: manuscrito del autor; referencia de la versión publicada comprobada]**.

## 11. Declaración previa

**Criterio.** La delimitación del léxico, la regla de medida, el tratamiento de las grafías, la forma de descontar el azar, las lenguas y parejas de control y la lectura de cada resultado se fijaron por escrito antes de ejecutar cada prueba.

**Justificación y uso equivalente.** Impide ajustar el método al resultado. Fijar por escrito y con fecha, antes del análisis, cómo se medirá y cómo se leerá el resultado es la práctica del registro previo, que separa el análisis confirmatorio del exploratorio y limita los «grados de libertad del investigador»: Roettger (2021) **[V]**, que la admite también para datos ya existentes, siempre que se declare lo que se sabía de ellos.

**Límite.** Aquí la declaración es interna (un registro fechado propio), no un depósito en un registro público.

## Referencias añadidas en este documento

- List, J.-M. (2012). SCA: Phonetic alignment based on sound classes. En/In D. Lassiter & M. Slavkovik (eds.), *New Directions in Logic, Language and Computation* (Lecture Notes in Computer Science 7415), 32–51. Berlin, Heidelberg: Springer. doi:10.1007/978-3-642-31467-4_3
- Roettger, T. B. (2021). Preregistration in experimental linguistics: applications, challenges, and limitations. *Linguistics* 59(5), 1227–1249. doi:10.1515/ling-2019-0048
- Macklin-Cordes, J. L., Bowern, C. & Round, E. R. (2021). Phylogenetic signal in phonotactics. *Diachronica* 38(2), 210–258. doi:10.1075/dia.20004.mac  (112 vocabularios pama-ñunganos / 112 Pama-Nyungan vocabularies)
- Nerbonne, J. (2010). Measuring the diffusion of linguistic change. *Philosophical Transactions of the Royal Society B* 365(1559), 3821–3828. doi:10.1098/rstb.2010.0048
- Dautriche, I., Mahowald, K., Gibson, E. & Piantadosi, S. T. (2017). Wordform similarity increases with semantic similarity: An analysis of 100 languages. *Cognitive Science* 41(8), 2149–2169. doi:10.1111/cogs.12453
