# Automated Student Assessment Prize (ASAP)

This repo contains a copy of ASAP dataset for essay scoring converted into a better format.

## Features

- **Reorganized** and **cleaned** from unnecessary data.
- **Normalized** scores.
- Uniform **labels** across all prompts are added.
- **Min** and **Max** scores are added.
- Converted to **'.parquet'**.
- Merged with **normalized** version of `ASAP++` dataset.
- Rubrics, prompt texts and sources were manually extracted from `*.docx` and `*.xlsx`.

## Dataset Overview

|    | Prompt   | Genre       |   Texts |   Avg. Words |   Min. Words |   Max. Words |   Avg. Norm. Score |
|---:|:---------|:------------|--------:|-------------:|-------------:|-------------:|-------------------:|
|  0 | 1        | Argument    |    1783 |       365.77 |            8 |          785 |               0.65 |
|  1 | 2        | Argument    |    1800 |       403.29 |           31 |         1119 |               0.48 |
|  2 | 3        | Explanation |    1726 |       109.27 |           10 |          375 |               0.62 |
|  3 | 4        | Explanation |    1770 |        95.74 |            2 |          357 |               0.48 |
|  4 | 5        | Explanation |    1805 |       124.45 |            4 |          743 |               0.6  |
|  5 | 6        | Explanation |    1800 |       153.9  |            3 |          454 |               0.68 |
|  6 | 7        | Narrative   |    1569 |       169.44 |            5 |          592 |               0.54 |
|  7 | 8        | Narrative   |     723 |       612.49 |            4 |          904 |               0.62 |
|  8 | Total    |             |   12976 |       254.29 |            2 |         1119 |               0.58 |

Columns: `['id', 'text', 'prompt', 'score', 'min_score', 'max_score', 'norm_score', 'label', 'narrativity', 'language', 'prompt_adherence', 'conventions', 'sentence_fluency', 'word_choice', 'organization', 'content']`

## Usage

- `ASAP.parquet` contains the processed dataset.
- `convert.py` for processing the dataset.
- `analyze.py` generates a table in "Dataset Overview" section.
- `descriptions.json` contain prompts, rubrics, sources and score ranges for each prompt.
- `descriptions/` contains rubrics and descriptions from the original dataset.
- `*.md` files in `descriptions/` contain rubrics, prompts and sources extracted from `*.docx` and `.xlsx` documents. In `rubrics.md`, all text directly referencing particular score point is removed.
- `generate_descriptions.py` generates `descriptions.json`.
- `linguistic_features.parquet` contains linguistic feature analysis for each text in `ASAP.parquet` (see description below).
- `generate_linguistic_features.py` generates `linguistic_features.parquet` from `ASAP.parquet`.
- `original/` contains the original dataset

## Linguistic features

`linguistic_features.parquet` contains the analysis for the following linguistic features in all texts:

|Column|Description|
|---|---|
|id|Text id in `ASAP.parquet`|
|chars|Character Count|
|words|Word Count|
|4sqrt_words|Fourth Root of Word Count|
|avg_word_len|Average Word Length|
|words_gr5|Word Count > 5 Char|
|words_gr6|Word Count > 6 Char|
|words_gr7|Word Count > 7 Char|
|words_gr8|Word Count > 8 Char|
|diff_words|Difficult Word Count|
|long_words|Long Word Count|
|spell_err|Spelling Errors|
|uniq_words|Unique Word Count|
|nouns|Noun Count|
|verbs|Verb Count|
|adj|Adjective Count|
|adv|Adverb Count|
|stop_words|Stop Words Count|
|sentences|Sentence Count|
|avg_sentence_len|Average Sentence Length|
|exclamations|Exclamation Mark Count|
|questions|Question Mark Count|
|commas|Comma Count|
|avg_syllables|Average Syllables Per Word|
|poly_syllable|Polysyllablic Words|
|flesch|Flesch Reading Ease|
|gunning_fog|Gunning Fog|
|smog|Smog Index|

## References

ASAP dataset:

```
@misc{asap-aes,
    author = {Ben Hamner, Jaison Morgan, lynnvandev, Mark Shermis, Tom Vander Ark},
    title = {The Hewlett Foundation: Automated Essay Scoring},
    publisher = {Kaggle},
    year = {2012},
    url = {https://kaggle.com/competitions/asap-aes}
}
```

ASAP++ dataset:

```
@inproceedings{mathias-bhattacharyya-2018-asap,
    title = "{ASAP}++: Enriching the {ASAP} Automated Essay Grading Dataset with Essay Attribute Scores",
    author = "Mathias, Sandeep  and
      Bhattacharyya, Pushpak",
    editor = "Calzolari, Nicoletta  and
      Choukri, Khalid  and
      Cieri, Christopher  and
      Declerck, Thierry  and
      Goggi, Sara  and
      Hasida, Koiti  and
      Isahara, Hitoshi  and
      Maegaard, Bente  and
      Mariani, Joseph  and
      Mazo, H{\'e}l{\`e}ne  and
      Moreno, Asuncion  and
      Odijk, Jan  and
      Piperidis, Stelios  and
      Tokunaga, Takenobu",
    booktitle = "Proceedings of the Eleventh International Conference on Language Resources and Evaluation ({LREC} 2018)",
    month = may,
    year = "2018",
    address = "Miyazaki, Japan",
    publisher = "European Language Resources Association (ELRA)",
    url = "https://aclanthology.org/L18-1187",
}
```

## Contribution

Feel free to fork this repo and make pull requests.

If you like my work, please, support me:

BTC: 32F3zAnQQGwZzsG7R35rPUS269Xz11cZ8B
