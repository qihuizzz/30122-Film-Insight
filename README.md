<h1>Film Insight</h1>

[Write Description here.]



# The below is under construction.

## Getting Started with the Virtual Environment

1. Clone this repository.
2. From the root directory, ``30122-Film-Insight``, run ``poetry install``.
3. Run ``poetry shell``.

## Part 1: Gathering the Data

In order to analyze the movie reviews, they need to be collected using web scraping from bean boards and rotten tomatoes. Web scraping process can take several minutes to run, so we have saved the json files down in the ``data`` directory. 

If you would like to run the scraper yourself, the code for completeing this can be found in each source's respective directory: ``*****.py``, and each of these sources can be scraped individually in the interpreter by running the following:

``$ python3 -m film-insight.scrape``



## Part 2: Token and Sentiment Analysis

To transform the raw data scraped from both web sites into a useable cleaned format run the following:

``$ python3 **.py **.json``


``$ python3 **.py **json``

This creates two respective dataframes of cleaned data for each news source in the the data folder in film-insights folder.

## Part 3: Data Visualization

To visualize the analyzed data, please run the following command:

``$ python3 -m film-insight.dashboard.dash``

This will open a port (7997) on the Flask app, and you will be able to see three plots:

1. Two word clouds, one with Douban data, and one with Rotten Tomatoes data. 
2. ***
3. ***