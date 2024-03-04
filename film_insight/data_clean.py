import numpy as np
import jieba
import re
import pandas as pd
import pathlib


douban = pd.read_excel(pathlib.Path(__file__).parent / "data/douban_data.xlsx")
print(douban)
rottentomatoes = pd.read_excel(pathlib.Path(__file__).parent / "data/rottentomatoes_data.xlsx")
print(rottentomatoes)

# rottentomatoes data cleaning
missing_values = rottentomatoes.isnull().sum()
duplicate_rows = rottentomatoes.duplicated().sum()
rottentomatoes = rottentomatoes.drop_duplicates()

print("clean data", rottentomatoes.shape)
# Remove rows where 'content' is missing for Rotten Tomatoes data
rottentomatoes = rottentomatoes[~rottentomatoes["content"].isnull()]

# douban data cleaning
missing_values = douban.isnull().sum()
duplicate_rows = douban.duplicated().sum()
douban = douban.drop_duplicates()
# Remove rows where 'content' is either missing or contains '数据出错' for Douban data
douban = douban[~douban["content"].isnull() & ~douban["content"].str.contains("wrong")]
douban = douban[~douban["score"].isnull() & ~douban["score"].str.contains("score 0")]
print("clean data", douban.shape)


# create a function to remove stopwords
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, encoding="UTF-8").readlines()]
    return stopwords


# douban data cleaning more
list_douban = []


def processing(text, stopwords):
    try:
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\d+", "", text)
        sentence_depart = jieba.cut(text.strip())
        outstr = ""
        for word in sentence_depart:
            if word not in stopwords and word != "\t" and word.strip() != "":
                list_douban.append(word)
                outstr += word + " "
        return outstr.strip()
    except Exception as e:
        print(f"Error processing text: {e}")
        return None


# load stopwords in chinese
stopwords = stopwordslist(pathlib.Path(__file__).parent / "data/china.txt")

douban["content"] = douban["content"].apply(lambda x: processing(x, stopwords))

# remove rows that have missing values
douban.dropna(subset=["content"], inplace=True)
douban.to_excel(pathlib.Path(__file__).parent / "data/douban_clean.xlsx")


# rottentomatoes data cleaning more
list_rottentomatoes = []


def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", text)


def processing_en(text, stopwords):
    try:
        text = remove_emojis(text)
        text = re.sub("[\u4e00-\u9fa5]", "", text)
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\d+", "", text)
        sentence_depart = jieba.cut(text.strip())
        outstr = ""
        for word in sentence_depart:
            if word not in stopwords and word != "\t" and word.strip() != "":
                list_rottentomatoes.append(word)
                outstr += word + " "
        return outstr.strip()
    except Exception as e:
        print(f"Error processing text: {e}")
        return None


# upload stopwords in english
stopwords_en = stopwordslist(pathlib.Path(__file__).parent / "data/english.txt")
rottentomatoes["content"] = rottentomatoes["content"].apply(
    lambda x: processing_en(x, stopwords_en)
)

# remove rows that have missing values
rottentomatoes.dropna(subset=["content"], inplace=True)

rottentomatoes.to_excel(pathlib.Path(__file__).parent / "data/rottentomatoes_clean.xlsx")
