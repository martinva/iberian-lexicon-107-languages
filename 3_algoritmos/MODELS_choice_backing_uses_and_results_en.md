# The statistical models of the study: why they were chosen, backing, parallel uses and results

One record per model. The detail of each algorithm is in `ALGORITHMS_AND_BACKING_en.md`; the criteria, in `2_criterios/CRITERIA_en.md`; the full figures, in `resultados/EXPECTED_RESULTS_en.md`. Translation of `MODELOS_eleccion_respaldo_usos_y_resultados.md`, which prevails in case of doubt.

Status of what is said about each work by others: **[V]** checked in the source or in its abstract; **[T]** inferred from the title only.

---

## 1. Measure of resemblance: edit distance over sound classes

**What it is.** Each word is reduced to sound classes (p and b are the same class, and so on) and the minimum cost of converting one into the other is counted, with vowels at half weight.

**Why it was chosen.**
- Iberian has no secure relatives: regular sound correspondences, the classical method, cannot be used. A measure is needed that does not presuppose them.
- The Iberian script does not distinguish voiceless from voiced stops; sound classes put all languages on the same footing in that respect.
- It is a simple, public measure with no parameters fitted to Iberian or to Basque.

**Backing.** Consonant classes: Dolgopolsky (1986, cited through others); Turchin, Peiros and Gell-Mann (2010) [V]; List's SCA model (2012) [V]. Normalised edit distance: the ASJP programme, Wichmann et al. (2010) [V].

**Parallel uses.**
- Wichmann et al. (2010): evaluate distance measures between 40-word lists of thousands of languages [V].
- Jäger (2015): weighted alignment on 40-concept lists; concludes that there is support for macrofamilies [T].
- Turchin et al. (2010): consonant classes with resampling, applied to Indo-European, Semitic and Altaic; the proto-languages of Altaic show a significant resemblance (probabilities between 0.01 and less than 10⁻⁵) [V].

**Own check.** With 106 languages of known family, the measure separates same-family pairs from the rest with an area under the curve of 0.816 (0.5 would be chance; 1, perfect separation).

**Own decision.** The half weight of vowels. It was chosen with known relationships, without using Iberian or Basque.

---

## 2. Meaning-based test: permutation test

**What it is.** For each Iberian word, the most similar word among those of the same meaning is looked up in the dictionary of another language. This is compared with what results from replacing those words with random ones from the same dictionary and of the same length. It is repeated 500 times.

**Why it was chosen.**
- It assumes no theoretical distribution: chance is measured on the data themselves.
- It admits small samples (30 and 10 units).
- Drawing within the same dictionary discounts its size and its wealth of synonyms, which would otherwise favour large dictionaries.
- It has been the usual procedure for this question for half a century.

**Backing.** Oswalt (1970) and Ringe (1992), cited through others; Baxter and Manaster Ramer (2000) [V]; Kessler (2001) [V], the reference monograph.

**Parallel uses.**
- Kilani (2015): non-basic lists and several candidates per meaning, applied to Pre-Greek against Proto-Basque, Proto-Uralic and others [V]. It is the design closest to ours. The abstract does not give the result; it must be read in the article.
- Blevins and Sproat (2021): Proto-Basque against Proto-Indo-European, validated on one hundred language pairs of known relationship [V]; they present the result as statistical evidence in favour [T].
- Kassian et al. (2021): permutation test on reconstructions; partial support for the Altaic macrofamily [T].
- Ceolin (2019): applies the tests of Oswalt, Ringe, Baxter–Manaster Ramer and Kessler to Turkish, Mongolian and Manchu; only partial support: Mongolian and Manchu give significant correspondences, Turkish and Mongolian a marginal resemblance that may be due to contact, and Turkish and Manchu test positive under no condition [V, abstract].
- Wichmann et al. (2010): correct the distance between words of the same meaning by that between words of different meaning, which is the function the draw fulfils here [V].

**Length-matched chance.** Words of common meaning are shorter than the dictionary average and therefore resemble any short word more. Without correcting for this, unrelated languages gave values of −4 to −6. No precedent has been located in comparison between languages. The same principle is applied by Dautriche, Mahowald, Gibson and Piantadosi (2017) [V] within each language: they permute form and meaning only among words of the same length, in 100 languages, and find that words of similar meaning are more alike in form.

**The draw.** Each candidate is replaced once per draw by a word of its own length; within each length no word is repeated, and a candidate shared by several units receives the same substitute in all of them. The drawn set thus has the same structure as the real one.

**Results.** Basque first with all seven dictionaries (from −9.7 to −12.8 in the complete ones); next language between −3.3 and −4.8, a value that comes largely from the four units proposed as Latin loans. Without them, Basque holds (from −9.6 to −12.1) and the Romance languages fall within the range of unrelated languages (from +0.4 to −3.5).

---

## 3. Control languages and pairs

**What it is.** The same tests, with nothing changed, applied to cases with a known answer: four languages with relatives (Umbrian, Gothic, Cornish, Dalmatian), two isolates (Etruscan, Sumerian) and, in the second part, 42 language pairs.

**Why it was chosen.** A value of −11 says nothing unless one knows what value the method gives when there is a relationship and when there is none. This is what turns the figures into a scale.

**Backing and parallel use.** Blevins and Sproat (2021) validate their method on one hundred language pairs of known relationship [V]. It is general practice in automatic comparison (Wichmann et al. 2010; Jäger 2015).

**Results.** The relative is the first language in 18 of 20 samples of Table 10 and, with 100 samples per language, in 100 (Dalmatian), 95 (Umbrian), 90 (Cornish) and 79 (Gothic); none of 200 samples of languages without relatives reaches the value or the separation of Iberian with Basque (best value, −6.9, for Etruscan). Dalmatian against Romance, from −12.1 to −15.5; Cornish against Welsh, from −6.7 to −13.6; Sumerian, not beyond −2.8. The value of Iberian with Basque is of the order of Cornish with Welsh.

---

## 4. Sound-combination profile, with Jensen-Shannon divergence

**What it is.** One counts how often each sound class is followed by each other one in the whole vocabulary of a language, and measures the difference between the profiles of two languages. It uses no meanings.

**Why it was chosen.**
- The Iberian meanings are proposals. A test was needed that did not depend on them.
- It uses the whole corpus (2,229 forms), not only the 30 units.
- Jensen-Shannon divergence is the standard measure for comparing two frequency distributions: it is symmetric and always lies between 0 and 1.

**Backing.** Macklin-Cordes, Bowern and Round (2021) [V]: in 112 Pama-Nyungan vocabularies, the frequency of transitions between sound classes retains a signal of relationship.

**Where it departs.** They test each transition against a known tree; they do not compute distances between languages. The distance between profiles and its validation are from this work. It is the model with least direct backing and was therefore validated separately.

**Own validation.** The language with the closest profile is of the same family for 77 of 98 languages (79 %; by chance, 20 %).

**Results.** Basque first of 107 (0.153; Latin 0.174), in 500 of 500 resamplings. In 17 pairs of languages with heavy lexical borrowing, the donor is in no case the language of closest profile (median rank, 72 of 106); this is a descriptive fact, which does not allow contact to be excluded. Also with the lead plaques alone, with the languages reduced to what Iberian writes, and against 35 languages from other parts of the world.

**Limits.** The way sounds combine also reflects typology and areal contact. With the languages reduced the test discriminates less well (70 %) and Umbrian no longer points to Latin.

---

## 5. Numeral series against a worldwide database

**What it is.** The Iberian series is compared, value by value, with that of 3,811 languages. The database itself serves as the yardstick: at what distance languages without relatives have their nearest neighbour, and how often a language's nearest neighbour is of its family.

**Why it was chosen.**
- Low numerals are basic vocabulary, the least exposed to borrowing, and the only vocabulary of that kind the material offers.
- Three values (1, 10, 20) have external support (a coin mark, a stone weight and a capacity mark; Ferrer i Jané 2022: 16-19), with no involvement of Basque.
- A worldwide database makes it possible to say what the distance obtained means, without assumptions.

**Backing.** Chan's database (2019), Numeralbank edition. The calibration with the database itself is from this work; it follows the same logic as the controls (record 3).

**Results.** Basque at 0.317; the second language, at 0.756. None of the 110 languages without relatives in the database has so close a neighbour (the closest, 0.407). When the neighbour lies between 0.2 and 0.5, it is of the same family in 162 of 165 cases.

---

## 6. Stable and less stable meanings

**What it is.** Meanings that are rarely borrowed (one, two, give, earth) are separated from those that are borrowed easily, and resemblance is measured in each group.

**Why it was chosen.** It is the established way of telling inheritance from borrowing when neither grammar nor regular correspondences are available: borrowing concentrates in cultural vocabulary; inheritance shows above all in basic vocabulary.

**Backing.**
- Tadmor, Haspelmath and Taylor (2010) [V, abstract]: across 41 languages, the proportion of loanwords varies from one semantic field to another; hence the Leipzig–Jakarta list.
- Chen Baoya's rank analysis, set out in Wang and Minett (2005: 123-124) [V], who warn that its reliability had not been established.

**Parallel use.** McMahon et al. (2005) [V, abstract]: more and less stable sublists applied to Quechua and Aymara; they conclude that contact is the most likely explanation. That is, the method also returns "contact" when that is the case.

**Where it departs.** It is applied to 40 meanings and with a distance measure, not a cognate count. Because of Wang and Minett's warning, it was checked with 42 pairs.

**Results.** Close relatives 0.40 / 0.28; distant relatives 0.13 / 0.06; contact only 0.04 / 0.05. Iberian–Basque 0.53 / 0.45. With only the meanings with external support, 0.56. With eleven stable meanings, it is presented as an indication.

---

## 7. Proximity by zones

**What it is.** The sound-combination profile (record 4) computed in five zones, from north to south, with samples of the same size.

**Why it was chosen.** If Iberian and Basque-Aquitanian had formed a continuous chain of varieties, northern Iberian should resemble Basque more. It is a prediction that can be tested without using meanings.

**Backing.** Dialectometry: Nerbonne (2010) [V], who measures how linguistic difference grows with geographic distance.

**Results.** Basque first in all five zones, with no gradient (from −2.2 to −2.5). Iberian is very uniform. In the lead plaques of Narbonensis–Roussillon, Basque and Latin are almost level.

---

## 8. Resampling

**What it is.** Repeating a test with random samples of the material itself (with replacement, or by halves) to see whether the result depends on a few words.

**Why it was chosen.** It is the standard way of measuring the stability of a result without theoretical assumptions. Turchin et al. (2010) use it with consonant classes [V].

**Results.** Basque first in all resamplings of the sound profile.

---

## 9. Prior declaration

**What it is.** Fixing in writing, before running, what is measured, how, and what would count against.

**Backing.** Roettger (2021) [V]: preregistration separates confirmatory from exploratory analysis and limits the possibility of fitting the method to the result. Here it is an internal, dated record, not a public deposit.

---

## 10. Robustness to the list of units

**What it is.** The meaning-based test repeated removing units (one by one, at random, the most favourable ones) and swapping meanings between units.

**Why it was chosen.** The Iberian meanings are proposals. One needs to know whether the result depends on a few units and whether the test stops giving a result when meanings are wrongly assigned, which is what must happen if it measures a relation between form and meaning.

**Backing.** These are standard sensitivity analyses: leave-one-out, subsampling and label permutation. Permuting the form–meaning mapping is the same principle as the main test (Kessler 2001) and as Dautriche et al. (2017).

**Results.** Basque first when any one of the 30 units is removed; with 20 at random, in 2,000 of 2,000; with 10, in 1,975 of 2,000. Thirteen of the 28 comparable units must be removed, by choice, for it to lose first place. With 15 meanings swapped the value is still around −6; with all 30, it falls to the level of chance. With the 24 units whose meaning was obtained without Basque comparison (closed inventory of Monograph IV), −9.3; next, −4.0. In the 13 level-II units with no Basque correspondence pointed out, Basque and Tagalog are practically tied (−4.4 and −4.3).

---

## 11. Permutation of the meanings and correction for the number of languages

**What it is.** The Iberian forms and the candidates are left as they are, and only the meaning assigned to each unit is changed (100,000 random reassignments). The real value is compared with those of the reassignments. The probability is multiplied by the number of languages compared.

**Why it was chosen.** The substitution test depends on how the dictionary words are drawn. This one draws none: it measures directly whether the forms resemble the words of their proposed meaning more than those of the other meanings in the list. And with 500 draws the smallest possible probability (0.002) does not allow correcting for 32 languages.

**Backing.** It is the permutation test of Oswalt (1970) and Kessler (2001) [V], with a distance instead of a count of matches. The Bonferroni correction is the usual one for multiple comparisons.

**Results.** Basque: value −10.1; none of 100,000 permutations equals the proposed assignment; probability corrected for 32 languages, 0.0003. The same with Open Data Euskadi, Azkue and WordNet. Galician also passes the threshold with the 30 units (−4.0; corrected 0.003); without the four units proposed as Latin loans it loses it (0.19) and Basque is the only language that keeps it (−9.8; 0.0003). Length-conditioned permutation: Basque −8.3; none of 100,000; corrected, 0.0003 (Galician 0.002; Tagalog 0.01); without the four loans, Basque −7.6 (0.0003), Galician 0.07, Tagalog 0.71. Substitution with 20,000 draws: −12.3; corrected probability, 0.0016.

---

## What comes from the literature and what is our own

| Element | Origin |
|---|---|
| Sound classes, edit distance | Literature, unchanged |
| Half weight of vowels | Own; validated with known families |
| Permutation test with several candidates | Literature (Kilani 2015) |
| Drawing within the dictionary | Own; same function as the correction of Wichmann et al. (2010) |
| Length-matched chance | Own between languages; principle in use (Dautriche et al. 2017) |
| Distance between sound profiles | Own, building on the finding of Macklin-Cordes et al. (2021); validated separately |
| Calibration of the numeral series with the worldwide database | Own |
| Stable and less stable with a distance measure | Own adaptation of Chen and of McMahon et al.; validated with 42 pairs |

## What remains to be checked

- Result of Kilani (2015): the abstract does not give it. It must not be cited in the article until read in the source.
- McMahon et al. (2005) and Tadmor et al. (2010): read in abstract only.
