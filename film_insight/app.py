"""
Code contributor: Fuyuki Tani

This code is inspired by cappyfoodies project.
url:https://github.com/uchicago-2023-capp30122/30122-project-cappyfoodies/tree/main
"""

import sys
from .dashboard import dash_main


def run_dashboard():
    """
    Running dashboard
    Written by Fuyuki Tani
    """
    dash_main.app.run_server(debug=False)


def run_scrape(): 
    """
    Scrape Web Sites
    Written by:
    """
    pass    

def run_clean():
    """
    Clean datasets
    Written by:  
    """
    from film_insight import data_clean


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
                (4) Quit
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
    else:
        sys.exit()
