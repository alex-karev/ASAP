#!/usr/bin/python
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

# Constants
DATASET_PATH = "ASAP.parquet"
GENRES = ["Argument"] * 2 + ["Explanation"] * 4 + ["Narrative"] * 2

# Check dataset
if not os.path.exists(DATASET_PATH):
    print("Dataset {} was not found!\nUse convert.py first".format(DATASET_PATH))
    sys.exit(1)

# Load dataset
print("Loading dataset...")
df = pd.read_parquet(DATASET_PATH)
print(df)

# Count texts
n_prompts = len(df["prompt"].unique())
n_texts = len(df)
n_prompt_texts = [len(df[df["prompt"] == x]) for x in range(1, n_prompts+1)]

# Count words
avg_prompt_words = []
min_prompt_words = []
max_prompt_words = []

for prompt in range(1, n_prompts+1):
    avg_words = 0
    min_words = sys.maxsize
    max_words = -1
    texts = df[df["prompt"] == prompt]["text"]

    for text in texts:
        n_words = len(text.split(" "))
        min_words = min(min_words, n_words)
        max_words = max(max_words, n_words)
        avg_words += n_words
   
    avg_words /= len(texts)
    
    min_prompt_words.append(min_words)
    max_prompt_words.append(max_words)
    avg_prompt_words.append(avg_words)

# Count total words
avg_words = sum(avg_prompt_words) / len(avg_prompt_words)
min_words = min(min_prompt_words)
max_words = max(max_prompt_words)

# Calculate average scores
avg_prompt_scores = [df[df["prompt"] == x]["norm_score"].mean() for x in range(1, n_prompts+1)]
avg_score = sum(avg_prompt_scores) / len(avg_prompt_scores)

# Generate statical dataframe
df_stats = pd.DataFrame({
    "Prompt": list(range(1, n_prompts+1)),
    "Genre": GENRES,
    "Texts": n_prompt_texts,
    "Avg. Words": avg_prompt_words,
    "Min. Words": min_prompt_words,
    "Max. Words": max_prompt_words,
    "Avg. Norm. Score": avg_prompt_scores
})

# Add total
df_stats.loc[n_prompts] = ["Total", "", n_texts, avg_words, min_words, max_words, avg_score]

# Round values
df_stats = df_stats.round(2)

# Output statistics
print(df_stats)
print(df_stats.to_markdown(mode="github"))
print("Columns:", df.columns)

# Plot correlation matrix
matrix = df.drop("text", axis=1).corr()
labels = [x for x in matrix.columns]
plt.imshow(matrix, cmap="Blues")
plt.colorbar()
plt.xticks(range(len(matrix)), labels, rotation=45, ha="right")
plt.yticks(range(len(matrix)), labels)
plt.show()
