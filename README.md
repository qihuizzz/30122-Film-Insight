<h1>Film Insight</h1>

[Write Description here.]


## Getting Started

1. Clone this repository.
2. From the root directory, ``30122-Film-Insight``, run ``poetry install``.
3. Run ``poetry shell``.
4. Run ``poetry run python -m film_insight``.
- You can choose:  
    (1) The Dashboard  
    (2) Scrape Data  
    (3) Clean Data
    (4) Plot from Data
    (5) Quit App  

## 1: Data Visualization

If you want to skip data scraping/cleaning and just visualize the analyzed data, please type 1.
This will open a port (7997) on the Flask app, and you will be able to see three plots:

1. Two word clouds, one with Douban data, and one with Rotten Tomatoes data. 
2. ***
3. ***

## 2: Gathering Data

If you want to scrape the latest data, please type 2.
In order to analyze the movie reviews, they need to be collected using web scraping from bean boards and rotten tomatoes. Web scraping process can take several minutes to run, so we have saved the json files down in the ``data`` directory. 

## 3: Clean Data

To transform the raw data scraped from both web sites into a useable cleaned format, please type 3.
This creates two respective data file of cleaned data for each web sites in the the data folder in film-insights folder.

## 4: Plot from Data

[Explain Here]
