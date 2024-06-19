#!/usr/bin/python
import pandas as pd
from pathlib import Path

# Constants
TARGET_PATH = "ASAP.parquet"
TARGET_RANGE = (0.0, 1.0)
TARGET_LABELS = (0,9)

SOURCE_LABELS = [(2,12), (1,6), (0,3), (0,3), (0,4), (0,4), (0,30), (0,60)]
SOURCE_PATH = "original/ASAP.tsv"
SOURCE_PATH_PLUS_PLUS = "original/asap-plus-plus"
SOURCE_ENCODING = "latin1"
SOURCE_SEPARATOR = "\t"
SOURCE_SEPARATOR_PLUS_PLUS = ","

# Read dataset and convert it to dataframe
print("Reading {}...".format(SOURCE_PATH))
input_df = pd.read_csv(SOURCE_PATH, sep=SOURCE_SEPARATOR, encoding=SOURCE_ENCODING)
print(input_df)

# Read asap++ dataset and convert it to dataframe
print("Reading {}...".format(SOURCE_PATH_PLUS_PLUS))
input_plus_plus = []
for i in range(1, 6):
    path = Path(SOURCE_PATH_PLUS_PLUS) / "Prompt-{}.csv".format(i)
    prompt_df = pd.read_csv(path)
    # Raname incorrectly named columns
    prompt_df = prompt_df.rename(columns={"EssayID": "Essay ID"})
    # Normalize columns
    for column in prompt_df.columns:
        if column == "Essay ID":
            continue
        min_value = prompt_df[column].min()
        max_value = prompt_df[column].max()
        prompt_df[column] = (prompt_df[column]-min_value)/(max_value - min_value)
    # Save prompt
    input_plus_plus.append(prompt_df)
input_plus_plus_df = pd.concat(input_plus_plus, axis=0)

# Extract information
print("Processing dataset...")
scores = input_df["domain1_score"]
texts = input_df["essay"]
prompts = input_df["essay_set"]
ids = input_df["essay_id"]

# Add score ranges
min_scores = [SOURCE_LABELS[x-1][0] for x in prompts]
max_scores = [SOURCE_LABELS[x-1][1] for x in prompts]

# Normalize scores and reassign labels
normalized_scores = []
labels = []
for i, x in enumerate(scores):
    min_x = min_scores[i]
    max_x = max_scores[i]
    norm_x = (x - min_x) / (max_x - min_x)
    label_x = norm_x * (TARGET_LABELS[1] - TARGET_LABELS[0]) - TARGET_LABELS[0]
    label_x = round(label_x)
    norm_x = norm_x * (TARGET_RANGE[1] - TARGET_RANGE[0]) - TARGET_RANGE[0]
    normalized_scores.append(norm_x)
    labels.append(label_x)

# Create new dataset
df = pd.DataFrame({
    "id": ids,
    "text": texts,
    "prompt": prompts,
    "score": scores,
    "min_score": min_scores,
    "max_score": max_scores,
    "norm_score": normalized_scores,
    "label": labels
})

# Add ASAP++ columns
for column in input_plus_plus_df.columns:
    if column == "Essay ID": continue
    df.insert(8, column.lower().replace(" ","_"), [-1.0] * len(df), True) # type: ignore

# Merge with ASAP++
print("Merging with ASAP++...")
for index, row in input_plus_plus_df.iterrows():
    id = int(row["Essay ID"])
    item = df[df["id"] == id]
    item_index = item.index
    for column in input_plus_plus_df.columns:
        if column == "Essay ID": continue
        df.loc[item_index, column.lower().replace(" ","_")] = row[column]
print(df)

# Save dataset
print("Saving...")
df.to_parquet(TARGET_PATH)
print("The dataset was saved to {}.".format(TARGET_PATH))
