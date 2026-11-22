# Algorithms and their backing

For each algorithm: what it does, an example, where it comes from and where it departs from its precedents. The step-by-step formulation is in `5_especificacion/FUNCTIONAL_SPECIFICATION_en.md`, section 3. Full references and their verification status are in `2_criterios/CRITERIA_en.md` and in the bibliography of the article. This text is a translation of `ALGORITMOS_Y_RESPALDO.md`, which prevails in case of doubt.

## 1. Distance between two words

**What it does.** It converts each word into a string of sound classes and measures the minimum cost of transforming one into the other, with vowels at half cost, divided by the weighted mean length.

**Examples.**

| Iberian | Other form | Reduced forms | Operations | Distance |
|---|---|---|---|---|
| *luŕa* | *lur* | LuRa / LuR | delete one vowel | 0.5 / 2.75 = 0.18 |
| *śalir* | *zilar* | SaLiR / SiLaR | replace two vowels | 1 / 4 = 0.25 |
| *laku* | *lagun* | LaKu / LaKuN | add one consonant | 1 / 3.5 = 0.29 |
| *abaŕ* | *hamar* | aPaR / aMaR | replace one consonant | 1 / 3 = 0.33 |

**Origin.** Normalised edit distance is the measure of the ASJP programme (Wichmann et al. 2010). Sound classes: Dolgopolsky (1986) and List (2012). Jäger (2015) uses the same basis, with weights learned from the data, on 40-concept lists.

**Where it departs.** The half weight of vowels is our own decision. It was chosen with known relationships (NorthEuraLex), without using Iberian or Basque, because it was the variant that best separated languages of the same family.

## 2. Meaning-based test

**What it does.** For each Iberian unit it looks up, in a dictionary, the words with the same meaning and records the closest one. The mean of those distances is compared with the one obtained by replacing the same-meaning words with random words of the same length.

**Example.** With the Open Data Euskadi lexicon, the mean distance of the 30 units to the closest word of their meaning is 0.45; with random words of the same length, 0.74; none of 500 draws gives 0.45 or less.

**Origin.** Permutation test on word lists: Oswalt (1970), Ringe (1992), Baxter and Manaster Ramer (2000), Kessler (2001). Several candidates per meaning and non-basic lists: Kilani (2015). Correction by the distance between words of different meaning: Wichmann et al. (2010).

**Where it departs.** (a) The draw is made within the dictionary itself, which discounts its size and its wealth of synonyms. (b) The drawn words have the same length as those replaced; in each draw none is repeated, and a candidate shared by several units receives the same substitute in all of them. (c) The main analysis adds the permutation of the meanings among the units (Oswalt 1970; Kessler 2001), which draws no word, and the Bonferroni correction for the number of languages. No precedent located in comparison between languages; the same principle, permuting only among words of equal length, is applied by Dautriche et al. (2017) within each language. Here it was motivated by the control languages.

## 3. Sound-combination profile

**What it does.** It counts how often each sound class follows each other one in the vocabulary of a language, including word beginning and word end, and measures the difference between the profiles of two languages. It uses no meanings.

**Example.** The word `SaLiR` contributes the pairs `^S`, `Sa`, `aL`, `Li`, `iR`, `R$`.

**Origin.** Macklin-Cordes, Bowern and Round (2021) show that the frequency of transitions between sound classes retains a signal of relationship; they test each transition against a known tree and do not compute distances between languages.

**Where it departs.** The distance between profiles (Jensen-Shannon divergence) and its validation are from this work. Validation: in NorthEuraLex, the language with the closest profile is of the same family for 77 of 98 languages with relatives in the base (79 %; by chance, 20 %).

**Limit.** The way sounds combine also reflects typology and areal contact, not only inheritance.

## 4. Numeral series

**What it does.** It compares the Iberian numeral series, value by value, with that of each language in a worldwide database, and uses the database itself to learn what the distance obtained means: at what distance languages without relatives have their nearest neighbour, and how often a language's nearest neighbour is of its own family.

**Origin.** Chan's database (2019). The use of the database itself as an empirical reference is from this work.

## 5. Advantage in stable and less stable meanings

**What it does.** It separates the meanings into two groups, according to whether or not they appear in the basic-vocabulary lists, and measures in each how much closer a word is to the one that corresponds to it by meaning than to random words.

**Reading.** In related languages, the advantage is greater in the stable meanings. In languages that have only been in contact, it is small and not concentrated in them.

**Origin.** Chen Baoya's rank analysis (in Wang and Minett 2005: 123-124); sublists of McMahon et al. (2005); lists of Tadmor, Haspelmath and Taylor (2010) and of Swadesh.

**Where it departs.** It is applied to the 40 meanings available, not to the complete lists, and with a distance measure instead of a cognate count. It is therefore validated with 42 language pairs of known relationship.

## 6. Proximity by zones

**What it does.** It computes the sound-combination profile of each zone of the Iberian territory and its distance to Basque, with samples equalised in size, to see whether the proximity changes from north to south.

**Origin.** Dialectometry (Nerbonne 2010).

**Limit.** There are no texts from the zone of contact with Basque-Aquitanian.
