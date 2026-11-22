# Protocolo para medir la afinidad de una lengua de corpus reducido con significados propuestos

Este documento describe el procedimiento del estudio como un protocolo aplicable a otras lenguas. Las piezas proceden de la lingüística comparada cuantitativa (véase `MODELOS_eleccion_respaldo_usos_y_resultados.md`); lo que aquí se fija es su combinación, el orden de los pasos y las comprobaciones que hacen legible el resultado.

## A qué caso se dirige

Una lengua con estas tres condiciones, que impiden aplicar el método comparativo clásico:

1. **Corpus reducido**: unos cientos o pocos miles de formas, sin gramática descrita.
2. **Significados propuestos, no seguros**: se conocen por el contexto de los documentos, por la metrología o por bilingües, no por traducción.
3. **Sin parientes establecidos**: no se pueden usar correspondencias regulares de sonidos como punto de partida.

## Principios

| Principio | Cómo se cumple |
|---|---|
| El material se delimita por un criterio externo al resultado | Soporte y tipo de documento, no palabras escogidas |
| Los significados se fijan antes de comparar, y se anota de dónde sale cada uno | Grado (A, B, C) y origen (dato externo, posición en una serie, casilla documental, apoyo indirecto) |
| Todas las lenguas se tratan igual | Mismas reglas de reducción, misma medida, mismos diccionarios |
| El azar se mide sobre los propios datos | Sorteo dentro del mismo diccionario y con la misma longitud; permutación de los significados entre las unidades |
| Toda cifra se lee contra casos de respuesta conocida | Lenguas y parejas de control, con las mismas reglas |
| Lo que depende de los significados se contrasta con algo que no depende de ellos | Prueba sin significados sobre todo el corpus |
| Lo que se espera y lo que contaría en contra se escribe antes de ejecutar | Registro fechado |

## Pasos

**Primera parte: ¿hay afinidad con alguna lengua, y es mayor que el azar?**

1. **Delimitar el léxico** por un criterio objetivo y documentar su representatividad en el corpus.
2. **Fijar los significados y sus términos** en las lenguas puente, con grado y origen.
3. **Reducir** las formas de todas las lenguas a clases de sonidos, con reglas generales por lengua.
4. **Prueba con significados**: distancia a la palabra más próxima del mismo significado, frente al azar igualado por longitud; con varios diccionarios independientes de cada lengua.
5. **Prueba sin significados**: perfil de combinaciones de sonidos de todo el corpus frente al de cada lengua, validado con familias conocidas.
6. **Vocabulario básico disponible** (aquí, la serie numeral) frente a una base mundial, usando la propia base como regla de lo que significa cada distancia.
7. **Controles**: las mismas pruebas con lenguas de filiación conocida y con lenguas aisladas.
8. **Comprobaciones de solidez**: sin los préstamos identificados, con formas flexionadas y sinónimos, por remuestreo, quitando unidades y cambiando significados.
9. **Contraste principal**: permutación de los significados entre las unidades y corrección por el número de lenguas comparadas.

**Segunda parte: si hay una lengua destacada, ¿de qué tipo es la relación?** (da indicios, no una prueba)

10. **Significados estables frente a poco estables**, con parejas de control emparentadas, en contacto y sin relación.
11. **Desglose por origen del significado**: el resultado se da aparte para los significados obtenidos sin ayuda de la lengua con la que se compara. Es la respuesta a la objeción de circularidad.
12. **Variación geográfica**: la prueba sin significados por zonas, con muestras igualadas.

## Qué permite afirmar y qué no

- Permite afirmar: qué lengua es la más próxima, con qué margen sobre la siguiente, con qué probabilidad de azar, y si el reparto del parecido corresponde al de las lenguas emparentadas o al de las que solo han tenido contacto.
- No permite afirmar: un parentesco demostrado. Para eso hacen falta la gramática y las correspondencias regulares de sonidos.

## Lo propio de este protocolo

- El azar igualado por longitud en la comparación entre lenguas.
- La distancia entre perfiles de combinaciones de sonidos y su validación por familias.
- La calibración de la serie numeral con la base mundial.
- La prueba de estables y poco estables con medida de distancia, validada con parejas de control.
- El desglose del resultado según el origen de cada significado.

## Cómo aplicarlo a otra lengua

Hay que sustituir tres archivos de `1_fuentes_lexicas/`: las unidades con sus significados, el corpus y, si la escritura lo exige, la regla de reducción de sus signos. Los diccionarios, las bases de comparación, los controles y los programas no cambian.
