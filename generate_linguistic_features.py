#/usr/bin/python
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag, download
from textstat.textstat import textstatistics
import enchant
import re

# Load dataset
df = pd.read_parquet("ASAP.parquet")

# Define parameters
tokenize_filter = '[^A-Za-z\- ]+'
spellcheck_dict = enchant.Dict("en_US")
difficult_words_list = []
with open("./difficult_words.txt", "r") as f:
    difficult_words_list = f.read().split("\n")
download('stopwords')
download('punkt_tab')
download('averaged_perceptron_tagger_eng')
stopwords_list = set(stopwords.words('english'))
noun_tags = ["NN","NNS","NNP","NNPS"]
verb_tags = ["MD","VB","VBD","VBG","VBN","VBP","VBZ"]
adjective_tags = ["JJ", "JJR", "JJS"]
adverbs_tags = ["RB","RBR","RBS","WRB"]

#
# Functions
#

# Tokenize by words
def tokenize(text: str) -> list[str]:
    _text = text.replace("/"," ")
    _text = _text.replace("/"," ")
    tokens = []
    for word in word_tokenize(text):
        if "@" in word:
            word = word.lower()
        word_clean = re.sub(tokenize_filter, '', word)
        if len(word_clean) > 0:
            tokens.append(word_clean)
    return tokens

# Count characters
def count_characters(text: str) -> int:
    return len(text)

# Count words
def count_words(tokens: list[str], limit: int = 0) -> int:
    n = 0
    for word in tokens:
        if len(word) > limit:
            n += 1
    return n

# Fourth root of word count
def fourth_root_of_word_count(tokens: list[str]) -> float:
    words = count_words(tokens)
    return words ** (1/4)

# Average word length
def average_word_length(tokens: list[str]) -> float:
    avg = 0
    for word in tokens:
        avg += len(word)
    avg /= len(tokens)
    return avg

# Difficult words
def count_difficult_words(tokens: list[str]) -> int:
    n = 0
    for word in tokens:
        if word in difficult_words_list:
            n += 1
    return n

# Count long words
def count_long_words(tokens: list[str], average_length: float) -> int:
    n = 0
    for word in tokens:
        if len(word) > average_length:
            n += 1
    return n

# Count spelling errors
def count_spelling_errors(tokens: list[str]) -> int:
    n = 0
    for word in tokens:
        if not spellcheck_dict.check(word) and word != "th" and word != "nt":
            n += 1
    return n

# Count unique words
def count_unique_words(tokens: list[str]) -> int:
    unique = []
    for word in tokens:
        word_lower = word.lower()
        if not word_lower in unique:
            unique.append(word_lower)
    return len(unique)

# Count stop words 
def count_stop_words(tokens: list[str]) -> int:
    n = 0
    for word in tokens:
        if word.lower() in stopwords_list:
            n += 1
    return n

# Count speech parts
def count_speech_parts(tokens: list[str]) -> dict[str, int]:
    words = []
    for word in tokens:
        if not word.lower() in stopwords_list:
            words.append(word)
    tags = [tag for w, tag in pos_tag(words)]
    tag_stats = {"nouns": 0, "verbs": 0, "adjectives": 0, "adverbs": 0}
    for tag in tags:
        if tag in noun_tags:
            tag_stats["nouns"] += 1
        elif tag in verb_tags:
            tag_stats["verbs"] += 1
        elif tag in adjective_tags:
            tag_stats["adjectives"] += 1
        elif tag in adverbs_tags:
            tag_stats["adverbs"] += 1
    return tag_stats

# Get sentences
def get_sentences(text: str) -> list[str]:
    return sent_tokenize(text)

# Count sentences
def count_sentences(sentences: list[str]) -> int:
    return len(sentences)

# Calculate average sentence length
def average_sentence_length(sentences: list[str]) -> float:
    avg_len = 0
    for sentence in sentences:
        tokens = word_tokenize(re.sub(tokenize_filter, '', sentence))
        avg_len += len(tokens)
    avg_len /= len(sentences)
    return avg_len

# Count punctuation marks
def count_punctuation_marks(text: str) -> dict[str, int]:
    marks = {"exclamation": 0, "question": 0, "comma": 0}
    for c in text:
        if c == "!":
            marks["exclamation"] += 1
        elif c == "?":
            marks["question"] += 1
        elif c == ",":
            marks["comma"] += 1
    return marks

# Avg syllable count
def average_syllables(text: str, tokens: list[str]) -> float:
    syllable = textstatistics().syllable_count(text)
    return float(syllable) / float(len(tokens))

# Count poly syllable
def count_poly_syllable(tokens: list[str]):
    n = 0
    for word in tokens:
        syllable_count = textstatistics().syllable_count(word)
        if syllable_count >= 3:
            n += 1
    return n

# Flesch readability index
def flesch(avg_sentence_length: float, avg_syllables: float) -> float:
    fre = 206.835 - float(1.015 * avg_sentence_length) - float(84.6 * avg_syllables)
    return fre

# SMOG readability index
def smog(n_sentences: int, n_poly_syllable) -> float:
    if n_sentences >= 3:
        return (1.043 * (30*(n_poly_syllable / n_sentences))**0.5) + 3.1291
    else:
        return 0

# Gunning fog readability index
def gunning_fog(n_difficult: int, tokens: list[str], avg_sentence_length: float) -> float:
    per_diff_words = (n_difficult / len(tokens) * 100) + 5
    grade = 0.4 * (avg_sentence_length + per_diff_words)
    return grade

# Count average word length
print("Counting average word length...")
total_average_word_length = 0
for index, row in df.iterrows():
    text: str = row["text"] #type: ignore
    tokens = tokenize(text)
    total_average_word_length += average_word_length(tokens)
total_average_word_length = total_average_word_length / len(df)

# Generate dataset
data = []
n = 0
print("Generating dataset...")
for index, row in df.iterrows():
    if (n+1) % 1000 == 0:
        print("\tProcessing text {}/{}...".format(n+1, len(df)))
    text: str = row["text"] #type: ignore
    tokens = tokenize(text)
    sentences = get_sentences(text)
    pos = count_speech_parts(tokens)
    punctuation = count_punctuation_marks(text)
    avg_sentence_length = average_sentence_length(sentences)
    avg_syllables = average_syllables(text, tokens)
    n_sentences = count_sentences(sentences)
    n_poly_syllable = count_poly_syllable(tokens)
    n_difficult = count_difficult_words(tokens)
    data.append({
        "id"               : row["id"],
        "chars"            : count_characters(text),
        "words"            : count_words(tokens),
        "4sqrt_words"      : fourth_root_of_word_count(tokens),
        "avg_word_len"     : average_word_length(tokens),
        "words_gr5"        : count_words(tokens, 5),
        "words_gr6"        : count_words(tokens, 6),
        "words_gr7"        : count_words(tokens, 7),
        "words_gr8"        : count_words(tokens, 8),
        "diff_words"       : n_difficult,
        "long_words"       : count_long_words(tokens, total_average_word_length), 
        "spell_err"        : count_spelling_errors(tokens),
        "unique_words"     : count_unique_words(tokens),
        "stop_words"       : count_stop_words(tokens),
        "nouns"            : pos["nouns"],
        "verbs"            : pos["verbs"],
        "adj"              : pos["adjectives"],
        "adv"              : pos["adverbs"],
        "sentences"        : n_sentences,
        "avg_sentence_len" : avg_sentence_length,
        "exclamations"     : punctuation["exclamation"],
        "questions"        : punctuation["question"],
        "commas"           : punctuation["comma"],
        "avg_syllables"    : avg_syllables,
        "poly_syllable"    : n_poly_syllable,
        "flesch"           : flesch(avg_sentence_length, avg_syllables),
        "gunning_fog"      : gunning_fog(n_difficult, tokens, avg_sentence_length),
        "smog"             : smog(n_sentences, n_poly_syllable)
    })
    n += 1

print("Done!")
df_stat = pd.DataFrame(data)
print(df_stat)

print("Saving...")
save_path = "linguistic_features.parquet"
df_stat.to_parquet(save_path)
print("Saved to '{}'.".format(save_path))

