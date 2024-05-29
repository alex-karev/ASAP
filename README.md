# Automated Student Assessment Prize (ASAP)

This repo contains a copy of ASAP dataset for essay scoring converted into a better format.

## Features

- **Reorganized** and **cleaned** from unnecessary data.
- **Normalized** scores and added.
- Uniform **labels** across all prompts are added.
- **Min** and **Max** scores are added.
- Converted to **'.parquet'**.

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

## Usage

- `ASAP.parquet` contains the processed dataset.
- `convert.py` for processing the dataset.
- `analyze.py` generates a table in "Dataset Overview" section.
- `descriptions/` contains rubrics and descriptions from the original dataset.
- `original/` contains the original dataset

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

## Contribution

Feel free to fork this repo and make pull requests.

If you like my work, please, support me:

BTC: 32F3zAnQQGwZzsG7R35rPUS269Xz11cZ8B
