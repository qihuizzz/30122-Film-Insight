import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import csv
import time
import re
import os
data = pd.read_excel("data/douban_url.xlsx")
print(data)

def get_url_and_save(url, name, date, output_file):
    # 加入请求头 加入Cookies 反爬手段
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
        "Cookie": 'douban-fav-remind=1; _vwo_uuid_v2=DEFE3CD29792EFE4E5D82AC567627C1BD|73f48a17f7f18e4a1c6ac8c0609a6f21; _vwo_uuid_v2=DEFE3CD29792EFE4E5D82AC567627C1BD|73f48a17f7f18e4a1c6ac8c0609a6f21; gr_user_id=544773db-6c63-473e-9fdd-19702520fc91; viewed="25743117_2644463"; ll="118304"; bid=y3EVXFLg61A; __gads=ID=c139cfda725c6324-2248938f51cf0075:T=1638456926:RT=1638456926:S=ALNI_MbwKj_ntn1NP377bYUdN3HdGPzH5g; __utmz=30149280.1640533899.32.26.utmcsr=so.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; __utmz=223695111.1640533995.12.8.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __yadk_uid=4oy5FCmkqJAR9rAmNboSpb4c7fACbc9N; dbcl2="250810982:4DkSj8RLP7w"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.25081; ck=8HEs; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1640615221%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.1971731490.1571369978.1640533899.1640615221.33; __utmc=30149280; __utma=223695111.1748498060.1604721525.1640533995.1640615221.13; __utmb=223695111.0.10.1640615221; __utmc=223695111; ap_v=0,6.0; _pk_id.100001.4cf6=781111bba4703c8b.1604721525.13.1640616409.1640539932.; __utmt=1; __utmb=30149280.2.10.1640615221'
    }
    all_data = []

    for page in range(2):  # 处理第一页和第二页
        if page > 0:
            current_start = int(re.search(r"start=(\d+)", url).group(1))
            next_start = current_start + 20
            url = re.sub(r"start=\d+", f"start={next_start}", url)

        request = urllib.request.Request(url=url, headers=headers)
        html = urllib.request.urlopen(request).read().decode("UTF-8")
        soup = BeautifulSoup(html, 'lxml')
        items = soup.select('div.comment-item')

        for i in items:
            try:
                data_text = {
                    'name': name,
                    'year': date,
                    'score': i.select("span.rating")[0].get("title"),  # 获取属性

                    'content': i.select("span.short")[0].get_text().replace("\n", '')  # 获取内容
                }
                all_data.append(data_text)
            except Exception as e:
                data_text = {
                    'name': name,
                    'year': date,
                    'score': 'score 0',  # 获取属性

                    'content': 'wrong'
                }
                all_data.append(data_text)
    print(all_data)
    # 保存数据到Excel文件
    # df = pd.DataFrame(all_data)
    # if os.path.exists(output_file):
    #     with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
    #         df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
    # else:
    #     df.to_excel(output_file, index=False)

# 文件名
output_file = 'data/douban_data.xlsx'

# 遍历Excel文件中的每一行，对每个URL执行get_url_and_save函数
for index, row in data.iterrows():
    time.sleep(1)
    name = row['name']
    url = row['url']
    date = row['year']
    get_url_and_save(url, name, date, output_file)
    print(url,'end','-'*30)
