<h1>Film Insight</h1>

This project focuses on the analysis of Chinese and American movie reviews. We extracted information such as movie names, ratings, release years, and reviews of war movies from China's Douban and the United States' Rotten Tomatoes websites. Our analysis covers four aspects to examine the differing reactions to war movies between China and the U.S.

Firstly, we clean the data to remove characters that could interfere with the analysis. Then, we conduct sentiment analysis on the reviews and compare the sentiment scores with the actual ratings on the websites to assess the authenticity and effectiveness of the ratings. Next, we analyze the reviews of Chinese and American movies using word cloud visuals. Furthermore, we divide the timeline into three periods to compare the ratings of movies from different times between China and the U.S. Lastly, we perform LDA (Latent Dirichlet Allocation) topic analysis on the reviews and calculate the number of topic words for different websites using the average cosine rate.

Given the linguistic differences between Chinese and English, we processed the data separately but aimed to present our findings in a directly comparable manner, highlighting the nuanced perceptions of war movies across cultures.


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
