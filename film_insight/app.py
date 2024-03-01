"""
Code contributor: Everyone
"""
import sys
#from .dashboard import dash

def run_dashboard():
    """
    Running dashboard
    Written by Fuyuki Tani
    """
    pass
    '''
    app = dash.app
    app.run_server(debug=False)
    '''

def run_scrape(): 
    """
    Scrape Web Sites
    Written by:
    """
    return ####

def run_clean():
    """
    Clean datasets
    Written by:  
    """
    return ###


def run():
    """
    User enter an option and interact with the program
    """
    print("Welcome to Cook County Food Accessibility and Security App!")
    user_input = input(
        """Please Enter: 
                (1) The Dashboard, 
                (2) Scrape Data,
                (3) Clean Data
                (4) Quit App.
                Option: """)
    if user_input == "1":
        print("running dashboard...")
        run_dashboard()
    elif user_input == "2":
        print("running data scraping...")
        run_scrape()
    elif user_input == "3":
        print("running data cleaning...")
        run_clean()

    else:
        sys.exit()
