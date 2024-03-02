'''
Code contributor: Fuyuki Tani
'''

import sys
import pathlib
import pandas as pd
import numpy as np
from collections import Counter

# These functions below take in the csvs that are the csvs that are created
# from "preprocess", and format the csvs so that they're fit to use as Pandas
# data structures in the file "__main__.py" for data visulization. 

# Loading in the data and setting them as global dataframe variables:
db_data = pathlib.Path(__file__).parent / "../data/douban_clean.xlsx"
rt_data = pathlib.Path(__file__).parent / "../data/rottentomatoes_clean.xlsx"

df_db = pd.read_excel(db_data)
df_rt = pd.read_excel(rt_data)


### BELOW ARE THE HELPER FUNCTIONS THAT WILL BE USED FOR DATA VISUALIZATION ###


def word_count():
    """
    Returns:
        This returns the db & rt dataframes it as a Pandas series. We have to
        parse through the dataframe in order to count the salient words and
        count the terms. Lastly, it's called when creating the wordcloud 
        visualizations. 
    """

    # Initializing lists to create Pandas dataframes:
    db_count = []
    rt_count = []

    # Parsing through the dataframes:
    for val in df_db.clean_text.values:
        db_count += eval(val)

    for val in df_rt.clean_text.values:
        rt_count += eval(val)

    # Converting the lists to a series, and saving it to a variable:
    db_count = pd.Series(Counter(db_count)).sort_values(ascending = False)
    rt_count = pd.Series(Counter(rt_count)).sort_values(ascending = False)

    # Return statement:
    return db_count, rt_count

