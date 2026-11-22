# Protocol for measuring the affinity of a small-corpus language with proposed meanings

This document describes the study's procedure as a protocol applicable to other languages. The components come from quantitative comparative linguistics (see `MODELS_choice_backing_uses_and_results_en.md`); what is fixed here is their combination, the order of the steps and the checks that make the result readable. Translation of `PROTOCOLO.md`, which prevails in case of doubt.

## The case it addresses

A language meeting these three conditions, which prevent the classical comparative method from being applied:

1. **Small corpus**: a few hundred or a few thousand forms, with no described grammar.
2. **Proposed, not secure, meanings**: they are known from the context of the documents, from metrology or from bilinguals, not from translation.
3. **No established relatives**: regular sound correspondences cannot be used as a starting point.

## Principles

| Principle | How it is met |
|---|---|
| The material is delimited by a criterion external to the result | Medium and type of document, not chosen words |
| Meanings are fixed before comparing, and where each comes from is recorded | Grade (A, B, C) and origin (external evidence, position in a series, documentary slot, indirect support) |
| All languages are treated alike | Same reduction rules, same measure, same dictionaries |
| Chance is measured on the data themselves | Drawing within the same dictionary and with the same length; permutation of the meanings among the units |
| Every figure is read against cases with a known answer | Control languages and pairs, under the same rules |
| What depends on the meanings is checked against something that does not | Test without meanings on the whole corpus |
| What is expected and what would count against is written down before running | Dated record |

## Steps

**Part one: is there an affinity with any language, and is it greater than chance?**

1. **Delimit the lexicon** by an objective criterion and document its representativeness in the corpus.
2. **Fix the meanings and their terms** in the bridge languages, with grade and origin.
3. **Reduce** the forms of all languages to sound classes, with general rules per language.
4. **Meaning-based test**: distance to the closest word of the same meaning, against length-matched chance; with several independent dictionaries of each language.
5. **Test without meanings**: sound-combination profile of the whole corpus against that of each language, validated with known families.
6. **Available basic vocabulary** (here, the numeral series) against a worldwide database, using the database itself as the yardstick for what each distance means.
7. **Controls**: the same tests with languages of known affiliation and with isolates.
8. **Robustness checks**: without the identified loans, with inflected forms and synonyms, by resampling, removing units and swapping meanings.
9. **Main analysis**: permutation of the meanings among the units and correction for the number of languages compared.

**Part two: if one language stands out, what kind of relationship is it?** (gives indications, not proof)

10. **Stable against less stable meanings**, with control pairs that are related, in contact and unrelated.
11. **Breakdown by origin of the meaning**: the result is given separately for the meanings obtained without the help of the language with which the comparison is made. This is the answer to the objection of circularity.
12. **Geographic variation**: the test without meanings by zones, with equalised samples.

## What it allows one to state and what it does not

- It allows one to state: which language is the closest, by what margin over the next, with what probability of chance, and whether the distribution of the resemblance corresponds to that of related languages or to that of languages that have only been in contact.
- It does not allow one to state: a proven genetic relationship. That requires grammar and regular sound correspondences.

## What is specific to this protocol

- Length-matched chance in comparison between languages.
- The distance between sound-combination profiles and its validation by families.
- The calibration of the numeral series with the worldwide database.
- The test of stable and less stable meanings with a distance measure, validated with control pairs.
- The breakdown of the result by the origin of each meaning.

## How to apply it to another language

Three files in `1_fuentes_lexicas/` must be replaced: the units with their meanings, the corpus and, if the script requires it, the reduction rule for its signs. The dictionaries, the comparison databases, the controls and the programs do not change.
