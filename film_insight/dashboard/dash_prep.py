'''
Code contributor: Fuyuki Tani
'''

import requests
import pathlib
import pandas as pd
import time
from bs4 import BeautifulSoup
import os
import shutil



# ソースフォルダとデスティネーションフォルダのパスを指定
source_folder = pathlib.Path(__file__).parent / '../image'
destination_folder = pathlib.Path(__file__).parent / 'assets'

def copy_images():
    # もしデスティネーションフォルダが存在しなければ作成
    if not destination_folder.exists():
        destination_folder.mkdir(parents=True)

    # ソースフォルダ内のすべてのファイルをコピー
    for file_name in os.listdir(source_folder):
        source_file = os.path.join(source_folder, file_name)
        destination_file = os.path.join(destination_folder, file_name)
        shutil.copy(source_file, destination_file)




def get_douban_url(df):
    urls = df['url'].astype(str)
    
    urls = urls.str.replace(r'/comments.*', '', regex=True)
    
    df['URL'] = urls
    
    return df


def get_rotten_tomatoes_url(df):
    df['URL'] = ''
    
    for i, row in df.iterrows():
        title = row['Movie Title']
        url = _helper_get_rotten_tomatoes_url(title)
        df.at[i, 'URL'] = url
        time.sleep(1)
    
    return df

def _helper_get_rotten_tomatoes_url(movie_title):
    # Rotten Tomatoes の検索URLを作成
    search_url = f"https://www.rottentomatoes.com/search?search={movie_title.replace(' ', '+')}"
    
    # 検索結果ページを取得
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    elem = soup.select("#search-results > search-page-result:nth-child(2) > ul > search-page-media-row:nth-child(1) > a:nth-child(2)")
    url = elem[0]['href']
    return url
