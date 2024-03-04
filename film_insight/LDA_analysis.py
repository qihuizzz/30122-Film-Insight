import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from data_clean import *
import itertools
from gensim import corpora, models


def LDA(data1, data2, data3, data4):
    df = pd.read_excel(data1)
    df["word"] = df["word"].astype(str)
    pos_dict = corpora.Dictionary([[i] for i in df["word"]])
    pos_corpus = [pos_dict.doc2bow(j) for j in [[i] for i in df["word"]]]

    # calculate cosine similarity
    def cos(vector1, vector2):
        dot_product = 0.0
        normA = 0.0
        normB = 0.0
        for a, b in zip(vector1, vector2):
            dot_product += a * b
            normA += a**2
            normB += b**2
        if normA == 0.0 or normB == 0.0:
            return None
        else:
            return dot_product / ((normA * normB) ** 0.5)

    # calculate average cosine similarity
    def lda_k(x_corpus, x_dict):
        mean_similarity = []
        mean_similarity.append(1)

        for i in np.arange(2, 11):
            lda = models.LdaModel(x_corpus, num_topics=i, id2word=x_dict)
            term = lda.show_topics(num_words=50)

            # extract top words for each topic
            top_word = []
            for k in range(i):
                top_word.append(
                    [
                        "".join(re.findall('"(.*)"', item))
                        for item in term[k][1].split("+")
                    ]
                )

            # construct a matrix for each topic
            unique_word = set(sum(top_word, []))
            mat = []
            for words in top_word:
                mat.append(tuple([words.count(k) for k in unique_word]))

            # calculate cosine similarity
            p = list(itertools.permutations(range(i), 2))
            top_similarity = [
                cos(mat[pair[0]], mat[pair[1]])
                for pair in p
                if cos(mat[pair[0]], mat[pair[1]]) is not None
            ]
            mean_similarity.append(
                sum(top_similarity) / len(top_similarity) if top_similarity else 0
            )

        return mean_similarity

    # calculate average cosine similarity
    pos_k = lda_k(pos_corpus, pos_dict)

    # plot the average cosine similarity
    plt.figure(figsize=(10, 8))
    plt.plot(pos_k)
    plt.xlabel(data2)
    plt.ylabel("average cosine similarity")
    plt.title("LDA analysis")
    plt.savefig(data3)
    print(f"{data2} Successfully saved")
    plt.show()

    # LDA analysis
    pos_lda = models.LdaModel(pos_corpus, num_topics=data4, id2word=pos_dict)
    print(pos_lda.print_topics(num_words=30))
    print("=" * 30)


LDA("data/douban_word.xlsx", "douban", "image/douban_LDA", 3)
LDA("data/rottentomatoes_word.xlsx", "rottentomatoes", "image/rottentomatoes_LDA", 2)
