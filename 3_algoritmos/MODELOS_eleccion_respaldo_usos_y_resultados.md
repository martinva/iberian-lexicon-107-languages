# Los modelos estadísticos del estudio: por qué se eligieron, respaldo, usos paralelos y resultados

Una ficha por modelo. El detalle de cada algoritmo está en `ALGORITMOS_Y_RESPALDO.md`; los criterios, en `2_criterios/CRITERIOS.md`; las cifras completas, en `resultados/RESULTADOS_ESPERADOS.md`.

Estado de lo que se dice de cada trabajo ajeno: **[V]** comprobado en la fuente o en su resumen; **[T]** se deduce solo del título.

---

## 1. Medida del parecido: distancia de edición sobre clases de sonidos

**Qué es.** Cada palabra se reduce a clases de sonidos (p y b son la misma clase, etc.) y se cuenta el coste mínimo de convertir una en otra, con las vocales a mitad de peso.

**Por qué se eligió.**
- El ibérico no tiene parientes seguros: no se pueden usar correspondencias regulares de sonidos, que es el método clásico. Hace falta una medida que no las presuponga.
- La escritura ibérica no distingue sordas de sonoras; las clases de sonidos igualan a todas las lenguas en ese punto.
- Es una medida simple, pública y sin parámetros ajustados al ibérico ni al euskera.

**Respaldo.** Clases de consonantes: Dolgopolsky (1986, citado por otros); Turchin, Peiros y Gell-Mann (2010) [V]; modelo SCA de List (2012) [V]. Distancia de edición normalizada: programa ASJP, Wichmann y otros (2010) [V].

**Usos paralelos.**
- Wichmann y otros (2010): evalúan medidas de distancia entre listas de 40 palabras de miles de lenguas [V].
- Jäger (2015): alineamiento ponderado sobre listas de 40 conceptos; concluye que hay apoyo para macrofamilias [T].
- Turchin y otros (2010): clases de consonantes con remuestreo, aplicadas al indoeuropeo, semítico y altaico; las protolenguas del altaico muestran una semejanza significativa (probabilidades entre 0,01 y menos de 10⁻⁵) [V].

**Comprobación propia.** Con 106 lenguas de familia conocida, la medida separa las parejas de la misma familia del resto con un área bajo la curva de 0,816 (0,5 sería el azar; 1, la separación perfecta).

**Decisión propia.** El medio peso de las vocales. Se eligió con parentescos conocidos, sin usar el ibérico ni el euskera.

---

## 2. Prueba con significados: prueba de permutación

**Qué es.** Para cada palabra ibérica se busca, en el diccionario de otra lengua, la palabra más parecida entre las del mismo significado. Se compara con lo que sale al sustituir esas palabras por otras al azar del mismo diccionario y de la misma longitud. Se repite 500 veces.

**Por qué se eligió.**
- No supone ninguna distribución teórica: el azar se mide sobre los propios datos.
- Admite muestras pequeñas (30 y 10 unidades).
- Sortear dentro del mismo diccionario descuenta su tamaño y su riqueza en sinónimos, que de otro modo favorecerían a los diccionarios grandes.
- Es el procedimiento habitual para esta pregunta desde hace medio siglo.

**Respaldo.** Oswalt (1970) y Ringe (1992), citados por otros; Baxter y Manaster Ramer (2000) [V]; Kessler (2001) [V], que es la monografía de referencia.

**Usos paralelos.**
- Kilani (2015): listas no básicas y varios candidatos por significado, aplicado al pregriego frente al protoeuskera, el protourálico y otros [V]. Es el diseño más cercano al nuestro. El resumen no da el resultado; hay que leerlo en el artículo.
- Blevins y Sproat (2021): protoeuskera frente a protoindoeuropeo, con validación en cien pares de lenguas de relación conocida [V]; presentan el resultado como evidencia estadística a favor [T].
- Kassian y otros (2021): prueba de permutación sobre reconstrucciones; apoyo parcial a la macrofamilia altaica [T].
- Ceolin (2019): aplica las pruebas de Oswalt, Ringe, Baxter–Manaster Ramer y Kessler al turco, mongol y manchú; apoyo solo parcial: mongol y manchú dan correspondencias significativas, turco y mongol una semejanza marginal que puede deberse al contacto, y turco y manchú no dan positivo en ninguna condición [V, resumen].
- Wichmann y otros (2010): corrigen la distancia entre palabras del mismo significado con la de palabras de significado distinto, que es la función que cumple aquí el sorteo [V].

**Azar igualado por longitud.** Las palabras de significado común son más cortas que la media del diccionario y por eso se parecen más a cualquier palabra breve. Sin corregirlo, lenguas sin relación daban valores de −4 a −6. En la comparación entre lenguas no se ha localizado un precedente. El mismo principio lo aplican Dautriche, Mahowald, Gibson y Piantadosi (2017) [V] dentro de cada lengua: permutan forma y significado solo entre palabras de la misma longitud, en 100 lenguas, y hallan que las palabras de significado próximo se parecen más en la forma.

**El sorteo.** Cada candidata se sustituye una vez por sorteo por una palabra de su misma longitud; dentro de cada longitud no se repite ninguna, y una candidata compartida por varias unidades recibe la misma sustituta en todas. Así el conjunto sorteado tiene la misma estructura que el real.

**Resultados.** Euskera primero con los siete diccionarios (de −9,7 a −12,8 en los completos); lengua siguiente entre −3,3 y −4,8, valor que procede en buena parte de las cuatro unidades propuestas como préstamos latinos. Sin ellas, el euskera se mantiene (de −9,6 a −12,1) y las lenguas romances quedan en el tramo de las lenguas sin relación (de +0,4 a −3,5).

---

## 3. Lenguas y parejas de control

**Qué es.** Las mismas pruebas, sin cambiar nada, aplicadas a casos de respuesta conocida: cuatro lenguas con parientes (umbro, gótico, córnico, dálmata), dos aisladas (etrusco, sumerio) y, en la segunda parte, 42 parejas de lenguas.

**Por qué se eligió.** Un valor de −11 no dice nada si no se sabe qué valor da el método cuando hay parentesco y cuando no lo hay. Es lo que convierte las cifras en una escala.

**Respaldo y uso paralelo.** Blevins y Sproat (2021) validan su método con cien pares de lenguas de relación conocida [V]. Es práctica general en la comparación automática (Wichmann y otros 2010; Jäger 2015).

**Resultados.** El pariente es la primera lengua en 18 de 20 muestras de la tabla 10 y, con 100 muestras por lengua, en 100 (dálmata), 95 (umbro), 90 (córnico) y 79 (gótico); ninguna de 200 muestras de lenguas sin parientes alcanza el valor ni la separación del ibérico con el euskera (mejor valor, −6,9, en el etrusco). Dálmata frente a romances, de −12,1 a −15,5; córnico frente a galés, de −6,7 a −13,6; sumerio, no pasa de −2,8. El valor del ibérico con el euskera es del orden del córnico con el galés.

---

## 4. Perfil de combinaciones de sonidos, con divergencia de Jensen-Shannon

**Qué es.** Se cuenta con qué frecuencia cada clase de sonido va seguida de cada otra en todo el vocabulario de una lengua, y se mide la diferencia entre los perfiles de dos lenguas. No usa significados.

**Por qué se eligió.**
- Los significados ibéricos son propuestas. Hacía falta una prueba que no dependiera de ellas.
- Usa todo el corpus (2.229 formas), no solo las 30 unidades.
- La divergencia de Jensen-Shannon es la medida estándar para comparar dos distribuciones de frecuencias: es simétrica y siempre está entre 0 y 1.

**Respaldo.** Macklin-Cordes, Bowern y Round (2021) [V]: en 112 vocabularios pama-ñunganos, la frecuencia de las transiciones entre clases de sonidos conserva señal de parentesco.

**En qué se aparta.** Ellos contrastan cada transición con un árbol conocido; no calculan distancias entre lenguas. La distancia entre perfiles y su validación son de este trabajo. Es el modelo con menos respaldo directo y por eso se validó aparte.

**Validación propia.** La lengua de perfil más próximo es de la misma familia en 77 de 98 lenguas (79 %; por azar, 20 %).

**Resultados.** Euskera primero de 107 (0,153; latín 0,174), en 500 de 500 remuestreos. En 17 parejas de lenguas con préstamo léxico intenso, la donante no es en ningún caso la de perfil más próximo (puesto mediano, 72 de 106); es un dato descriptivo, que no permite excluir el contacto. También con los plomos solos, con las lenguas reducidas a lo que el ibérico escribe y frente a 35 lenguas de otras zonas del mundo.

**Límites.** La manera de combinar sonidos también refleja tipología y contacto de área. Con las lenguas reducidas la prueba distingue peor (70 %) y el umbro deja de señalar al latín.

---

## 5. Serie numeral frente a una base mundial

**Qué es.** La serie ibérica se compara, valor a valor, con la de 3.811 lenguas. La propia base sirve de regla: a qué distancia tienen su vecino más próximo las lenguas sin parientes, y cuántas veces el vecino más próximo de una lengua es de su familia.

**Por qué se eligió.**
- Los numerales bajos son vocabulario básico, el menos expuesto al préstamo, y el único de ese tipo que ofrece el material.
- Tres valores (1, 10, 20) tienen apoyo externo (una marca monetal, un peso de piedra y una marca de capacidad; Ferrer i Jané 2022: 16-19), sin intervención del euskera.
- Una base mundial permite decir qué significa la distancia obtenida, sin supuestos.

**Respaldo.** Base de Chan (2019), edición de Numeralbank. La calibración con la propia base es de este trabajo; sigue la misma lógica de los controles (ficha 3).

**Resultados.** Euskera a 0,317; la segunda lengua, a 0,756. Ninguna de las 110 lenguas sin parientes en la base tiene un vecino tan próximo (la más cercana, 0,407). Cuando el vecino está entre 0,2 y 0,5, es de la misma familia en 162 de 165 casos.

---

## 6. Significados estables y poco estables

**Qué es.** Se separan los significados que rara vez se prestan (uno, dos, dar, tierra) de los que se prestan con facilidad, y se mide el parecido en cada grupo.

**Por qué se eligió.** Es la manera establecida de distinguir herencia de préstamo cuando no se dispone de gramática ni de correspondencias regulares: el préstamo se concentra en el vocabulario cultural; la herencia se ve sobre todo en el básico.

**Respaldo.**
- Tadmor, Haspelmath y Taylor (2010) [V, resumen]: sobre 41 lenguas, la proporción de préstamos varía de un campo semántico a otro; de ahí la lista Leipzig–Yakarta.
- Análisis por rangos de Chen Baoya, expuesto en Wang y Minett (2005: 123-124) [V], que advierten de que su fiabilidad no estaba establecida.

**Uso paralelo.** McMahon y otros (2005) [V, resumen]: sublistas más y menos estables aplicadas al quechua y al aimara; concluyen que el contacto es la explicación más probable. Es decir, el método también da «contacto» cuando lo hay.

**En qué se aparta.** Se aplica a 40 significados y con una medida de distancia, no con recuento de cognados. Por la advertencia de Wang y Minett, se comprobó con 42 parejas.

**Resultados.** Parientes cercanas 0,40 / 0,28; parientes lejanas 0,13 / 0,06; solo contacto 0,04 / 0,05. Ibérico–euskera 0,53 / 0,45. Con solo los significados con apoyo externo, 0,56. Con once significados estables, se presenta como indicio.

---

## 7. Proximidad por zonas

**Qué es.** El perfil de combinaciones de sonidos (ficha 4) calculado en cinco zonas, de norte a sur, con muestras del mismo tamaño.

**Por qué se eligió.** Si el ibérico y el vasco-aquitano hubieran formado una cadena continua de hablas, el ibérico del norte debería parecerse más al euskera. Es una previsión que se puede comprobar sin usar significados.

**Respaldo.** Dialectometría: Nerbonne (2010) [V], que mide cómo crece la diferencia lingüística con la distancia geográfica.

**Resultados.** Euskera primero en las cinco zonas, sin gradiente (de −2,2 a −2,5). El ibérico es muy uniforme. En los plomos de Narbonense–Rosellón, el euskera y el latín quedan casi igualados.

---

## 8. Remuestreo

**Qué es.** Repetir una prueba con muestras al azar del propio material (con reposición, o por mitades) para ver si el resultado depende de unas pocas palabras.

**Por qué se eligió.** Es la forma estándar de medir la estabilidad de un resultado sin supuestos teóricos. Turchin y otros (2010) lo usan con clases de consonantes [V].

**Resultados.** Euskera primero en todos los remuestreos del perfil de sonidos.

---

## 9. Declaración previa

**Qué es.** Fijar por escrito, antes de ejecutar, qué se mide, cómo y qué contaría en contra.

**Respaldo.** Roettger (2021) [V]: el registro previo separa el análisis confirmatorio del exploratorio y limita la posibilidad de ajustar el método al resultado. Aquí es un registro interno y fechado, no un depósito público.

---

## 10. Solidez frente a la lista de unidades

**Qué es.** La prueba con significados repetida quitando unidades (una a una, al azar, las más favorables) y cambiando los significados entre unidades.

**Por qué se eligió.** Los significados ibéricos son propuestas. Hay que saber si el resultado depende de unas pocas unidades y si la prueba deja de dar resultado cuando los significados se asignan mal, que es lo que debe ocurrir si mide una relación entre forma y significado.

**Respaldo.** Son análisis de sensibilidad habituales: quitar un dato cada vez, submuestreo y permutación de etiquetas. La permutación de la correspondencia entre forma y significado es el mismo principio de la prueba principal (Kessler 2001) y de Dautriche y otros (2017).

**Resultados.** Euskera primero al quitar cualquiera de las 30 unidades; con 20 al azar, en 2.000 de 2.000; con 10, en 1.975 de 2.000. Hay que quitar, eligiéndolas, 13 de las 28 comparables para que pierda el primer puesto. Con 15 significados cambiados el valor sigue en torno a −6; con los 30, queda en el nivel del azar. Con las 24 unidades cuyo significado se obtuvo sin comparación vasca (inventario cerrado de la Monografía IV), −9,3; siguiente, −4,0. En las 13 unidades de nivel II sin correspondencia vasca señalada, el euskera y el tagalo quedan prácticamente igualados (−4,4 y −4,3).

---

## 11. Permutación de los significados y corrección por el número de lenguas

**Qué es.** Las formas ibéricas y las candidatas se dejan como están y se cambia solo qué significado corresponde a cada unidad (100.000 repartos al azar). El valor real se compara con los de esos repartos. La probabilidad se multiplica por el número de lenguas comparadas.

**Por qué se eligió.** La prueba de sustitución depende de cómo se sortean las palabras del diccionario. Esta no sortea ninguna: mide directamente si las formas se parecen a las palabras de su significado propuesto más que a las de los otros significados de la lista. Y con 500 sorteos la menor probabilidad posible (0,002) no permite corregir por 32 lenguas.

**Respaldo.** Es la prueba de permutación de Oswalt (1970) y Kessler (2001) [V], con una distancia en lugar de un recuento de coincidencias. La corrección de Bonferroni es la habitual para comparaciones múltiples.

**Resultados.** Euskera: valor −10,1; ninguna de 100.000 permutaciones iguala la asignación propuesta; probabilidad corregida por 32 lenguas, 0,0003. Lo mismo con Open Data Euskadi, Azkue y WordNet. El gallego supera también el umbral con las 30 unidades (−4,0; corregida 0,003); sin las cuatro unidades propuestas como préstamos latinos lo pierde (0,19) y el euskera es la única lengua que lo conserva (−9,8; 0,0003). Permutación condicionada por la longitud: euskera −8,3; ninguna de 100.000; corregida, 0,0003 (gallego 0,002; tagalo 0,01); sin los cuatro préstamos, euskera −7,6 (0,0003), gallego 0,07, tagalo 0,71. Sustitución con 20.000 sorteos: −12,3; probabilidad corregida, 0,0016.

---

## Qué es de la bibliografía y qué es propio

| Elemento | Origen |
|---|---|
| Clases de sonidos, distancia de edición | Bibliografía, sin cambios |
| Medio peso de las vocales | Propio; validado con familias conocidas |
| Prueba de permutación con varios candidatos | Bibliografía (Kilani 2015) |
| Sorteo dentro del diccionario | Propio; misma función que la corrección de Wichmann y otros (2010) |
| Azar igualado por longitud | Propio entre lenguas; principio en uso (Dautriche y otros 2017) |
| Distancia entre perfiles de sonidos | Propia, sobre el hallazgo de Macklin-Cordes y otros (2021); validada aparte |
| Calibración de la serie numeral con la base mundial | Propia |
| Estables y poco estables con medida de distancia | Adaptación propia de Chen y de McMahon y otros; validada con 42 parejas |

## Lo que falta por comprobar

- Resultado de Kilani (2015): el resumen no lo da. No debe citarse en el artículo hasta leerlo en la fuente.
- McMahon y otros (2005) y Tadmor y otros (2010): leídos solo en resumen.
