import sys
import pathlib
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from ..sentiment_analysis.sentiment_analysis_test import execute_sentiment_analysis

df_r = pd.read_excel(pathlib.Path(__file__).parent / '../data/rottentomatoes_url.xlsx')
df_d = pd.read_excel(pathlib.Path(__file__).parent / '../data/douban_url.xlsx')

df_rcom = pd.read_excel(pathlib.Path(__file__).parent / '../data/rottentomatoes_data.xlsx')

fig_douban, fig_rotten = execute_sentiment_analysis()

######

# Create a function to generate movie cards
card_style = {'width': '12rem', 'height': '5rem'}

def generate_movie_cards(df):
    '''
    Convert movie list to card style.
    Input: datafile
    Output: 
    '''
    cards = []
    for index, row in df.iterrows():
        card = dbc.Card(
            dbc.CardBody([
                html.H6(html.A(row.iloc[0], href=row.iloc[1], target="_blank"), className="card-title"),
                html.P(f"Year: {row.iloc[2]}", className="card-year"),
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


    # Sentiment Analysis
    dbc.Row(html.H2("Sentiment Analysis"), justify='center', style={'margin-top': '20px'}),
    dbc.Row(html.P("Explain the analysis here.")),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig_douban),
        ], width=6),
        dbc.Col([
            dcc.Graph(figure=fig_rotten),
        ], width=6)
    ], justify='center'),


    # List of Movies from Rotten Tomatoes
    dbc.Row("List of Films from Rotten Tomatoes"),
    dbc.Row(generate_movie_cards(df_r)),

    # List of Movies
    dbc.Row("List of Films from Douban"),
    dbc.Row(generate_movie_cards(df_d)),

    # List 
    dbc.Row("List of Films"),
    dbc.Row([
        dcc.Dropdown(
            id='movie-dropdown',
            options=[{'label': movie, 'value': movie} for movie in df_rcom['Movie Title']],
            value=None,
            placeholder="Select a Movie Title"
        )
    ]),
    dbc.Row("List of Films"),
    dbc.Row(dash_table.DataTable(data=df_rcom.to_dict('records'), page_size=6)),

    html.Br(),

    dbc.Row("Sources: Douban and Rotten Tomatoes Websites"),
    

], fluid=True, style={'text-align': 'center'})


@app.callback(
    Output('datatable-interactivity', 'data'),
    [Input('movie-dropdown', 'value')]
)
def update_table(selected_movie):
    if selected_movie is not None:
        filtered_data = df_rcom[df_rcom['Movie Title'] == selected_movie]
        return filtered_data.to_dict('records')
    else:
        return df_rcom.to_dict('records')

# Main statement to debug:
if __name__ == '__main__':
    app.run_server(debug=True)
