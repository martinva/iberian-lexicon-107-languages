# Detailed functional specification

**Mathematical comparison of the lexicon of the Iberian lead plaques with that of other languages. Final model.**

This document describes, without reference to the code, everything needed to redo the calculations of the study: which data are used, how they are prepared, which rules are applied and what each program does. Anyone following it in any programming language should obtain the same results, subject to the proviso in section 0.4.

Each section points to the file in `4_programas/` that implements it. Function names in parentheses are those of the `ibcomp` package. File, folder and function names are in Spanish and are kept as they are; this text is a translation of `ESPECIFICACION_FUNCIONAL_es.md`, which prevails in case of doubt.

---

## 0. General conventions

### 0.1 Vocabulary

- **Form:** a word as it appears in a source.
- **Reduced form:** the same word converted into a string of *sound classes* (section 2). All comparisons are made between reduced forms.
- **Unit:** a meaning proposed for Iberian, with one or more Iberian forms that express it and a list of *terms* (Spanish and English words that translate it).
- **Dictionary:** a source for another language, converted into a table "reduced form → set of meanings".
- **Candidates** of a unit in a dictionary: the forms of the dictionary whose meaning matches one of the unit's terms.

### 0.2 Encoding

All text files are UTF-8. Before characters are compared, the Unicode normalisation stated in each rule (NFC or NFD) is applied.

### 0.3 Admitted length

Unless stated otherwise, a reduced form is admitted if it has between 2 and 12 symbols. Shorter or longer ones are discarded.

### 0.4 Chance and reproducibility

Several tests compare an observed value with those obtained in random *draws*. Each calculation uses its own random number generator, seeded with the text `20261120|<test>|<set>|<dictionary>` (`pruebas.generador`). The result therefore does not depend on the order in which the programs are run.

With Python's *Mersenne Twister* generator and that seed, results are identical from one run to the next. With another generator, the values that depend on draws (the *z* values) will vary by about half a unit; those that do not depend on draws (real distances, ranks in the sound-combination profile, numeral series) must match exactly.

There are three exceptions, where the numeric seed of the original calculation is kept so as to obtain the same samples: the sample of 400 languages in Table 5 (seed 20261118), the word samples of the control languages (section 4.6) and the concept draws of Annex A.3 (section 4.15). And there is a second generator: the permutations of 4.11 use NumPy's generator (`default_rng`, PCG64), seeded with 63 bits taken from the text generator; the length-conditioned variant consumes the same generator after the 100,000 free permutations, with no seed of its own.

The *z* values are computed and sorted unrounded; on screen and in the article they are given with two decimals. Exceptions in the result files: 4.10 (`t15`) stores its summaries with two decimals; 4.13 (`t19`), 4.17 (`t20`) and 4.18 (`t21`) store the per-language tables with three decimals, and the summary of 4.13 (medians and extremes) also with three, computed from the three-decimal values of the records, so that the article rounds only once from there. In 4.13 and 4.17 the orderings and the "first language" counts are made at full precision, before rounding; the files keep three decimals. Added programs: 4.20 (`t24`) saves its values with two decimals; 4.23 (`t26`) saves the individual z with three and the correlation unrounded; 4.24 (`t27`) saves distances with three. A null is considered constant when its range (max − min) does not exceed 10⁻¹² · max(1, max|null|): the floor 1 keeps a vector of tiny values from passing as variable. Edge cases (constant null, undefined z and their consumers, including the `t15` aggregates, the `t26` correlation with fewer than three pairs and the second language in `t24`) are checked with `4_programas/casos_limite.py`; the JSON files contain only finite numbers or null. Probabilities are stored unrounded; in the article they are given with as many decimals as needed for the comparison with 0.05 not to depend on rounding.

Test 3.2 stops with an error if, in some draw, the dictionary does not have enough words of a given length to substitute without repetition. The *z* value is not computed (left empty) if the draws are constant: standard deviation zero, or range (maximum minus minimum) not greater than 10⁻¹² × max(1, largest absolute value of the null) —the same rule with floor 1 given above—, so that a vector of equal values with floating-point residue does not yield a spurious *z*. An empty *z* is handled thus in each program: in 4.10 (`t15`) the language without *z* does not enter the ordering and, if it is Basque, the rank is left empty; in 4.11 (`t16`) the dictionary without *z* is excluded from the ordering and the summary; in 4.16 (`t17`) "None" is printed and the language does not enter the ceilings; in 4.23 (`t26`) a language without a computable ρ is kept in the table, counted in `sin_rho` and left out of the median and extremes; in the aggregates of 4.10 (a), if no case has a defined *z*, the aggregates are empty (null). Probabilities are stored unrounded, together with the number of draws equal to or below the real value.

### 0.5 Conventions of detail

Fixed after an independent blind replication, which flagged them as ambiguous. None changes a rank; some change counts.

| Point | Convention |
|---|---|
| Seeds | The seed text is `20261120` followed by the keys of the calculation, joined by `\|`. Meaning-based test: `20261120\|significados\|<set>\|<dictionary name>`. The literal keys of each calculation are in its program. A replication with other keys or another order of draws will give *z* values that differ within the margin (section 5), not identical ones |
| Order | Units, in file order. Candidates and reduced forms, deduplicated and in alphabetical order of their characters (Unicode order) |
| Standard deviation | Population (divisor *n*), over the values of the draws |
| Ties | Orderings of languages by value are made on the pair (value, language name): at equal value, alphabetical order of the name (4.3, 4.12 and, in 4.4, the neighbours of Iberian, of Basque and of the controls). Two exceptions in 4.4: the family validation (nearest neighbour of each language) orders by the pair (value, language identifier in the base), not by name; and the neighbour lists of Iberian and Basque round the divergence to four decimals before ordering, so that two languages are ordered by name when their rounded divergences coincide (which can also happen with differences somewhat larger than 0.00005, depending on how the rounding falls). In the meaning-based test and in 4.10 the ordering is by value only, and at equal value the order of the source is kept (stable sort). In distance bands, the lower bound is included and the upper one is not |
| Coverage minimums | The number of units with candidates is compared with the unrounded threshold: 30 % of 26 requires 8 |
| Wiktionary languages | The files contain 37 language labels; the 35 with a normaliser are used. Armenian and Georgian have none and are left out |
| Glosses with parentheses | Everything from each opening parenthesis to the first closing one after it is removed (regular expression `\(.*?\)`); nested ones receive no separate treatment. From each piece a single initial particle (`to`, `a`, `an`, `the`) is removed, and a full match with the term is required |
| Open Data Euskadi | The Spanish equivalent is used whole, in lower case, without splitting it |
| Chan's numerals | The 2-to-12-symbol limit of section 0.3 is not applied: all non-empty forms are kept. Varieties with an empty `Glottocode` field are excluded from the selection of section 4.3, step 1. In step 5 all varieties having the three values enter, without the filters of step 1 |
| Iberian forms of the numerals | Those of the file `unidades_numerales.json` in all tests (ten: *abaŕ*, *baŕ*; twenty: *oŕkei*, *ogei*) |
| Cap on candidates (3.5 and 4.5) | Applied only once, before the draws; the same subset serves for the real value and for chance. In those two calculations the real value may depend on the seed |
| Groups by origin (Table 13) | The four proposed Latin loans are also part of the documentary-slot group: it is a sub-check, not a fifth group of a partition |

---

## 1. Lexical sources and their treatment

Files in `1_fuentes_lexicas/`. Implementation: `ibcomp/fuentes.py`.

### 1.1 Iberian units

`iberico/unidades_plomos.json` (30 units) and `iberico/unidades_numerales.json` (10 units). Each unit has:

| Field | Content |
|---|---|
| `id` | Identifier (A1 to A30; N1 to N8, N10, N20) |
| `formas` | List of Iberian forms in the Hesperia transcription |
| `glosa` | Proposed meaning |
| `terminos_es`, `terminos_en` | Spanish and English terms for the meaning |
| `terminos_es_v2`, `terminos_en_v2` | Extended list with synonyms (only for section 4.5) |
| `tipo` | Origin of the meaning: `a` from the documentary slot; `c` convergent, with toponymic support |

The four units proposed as Latin loans are those beginning with *bale*, *koŕta*, *saltu* and *oŕtin*.

### 1.2 Iberian corpus (Hesperia)

`iberico/hesperia_iberico_1599.csv` (columns `ref_hesperia`, `texto_crudo` and others) and `iberico/hesperia_metadatos.csv` (columns `ref_hesperia`, `material`, `signario` and others). They are linked by `ref_hesperia`. The two files are not redistributed: `iberico/descargar_hesperia.py` generates them from the Hesperia search engine (full listing, zone TODO, with the language filter IBERICO; references marked FALSA, SUSPECTA or LATINA are excluded, 16 of 1,615) and from the Generalidades, Epigrafía and Contexto tabs of each record; the program finally checks that the result matches, by its SHA-256 sum, the files used in the article (queries of 7 and 12 November 2026).

Extraction of the words of a record (`fuentes.hesperia`):

1. The characters `[ ] ( ) + - ?` and the combining underline and dot-below marks (U+0332, U+0331, U+0323) are removed from the text.
2. It is normalised to NFC and lower-cased.
3. It is split at any sequence of characters other than letters, digits, underscore, `ś`, `ŕ` or `ḿ`.
4. Empty stretches are discarded, as are those containing a digit and those containing three or more consecutive characters from the set `i v x l π` (numeral notations).
5. Each stretch is reduced with the rule in section 2.3 and admitted if it has 2 to 12 symbols.

For each record the set of distinct reduced forms is kept, together with:

- **Zone**, from the initial letters of the reference: Narbonensis–Roussillon (AUD, HER, PYO, HGA); Catalonia (GI, B, L); Ebro–Castellón (T, TE, Z, HU, CS); Valencia (V); South-east (A, MU, AB). Other references have no zone.
- **Lead (strict criterion):** the `material` field contains "PLOMO". Used in Table 14.
- **Lead (broad criterion):** the word "plomo" appears in any metadata field. Used in Table 8.

### 1.3 English Wiktionary (kaikki.org extraction)

`wikcionario/kaikki_control_20lenguas_2026-11-17.tsv` and `wikcionario/kaikki_control_silaba_simple_16lenguas_2026-11-18.tsv`. Four tab-separated columns: language (English name), word, category, gloss.

A line is used if (`fuentes.wikcionario_lemas`):

- it has exactly four columns;
- the language has a normaliser (section 2.2);
- the category is not `name`, `character`, `suffix`, `prefix` or `romanization`;
- the word, lower-cased, contains no spaces and consists only of letters.

**Terms of a gloss** (`fuentes.terminos_de_glosa`): whatever is in parentheses is deleted; the gloss is cut at commas and semicolons; each piece is lower-cased, stripped of surrounding spaces, of an initial `to`, `a`, `an` or `the`, and of trailing full stops and spaces.

For each language the dictionary is built: reduced form (the language's normaliser and the rule in section 2.4) → union of the terms of all the words that yield that form.

### 1.4 Other sources for Basque

| Source | File | Treatment | Terms |
|---|---|---|---|
| Azkue (1905-1906) | `euskera/azkue_lemas_equivalentes.csv` (`azkue_abbyy_v2.csv` in the working repository), columns `lema`, `equivalentes` | Lower-cased headword, no spaces, letters only. Meanings: `equivalentes` cut at commas and semicolons, lower-cased | Spanish |
| Trask (2008), reconstructed lexicon | `euskera/trask_formas_glosas.json` (`trask_lexico_nativo_derivado.json` in the working repository): entries with `proto` and `glosas` | Reconstructed forms containing an undetermined vowel or consonant (capital `V` or `C`) are discarded. From the others only the letters a–z, `ñ` and square brackets are kept; lower-cased | English |
| Open Data Euskadi | `euskera/opendata_euskadi_eu_es_v1.tsv`, columns `eu`, `es` (first line is a header) | Basque word with no spaces, letters only; Spanish equivalent lower-cased | Spanish |

In all of them the Basque normaliser and the rule in section 2.4 are applied.

### 1.5 Multilingual WordNet (MCR 3.0)

`wordnet_mcr/wn-data-{eus,spa,cat,glg}.tab`. Three columns: concept, type, word. Lines whose type ends in `lemma` are used. The word is lower-cased and underscores become spaces.

Each dictionary is "reduced form → set of concepts". The candidates of a unit are the forms that share a concept with the concepts in which any of its Spanish terms appears (looked up in the `spa` file).

### 1.6 Apertium (bilingual dictionaries)

`apertium/*.dix`. From each file the pairs `<l>…</l><r>…</r>` are extracted. Before the pairs are extracted, XML comments (`<!-- … -->`) are removed. On each side `<b/>` first becomes a space and then the other tags are removed; the text is lower-cased and underscores become spaces. The list of files, the side on which the compared language stands and its normaliser are given in `fuentes.APERTIUM_ES` (Spanish as bridge, 9 languages) and `fuentes.APERTIUM_EN` (English as bridge, 10 languages). The meaning of each word is its equivalent in the bridge language.

### 1.7 NorthEuraLex

`northeuralex/forms.csv` (columns `Language_ID`, `Segments`) and `languages.csv` (`ID`, `Name`, `Family`). Each form is given in the International Phonetic Alphabet, with segments separated by spaces; it is reduced with the rule in section 2.5.

### 1.8 Chan's numerals (2019)

`numerales_chan/forms.csv` (columns `Language_ID`, `Parameter_ID` = numeric value, `Form`) and `languages.csv` (`ID`, `Name`, `Family`, `Glottocode`). Each form is reduced with the rule in section 2.6. All non-empty forms of each value are kept, in file order.

### 1.9 Control languages

`wikcionario/kaikki_lenguas_de_control_2026-11-19.tsv`. Six columns: language, word, category, romanisation, cross-reference flag, glosses (separated by ` || `).

A word is eligible (`fuentes.lexico_control`) if: the cross-reference flag is `0`; the category is `noun`, `verb`, `adj`, `adv`, `num` or `pron`; the form (first romanisation if there is one; otherwise the word), once normalised (section 2.2), consists only of the letters a–z, `ñ` and `ð`; its reduced form has 3 to 10 symbols; and it has at least one gloss term made up of one or two words of the letters a–z. Glosses beginning with *see*, *the meaning*, *alternative*, *romanization*, *obsolete* or *misspelling*, and those containing *uncertain*, are ignored.

### 1.10 Inflected forms

`wikcionario/kaikki_formas_26lenguas_2026-11-18.tsv.gz` (gzip-compressed; only the `.gz` file is read): three columns (language, flag, form). The flag `L` marks a headword; the following lines are its inflected forms. `wikcionario/wikcionario_eu_formas_verbales_v1.csv` (columns `lema`, `forma`) adds Basque verb forms. Only forms of headwords present in the language's dictionary are used, with no spaces and letters only. The current headword is that of the last `L` line read, with its language; a form line is admitted only if its language is that of the current headword and that headword is in that language's dictionary. (An external audit counted, among the 8,233,273 lines of the file, 557 forms whose language is not that of the last headword; with the language check none can be admitted, and in these data none was before it was added.) The added Basque verb forms do not go through that filter, except that of belonging to a headword of the dictionary.

---

## 2. Criteria: from spelling to sound classes

Implementation: `ibcomp/texto.py`, `ibcomp/normalizadores.py`, `ibcomp/clases.py`.

### 2.1 Cleaning a form (`texto.limpia` and `texto.limpia_grafia`)

`texto.limpia`, for Iberian forms:

1. NFC and lower case.
2. Combining characters (Unicode category `Mn`) are removed, except the acute accent U+0301.
3. NFC again.
4. `* [ ] { } ( ) - ? ’ ‘ '`, spaces and full stops are removed.

`texto.limpia_grafia`, for dictionary words (output of a normaliser) and for the forms of the units in the meaning-based test. It does not call `limpia`; its steps are:

1. NFC and lower case.
2. Each character not in the list of kept characters is decomposed (NFD) and loses its combining marks (category `Mn`): `ê` → `e`, `ö` → `o`, `ǵ` → `g`. Kept as they are: `ś ŕ ḿ ñ š ç ł ŋ` (they have a class of their own in 2.4) and the vowels with an acute accent or a macron (`á é í ó ú ā ē ī ō ū`), which in 2.4 receive the class of their base vowel.
3. NFC again.
4. `* [ ] { } ( ) - ? ’ ‘ '`, spaces and full stops are removed.

The forms of the Iberian corpus (4.14, 4.4 and 4.8) still use `limpia`, which leaves precomposed characters alone: Hesperia's spelling does not use them outside the doubtful signs, which are excluded.

Simplification of double letters (`texto.dobles`): every contiguous repetition of the same letter, of any length, is reduced to one, except `rr` and `ll`.

### 2.2 Normalisers by language

Each language has a function that converts its spelling into a common spelling, by substitutions applied in a fixed order. For Albanian, Fijian, Zulu and Shona, and Somali, the substitutions are applied in a single left-to-right pass, trying at each position the sequences in the order of the list, so that what has been substituted is not transformed again. They are general, approximate rules, the same for every word of the language. The complete table, substitution by substitution, is the file `ibcomp/normalizadores.py`, which must be read as part of this specification: each function is an ordered list of text substitutions. Languages and function:

| Languages | Function |
|---|---|
| Basque | `n_eu` (unchanged) |
| Galician, Catalan, Occitan, Asturian, Romanian, Aragonese, Portuguese, French, Italian, Spanish, Sicilian, Sardinian | `n_rom`, with the language code |
| Latin | `n_la` |
| Welsh | `n_cy` |
| Icelandic, German, Swedish | `n_ger` |
| Finnish, Estonian | `n_fi` |
| Hungarian | `n_hu` |
| Turkish | `n_tr` (Wiktionary), `n_tr_apertium` (Apertium) |
| Albanian, Irish, Lithuanian, Maltese, Swahili, Quechua | `n_sq`, `n_ga`, `n_lt`, `n_mt`, `n_sw`, `n_qu` |
| Serbo-Croatian | `n_hbs` |
| Hawaiian, Samoan, Tongan | `n_poli` |
| Fijian; Indonesian and Malay; Tagalog; Malagasy | `n_fj`; `n_indo`; `n_tl`; `n_mg` |
| Zulu and Shona; Hausa; Yoruba; Somali; Classical Nahuatl | `n_bantu`; `n_ha`; `n_yo`; `n_so`; `n_nah` |
| Umbrian, Gothic, Cornish, Dalmatian, Etruscan, Sumerian | `norm_control` |

Criteria common to almost all: accents are removed; double letters are simplified (except `rr` and `ll`); affricates are written `tx` or `ts`; the palatal fricative, `x`; the palatal glide, `j`. `v` and `w` receive no common treatment: the normalisers of the languages in which `v` or `w` stand for [b] or [β] turn them into `b` (Romance, Greek, Turkish, Albanian, among others; each function says so); the Basque one changes nothing, and in languages without that rule `v` goes to class B (with `f`) and `w` to class W in 2.4.

### 2.3 Iberian form, sign by sign (`clases.red_ib`)

The form is cleaned (2.1) and each letter is replaced as follows: `p b` → P; `t d` → T; `k g` → K; `s ś` → S; `r ŕ` → R; `l` → L; `m ḿ` → M; `n` → N; each vowel, by its base letter in lower case. Anything else is omitted. Used for the corpus (sound profile) and for the numerals.

### 2.4 Form in common spelling (`clases.reducida`)

Used for the dictionaries and, in the meaning-based test, also for the forms of the Iberian units.

1. The form is cleaned with `limpia_grafia` (2.1).
2. If it begins with `h`, that `h` is removed.
3. If it begins with `i` followed by `a`, `e`, `o` or `u`, that `i` is replaced by `j`.
4. It is read from left to right. If the next two characters form a digraph, its class is emitted and two characters are consumed: `tx tz ts tś ch` → C; `sh` → S; `ll` → L; `rr` → R; `ng` → N.
5. Otherwise the class of the character is emitted: `p b` → P; `f v` → B (the `v` of languages whose normaliser has not turned it into `b`); `w` → W; `t d` → T; `k g q` → K; `ʔ h` → H; `s ś z x š ç` → S; `c` → C; `m ḿ` → M; `n ñ ŋ` → N; `r ŕ` → R; `l ł` → L; `y j` → J; a vowel, its base letter in lower case. Anything else is omitted.

### 2.5 Phonetic transcription (`clases.red_afi`)

For each segment: the length marks `ː` and `ˑ` are removed; its class is looked up in LingPy's SCA table (`clases_sca/converter`). If it is not there, it is reduced to its base letters (NFD decomposition, letters only) and looked up again. If still not there, the class of its first letter is taken, unless the first two are a stop (class T, P or K) followed by a sibilant (S), in which case the class is C.

Tone and marker classes (`1` to `6`, `_`, `9`) are discarded. The six SCA vowel classes are written in lower case: A → a, E → e, I → i, U → o, O → o, Y → u. `ʜ` → H is added to LingPy's table (voiceless epiglottal fricative, 112 occurrences in NorthEuraLex, absent from the table). Inventory of what these rules omit in NorthEuraLex: the morpheme separator `+` (7,074 occurrences) and the tone marks `² ⁴ ⁵¹` (1,542); no other segment.

### 2.6 Chan's numerals (`clases.red_chan`)

The form is lower-cased and put in NFC. Each character is replaced by its SCA class; if it has none, by that of its base letter. Anything without a class is omitted. Finally, every contiguous repetition of the same class, of any length, is reduced to one.

### 2.7 Control languages (`normalizadores.red_control`)

The normalised word is split at `ð`; each part is reduced with 2.4 and the parts are joined with the class D.

### 2.8 Reduction to the inventory that Iberian writes (`clases.proyecta`)

B → P; D → T; G → K; C → S; M → N; W → o; J → i; H and `!` are deleted. Forms left with fewer than two symbols are discarded.

---

## 3. Algorithms

### 3.1 Distance measure (`distancia.dist`)

The function's results are kept in a cache of up to four million pairs (`functools.lru_cache`); the cache affects only time and memory, not the values. Between two reduced forms *a* and *b*:

- If either is empty, the distance is 1. If they are equal, 0.
- Weight of a symbol: 0.5 if it is a vowel (lower case); 1 if it is a consonant.
- Costs: inserting or deleting a symbol costs its weight; replacing a vowel by a different vowel costs 0.5; any other replacement of different symbols costs 1.
- The minimum cost of transforming *a* into *b* is computed (dynamic programming, as in edit distance).
- That cost is divided by the mean of the total weights of *a* and *b*.

Example: *śalir* reduces to `SaLiR` (weight 4) and *zilar* to `SiLaR` (weight 4). There are two vowel-for-vowel replacements: cost 1. Distance: 1 / 4 = 0.25.

### 3.2 Meaning-based test (`pruebas.prueba_significados`)

Input: a set of units, a dictionary and the field of terms that corresponds to the dictionary (Spanish or English).

1. For each unit its candidates are obtained. If it has none, the unit does not count.
2. Distance of the unit: the smallest between any of its forms (reduced with 2.4) and any of its candidates.
3. If the units with candidates are fewer than the required minimum, the dictionary is discarded. The minimum is the larger of 4 and 30 % of the number of units (40 % for Wiktionary and its historical layers; in Table 9, the larger of 3 and 30 %).
4. **Real value:** mean of the distances of the units with candidates.
5. **Chance:** repeated 500 times. In each repetition all the distinct candidates of all the units are pooled and grouped by their length in symbols. For each length, as many forms of the same dictionary and of that length as there are distinct candidates are drawn at random, without repeating any, and assigned one by one to the candidates (sorted alphabetically). Each candidate is thus replaced by a form of its own length; a candidate shared by several units receives the same substitute in all of them. The distance of each unit (the smallest between any of its forms and the substitutes of its candidates) and the mean are recomputed. If for some length the dictionary had fewer forms than candidates, the draw is made with repetition.

   If a cap on candidates per unit is set (only in 4.5), the candidates of a unit exceeding it are reduced once, at random, to that number; the same subset serves for the real value and for the draws.
6. **Result:** *z* = (real value − mean of the 500 repetitions) / standard deviation of the 500 repetitions. *p* = (1 + number of repetitions with a value less than or equal to the real one) / 501. **Advantage** = mean of the repetitions − real value.

Dictionaries are ordered by *z*, from lowest to highest. A more negative *z* indicates greater closeness.

### 3.3 Sound-combination profile (`pruebas.perfil`, `pruebas.divergencia`)

- **Profile** of a set of distinct reduced forms: `^` is prefixed and `$` suffixed to each form; all pairs of consecutive symbols are counted; each count is divided by the total.
- **Distance** between two profiles *P* and *Q*: Jensen-Shannon divergence in bits. With *M* = (*P* + *Q*) / 2, it is ½ Σ *P* log₂(*P* / *M*) + ½ Σ *Q* log₂(*Q* / *M*), summing over all pairs present in either. It is 0 if they are identical and 1 if they share no pair.

### 3.4 Numeral series

Distance between two series: mean of the distances (3.1) between numerals of the same value. Where Iberian has two forms for a value, the smaller is taken. Iberian forms are reduced with 2.3.

### 3.5 Advantage by groups of meanings (`pruebas.ventaja_por_grupos`)

For an examined language *X* (with one or more reduced forms per meaning) and a dictionary *Y*:

1. For each meaning with forms in *X* and candidates in *Y*: if there are more than 40 candidates, 40 are taken at random. Real distance: the smallest between the forms and the candidates. Chance: the same, replacing the candidates as in 3.2 (without repeating forms and preserving shared candidates), as many times as there are draws.
2. For each group of meanings with at least three: advantage = mean of chance − real mean.

**Groups.** Stable: N1 to N5, A13, A21, A24, A27, A28, A30 (one to five, woodland/hill, give, earth, grass, road, make). Less stable: the other 29. Criterion: the main gloss appears in the Leipzig–Jakarta list of 100 meanings or in the Swadesh list of 207.

---

## 4. Programs

Each program is run without arguments from `4_programas/` and writes to `resultados/` a JSON file of the same name.

### 4.1 `t06_t07_significados.py` — Tables 6 and 7

Applies test 3.2 to two sets (the 30 units of the lead plaques; the 10 of the numeral series) against four groups of dictionaries:

| Group | Dictionaries | Terms | Minimum |
|---|---|---|---|
| Wiktionary and historical dictionaries | 35 Wiktionary languages; Azkue; Trask, reconstructed (Trask's etymological dictionary was excluded as contaminated by the comparison itself and is not read by the program) | English (Spanish for Azkue) | 40 % |
| Bilingual, Spanish as bridge | Open Data Euskadi; Apertium, 9 languages | Spanish | 30 % |
| Bilingual, English as bridge | Apertium, 10 languages | English | 30 % |
| Concept by concept | WordNet: Basque, Catalan, Galician, Spanish | Spanish, via concepts | 30 % |

### 4.2 `t09_prestamos.py` — Table 9

The same test and the same dictionaries, with the 30 units split into two sets: the 4 proposed as Latin loans and the other 26. Minimum: the larger of 3 and 30 %.

### 4.3 `t04_t05_numerales.py` — Tables 4 and 5, Figure 3

1. **Selection of languages.** From each variety the first form of each value 1, 2, 3, 4, 5, 6, 7, 8 and 10 is taken. Varieties are read in the order of the database and the first of each Glottolog code is kept that has all nine values, whose code is not empty and does not begin with `xxxx` and whose family is not *Bookkeeping*, *Unattested*, *Unclassifiable*, *Pidgin*, *Mixed Language*, *Artificial Language*, *Speech Register* or *Sign Language*. Family of a language: the `Family` field; if empty, the language forms a family of its own.
2. **Iberian.** Distance of the Iberian series (*ban*; *bi*, *bin*; *iŕur*; *lauŕ*; *borste*, *bors*; *śei*; *sisbi*; *sorse*; *abaŕ*, *baŕ*) to each language; they are ranked. The forms are read from the units file.
3. **Languages without relatives in the database.** For each language whose family has a single member in the selection (which is not the same as being an isolate: it may be due to the coverage of the database), the closest language is found and its distance recorded.
4. **Languages with relatives.** A sample of 400 languages is taken from families of five or more members (seed 20261118, over the list in selection order). For each, the closest language is found and its distance recorded, together with whether it is of the same family. Counts are given by distance bands.
5. **Values with external support.** With the values 1, 10 and 20 (*ban*; *abaŕ*, *baŕ*; *oŕkei*, *ogei*), all varieties that have them, first form of each value. The rank of Basque (code `basq1248`) and the first non-Basque variety are recorded.
6. **Shuffled values.** With the ten values, for the four closest varieties: 2,000 times the values of the variety are reordered at random and the distance recomputed.

### 4.4 `t08_perfil.py` — Table 8 and section 7.4

For a base of languages (lexicon → profile per language):

1. **Validation.** For each language with a relative in the base, the language with the closest profile is found and it is recorded whether it belongs to its family. The hit rate expected by chance is also given: mean, over those languages, of (members of its family − 1) / (languages − 1).
2. **Controls.** Profile of the whole eligible lexicon of each control language (forms of 2 to 12 symbols, no gloss required) and its closest languages.
3. **Iberian.** Profile of all the forms of the corpus and, separately, of the forms of the lead plaques (broad criterion). Languages ranked by distance; rank of Basque.
4. **Resampling.** 500 times as many forms as the set has are drawn with replacement, and 500 times half of them without replacement; the number of times Basque is the closest language is counted. In each repetition a single Iberian sample is drawn, which is compared with all languages.

It is run four times: with NorthEuraLex (107 languages), with the forms as they are and with all of them reduced as in 2.8; and with the 35 Wiktionary languages (300 resamplings), in the same way. Families in Wiktionary: Romance (Latin, Catalan, Galician, Asturian, Occitan, Romanian, Sicilian, Sardinian); Celtic (Welsh, Irish); Uralic (Finnish, Estonian, Hungarian); Austronesian (Tagalog, Malagasy, Indonesian, Malay, Hawaiian, Samoan, Tongan, Fijian); Bantu (Swahili, Zulu, Shona).

### 4.5 `s82_formas_y_sinonimos.py` — section 8.2

Only the Wiktionary languages with more than 200 headwords that have inflected forms. For each, two dictionaries are built: with the headwords, and with the headwords plus their inflected forms (each form inherits the meanings of its headword). Test 3.2 is applied with 300 draws, a minimum of 40 % and, if a unit has more than 400 candidates, a cap of 400 (see 3.2). Variants: headwords; headwords and forms; headwords with the extended list of terms; headwords and forms with the extended list. For the numeral series, the first two.

### 4.6 `t10_controles.py` — Table 10

For each control language: its eligible words (1.9) are sorted alphabetically; with the seed 20261119 plus the sum of the Unicode codes of the letters of the English name of the language, eight successive samples of 30 words are drawn without replacement and the first five are used. Each sample is treated as a set of units: each word is a unit, its form is reduced with 2.7 and its terms are those of its gloss. Test 3.2 is applied against the 35 Wiktionary dictionaries, with 150 draws and a minimum of 12 words with candidates.

Expected relatives: Umbrian and Dalmatian, Latin and the Romance languages; Cornish, Welsh and Irish; Gothic, Icelandic; Etruscan and Sumerian, none.

### 4.7 `t11_t13_estables.py` — Tables 11 to 13

- **Table 12.** Algorithm 3.5 with the Iberian forms of the 40 units (reduced with 2.4) against each Wiktionary dictionary, 500 draws.
- **Table 13.** The same against Basque, with these groups: external evidence (N1, N10, N20, A1, A2, A17, A30); numerals by position (N2 to N8); documentary slot (A3 to A23, except A17); toponymic support (A24 to A29); proposed Latin loans (A6, A9, A11, A13). This last group is also computed against Galician.
- **Table 11.** For each pair (language *X*, language *Y*) of the fixed list: the forms of *X* for each meaning are those of its dictionary whose meaning matches an English term of the unit. At least 5 stable and 8 less stable meanings must have forms in *X* and candidates in *Y*. Repeated 20 times: one form of *X* per meaning is chosen at random and 3.5 is applied with 120 draws. The 20 repetitions are averaged. The list of pairs and their type of relation is in the program.

List of pairs (language *X* – language *Y*), fixed before running. There are 43; Zulu–Shona is left out for not reaching the minimum coverage of meanings, and 42 remain.

| Type of relationship | Pairs |
|---|---|
| Closely related | Catalan–Occitan; Galician–Asturian; Malay–Indonesian; Estonian–Finnish; Romanian–Latin; Catalan–Latin; Sardinian–Latin; Zulu–Shona |
| Distantly related | Irish–Welsh; Hungarian–Finnish; Irish–Latin; Icelandic–Latin; Lithuanian–Latin; Icelandic–Lithuanian; Tagalog–Malay; Malagasy–Malay; Hawaiian–Malay; Fijian–Malay; Swahili–Zulu; Hausa–Somali |
| Distant relationship and loans | Albanian–Latin; Welsh–Latin |
| Contact only | Tagalog–Galician; Tagalog–Catalan; Quechua–Galician; Basque–Latin; Basque–Galician; Basque–Catalan; Maltese–Sicilian; Hungarian–Turkish; Finnish–Icelandic; Romanian–Hungarian; Romanian–Turkish; Albanian–Turkish; Malagasy–Swahili |
| Unrelated | Basque–Finnish; Quechua–Hungarian; Hawaiian–Irish; Zulu–Icelandic; Yoruba–Lithuanian; Classical Nahuatl–Welsh; Hausa–Estonian; Fijian–Latin |

The pairs share languages and are not independent observations; the means by type are given as description.

### 4.8 `t14_zonas.py` — Table 14

For each zone (1.2), with the forms of its lead plaques (strict criterion) and with those of all its inscriptions:

1. Profile of the zone and distance to each of the 107 NorthEuraLex languages. Rank of Basque. Relative distance = (distance to Basque − mean of the 107 distances) / standard deviation of the 107.
2. Equalised samples: 300 times as many forms as the zone with fewest forms are drawn without replacement; the relative distance and the rank are averaged.
3. Repeated with all the languages and the Iberian forms reduced as in 2.8.
4. Variation within Iberian: 300 times, two disjoint samples of *n* forms are drawn from each zone (*n* = half the size of the smallest zone); the distance between the first sample of each zone and the second of each zone is computed. The mean is given for the same zone, for neighbouring zones, for non-neighbouring zones and for the two extremes.

---

### 4.9 `figuras.py` — Figures 1 to 3

It computes nothing. From the result files it draws: the *z* values of the Wiktionary languages with the 30 units (Figure 1, top); the distance of each of the 107 languages to the profile of the whole Iberian corpus (Figure 1, bottom); both values together for the languages present in both bases (Figure 2); and the histogram of the distances of the languages without relatives to their nearest neighbour in the numeral series, with the distance between Iberian and Basque (Figure 3). The vertical position of the points in Figure 1 only serves to separate them.

### 4.10 `t15_solidez_unidades.py` — Table 10 bis and section 8.4

With the 30 units of the lead plaques. For each dictionary the real distance (as in 3.2) and the chance distance in each of 500 draws are computed unit by unit; the *z* value of a subset of units is obtained by averaging its columns. Languages: those of Wiktionary with candidates for at least 40 % of the units.

1. **Removing one unit at a time:** value and rank of Basque in the 30 cases.
2. **Random subsets** of 20, 15 and 10 units, 2,000 of each size: number of times Basque is the first language, and median value. In every step of this section, a language enters the comparison of a subset if it keeps at least four units with candidates; the number of languages compared is stored in each result by group (`lenguas_comparadas`). The swapped-meanings trial (step 5) stores the median, the 5th and 95th percentiles and the two extremes of the 300 repetitions.
3. **By origin of the meaning:** external evidence, which is level I (A1, A2, A3, A17, A30; A3 has no Basque candidates and is counted in the group although it is not comparable); toponymic support (A24 to A29); documentary slot (the rest). And by levels of provenance according to the closed inventory of Monograph IV (section 5.1, Table 5): levels I and II together (all except A24 to A29); level II with a Basque correspondence pointed out after the meaning was fixed (A8, A10, A14, A15, A19, A20); level II with no correspondence pointed out (the rest of the documentary slot); the latter without the four proposed Latin loans (A6, A9, A11, A13).
4. **Adversarial removal:** units are sorted by their real distance to Basque, from smallest to largest, and removed one by one; the number that must be removed for Basque to cease to be the first language is recorded.
5. **Swapped meanings:** with Open Data Euskadi, Wiktionary and WordNet. For each pair (unit, meaning of another unit) the real and chance distances are computed (200 draws). *k* units chosen at random (*k* = 5, 10, 15, 20, 30) are given the meaning of another of them by rotation; 300 repetitions per *k*; the median *z* value and the 5th and 95th percentiles are given.

### 4.11 `t16_contraste_principal.py` — section 8.5

Main analysis: the 30 units of the lead plaques against the Wiktionary languages with candidates for at least 40 % of the units.

1. **Substitution with 20,000 draws.** Test 3.2 for Basque with 20,000 draws. The probability is multiplied by the number of languages compared (Bonferroni correction), capped at 1.
2. **Permutation of the meanings.** For each language, with the units that have candidates (minimum 12): the table of distances between each unit *i* and the candidates of the meaning of each unit *j* is built (the smallest distance between the forms of *i* and those candidates). Real value: mean of the diagonal. 100,000 random permutations of the columns are generated and, for each, the mean of the distances between each unit and the meaning assigned to it. *p* = (1 + number of permutations with a value less than or equal to the real one) / 100,001; *z* relative to the permutations. No dictionary word is drawn. It is also applied to Open Data Euskadi, Azkue and WordNet (Basque and Spanish).
3. **The same without the four units proposed as Latin loans.**
4. **Length-conditioned permutation.** As step 2, but the units are grouped by the length (number of symbols) of their first reduced form, and meanings are permuted only within each group; units alone in their group keep theirs. The number of distinct permutations possible (product of the factorials of the group sizes) and the number of units that can change are also given. Declared before running (`resultados/DECLARACIONES_PREVIAS.md`, entry 2).

Seed of the permutations: NumPy `default_rng` generator seeded with the 63 bits given by `pruebas.generador('permutacion', <key of the calculation>, <dictionary name>)`; each calculation and each dictionary thus has its own sequence. When counting the permutations equal to or better than the real value, a numerical tolerance of 10⁻¹² is allowed (a permutation counts if its value is ≤ real + 10⁻¹²), in both variants. The conditioned variant is also computed, and reported, in step 3 (without the four loans).

### 4.12 `t18_perfil_contacto.py` — Table 15 and section 11.3

With NorthEuraLex and the profiles of section 3.3 (forms as they are, without the reduction of 2.8). For each pair (borrowing language, donor language) the other 106 languages are ranked by their profile distance to the first, and the rank of the second, its distance and the closest language are recorded. No draws. Pairs, fixed before running (database names): Basque–Spanish; Basque–Latin; Basque–Catalan; Hungarian–Turkish; Romanian–Bulgarian; Standard Albanian–Latin; Standard Albanian–Modern Greek; Japanese–Mandarin Chinese; Korean–Mandarin Chinese; Finnish–Swedish; English–French; Western Farsi–Standard Arabic; Turkish–Standard Arabic; Turkish–Western Farsi; Breton–French; Armenian–Western Farsi; Hindi–Western Farsi.

### 4.13 `t19_potencia_controles.py` — section 8.3 (power and false positives)

As 4.6, with 100 samples of 30 words per control language. Samples are taken, one after another, from a generator seeded with `20261120|potencia|<language>` over the list of eligible words in alphabetical order; the test of each sample uses the key `potencia|<language>|<sample number>`. Recorded per language: in how many samples the first language is a relative; the value of the first language; the separation from the second; and in how many samples the thresholds −9.3 (value) and 5.6 (separation) are reached. Declared before running in `resultados/DECLARACIONES_PREVIAS.md`.

### 4.14 `t01_t02_corpus.py` — Tables 1 and 2

With the corpus of section 1.2, but with its own segmentation, stricter than that of `fuentes.hesperia`:

- *Words.* From each line of `texto_crudo`, lines containing three or more capital letters in a row (Latin text) are discarded. Each line is split on `· : | , ; /` and spaces. From each piece the signs `[ ] + * ? - ( ) < >`, digits, the numerals `I V X Π`, the full stop and apostrophes are removed, and it is cleaned (2.1, `limpia`). What remains counts as a word if it has two or more characters and all are letters of the alphabet `a e i o u b t k d g l n m r ŕ s ś ḿ` (no `p`, which the Iberian script does not distinguish, and no `h`).
- *Complete words.* Those coming from a piece with none of the signs above (no brackets, crosses or question marks).
- *Distinct forms.* Two words are the same form if they coincide after equating `p b` → P, `t d` → T, `k g` → K, `s ś` → S, `m n ḿ` → N, `r ŕ` → R, `l` → L (`equivalente`).
- *Non-onomastic vocabulary.* On the complete words of four or more letters: those that the MLH V.2 classification (1.2) gives as a personal name, formant, coin legend, mark or abbreviation, or numeral, or as a doubtful name, are excluded; and those that, optionally removing one of the suffixes `ka te en ar e ban sken ḿi ir bi ki ite ke ku ḿ i`, split into two onomastic formants from the list of Rodríguez Ramos (2014) (each part of two or more letters).
- *Table 1.* By support: inscriptions, words, distinct forms and distinct non-onomastic forms. The totals row gives, besides the sum over supports, the number of distinct forms in the whole corpus (union), which is smaller because a form may occur on more than one support.
- *Table 2.* The percentages of names and of repetition are computed on the complete words of three or more letters; that of names applies the classifier above to those words. Repetition: two measures, the percentage of words whose form occurs more than once on the support and the percentage of words repeating a form already present (words minus distinct forms, divided by words). "Non-onomastic forms with a recognisable suffix" counts occurrences (not distinct forms) of complete non-onomastic words of four or more letters ending in one of the first thirteen suffixes of the list and leaving at least three letters before it.

No draws.

### 4.15 `a3_comprobacion_medida.py` — Annex A.3

With NorthEuraLex without Basque (106 languages). For each language and concept the first form in the file that has some class after 2.5 is taken (without applying the length filter of 0.3). Twelve draws of 40 concepts, taken from the list of concepts in alphabetical order with a generator seeded with the number 20261118 (the seed of the original calculation is kept; it is the third exception to 0.4). In each draw, the distance between two languages is the mean of the distances (3.1) between their forms for the same concept, over the concepts of the draw that have a form in both languages; if they share none, the distance is 1. The area under the curve with which that distance separates same-family pairs (field `Family` of `languages.csv`) from the rest is computed by ranks, with mid-ranks for ties; and the same only for old relationships: pairs of the same family, Indo-European or Uralic, with a non-empty `Subfamily` field that differs between the two languages. The mean of the twelve draws, the minimum and the maximum are given.

### 4.16 `t17_techo_circularidad.py` — section 8.4, trial on circularity

With the 30 units of the lead plaques and the Wiktionary languages with candidates for at least 40 % of them. Table of distances between each unit and the candidates of the meaning of every other unit, and its chance with 200 draws (as in 4.10, step 5; key `techo|<language>`). For each language three *z* values are computed: with the proposed meanings; assigning to each unit the meaning that brings it closest to that language within its field (accounting, land or persons, according to `parameters.csv`); and assigning it among the 30 without restriction. Precisions: the optimised assignment is not a permutation (the same meaning may be assigned to several units); it is chosen by minimum distance, not by *z*; the proposed assignment and the optimised ones may use different numbers of units (only those with candidates for the assigned meaning); and the optimisation is not repeated on each null draw, so the resulting *z* is not a calibrated probability that incorporates the process of choosing meanings. The result is inconclusive and the article says so: with that freedom, other languages reach values like that of Basque.

### 4.17 `t20_variacion_semillas.py` — Annex B.7

Each repetition is stored in `resultados/t20_repeticiones/NN.json` together with a fingerprint (SHA-256, 16 characters) of this program, of the `ibcomp` package and of the inputs as read (the 30 units and the Wiktionary dictionaries with their forms and terms); the summary counts only the repetitions whose fingerprint matches that of the current code and data, so that a change in the input data invalidates the stored repetitions just as a change in the code does, and `--regenerar` recomputes them all. The summary of 4.13 (`t19`) does not summarise a language whose file has fewer than 100 samples.

The test of 4.1 with the 30 units of the lead plaques and the Wiktionary languages (same minimum of units, 500 draws), repeated 40 times with the draw key `variacion|k` (k from 1 to 40) instead of the usual key. For each repetition the *z* value of each language is stored. For Basque and for the best of the other languages, the median, extremes and population standard deviation are given; the smallest separation; and the range per language. The repetitions are independent of each other and can be computed in ranges.

### 4.18 `t21_lecturas_alternativas.py` — Table 10 bis, row without alternative readings

With the tables of 4.10 (same keys and draws), *z* value of each language without units A11, A12, A13, A16 and A19 (those with, in some attestation, an alternative reading documented in the monographs), with the minimum of four comparable units; rank of Basque and next languages. Declared before running (entry 4).

### 4.19 `t22_calibracion_perfil.py` — Table 8, calibration

Profiles of 4.4 (full and reduced classes). For the 5,671 pairs of the 107 languages, distance (3.3) and type: same family if both have the same non-empty `Family` field; different families otherwise. Percentile of the Iberian–Basque distance in each group (proportion of pairs with a distance less than or equal to it), number of different-family pairs at that distance or less and the ten closest; for languages whose family has no other language in the base, distance to their nearest neighbour. No draws. Declared before running (entry 5).

### 4.20 `t23_tamano_diccionario.py` — section 8.4, dictionary size

On the Wiktionary rows of Table 6 (without Azkue or the reconstructed lexicon): Spearman correlation (mid-ranks for ties) between the number of forms and the *z* value, with and without Basque; rank of Basque by size; median size. No draws. Declared before running (entry 6).

### 4.21 `t24_jurado_procedencia.py` — Table 10 bis with the blind panel's classification

Repeats part (c) of 4.12 (`t15`: same real/random table per unit, same 500 draws and seed, Wiktionary languages with candidates for at least 40 % of the units, minimum of four comparable units per language) with the level-I, I-plus-II, II and III groups given by each judge's classification and by the least favourable one (lowest level given by any judge), read from `2_criterios/jurado/respuestas/cruce_con_la_clave.tsv` (columns `autor`, `Mistral`, `DeepSeek`, `Grok`, `menos_favorable`; control rows excluded). A group with fewer than four units comparable with Basque is not computed. Declared before the records were sent (entry 7). With the argument `suficiencia` it reads `respuestas_suficiencia/cruce_con_la_clave.tsv` (second question, entry 10) and writes `t24_jurado_procedencia_suficiencia.json`.

### 4.22 `t25_correspondencias.py` — section 11.4, regularity of correspondences

Units: the 30 lead-plaque units and the 10 numerals. For each Wiktionary language with candidates for at least 40 % of them, each unit is paired with its candidate at the smallest distance (3.1; ties, alphabetical). The first reduced Iberian form is aligned with the candidate by Needleman–Wunsch with the costs of 3.1 (vowel 0.5, consonant 1; vowel–vowel substitution 0.5, other 1; identity 0), traceback preferring the diagonal at equal cost; gap "−". R: proportion of columns whose pair is the most frequent for its class (by Iberian class, by Basque class and mean); R′: the same over non-identical columns. Permutation: 1,000 reassignments of candidates among units, generator `correspondencias|permutacion`. Equal-size check: random subsamples of as many non-identical columns as Basque has (200 per language, 20 per permutation), generator `correspondencias|submuestra`. Declared before running (entry 8); the size check was added afterwards.

### 4.23 `t26_prestabilidad.py` — section 11.5, borrowability gradient

Units: the 35 in `1_fuentes_lexicas/wold_prestabilidad_35_unidades.csv` (WOLD *Borrowed score*, copied by hand and published before computing). For each unit, individual *z* = (real distance − mean of the 500 draws) / deviation of the draws, with the table of 4.10 (`t15.tabla`, key `prestabilidad`); Spearman (mid-ranks for ties) between that *z* and the score, with Wiktionary Basque and Open Data Euskadi, and for each Wiktionary language with candidates for at least 40 % of the 35. Declared before running (entry 9).

### 4.24 `t27_etimologia_vasca.py` — section 11.6, etymological status and phonotactics of the Basque candidates

Source: column `etimologia` of `1_fuentes_lexicas/wikcionario/wikcionario_eu_en_v1.csv` (English Wiktionary etymology note; 5,513 records with a note). Declared rule (entry 11): *borrowed* if the note begins with "Borrowed from", "Borrowing from" or "Loanword from", or with "From" (or "Derived/Adapted from") followed by a donor language (Spanish, Classical/Late/Vulgar/Medieval Latin, French, Occitan, Gascon, Aragonese, Romance, Arabic, English, Italian, Catalan, Galician, Portuguese); *inherited* if it contains "Proto-Basque" or begins with "Inherited from"; *unknown* otherwise; *no note* if empty. Lemmas are reduced with `NORM['Basque']` and `reducida`; a form with several lemmas takes the class inherited > borrowed > unknown, and "mixed" if both inherited and borrowed occur. For each unit with candidates in Wiktionary Basque (`terminos_en`), the closest candidate (as in 4.22) and its class. Proportion of borrowings among the candidates with a note against (a) all candidates with a note for the same meanings and (b) the whole lexicon with a note; hypergeometric (K borrowed among N candidates with a note, n matched with a note, k observed) and 10,000 draws of one random candidate with a note per unit (generator `etimologia|sorteo`). Control: the four units in `PRESTAMOS_LATINOS`. Phonotactics: class-trigram model (two initial and one final boundary marks) with interpolated Kneser–Ney smoothing (discount 0.75, continuation counts at bigram and unigram level, unigram with add-0.5) trained on inherited forms and another on borrowed forms; a form is classed as borrowed if its per-segment entropy is lower under the borrowed model; 10-fold cross-validation (split with generator `etimologia|pliegues`). With the argument `amplia`, the undeclared post hoc rule (see entry 11) accepting "borrowed from" in any position; output `t27_etimologia_vasca_amplia.json`. Version 2 (after the phase-4e audit; correction documented in entry 11): a candidate's class is decided only from the lemmas whose gloss makes it eligible; borrowed is split by donor (Romance/Latin vs other); the hypergeometric and the draws use the same units as the observed count and both tails are published; phonotactics also classifies with the candidate forms excluded from training. Version-1 outputs are kept as `t27_etimologia_vasca_v1*`.

### 4.25 `t28_prediccion_prospectiva.py` — second article, prospective prediction (declaration 13)

`preparar`: stripped records (mechanical rule in the program) of the 36 units plus mechanical records of the 11 declared Hesperia words; for each, four candidate meanings (closest Wiktionary Basque, Galician and Latin lemma over the whole dictionary, study distance, alphabetical tie-break, plus one random Basque lemma with generator `prospectiva|azar|<code>`), shuffled with `prospectiva|orden|<code>`; key committed by SHA-256 before sending. `puntuar`: counts per judge and by majority against the binomial (p = 1/5 since "none" is allowed), with the no-U10 breakdown.

### 4.26 `t29_sufijos.py` — second article, suffixes (declaration 12)

`preparar`: mechanical count of the declared suffix inventory over the whole corpus (stem = two-formant personal name, unit, or another word attested twice), and key with SHA-256. `puntuar`: functions fixed by panel majority (≥2 of 3, excluding "indeterminable"); study distance between each Iberian suffix (first variant, reduced) and the Basque exponent of its function (ergative *-k*, genitive *-(r)en*, gentilic *-(t)ar*, determiner *-a*, "half" *erdi*; Trask 1997; Hualde & Ortiz de Urbina 2003); real mean against 10,000 permutations of the exponents among the functions (generator `sufijos|permutacion`). The reference-language comparison is pending (deviation recorded in declaration 12).

### 4.27 `t30_cloze.py` — second article, cloze as memory control (declaration 14)

`preparar`: stripped records without candidates and the three briefs (Basque-primed / Galician-primed / unprimed). `puntuar`: proposed form reduced with the primed language's normaliser (condition C uses Basque: recorded decision, the declaration fixed no reference for C); distance to the real Iberian form against 1,000 random same-length words of that language (generator `cloze|azar|<code>`); share of units below the chance median, also without numerals and without units whose Wiktionary note mentions Iberian.

### 4.28 `t31_reclasificacion_m4.py` — section 8.4, Monograph IV reclassification (declaration 16)

Imports `tabla`, `z_de` and the groups of `t15_solidez_unidades.py` unchanged (same 500 draws, same Wiktionary languages with candidates for at least 40 % of the units). Computes the Basque z value, its rank and the next language in three level II groups (with a later Basque correspondence; without; without and without the four Latin loans), with the original classification (check against v38) and the reclassified one (A7 and A18 move to the group with correspondence). Output: `resultados/t31_reclasificacion_m4.json`.

## 5. Expected results

The file `resultados/RESULTADOS_ESPERADOS.md` gives, table by table, the values that should be obtained and their comparison with those of the article.
