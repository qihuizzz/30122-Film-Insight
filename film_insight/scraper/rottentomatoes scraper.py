import os
import time
import pandas as pd
import requests
import json

# 文件名
output_file = '烂番茄data.xlsx'
data = pd.read_excel("烂番茄url.xlsx")


def get_url_and_save(url, name, time_year, output_file):
    all_data = []  # 此列表用于收集所有评论数据
    # 定义请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    }

    # 发送GET请求
    response = requests.get(url=url, headers=headers)

    # 解析JSON数据
    data = json.loads(response.text)

    # 提取所需数据
    extracted_data = [{
        'name': name,
        'quote': review['quote'],
        'score': review.get('score', 'Not provided'),
        'time': time_year
    } for review in data['reviews']]

    all_data.extend(extracted_data)  # 将提取的数据添加到all_data中

    # 保存数据到Excel文件
    df = pd.DataFrame(all_data)
    if os.path.exists(output_file):
        with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
    else:
        df.to_excel(output_file, index=False)


for index, row in data.iterrows():
    time.sleep(1)
    name = row['Movie Title']
    url = row['url']
    time_year = row['时间']
    get_url_and_save(url, name, time_year, output_file)
