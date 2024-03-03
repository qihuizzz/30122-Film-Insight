import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jieba
import re
from collections import Counter
from data_clean import *


# 豆瓣词云
# 使用列表推导式去除空字符串和None值
cleaned_list = [item for item in list_douban if item not in ["", None, " "]]
# 将列表转换为DataFrame
df_cleaned = pd.DataFrame(cleaned_list, columns=["word"])
# 保存DataFrame到Excel文件
output_file_path = "data/douban_word.xlsx"  # 您可以自定义文件名和路径
df_cleaned.to_excel(output_file_path, index=False)
print(f"clean list {output_file_path}")

# 烂番茄词云
import pandas as pd

# 使用列表推导式去除空字符串和None值
cleaned_list = [item for item in list_rottentomatoes if item not in ["", None, " "]]
# 将列表转换为DataFrame
df_cleaned = pd.DataFrame(cleaned_list, columns=["word"])
# 保存DataFrame到Excel文件
output_file_path = "data/rottentomatoes_word.xlsx"  # 您可以自定义文件名和路径
df_cleaned.to_excel(output_file_path, index=False)
print(f"clean list {output_file_path}")

from wordcloud import WordCloud


def word_png(data1, data2):
    # 计算词频
    word_freq = Counter(data1[30:])
    # 指定中文支持的字体路径，这里以微软雅黑为例，您需要根据自己的情况调整
    font_path = "C:\\Windows\\Fonts\\SimHei.ttf"  # 这个路径需要根据您的系统和字体实际安装位置进行修改
    # 设置词云参数，包括中文支持的字体
    wordcloud = WordCloud(
        width=500, height=500, background_color="white", font_path=font_path
    ).generate_from_frequencies(word_freq)
    # 使用matplotlib绘制词云图
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")  # 不显示坐标轴
    plt.savefig(data2, dpi=300)
    plt.show()


# 词云图保存
word_png(list_douban[30:], "image/douban_word.jpg")
word_png(list_rottentomatoes[30:], "image/rottentomatoes_word.jpg")

# 可视化
# 分类电影到不同的时间段
rottentomatoes["time_period"] = pd.cut(
    rottentomatoes["year"],
    bins=[1999, 2010, 2020, 2024],
    labels=["2000-2010", "2010-2020", "2020-2024"],
)
# 统计每个时间段的评分分布
# 由于烂番茄评分是连续的，我们可以先将评分四舍五入到最近的整数以简化分布
rottentomatoes["rounded_score"] = rottentomatoes["rating"].round()
rating_distribution = (
    rottentomatoes.groupby(["time_period", "rounded_score"], observed=True)
    .size()
    .unstack(fill_value=0)
)
# 计算每个时间段的平均评分
average_rating_per_period = rottentomatoes.groupby("time_period", observed=True)[
    "rating"
].mean()

# 可视化
fig, ax1 = plt.subplots(figsize=(12, 8))
# 柱形图：不同评分的电影数量
colors = ["lightblue", "skyblue", "blue"]  # 定义颜色渐变
rating_distribution.plot(kind="bar", ax=ax1, width=0.8, color=colors, alpha=0.7)
ax1.set_xlabel("Time Period")
ax1.set_ylabel("Number of Ratings", color="b")
ax1.tick_params(axis="y", labelcolor="b")
ax1.set_title("Rottentomatoes Rating Distribution and Average Rating by Time Period")

# 折线图：各时间段的平均评分
ax2 = ax1.twinx()
average_rating_per_period.plot(
    kind="line",
    ax=ax2,
    marker="o",
    color="darkblue",
    linewidth=2,
    markersize=8,
    label="Average Rating",
)
ax2.set_ylabel("Average Rating", color="r")
ax2.tick_params(axis="y", labelcolor="r")
# 图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc="upper left")
plt.savefig("image/Rottentomatoes_time.jpg")

# 数据预处理
# 转换评分为数值
rating_conversion = {"力荐": 5, "推荐": 4, "还行": 3, "较差": 2, "很差": 1}
douban["numeric_rating"] = douban["score"].map(rating_conversion)
# 分类电影到不同的时间段
douban["time_period"] = pd.cut(
    douban["year"],
    bins=[1999, 2010, 2020, 2024],
    labels=["2000-2010", "2010-2020", "2020-2024"],
)
# 统计每个时间段的评分分布
rating_distribution = (
    douban.groupby(["time_period", "numeric_rating"], observed=True)
    .size()
    .unstack(fill_value=0)
)
# 计算每个时间段的平均评分
average_rating_per_period = douban.groupby("time_period", observed=True)[
    "numeric_rating"
].mean()
# 可视化
fig2, ax1 = plt.subplots(figsize=(12, 8))

# 柱形图：不同评分的电影数量
colors = ["lightgreen", "mediumseagreen", "green"]  # 定义颜色渐变
rating_distribution.plot(kind="bar", ax=ax1, width=0.8, color=colors, alpha=0.7)
ax1.set_xlabel("Time Period")
ax1.set_ylabel("Number of Ratings", color="g")
ax1.tick_params(axis="y", labelcolor="g")
ax1.set_title("Douban Rating Distribution and Average Rating by Time Period")

# 折线图：各时间段的平均评分
ax2 = ax1.twinx()
average_rating_per_period.plot(
    kind="line",
    ax=ax2,
    marker="o",
    color="darkgreen",
    linewidth=2,
    markersize=8,
    label="Average Rating",
)
ax2.set_ylabel("Average Rating", color="r")
ax2.tick_params(axis="y", labelcolor="r")

# 图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc="upper left")
plt.savefig("image/Douban_time.jpg")
plt.show()  # 显示图表

# LDA模型
import itertools
from gensim import corpora, models


def LDA(data1, data2, data3, data4):
    # 建立词典
    # 确保所有分词都是字符串类型
    df = pd.read_excel(data1)
    df["word"] = df["word"].astype(str)
    # 之后建立词典
    pos_dict = corpora.Dictionary([[i] for i in df["word"]])

    pos_corpus = [pos_dict.doc2bow(j) for j in [[i] for i in df["word"]]]

    # 主题数寻优函数
    def cos(vector1, vector2):  # 余弦相似度函数
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

    # 主题数寻优
    def lda_k(x_corpus, x_dict):
        mean_similarity = []
        mean_similarity.append(1)  # 初始相似度设置为1

        for i in np.arange(2, 11):  # 主题数从2到10
            lda = models.LdaModel(x_corpus, num_topics=i, id2word=x_dict)
            term = lda.show_topics(num_words=50)

            # 提取各主题词
            top_word = []
            for k in range(i):
                top_word.append(
                    [
                        "".join(re.findall('"(.*)"', item))
                        for item in term[k][1].split("+")
                    ]
                )

            # 构造词频向量
            unique_word = set(sum(top_word, []))
            mat = []
            for words in top_word:
                mat.append(tuple([words.count(k) for k in unique_word]))

            # 计算所有主题对的平均余弦相似度
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

    # 计算主题平均余弦相似度
    pos_k = lda_k(pos_corpus, pos_dict)

    # 绘制主题平均余弦相似度图形
    plt.figure(figsize=(10, 8))  # 设置画布大小
    plt.plot(pos_k)  # 绘制曲线
    plt.xlabel(data2)  # 设置x轴标签
    plt.ylabel("average cosine similarity")  # 设置y轴标签
    plt.title("LDA analysis")  # 设置图表标题
    plt.savefig(data3)  # 保存图表
    print(f"{data2} Successfully saved")
    plt.show()  # 显示图表

    # LDA主题分析
    pos_lda = models.LdaModel(pos_corpus, num_topics=data4, id2word=pos_dict)
    print(pos_lda.print_topics(num_words=30))
    print("=" * 30)


LDA("data/douban_word.xlsx", "douban", "image/douban_LDA", 3)
LDA("data/rottentomatoes_word.xlsx", "rottentomatoes", "image/rottentomatoes_LDA", 2)
