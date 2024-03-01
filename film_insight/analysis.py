import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

douban = pd.read_excel("data/douban_data.xlsx")
print(douban)
rottentomatoes = pd.read_excel("data/rottentomatoes_data.xlsx")
print(rottentomatoes)

# 烂番茄数据清洗
missing_values = rottentomatoes.isnull().sum()
duplicate_rows = rottentomatoes.duplicated().sum()
rottentomatoes = rottentomatoes.drop_duplicates()

print("clean data", rottentomatoes.shape)
# Remove rows where 'content' is missing for Rotten Tomatoes data
rottentomatoes = rottentomatoes[~rottentomatoes["content"].isnull()]

# 豆瓣数据清洗
missing_values = douban.isnull().sum()
duplicate_rows = douban.duplicated().sum()
douban = douban.drop_duplicates()
# Remove rows where 'content' is either missing or contains '数据出错' for Douban data
douban = douban[~douban["content"].isnull() & ~douban["content"].str.contains("wrong")]
douban = douban[~douban["score"].isnull() & ~douban["score"].str.contains("score 0")]
print("clean data", douban.shape)


import jieba
import re
import pandas as pd
from collections import Counter


# 创建停用词列表
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, encoding="UTF-8").readlines()]
    return stopwords


list_douban = []


# 豆瓣清洗
def processing(text, stopwords):
    try:
        # 更新正则表达式以去除所有标点符号和数字
        text = re.sub(r"[^\w\s]", "", text)  # 去除所有标点符号
        text = re.sub(r"\d+", "", text)  # 去除所有数字
        sentence_depart = jieba.cut(text.strip())
        outstr = ""
        for word in sentence_depart:
            if word not in stopwords and word != "\t" and word.strip() != "":
                list_douban.append(word)
                outstr += word + " "
        return outstr.strip()
    except Exception as e:
        print(f"Error processing text: {e}")  # 打印错误信息
        return None


# 加载停用词
stopwords = stopwordslist("data/china.txt")  # 修改为您的停用词文件路径

douban["content"] = douban["content"].apply(lambda x: processing(x, stopwords))
# 删除处理过程中出错的行
douban.dropna(subset=["content"], inplace=True)
douban.to_excel("data/douban_clean.xlsx")

# 烂番茄清洗
import jieba
import re
from collections import Counter

list_lanfanqie = []


# 去除表情符号的函数
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


# 数据清洗和分词处理函数
def processing_en(text, stopwords):
    try:
        text = remove_emojis(text)  # 先去除表情符号
        text = re.sub("[\u4e00-\u9fa5]", "", text)  # 清除所有中文字符
        # 更新正则表达式以去除所有标点符号和数字
        text = re.sub(r"[^\w\s]", "", text)  # 去除所有标点符号
        text = re.sub(r"\d+", "", text)  # 去除所有数字
        sentence_depart = jieba.cut(text.strip())
        outstr = ""
        for word in sentence_depart:
            if word not in stopwords and word != "\t" and word.strip() != "":
                list_lanfanqie.append(word)
                outstr += word + " "
        return outstr.strip()
    except Exception as e:
        print(f"Error processing text: {e}")  # 打印错误信息
        return None


# 加载停用词
stopwords_en = stopwordslist("data/english.txt")  # 修改为您的停用词文件路径
rottentomatoes["content"] = rottentomatoes["content"].apply(
    lambda x: processing_en(x, stopwords_en)
)
# 删除处理过程中出错的行
rottentomatoes.dropna(subset=["content"], inplace=True)

rottentomatoes.to_excel("data/rottentomatoes_clean.xlsx")
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
cleaned_list = [item for item in list_lanfanqie if item not in ["", None, " "]]
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
word_png(list_lanfanqie[30:], "image/rottentomatoes_word.jpg")

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
ax1.set_title("Rating Distribution and Average Rating by Time Period")

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
plt.savefig("image/douban_time.jpg")

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
ax1.set_title("Rating Distribution and Average Rating by Time Period")

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
plt.savefig("image/rottentomatoes_time.jpg")

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

    # 主题数寻优
    # 构造主题数寻优函数
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
        # 初始化平均余弦相似度
        mean_similarity = []
        mean_similarity.append(1)

        # 循环生成主题并计算主题间相似度
        for i in np.arange(2, 11):
            lda = models.LdaModel(x_corpus, num_topics=i, id2word=x_dict)  # LDA模型训练
            for j in np.arange(i):
                term = lda.show_topics(num_words=50)
            # 提取各主题词
            top_word = []
            for k in np.arange(i):
                top_word.append(
                    ["".join(re.findall('"(.*)"', i)) for i in term[k][1].split("+")]
                )  # 列出所有词
            # 构造词频向量
            word = sum(top_word, [])  # 列出所有的词
            unique_word = set(word)  # 去除重复的词
            # 构造主题词列表，行表示主题号，列表示各主题词
            mat = []
            for j in np.arange(i):
                top_w = top_word[j]
                mat.append(tuple([top_w.count(k) for k in unique_word]))
            p = list(itertools.permutations(list(np.arange(i)), 2))
            l = len(p)
            top_similarity = [0]
            for w in np.arange(l):
                vector1 = mat[p[w][0]]
                vector2 = mat[p[w][1]]
                top_similarity.append(cos(vector1, vector2))
            # 计算平均余弦相似度
            mean_similarity.append(sum(top_similarity) / l)
        return mean_similarity

    # 计算主题平均余弦相似度
    pos_k = lda_k(pos_corpus, pos_dict)

    # 绘制主题平均余弦相似度图形
    from matplotlib.font_manager import FontProperties

    font = FontProperties(size=14)
    # 解决中文显示问题
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    # 创建图片
    fig = plt.figure(figsize=(10, 8))
    ax1.plot(pos_k)
    ax1.set_xlabel(data2, fontproperties=font)
    plt.savefig(data3)
    print(data2, "Successfully saved")
    plt.show()

    # LDA主题分析
    pos_lda = models.LdaModel(pos_corpus, num_topics=data4, id2word=pos_dict)
    print(pos_lda.print_topics(num_words=30))
    print("=" * 30)


LDA("data/douban_word.xlsx", "douban", "image/douban_LDA", 2)
LDA("data/rottentomatoes_word.xlsx", "rottentomatoes", "image/rottentomatoes_LDA", 3)
