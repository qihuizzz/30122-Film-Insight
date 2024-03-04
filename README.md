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
    (4) Plot Graphs from Data  
    (5) Quit App  

## 1: Data Visualization

If you just want to see the dashboard, press 1.  
This will open a port, and you will be able to see plots and data below:

1. Two word clouds, one with Douban data, and one with Rotten Tomatoes data. 
2. Two LDA analysis, one with Douban data, and one with Rotten Tomatoes data. 
3. Two Sentiment Analysis, one with Douban data, and one with Rotten Tomatoes data. 
4. Two Time Lines, one with Douban data, and one with Rotten Tomatoes data.
5. Movie List we deal with. It includes the link to each sites.
6. Sample movie reviews we scrape and analyse. You can filter by movie titile.

## 2: Gathering Data

If you want to scrape the latest data, press 2.  
In order to analyze the movie reviews, they have to be collected using web scraping from bean boards and rotten tomatoes. The web scraping process can take several minutes, so we have stored the files in the ``data'' directory.

## 3: Clean Data

If you want to clean the scraped data, press 3.  
This process can be skipped because we have stored the data that has already been cleaned.

## 4: Plot Graphs from Data

If you want to plot graphs, press 4.  
However, the graphs created are only saved in a folder. To view the graph, select 1. As usual, graphs have already been plotted and saved.
