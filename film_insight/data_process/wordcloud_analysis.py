import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from data_clean import list_douban, list_rottentomatoes
from wordcloud import WordCloud


# douban word cloud
# remove empty strings and None values using list comprehension
cleaned_list = [item for item in list_douban if item not in ["", None, " "]]
# transform the list into a DataFrame
df_cleaned = pd.DataFrame(cleaned_list, columns=["word"])
# save the DataFrame to an Excel file
output_file_path = "data/douban_word.xlsx"
df_cleaned.to_excel(output_file_path, index=False)
print(f"clean list {output_file_path}")


# rottentomatoes word cloud
# remove empty strings and None values using list comprehension
cleaned_list = [item for item in list_rottentomatoes if item not in ["", None, " "]]
# transform the list into a DataFrame
df_cleaned = pd.DataFrame(cleaned_list, columns=["word"])
# save the DataFrame to an Excel file
output_file_path = "data/rottentomatoes_word.xlsx"  # 您可以自定义文件名和路径
df_cleaned.to_excel(output_file_path, index=False)
print(f"clean list {output_file_path}")


def word_png(data1, data2):
    # calculate word frequency
    word_freq = Counter(data1[30:])
    # specify the font path for Chinese support
    font_path = "C:\\Windows\\Fonts\\SimHei.ttf"
    # set word cloud parameters
    wordcloud = WordCloud(
        width=500, height=500, background_color="white", font_path=font_path
    ).generate_from_frequencies(word_freq)
    # draw the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(data2, dpi=300)
    plt.show()


# save the word cloud
word_png(list_douban[30:], "image/douban_word.jpg")
word_png(list_rottentomatoes[30:], "image/rottentomatoes_word.jpg")
