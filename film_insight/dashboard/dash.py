'''
Code contributor: Fuyuki Tani
'''

import sys
from .dash_prep import word_count
from wordcloud import WordCloud
import pathlib
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


### DATA VISUALIZATION FUNCTIONS ###


def plot_wordcloud_db():
    """
    Returns:
        This function creates a word cloud unique to Douban data, and the larger
        the words are, the more prevalent they are in terms on the frequency.
    """

    # Unpacking the tuple from data_viz_prep helper:
    db_count, _ = word_count()

    # Creating the word cloud:
    wordcloud_db = WordCloud(width=1000, height=500, background_color='white').generate_from_frequencies(db_count)
    fig = px.imshow(wordcloud_db, title="Douban Word Cloud")
    fig.update_layout(title_font_size=30, margin=dict(l=0, r=0, t=50, b=0), title=dict(x=0.5, xanchor='center'))

    # Return statement:
    return fig


def plot_wordcloud_rt():
    """
    Returns:
        This function creates a word cloud unique to Rotten Tomatoes, and the larger
        the words are, the more prevalent they are in terms on the frequency.
    """

    # Unpacking the tuple from data_viz_prep helper:
    _ ,rt_count = word_count()

    # Creating the word cloud:
    wordcloud_rt = WordCloud(width=1000, height=500, background_color='white').generate_from_frequencies(rt_count)
    fig = px.imshow(wordcloud_rt, title="Rotten Tomatoes Word Cloud")
    fig.update_layout(title_font_size=30, margin=dict(l=0, r=0, t=50, b=0), title=dict(x=0.5, xanchor='center'))

    # Return statement:
    return fig


### THE SETUP CODE FOR DASHBOARD ###

# Setting data viz function returns as variables

db_wordcloud = plot_wordcloud_db()
rt_wordcloud = plot_wordcloud_rt()


# HTML page setup :) : 
app = Dash(external_stylesheets = [dbc.themes.SIMPLEX])
app.layout = dbc.Container([

    html.Br(),

    dbc.Row(html.H1("Comparison of Movie Reviews"), justify='center'),

    html.Br(),

    dbc.Row([
        dbc.Col(dcc.Graph(id="Douban_wordcloud", figure=db_wordcloud)),
        dbc.Col(dcc.Graph(id="Rotten_tomatoes_wordcloud", figure=rt_wordcloud))
    ]),


    dbc.Row("Sources: Douban and Rotten Tomatoes Websites"),

], fluid=True, style={'text-align': 'center'})

# Main statement below:

if __name__ == '__main__':
    app.run_server(debug = True, host = '0.0.0.0', port = 7997)