# Compruébelo usted mismo / Check it yourself

*English below.*

Este repositorio está hecho para que cualquiera pueda intentar deshacer el resultado. Tres maneras, de la más rápida a la más completa:

1. **Sin instalar nada: la página interactiva** (<https://iberico.martinva.org>). Quite unidades de la lista, retire los cuatro préstamos latinos propuestos, quédese solo con las unidades de dato externo o de toponimia, y vea en el momento qué pasa con el valor de cada lengua.
2. **Cambie una fila y vuelva a ejecutar.** Si cree que un significado está mal, que una unidad es circular o que falta una lengua: edite `1_fuentes_lexicas/iberico/unidades_plomos.json` (o `cldf/parameters.csv`), ejecute `python3 4_programas/t06_t07_significados.py` (o pulse «Ejecutar todo» en el cuaderno de Colab) y compare con `resultados/RESULTADOS_ESPERADOS.md`.
3. **Replique desde las fuentes públicas.** `1_fuentes_lexicas/LEEME_fuentes.md` dice de dónde procede cada archivo; `5_especificacion/` describe cada regla con el detalle necesario para reescribir los programas sin leerlos. Dos réplicas independientes a ciegas se han hecho ya con esa especificación.

Si obtiene algo distinto de lo que dice el artículo, o encuentra un error en una regla, en un dato o en una lectura, **abra un *issue*** con lo que cambió y lo que obtuvo. Las objeciones que cambien un resultado se incorporan al artículo con su crédito, y las que no lo cambien se contestan igualmente. Lo que no se admite como objeción es «el ibérico no puede estar relacionado con el euskera»: el repositorio no afirma que lo esté; afirma qué valor da cada prueba y cómo se calcula.

---

This repository is built so that anyone can try to undo the result. Three ways, from the quickest to the most complete:

1. **Nothing to install: the interactive page** (<https://iberico.martinva.org>). Remove units from the list, withdraw the four proposed Latin loans, keep only the units with external evidence or with toponymic support, and see at once what happens to each language's value.
2. **Change one row and run again.** If you think a meaning is wrong, a unit is circular or a language is missing: edit `1_fuentes_lexicas/iberico/unidades_plomos.json` (or `cldf/parameters.csv`), run `python3 4_programas/t06_t07_significados.py` (or press "Run all" in the Colab notebook) and compare with `resultados/EXPECTED_RESULTS_en.md`.
3. **Replicate from the public sources.** `1_fuentes_lexicas/README_sources_en.md` says where each file comes from; `5_especificacion/` describes every rule in enough detail to rewrite the programs without reading them. Two independent blind replications have already been made from that specification.

If you get something different from what the article says, or find an error in a rule, a datum or a reading, **open an issue** with what you changed and what you got. Objections that change a result go into the article with credit; those that do not are answered all the same. What is not accepted as an objection is "Iberian cannot be related to Basque": the repository does not claim that it is; it states what value each test gives and how it is computed.
