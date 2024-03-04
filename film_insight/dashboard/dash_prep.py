'''
Code contributor: Fuyuki Tani
'''
import time
import os
import shutil
import requests
import pathlib
import pandas as pd
from bs4 import BeautifulSoup


def copy_images():
    '''
    This function copies images from the source folder to the destination folder.
    !! Dash requires all images to put in assets folder. Since relative path 
        doesn't work, I made this function.

    Input:
        None
    
    Output:
        None
    '''
    source_folder = pathlib.Path(__file__).parent / '../image'
    destination_folder = pathlib.Path(__file__).parent / 'assets'
    # If the destination folder doesn't exist, create it
    if not destination_folder.exists():
        destination_folder.mkdir(parents=True)

    # Copy all files from the source folder
    for file_name in os.listdir(source_folder):
        source_file = os.path.join(source_folder, file_name)
        destination_file = os.path.join(destination_folder, file_name)
        shutil.copy(source_file, destination_file)




def add_URL_column():
    '''
    This function adds a new 'URL' column to the DataFrame containing URLs.
    
    !! Since movie List from scraping section doesn't include movie url,
        I made this function.
    
    Input:
        None
    
    Output:
        None
    '''
    df_r = pd.read_excel(pathlib.Path(__file__).parent / '../data/rottentomatoes_url.xlsx')
    df_d = pd.read_excel(pathlib.Path(__file__).parent / '../data/douban_url.xlsx')

    print("Please wait while processing...")
    df_r = get_rotten_tomatoes_url(df_r)
    df_d = get_douban_url(df_d)

    df_r.to_excel(pathlib.Path(__file__).parent / '../data/rottentomatoes_url.xlsx', index=False)
    df_d.to_excel(pathlib.Path(__file__).parent / '../data/douban_url.xlsx', index=False)


def get_douban_url(df):
    '''
    This function extracts URLs from the 'url' column in the DataFrame and adds them to a new 'URL' column.
    
    Input:
        df: DataFrame - DataFrame containing URLs
    
    Output:
        df: DataFrame - DataFrame with the 'URL' column added
    '''
    urls = df['url'].astype(str)
    
    urls = urls.str.replace(r'/comments.*', '', regex=True)
    
    df['URL'] = urls
    
    return df


def get_rotten_tomatoes_url(df):
    '''
    This function extracts Rotten Tomatoes URLs for movies from the DataFrame and adds them to a new 'URL' column.
    
    Input:
        df: DataFrame - DataFrame containing movie titles
    
    Output:
        df: DataFrame - DataFrame with the 'URL' column added
    '''
    df['URL'] = ''
    
    for i, row in df.iterrows():
        title = row['Movie Title']
        url = _helper_get_rotten_tomatoes_url(title)
        df.at[i, 'URL'] = url
        time.sleep(3)
    
    return df

def _helper_get_rotten_tomatoes_url(movie_title):
    '''
    This function retrieves the Rotten Tomatoes URL for a given movie title by scraping the Rotten Tomatoes website.
    
    Input:
        movie_title: str - Title of the movie
    
    Output:
        url: str - Rotten Tomatoes URL for the movie
    '''
    # Create the Rotten Tomatoes search URL
    search_url = f"https://www.rottentomatoes.com/search?search={movie_title.replace(' ', '+')}"
    
    # Get the search results page
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    elem = soup.select("#search-results > search-page-result:nth-child(2) > ul > search-page-media-row:nth-child(1) > a:nth-child(2)")
    url = elem[0]['href']
    return url
