# Algoritmos y su respaldo

Para cada algoritmo: qué hace, un ejemplo, de dónde procede y en qué se aparta de sus precedentes. La formulación paso a paso está en `5_especificacion/ESPECIFICACION_FUNCIONAL_es.md`, apartado 3. Las referencias completas y su estado de verificación, en `2_criterios/CRITERIOS.md` y en la bibliografía del artículo.

## 1. Distancia entre dos palabras

**Qué hace.** Convierte cada palabra en una cadena de clases de sonidos y mide el coste mínimo de transformar una en otra, con las vocales a mitad de coste, dividido por la longitud media ponderada.

**Ejemplos.**

| Ibérico | Otra forma | Formas reducidas | Operaciones | Distancia |
|---|---|---|---|---|
| *luŕa* | *lur* | LuRa / LuR | suprimir una vocal | 0,5 / 2,75 = 0,18 |
| *śalir* | *zilar* | SaLiR / SiLaR | sustituir dos vocales | 1 / 4 = 0,25 |
| *laku* | *lagun* | LaKu / LaKuN | añadir una consonante | 1 / 3,5 = 0,29 |
| *abaŕ* | *hamar* | aPaR / aMaR | sustituir una consonante | 1 / 3 = 0,33 |

**Procedencia.** La distancia de edición normalizada es la medida del programa ASJP (Wichmann y otros 2010). Las clases de sonidos, de Dolgopolsky (1986) y List (2012). Jäger (2015) usa la misma base, con pesos aprendidos de los datos, sobre listas de 40 conceptos.

**En qué se aparta.** El medio peso de las vocales es una decisión propia. Se eligió con parentescos conocidos (NorthEuraLex), sin usar el ibérico ni el euskera, porque era la variante que mejor separaba las lenguas de la misma familia.

## 2. Prueba con significados

**Qué hace.** Para cada unidad ibérica busca, en un diccionario, las palabras del mismo significado y anota la más próxima. La media de esas distancias se compara con la que resulta al sustituir las palabras del mismo significado por palabras al azar de la misma longitud.

**Ejemplo.** Con el léxico de Open Data Euskadi, la distancia media de las 30 unidades a la palabra más próxima de su significado es 0,45; con palabras al azar de la misma longitud, 0,74; ninguno de 500 sorteos da 0,45 o menos.

**Procedencia.** Prueba de permutación sobre listas de palabras: Oswalt (1970), Ringe (1992), Baxter y Manaster Ramer (2000), Kessler (2001). Varios candidatos por significado y listas no básicas: Kilani (2015). Corrección por la distancia entre palabras de significado distinto: Wichmann y otros (2010).

**En qué se aparta.** (a) El sorteo se hace dentro del propio diccionario, lo que descuenta su tamaño y su riqueza de sinónimos. (b) Las palabras sorteadas tienen la misma longitud que las sustituidas; en cada sorteo no se repite ninguna, y una candidata compartida por varias unidades recibe la misma sustituta en todas. (c) El contraste principal añade la permutación de los significados entre las unidades (Oswalt 1970; Kessler 2001), que no sortea ninguna palabra, y la corrección de Bonferroni por el número de lenguas. Sin precedente localizado en la comparación entre lenguas; el mismo principio, permutar solo entre palabras de igual longitud, lo aplican Dautriche y otros (2017) dentro de cada lengua. Aquí lo motivaron las lenguas de control.

## 3. Perfil de combinaciones de sonidos

**Qué hace.** Cuenta con qué frecuencia cada clase de sonido sigue a cada otra en el vocabulario de una lengua, incluidos el inicio y el fin de palabra, y mide la diferencia entre los perfiles de dos lenguas. No usa significados.

**Ejemplo.** La palabra `SaLiR` aporta los pares `^S`, `Sa`, `aL`, `Li`, `iR`, `R$`.

**Procedencia.** Macklin-Cordes, Bowern y Round (2021) muestran que la frecuencia de las transiciones entre clases de sonidos conserva señal de parentesco; contrastan cada transición con un árbol conocido y no calculan distancias entre lenguas.

**En qué se aparta.** La distancia entre perfiles (divergencia de Jensen-Shannon) y su validación son de este trabajo. Validación: en NorthEuraLex, la lengua de perfil más próximo es de la misma familia en 77 de 98 lenguas con parientes en la base (79 %; por azar, 20 %).

**Límite.** La manera de combinar los sonidos refleja también la tipología y el contacto de área, no solo la herencia.

## 4. Serie numeral

**Qué hace.** Compara la serie numeral ibérica, valor a valor, con la de cada lengua de una base mundial, y usa la propia base para saber qué significa la distancia obtenida: a qué distancia tienen su vecino más próximo las lenguas sin parientes, y con qué frecuencia el vecino más próximo de una lengua es de su familia.

**Procedencia.** Base de Chan (2019). El uso de la propia base como referencia empírica es de este trabajo.

## 5. Ventaja en significados estables y poco estables

**Qué hace.** Separa los significados en dos grupos, según figuren o no en las listas de vocabulario básico, y mide en cada uno cuánto más cerca queda la palabra de la que le corresponde por significado que de palabras al azar.

**Lectura.** En lenguas emparentadas, la ventaja es mayor en los significados estables. En lenguas que solo han tenido contacto, es pequeña y no se concentra en ellos.

**Procedencia.** Análisis por rangos de Chen Baoya (en Wang y Minett 2005: 123-124); sublistas de McMahon y otros (2005); listas de Tadmor, Haspelmath y Taylor (2010) y de Swadesh.

**En qué se aparta.** Se aplica a los 40 significados disponibles, no a las listas completas, y con una medida de distancia en lugar del recuento de cognados. Por eso se valida con 42 parejas de lenguas de relación conocida.

## 6. Proximidad por zonas

**Qué hace.** Calcula el perfil de combinaciones de sonidos de cada zona del territorio ibérico y su distancia al euskera, con muestras igualadas en tamaño, para ver si la proximidad cambia de norte a sur.

**Procedencia.** Dialectometría (Nerbonne 2010).

**Límite.** No hay textos de la zona de contacto con el vasco-aquitano.
