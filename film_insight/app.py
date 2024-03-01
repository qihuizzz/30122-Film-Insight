"""
Code contributor: Everyone
"""
import sys
#from .dashboard import dash
#from import xxxx

def run_dashboard():
    """
    Running dashboard
    Written by Fuyuki Tani
    """
    pass
    '''
    dash.run_server(debug=False)
    '''

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
    pass


def run():
    """
    User enter an option and interact with the program
    """
    print("This is Film Insiht. How May I help you?")
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
