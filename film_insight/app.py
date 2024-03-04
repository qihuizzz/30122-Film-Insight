"""
Code contributor: Fuyuki Tani

This code is inspired by cappyfoodies project.
url:https://github.com/uchicago-2023-capp30122/30122-project-cappyfoodies/tree/main
"""

import sys
from .dashboard import dash_main
from .dashboard import dash_prep

def run_dashboard():
    """
    Running dashboard
    Written by Fuyuki Tani
    """
    dash_prep.copy_images()
    dash_main.app.run_server(debug=False)


def run_scrape(): 
    """
    Scrape Web Sites
    """
    from film_insight.data_scraper import rottentomatoes_scraper
    from film_insight.data_scraper import douban_scraper


def run_clean():
    """
    Clean Data
    """
    from film_insight.data_process import data_clean
    dash_prep.add_URL_column()


def run_plot():
    """
    Plot graphs from Data
    """
    from film_insight.data_process import wordcloud_analysis, sentiment_analysis, graph_analysis, LDA_analysis



def run():
    """
    Allows the user to interact with the program by selecting options.
    """
    print("Welcome to Film Insiht! How may I help you?")
    user_input = input(
        """Please select an option:
                (1) Launch Dashboard
                (2) Scrape Data
                (3) Clean Data
                (4) Plot Graphs from Data
                (5) Quit
                Option: """)
    if user_input == "1":
        print("Launching Dashboard...")
        run_dashboard()
    elif user_input == "2":
        print("Scraping Data...")
        run_scrape()
    elif user_input == "3":
        print("Cleaning Data...")
        run_clean()
    elif user_input == "4":
        print("Plotting graphs...")
        run_plot()
    else:
        sys.exit()
