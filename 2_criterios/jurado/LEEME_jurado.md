# Segunda codificación de la procedencia de los significados: jurado ciego

*English summary below.*

**Registro previo (21-11-2026).** Este directorio se publica antes de que ningún codificador vea las fichas. Contiene las 42 fichas ciegas (`FICHAS_A_CIEGAS.md`: 36 unidades del estudio, entre ellas tres numerales en representación de los siete asignados por posición, y 6 fichas de control inventadas de nivel evidente), el encargo para los codificadores (`ENCARGO_codificador.md`) y el del crítico (`ENCARGO_critico.md`). La clave que relaciona cada código con su unidad no se publica hasta recibir las respuestas; su suma SHA-256 es:

    0a967cc6e39d1b0ccf0b0bc52ab3541987459f283f9b9eb113e52b7237a2507a

Las fichas describen la prueba con que se propuso cada significado, sin el término ibérico ni el nombre de ninguna lengua; sus recuentos y pruebas se contrastaron con las Monografías I–IV (v5.2) el 21-11-2026.

**Procedimiento.**
1. Tres modelos de lenguaje de tres fabricantes distintos, cada uno en una conversación nueva, sin memoria ni instrucciones personalizadas: dos como codificadores y uno como crítico (que busca en cada ficha la razón más fuerte para rebajar el nivel).
2. A cada uno se le entrega solo `FICHAS_A_CIEGAS.md` y el texto de su encargo. Si pide aclaraciones, la única respuesta es «Codifica con la información de las fichas».
3. Se guarda la respuesta completa de cada uno, con fecha y nombre del modelo, y se publica íntegra en este directorio junto con la clave.
4. Reglas fijadas de antemano: el modelo que falle más de una de las seis fichas de control no cuenta; de los modelos válidos se toma, para cada ficha, el nivel más bajo asignado.
5. Resultado: concordancia con la clasificación del autor (Monografía IV, tabla 5; `../FICHAS_procedencia.md`), lista de discrepancias, y nueva ejecución de `t15_solidez_unidades.py` con la clasificación menos favorable. Se publica sea cual sea.

**Resultado (21-11-2026).** Las tres respuestas, la clave y el cruce están en `respuestas/`; el contraste con la previsión, en `../../resultados/DECLARACIONES_PREVIAS.md` (entrada 7); el cálculo, en `t24_jurado_procedencia.py`. En resumen: controles 5 de 6 en los tres jueces (el sexto estaba mal calibrado); κ de Fleiss entre jueces 0,72; el jurado rebajó 12 de las 19 unidades de nivel II y 5 de las 8 de nivel I, más de lo previsto; con la clasificación menos favorable el euskera sigue primero en el grupo de niveles I y II (−6,57; siguiente, albanés −2,23).

**Segunda pregunta (declaración 10).** Con la pregunta de suficiencia («dejando aparte el paralelo, ¿basta la prueba restante?»), en `respuestas_suficiencia/`: vuelven a II tres de las seis unidades con paralelo posterior (una menos de lo previsto), bajan otras ocho de prueba documental corta, y el euskera sigue primero en el grupo de niveles I y II (−8,63; catalán −3,08; 11 comparables).

**Límite.** El jurado juzga si la prueba descrita basta para fijar el significado sin recurrir a una lengua viva; no comprueba que la descripción sea fiel a las inscripciones. Un codificador humano que acepte las mismas fichas y el mismo encargo puede añadirse con el mismo procedimiento.

---

**Blind panel for the second coding of meaning provenance.** Published before any coder sees the records: 42 blind records (36 units of the study, including three numerals standing for the seven assigned by position, and 6 invented control records of obvious level), the coder brief and the critic brief. The key linking codes to units is withheld until the answers are in; its SHA-256 sum is given above. Procedure: three language models from three vendors, each in a fresh session without memory (two coders, one critic); only the records and the brief are given; full answers are stored with date and model and published verbatim with the key; a model failing more than one of the six controls is discarded; for each record the lowest level among valid models is taken; agreement with the author's classification is reported and `t15` is re-run with the least favourable classification, whatever the outcome. Result (21 November 2026): answers, key and cross-table in `respuestas/`; comparison with the prediction in `resultados/DECLARACIONES_PREVIAS.md`, entry 7; computation in `t24_jurado_procedencia.py`. In short: controls 5 of 6 for all three judges (the sixth was miscalibrated); Fleiss's κ between judges 0.72; the panel lowered 12 of the 19 level-II units and 5 of the 8 level-I units, more than predicted; under the least favourable classification Basque remains first in the level-I-plus-II group (−6.57; next, Albanian −2.23). Limit: the panel judges whether the evidence described suffices without recourse to a living language; it does not check the descriptions against the inscriptions.
