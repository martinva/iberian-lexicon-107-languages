# Criteria of the study and their justification

Each criterion is stated, justified and, where one exists, referred to an equivalent use in the literature. The exact application of each is in `5_especificacion/FUNCTIONAL_SPECIFICATION_en.md`. This text is a translation of `CRITERIOS.md`, which prevails in case of doubt.

Status of the references: **[V]** checked in the source or in its publisher's record; **[P]** partly checked (what is missing is stated); **[C]** cited through another work.

## 1. Which Iberian lexicon is compared

**Criterion.** Two closed sets: the numeral series and the units of measure (lexicon with metrological support), and the 30 lexical units of the lead plaques with economic content.

**Justification.**
- The medium is chosen for an objective reason: lead plaques are 9 % of the inscriptions and hold 41 % of the words and more than half of the vocabulary that is not a proper name; only in them do words appear regularly inside a text, next to figures and in recurring positions (Tables 1 and 2).
- Within the lead plaques no words are selected for this study: the units taken are those resulting from the analysis of those documents in Monographs I–IV.
- The meanings were proposed before the comparison, from the position of each term in the slots of the documents and from its relation to figures and units of measure.

**Equivalent use.** Closed lists, not limited to basic vocabulary and with several terms per meaning: Kilani (2015) **[V]**.

## 2. How a meaning is expressed

**Criterion.** Each unit carries a list of Spanish and English terms, fixed before any dictionary was consulted. A dictionary word is a candidate if its gloss matches one of those terms exactly, once articles and parenthetical clarifications are removed. Partial matches are not admitted.

**Justification.** Exact matching prevents the number of candidates from being enlarged at will. The list of terms is public and is part of the data.

## 3. Degree of certainty and origin of each meaning

**Criterion.** Each unit carries a grade (A, value secured by metrology or by the literature; B, regularity documented in a text or group of texts; C, working hypothesis) and an origin (external evidence; position in the numeral series; documentary slot; toponymic support).

**Justification.** It allows results to be given separately for the meanings obtained without any involvement of Basque and for the rest (Table 13), and thus to measure how much of the result could be due to the way the meanings were assigned.

## 4. Sound classes

**Criterion.** Comparisons are made between forms reduced to sound classes, with the SCA model and its table as distributed by LingPy, unmodified.

**Justification and equivalent use.** Grouping consonants by their tendency to replace one another in language change is an established procedure: Dolgopolsky (1986) **[C]**; Turchin, Peiros and Gell-Mann (2010) **[V]**, who apply it to Indo-European, Semitic and Altaic; List (2012) **[V]**, who extends it in the SCA model. It is the reference grouping in current automatic lexical comparison.

**Own check.** With the 106 NorthEuraLex languages classified by family and 40-concept lists, the distance separates same-family pairs from the rest with an area under the curve of 0.816 (0.777 for old relationships). Program `a3_comprobacion_medida.py`.

## 5. From spelling to sounds

**Criterion.** NorthEuraLex provides phonetic transcription and is reduced directly. Dictionaries are taken in their spelling and converted to a common spelling with general rules per language, fixed before the tests were run and applied to every word of the language.

**Justification.** There is no phonetic transcription of the complete dictionaries. The rules are approximate, but they are the same for all the words of a language, so they cannot favour some units over others. Their effect is tested with the control languages, treated by the same procedure.

**Limit.** An opaque spelling (Irish, French) is represented worse than a transparent one (Basque, Finnish). This may penalise those languages; it cannot explain the result of Basque against other languages with equally transparent spelling.

## 6. Iberian script

**Criterion.** Iberian forms are taken in the Hesperia transcription. The script does not generally distinguish voiceless from voiced stops: *b*/*p*, *t*/*d* and *k*/*g* fall into the same class on both sides of the comparison, because the SCA model groups each pair.

**Check.** The sound-combination profile is repeated reducing all languages to the inventory that Iberian writes; the result does not change (Table 8).

## 7. Discounting chance

**Criterion.** The observed value is compared with the one obtained by replacing the words of matching meaning with words taken at random from the same dictionary and of the same length, without repeating any within a draw and giving the same substitute to a candidate shared by several units. The main analysis adds the permutation of the meanings among the units and the correction for the number of languages compared (Bonferroni).

**Justification and equivalent use.** Permutation tests are the usual procedure for assessing resemblance between word lists: Oswalt (1970) **[C]**; Ringe (1992) **[C]**; Baxter and Manaster Ramer (2000) **[V]**; Kessler (2001) **[V]**; Kilani (2015) **[V]**; Ceolin (2019) **[V]**; Kassian et al. (2021) **[V]**. Correcting the distance between words of the same meaning by the distance between words of different meaning, within the same pair of languages, is what Wichmann et al. (2010) **[V]** propose; drawing within the dictionary itself fulfils that function.

**Matching length.** In the literature on comparison between languages no precedent has been located for matching the length of the drawn words. The principle is, however, in use in a neighbouring problem: Dautriche, Mahowald, Gibson and Piantadosi (2017) **[V]**, when measuring in 100 languages whether words of similar meaning are more alike in form, obtain the chance level by permuting the form–meaning mapping only among words of the same length, for the same reason: length by itself conditions the distance between forms. Here it was adopted because the control languages showed that, without it, unrelated languages obtained values of −4 to −6: words with a common meaning are shorter than an arbitrary dictionary word. With the correction, an isolate does not go beyond −2.5.

## 8. Control languages

**Criterion.** The same tests, with nothing changed, are applied to languages of known affiliation (Umbrian, Gothic, Cornish, Dalmatian) and to isolates (Etruscan, Sumerian); and, in the second part, to 42 pairs of languages that are related, in contact or unrelated.

**Justification and equivalent use.** Validating a comparison method with pairs of known relationship: Blevins and Sproat (2021) **[V]**, with one hundred language pairs.

## 9. Stable and less stable meanings

**Criterion.** A meaning is stable if its main gloss appears in the Leipzig–Jakarta list of 100 meanings or in the Swadesh list of 207.

**Justification and equivalent use.** Meanings differ in their resistance to borrowing: Tadmor, Haspelmath and Taylor (2010) **[V: abstract]**, on 41 languages, the source of the Leipzig–Jakarta list. Comparing resemblance in a basic rank and in a less basic one to separate inheritance from contact is Chen Baoya's rank analysis, set out in Wang and Minett (2005: 123-124) **[V]**, who warn that its reliability had not been established. Sublists of highly stable and less stable meanings, applied to Quechua and Aymara: McMahon et al. (2005) **[V: abstract and excerpt]**; in that case the result pointed to contact.

**Own adaptation.** The lists are applied to the 40 meanings available, and the measure is the advantage over chance, not the proportion of cognates. Because of the warning cited, its discriminating power is checked with the 42 control pairs.

## 10. Zones

**Criterion.** Five zones from north to south, defined by the provenance code in Hesperia. They are compared with samples of the same size.

**Justification and equivalent use.** The relation between linguistic distance and geographic distance is the subject of dialectometry: Nerbonne (2010) **[V: author's manuscript; reference of the published version checked]**.

## 11. Prior declaration

**Criterion.** The delimitation of the lexicon, the measurement rule, the treatment of spellings, the way of discounting chance, the control languages and pairs and the reading of each result were fixed in writing before each test was run.

**Justification and equivalent use.** It prevents the method from being fitted to the result. Fixing in writing and with a date, before the analysis, how things will be measured and how the result will be read is the practice of preregistration, which separates confirmatory from exploratory analysis and limits "researcher degrees of freedom": Roettger (2021) **[V]**, who also admits it for pre-existing data, provided that what was already known about them is disclosed.

**Limit.** Here the declaration is internal (our own dated record), not a deposit in a public registry.

## References added in this document

- List, J.-M. (2012). SCA: Phonetic alignment based on sound classes. En/In D. Lassiter & M. Slavkovik (eds.), *New Directions in Logic, Language and Computation* (Lecture Notes in Computer Science 7415), 32–51. Berlin, Heidelberg: Springer. doi:10.1007/978-3-642-31467-4_3
- Roettger, T. B. (2021). Preregistration in experimental linguistics: applications, challenges, and limitations. *Linguistics* 59(5), 1227–1249. doi:10.1515/ling-2019-0048
- Macklin-Cordes, J. L., Bowern, C. & Round, E. R. (2021). Phylogenetic signal in phonotactics. *Diachronica* 38(2), 210–258. doi:10.1075/dia.20004.mac  (112 vocabularios pama-ñunganos / 112 Pama-Nyungan vocabularies)
- Nerbonne, J. (2010). Measuring the diffusion of linguistic change. *Philosophical Transactions of the Royal Society B* 365(1559), 3821–3828. doi:10.1098/rstb.2010.0048
- Dautriche, I., Mahowald, K., Gibson, E. & Piantadosi, S. T. (2017). Wordform similarity increases with semantic similarity: An analysis of 100 languages. *Cognitive Science* 41(8), 2149–2169. doi:10.1111/cogs.12453
