'''
Code contributor: Fuyuki Tani
'''

import sys
import pathlib
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from ..sentiment_analysis.sentiment_analysis_test import execute_sentiment_analysis



df = pd.read_excel(pathlib.Path(__file__).parent / '../data/rottentomatoes_url.xlsx')


### test area ###
fig_douban, fig_rotten = execute_sentiment_analysis()



######

# Create a function to generate movie cards
card_style = {'width': '15rem', 'height': '5rem'}

def generate_movie_cards(df):
    cards = []
    for index, row in df.iterrows():
        card = dbc.Card(
            dbc.CardBody([
                html.H5(html.A(row['Movie Title'], href=row['url'], target="_blank"), className="card-title"),
                html.H6(f"Year: {row['year']}", className="card-year"),
            ]),
            style=card_style,
            className="mb-3",
        )
        cards.append(card)
    return cards




### THE SETUP CODE FOR DASHBOARD ###

# HTML page setup :) : 
app = Dash(external_stylesheets=[dbc.themes.PULSE])

LDA_d = "assets/douban_LDA.jpg"
LDA_r = "assets/rottentomatoes_LDA.jpg"


app.layout = dbc.Container([

    html.Br(),

    dbc.Row(html.H1("Comparison of Movie Reviews"), justify='center'),

    dbc.Row("List of Films"),
    dbc.Row(dash_table.DataTable(data=df.to_dict('records'), page_size=6)),

    dbc.Row("List of Films"),
    dbc.Row(generate_movie_cards(df)),

    # LDA
    dbc.Row(html.H2("LDA Analysis"), justify='center', style={'margin-top': '20px'}),
    dbc.Row(html.P("Explain the analysis here.")),

    dbc.Row([
        dbc.Col([
            html.H3("Douban LDA"),
            html.P("This image shows Douban LDA."),
            html.Img(src=LDA_d, style={'width': '100%', 'height': 'auto'}),
        ], width=6),
        dbc.Col([
            html.H3("Rotten Tomatoes LDA"),
            html.P("This image shows Rotten Tomatoes LDA."),
            html.Img(src=LDA_r, style={'width': '100%', 'height': 'auto'}),
        ], width=6)
    ], justify='center'),


    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig_douban),
        ], width=6),
        dbc.Col([
            dcc.Graph(figure=fig_rotten),
        ], width=6)
    ], justify='center'),

    html.Br(),

    dbc.Row("Sources: Douban and Rotten Tomatoes Websites"),
    

], fluid=True, style={'text-align': 'center'})



# Main statement to debug:
if __name__ == '__main__':
    app.run_server(debug = True)