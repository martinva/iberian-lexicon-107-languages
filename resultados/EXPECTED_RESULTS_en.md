# Expected results

*Versión en español: `RESULTADOS_ESPERADOS.md`.*

Values given by each program in `4_programas/` with the data in `1_fuentes_lexicas/`, Python 3 and the package seed (20261120). The article (draft v26) gives these same figures. The complete output of each program, line by line, is the `.log` file of the same name in this folder, and the unrounded values are in the `.json`; this document summarises what a replication should find.

**Change of 21 November 2026 (third run, after the second audit review).** The files now store the *z* values unrounded (on screen and here, two decimals); `t15` stores the extremes of the swapped-meanings trial; `t20` corrects the labels of its extremes; `ʜ` is added to the class table (it moves some Table 14 values by one hundredth and no rank).

**Change of 21 November 2026 (second run).** All programs were run again after the corrections of the code audit, declared beforehand in `DECLARACIONES_PREVIAS.md` (entry 2). No rank changes; *z* values move by less than one unit. The historical dictionary derived from Trask is withdrawn and the length-conditioned permutation is added (`t16`, part d).

## How to read the comparison

- **Exact:** values that do not depend on draws (real distances, ranks of the numeral series, sound profile, corpus counts). They must repeat with no difference at all.
- **With draws:** *z* values, advantages and permutation counts. With the same programs and seed they repeat exactly. With another seed or implementation they vary: in 40 repetitions of the Table 6 test, the Basque *z* ranges from −11.6 to −13.3 and that of the other languages moves by about half a unit (`t20`).
- What a replication must reproduce is the **rank** of each language and its **separation** from the next, not the second decimal of a *z*.
- **Permutation of meanings (`t16`):** only units with candidates in the language are permuted; the others are removed first.

## Tables 1 and 2 (`t01_t02_corpus.py`) — exact

| Support | Inscriptions | Words | Distinct | Distinct non-onomastic |
|---|---|---|---|---|
| Lead | 143 | 1,171 | 1,020 | 388 |
| Pottery | 1,217 | 1,237 | 848 | 164 |
| Stone | 214 | 379 | 339 | 122 |
| Other | 25 | 41 | 40 | 13 |
| Total | 1,599 | 2,828 | 2,095 (sum over supports: 2,247) | 679 (sum: 687) |

Lead / pottery: words per inscription 8.2 / 1.0; one word or fewer 33 / 1,103; five or more 71 / 9; ten or more 39 / 2; complete 729 / 639; mean length 7.7 / 5.3; of two or three letters 81 / 258; of six or more 512 / 236; names 33 % / 60 %; words in repeated forms 15 % / 32 %; words repeating a form already present 9.3 % / 20.3 %.

## Tables 4 and 5 (`t04_t05_numerales.py`) — exact

3,811 languages, 239 families, 110 without relatives. Basque 0.317, rank 1; second, 0.756 (Wapa). Languages without relatives: the closest to its neighbour, 0.407. Neighbour between 0.2 and 0.3, of the same family in 53 of 54; between 0.3 and 0.4, 63 of 63; between 0.4 and 0.5, 46 of 48; between 0.2 and 0.5, 162 of 165. Values 1, 10 and 20: Basque 0.435; first non-Basque, 0.584 (Falam Chin).

## Tables 6 and 7 (`t06_t07_significados.py`)

Basque, 30 units (real and chance, exact with the seed; *z*):

| Dictionary | Forms | Units | Real | Chance | *z* |
|---|---|---|---|---|---|
| Wiktionary | 3,814 | 28 | 0.432 | 0.817 | −12.77 |
| Azkue (1905-1906) | 31,253 | 30 | 0.503 | 0.784 | −10.26 |
| Reconstructed (Trask 2008) | 391 | 15 | 0.557 | 0.928 | −7.20 |
| Open Data Euskadi | 41,940 | 30 | 0.452 | 0.740 | −10.88 |
| Apertium, Spanish bridge | 7,028 | 28 | 0.526 | 0.863 | −9.95 |
| Apertium, English bridge | 6,885 | 28 | 0.501 | 0.786 | −9.67 |
| WordNet | 17,989 | 30 | 0.379 | 0.658 | −11.86 |

Next languages: Wiktionary (34 dictionaries), Galician −4.27, Tagalog −3.87, Asturian −3.29, Latin −0.46 (rank 22); Spanish bridge (10), Galician −4.77, Italian −2.91, Aragonese −2.83; English bridge (9), Catalan −3.63, Icelandic −3.23, Spanish −3.09; WordNet (4), Galician −3.25, Catalan −2.37, Spanish −1.70.

Metrological lexicon (10 units), Basque: Azkue −11.44; reconstructed −10.69; Wiktionary −10.55; Open Data −11.30; Apertium Spanish −10.22; Apertium English −10.36; WordNet −10.48. Second language: Turkish −3.32 (Wiktionary) and −3.39 (Apertium English).

## Table 8 (`t08_perfil.py`) — exact, except the resamplings

Full classes: the closest language is of the same family in 77 of 98; reduced, 69 of 98. Iberian, whole corpus (2,229 forms): Basque 0.153, Latin 0.174, Finnish 0.205; lead plaques (1,072): 0.158 and 0.179; first in 500 of 500 resamplings and in 500 of 500 halves. Reduced: Basque 0.070, Sakha 0.094. Wiktionary (35 languages): Basque 0.106, Finnish 0.131 (validation 17 of 24); reduced 0.058 and 0.090 (15 of 24); 300 of 300. Controls: Umbrian, Latin 0.166; Gothic, Lak 0.251 and Icelandic 0.254; Cornish, Welsh 0.124 and Breton 0.141; Dalmatian, Swedish 0.151 and Romanian 0.168; reduced Umbrian, Portuguese 0.120, Basque 0.124, Latin 0.133.

## Profile calibration (`t22_calibracion_perfil.py`) — exact

Full classes: Iberian–Basque 0.1533; 6.5th percentile of 1,053 same-family pairs; 0.11th of 4,618 different-family pairs (5 at that distance or less; minimum 0.1345, Swedish–Veps). Reduced: 0.0696; percentiles 2.4 and 0.02 (1 pair: Estonian–Hindi 0.0681). Languages without relatives in the base: 9.

## Table 9 (`t09_prestamos.py`)

26 units, Basque: Wiktionary −12.06; Azkue −9.63; reconstructed −7.28; Apertium Spanish −10.33; Open Data −10.20; Apertium English −10.58; WordNet −10.83. Next: Galician −2.57 (Wiktionary), −3.49 (Apertium), −1.43 (WordNet); Icelandic −3.13; Catalan −2.89 (Apertium English); Latin +0.37. Four loans: Galician −4.62 / −4.50 / −4.96; Tagalog −4.62; Asturian −4.59 / −3.89; Aragonese −4.06; Occitan −3.95; Catalan −3.66; Basque −2.94 (Wiktionary), −2.62 (Azkue), −3.38 (Open Data), −1.95 and −1.45 (Apertium), −3.05 (WordNet).

## Section 8.2 (`s82_formas_y_sinonimos.py`)

24 languages. 30 units, Basque: citation form −12.11 (Galician −4.32); with inflected forms −10.77 (Tagalog −3.37); with synonyms −12.10 (Galician −4.56); with both −11.08 (Tagalog −2.88). Metrological lexicon: citation −10.11 (Turkish −3.64); with forms −11.85 (Galician −1.66).

## Table 10 (`t10_controles.py`) and power (`t19_potencia_controles.py`)

Five samples: Umbrian 5 of 5 (−4.62 to −8.08); Gothic 4 of 5 (−3.01 to −6.81); Cornish 4 of 5 (−6.67 to −13.58); Dalmatian 5 of 5 (−12.07 to −15.48); Etruscan, −2.39 to −4.76; Sumerian, −1.61 to −2.76.

One hundred samples:

| Language | Relative first | *z* of the first (median; best) | Separation (median; largest) | Reaches −9.3 | Reaches 5.6 |
|---|---|---|---|---|---|
| Dalmatian | 100 | −13.96; −18.01 | 1.21; 4.74 | 100 | 0 |
| Umbrian | 95 | −6.17; −9.41 | 1.13; 5.77 | 1 | 1 |
| Cornish | 90 | −9.79; −15.12 | 2.96; 8.11 | 64 | 14 |
| Gothic | 79 | −4.56; −9.83 | 1.55; 6.36 | 1 | 2 |
| Etruscan | — | −3.44; −6.85 | 0.43; 2.64 | 0 | 0 |
| Sumerian | — | −2.17; −3.75 | 0.29; 1.69 | 0 | 0 |

Etruscan: the first language is Latin in 39 samples, Asturian in 17, Romanian in 12 and Sicilian in 9.

## Table 10 bis and section 8.4 (`t15_solidez_unidades.py`)

32 languages. Full list: Basque −12.53; Galician −4.07. Removing one unit: first in 30 of 30; from −11.75 to −12.97; smallest separation 7.48. At random: 20 units, 2,000 of 2,000, median −10.14; 15, 1,999, −8.76; 10, 1,975, −7.16.

| Group | Units (comparable) | Basque | Next |
|---|---|---|---|
| Level I | 5 (4) | −5.75 | Catalan −3.15 |
| Level II | 19 (18) | −8.06 | Galician −3.80 |
| Level III (toponymy) | 6 (6) | −8.29 | Welsh −2.35 |
| Levels I and II | 24 (22) | −9.28 | Galician −3.97 |
| Level II with a correspondence pointed out | 6 (6) | −7.27 | Galician −2.83 |
| Level II without correspondence | 13 (12) | −4.43 | Tagalog −4.25 |
| The same without Latin loans | 9 (8) | −3.15 | Albanian −2.41 |
| Without the 5 with an alternative reading (`t21`) | 25 | −11.84 | Galician −3.61 |

Adverse removal: Basque loses first place when 13 units are removed; its value rises above −3 when 15 are removed. Swapped meanings (medians; Open Data / Wiktionary / WordNet): none −10.99 / −12.58 / −11.64; 5: −9.39 / −10.66 / −9.78; 10: −7.46 / −8.75 / −8.02; 15: −5.66 / −6.62 / −6.26; 20: −4.02 / −4.63 / −4.47; 30: −0.29 / −0.62 / −0.63. With 15 swapped, Open Data: 5th percentile −7.87, 95th percentile −3.58, most marked case −10.25, least marked −1.80 (the file stores the four values for each size and dictionary).

## Section 8.4, dictionary size (`t23_tamano_diccionario.py`) — exact

32 languages; Spearman(forms, *z*) −0.337 (−0.378 without Basque); Basque 3,814 forms, rank 21 of 32 by size; median 6,646.

## Table 10 bis with the panel's classification (`t24_jurado_procedencia.py`) — exact

| Classification | Levels I and II (units; comparable) | Basque | Next | Level III | Level II alone |
|---|---|---|---|---|---|
| Author | 24; 22 | −9.28 | Galician −3.97 | −8.29 (Welsh −2.35) | −8.06 (Galician −3.80) |
| Mistral | 17; 16 | −6.60 | Tagalog −4.13 | −11.10 (Galician −2.34) | −6.24 (Tagalog −4.05) |
| DeepSeek | 17; 16 | −6.60 | Tagalog −4.13 | −11.10 (Galician −2.34) | −5.26 (Tagalog −4.89) |
| Grok (critic) | 12; 11 | −6.57 | Albanian −2.23 | −10.81 (Galician −4.24) | −6.19 (Albanian −2.31) |
| Least favourable | 12; 11 | −6.57 | Albanian −2.23 | −10.81 (Galician −4.24) | −6.19 (Albanian −2.31) |

Second question (sufficiency; `t24_jurado_procedencia.py suficiencia`): least favourable, levels I and II 12; 11, Basque −8.63, Catalan −3.08; level II −8.24 (Catalan −3.19); level III −9.24 (Tagalog −4.23). Mistral I and II −9.32 (16; 15; Galician −3.72); DeepSeek −9.47 (13; 12; Catalan −3.26); Grok −10.26 (19; 18; Galician −3.81).

The level-I-only group is computed only with the author's classification (−5.75; Catalan −3.15); with the others fewer than four comparable units remain.

## Section 11.4, correspondences (`t25_correspondencias.py`) — exact

Basque: 38 pairs, 195 columns, 77 non-identical; R 0.641; R′ 0.442. Permutation (1,000): R′ median 0.315, 90th percentile 0.337, none ≥ 0.442. Languages: 32; Basque 1st by R′ (Lithuanian 0.385). Size equalised to 77: permutation median 0.378, p90 0.396, none ≥ 0.442; languages: Basque 0.442, Lithuanian 0.438, Hausa 0.418.

## Section 11.5, borrowability (`t26_prestabilidad.py`) — exact

ρ: Wiktionary −0.146 (34 units); Open Data Euskadi −0.039 (35). 33 languages: median −0.004, minimum −0.452, maximum +0.305.

## Section 11.6, etymological status and phonotactics (`t27_etimologia_vasca.py`) — exact

Version 2 (current). Declared rule: forms 423 borrowed, 540 inherited, 2,399 unknown, 1,090 no note. Matched: 38 with a candidate, 31 with an eligible note; 2 borrowed (Romance/Latin 1), 18 inherited, 11 unknown; proportion 0.065 against 0.125 (same units) and 0.126 (lexicon); hypergeometric p(≥2) 0.961 and p(≤2) 0.162; draws mean 2.24, p(≥2) 0.7193. Control: *koŕta* borrowed (Romance/Latin), *bale* no note, *oŕtin* unknown, *saltu* inherited. Phonotactics: cross-validation 0.839 / 0.804; out of sample 11 of 38 as borrowed (with candidates in training, 8). With `amplia`: 3/31 (Romance 2) against 0.167 and 0.209; p(≥3) 0.959, p(≤3) 0.143; phonotactics out of sample 11 of 38. (Version 1 kept as `t27_etimologia_vasca_v1*`: 2/32 = 0.062; phonotactics 8 of 38.)

## Table 10 ter and section 8.5 (`t16_contraste_principal.py`)

| Test | Language | *z* | Equal or better out of 100,000 | Corrected *p* |
|---|---|---|---|---|
| (b) 30 units, 32 languages | Basque | −10.09 | 0 | 0.00032 |
| | Galician | −3.97 | 7 | 0.00256 |
| | Albanian | −3.12 | 118 | 0.038 |
| | Tagalog | −3.11 | 168 | 0.0541 |
| | Catalan | −2.69 | 473 | 0.152 |
| | Asturian | −2.66 | 582 | 0.187 |
| (c) without the four loans, 31 languages | Basque | −9.77 | 0 | 0.00031 |
| | Galician | −2.64 | 603 | 0.187 |
| | Albanian | −2.38 | 1,019 | 0.316 |
| | Tagalog | −1.62 | 5,576 | 1 |
| (d) length-conditioned | Basque | −8.34 | 0 | 0.00032 |
| | Galician | −4.17 | 5 | 0.0019 |
| | Tagalog | −3.58 | 33 | 0.011 |
| | Catalan | −2.82 | 299 | 0.096 |
| | Asturian | −2.39 | 1,076 | 0.345 |
| | Albanian | −2.12 | 2,047 | 0.655 |
| (d) without the four loans, 31 languages | Basque | −7.63 | 0 | 0.00031 |
| | Galician | −2.99 | 240 | 0.075 |
| | Tagalog | −2.08 | 2,294 | 0.71 |
| | Catalan | −1.80 | 3,895 | 1 |

Other Basque dictionaries, (b): Open Data −9.10; Azkue −8.74; WordNet −9.32; 0 of 100,000 in all three. Spanish WordNet −1.59. (d), Basque: 9.04 × 10^15 distinct permutations possible; 27 units can change. (a) Substitution with 20,000 draws: *z* −12.32; *p* 0.00005; corrected 0.0016.

## Tables 11 to 13 (`t11_t13_estables.py`)

| Relationship | Pairs | Stable | Less stable | Stable larger in |
|---|---|---|---|---|
| Closely related | 7 | 0.405 | 0.279 | 7 |
| Distantly related | 12 | 0.133 | 0.060 | 11 |
| Distant relationship and loans | 2 | 0.148 | 0.055 | 2 |
| Contact only | 13 | 0.036 | 0.051 | 5 |
| Unrelated | 8 | −0.014 | −0.006 | 3 |

The value of each pair is in `t11_t13_estables.log`. Iberian against Basque: stable 0.533 (11); less stable 0.445 (27); without the numerals two to five 0.447; without *saltu* 0.588. Second language on stable meanings: Welsh 0.145. By origin: external evidence 0.560 (7); numerals two to eight 0.740 (7); document slot 0.307 (18); toponymy 0.548 (6); four loans 0.238 (against Galician, 0.341).

## Table 14 (`t14_zonas.py`) — exact, except the equalised samples

Lead plaques only / all inscriptions (full sample of each zone, field `relativa`): Narbonensis–Roussillon −2.16 / −2.25; Catalonia −2.52 / −2.37; Ebro–Castellón −2.39 / −2.37; Valencia −2.49 / −2.42; South-east −2.37 / −2.42. Narbonensis, equalised samples: Basque first in 197 of 300. Variation: same zone 0.073; neighbouring 0.083; non-neighbouring 0.092; extremes 0.101.

## Table 15 (`t18_perfil_contacto.py`) — exact

Rank of the donor (of 106): Basque–Spanish 76, –Latin 19, –Catalan 65; Hungarian–Turkish 21; Romanian–Bulgarian 7; Albanian–Latin 17, –Greek 85; Japanese–Chinese 73; Korean–Chinese 72; Finnish–Swedish 27; English–French 32; Persian–Arabic 105; Turkish–Arabic 94, –Persian 103; Breton–French 5; Armenian–Persian 96; Hindi–Persian 87. Median, 72.

## Section 8.4, trial on circularity (`t17_techo_circularidad.py`) — inconclusive

Basque with the proposed meanings: −13.68. Choosing meanings at convenience within the field of each unit: Malay −12.11 (Basque −15.40). Choosing them without restriction: Malay −15.89 (Basque −14.98). With that freedom other languages reach values like that of Basque: the test does not serve to bound circularity, and the article says so.

## Annex A.3 (`a3_comprobacion_medida.py`) — exact

106 languages, 5,565 pairs, 1,053 of the same family, 843 of old relationship. Area under the curve 0.816 (0.777 for old relationships); between 0.776 and 0.853 depending on the draw. This program keeps its original seed (20261118).

## Annex B.7, variation between seeds (`t20_variacion_semillas.py`)

40 repetitions of the Table 6 test with different draw keys. Basque first in 40; value from −11.59 (least marked) to −13.33 (most marked); median −12.38; deviation 0.41. Best of the others: from −3.93 to −4.44; deviation 0.12. Separation: smallest 7.31; median 8.28; largest 9.06. Other languages: median range 0.28; largest 0.57. It takes about three hours in a single process; it can be split into ranges (`python3 t20_variacion_semillas.py 1 20`).

## Remarks

- The figures of the first run (before the corrections of 21 November 2026) remain in the repository history.
- Test (d) of `t16` without the four loans is computed in the same pass as (c) and stored in `c_permutacion_sin_prestamos[*].condicionada_por_longitud`.
- The variation between seeds has been measured for the Table 6 test; not for the other tests.
