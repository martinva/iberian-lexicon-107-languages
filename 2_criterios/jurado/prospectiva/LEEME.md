# Predicción prospectiva (declaración 13)

- `FICHAS_prospectiva.md`: las 47 fichas (36 unidades con la ficha de la declaración 7 despojada por regla mecánica —véase `4_programas/t28_prediccion_prospectiva.py`— y 11 palabras de Hesperia con ficha construida mecánicamente) con los cuatro significados candidatos A–D.
- `ENCARGO_prospectiva.md`: el texto enviado a los jueces.
- `clave_sha256.txt`: SHA-256 de la clave, publicado antes de enviar las fichas. La clave en claro se publica con las respuestas.
- `respuestas/`: respuestas íntegras de los jueces, clave en claro y cruce (tras la prueba).

Generación y puntuación: `python3 4_programas/t28_prediccion_prospectiva.py preparar | puntuar`.
