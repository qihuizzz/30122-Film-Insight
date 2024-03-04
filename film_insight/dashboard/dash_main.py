'''
Code contributor: Fuyuki Tani

Text part: written by Zirong Li
'''

import pathlib
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd


##### TEXT PART #####

note_WC_R = '''The word cloud from Rotten Tomatoes showcases the key elements viewers focus on in war movies, highlighting "War," "Scenes," "Story," and "Soldiers" as central discussion points. It reflects an audience interest in narrative depth, historical accuracy, and the quality of performances, with specific attention to how significant historical events like World War II are portrayed. This analysis suggests that viewers value emotionally impactful and artistically successful films, often recommending those that leave a lasting impression.'''
note_WC_D = '''This Chinese word cloud from Douban reflects the multifaceted discussions surrounding war movies, highlighting not only the thematic and artistic elements like "war," "director," "plot," and "actors" but also the deeper exploration into "history," "human nature," and "society." The presence of terms such as "touching," "real," and "thought-provoking" showcases the audience's emotional engagement and intellectual response to these films. This analysis indicates that Douban users value both the technical execution and the emotional depth of war movies, alongside their historical and social relevance.'''

note_LDA = '''The LDA analysis process involves reading pre-processed text data where movie reviews have been split into individual words. A dictionary is created with a unique ID for each word using corpora.Dictionary. Each word is then transformed into a bag-of-words model using doc2bow, creating vectors of word occurrences. The LdaModel from Gensim is trained on this data, testing topic numbers from 2 to 10 to find an optimal count. The differentiation between topics is measured using cosine similarity, with lower values indicating clearer distinction. Based on this metric, 3 topics for Douban and 2 for Rotten Tomatoes were selected. Finally, the model outputs the top 30 weighted keywords for each topic, which helps in understanding the distinct thematic structures within the movie reviews.'''
note_LDA_R = '''The graph depicts the relationship between the number of topics in a Rotten Tomatoes LDA topic model and the average cosine similarity between the topics. With only one topic, the similarity is naturally at its maximum of 1. As the number of topics increases to two, there is a sharp decline in average cosine similarity, indicating distinct separation between the topics. Adding more topics beyond this point does not significantly change the similarity, which suggests that a small number of topics are sufficient for clear differentiation in the dataset. This optimal number of topics provides a balance between specificity and manageability in the model.'''
note_LDA_D = '''The graph of LDA analysis on the Douban dataset illustrates that as the number of topics increases from 1 to 2, there's a significant drop in the average cosine similarity, indicating enhanced topic differentiation. Beyond 2 topics, the average cosine similarity approaches zero, suggesting that additional topics do not substantially increase differentiation. This implies that a topic count of 2-3 is optimal for capturing the main themes within the dataset, as further increase in topics doesn't significantly improve topic differentiation.'''

note_SA = '''First, the process involves using jieba for Chinese word segmentation, followed by data cleaning with a custom list of stop words. Then, text is converted into vector form using CountVectorizer to fit the model. To address the issue of data imbalance, the SMOTE algorithm is employed to generate samples for the minority class. Subsequently, a Multinomial Naive Bayes model is trained for sentiment classification. The model's performance is evaluated by generating a confusion matrix, which is then visualized as a heatmap to clearly display the accuracy and misclassification of classification results. This entire process includes data preprocessing and vectorization, model training, evaluation, and result visualization, offering a comprehensive solution for sentiment analysis of Chinese text.'''
note_SA_R = '''The provided Confusion Matrix for Douban Sentiment Analysis illustrates that the sentiment analysis model accurately categorizes the majority of reviews across various sentiment classes, with particularly high accuracy for extreme sentiments such as "Highly Recommended" and "Very Poor." There is some misclassification between adjacent categories, suggesting the model's challenges in distinguishing nuanced differences in sentiment. Overall, the high diagonal values indicate effective model performance, but there is room for improvement in differentiating between middle-range sentiments like "Fair" or "Recommended."'''
note_SA_D = '''The confusion matrix for beanstalk sentiment analysis demonstrates high accuracy in categorizing comments across various sentiment levels, with diagonal values showing a high percentage of correct classifications (90-93%) for each category. Non-diagonal values indicate relatively low misclassification rates, illustrating the model's effectiveness in distinguishing between different sentiment classes. Despite its overall strong performance, there are some errors, particularly between adjacent sentiment categories, suggesting potential areas for further optimization and feature engineering to enhance model accuracy.'''


##### READ DATA #####

# Read data from files
df_r = pd.read_excel(pathlib.Path(__file__).parent / '../data/rottentomatoes_url.xlsx')
df_d = pd.read_excel(pathlib.Path(__file__).parent / '../data/douban_url.xlsx')
df_rcom = pd.read_excel(pathlib.Path(__file__).parent / '../data/rottentomatoes_data.xlsx')
df_dcom = pd.read_excel(pathlib.Path(__file__).parent / '../data/douban_data.xlsx')

# Paths for images
WC_r = "assets/rottentomatoes_word.jpg"
WC_d = "assets/douban_word.jpg"
LDA_d = "assets/douban_LDA.png"
LDA_r = "assets/rottentomatoes_LDA.png"
SA_d = "assets/Douban Sentiment Analysis Confusion Matrix.png"
SA_r = "assets/Rottentomatoes Sentiment Analysis Confusion Matrix.png"
TL_r = "assets/rottentomatoes_time.jpg"
TL_d = "assets/douban_time.jpg"


##### FUNCTION FOR DASHBOARD #####

# Function to generate movie cards
card_style = {'width': '12rem', 'height': '5rem'}
def generate_movie_cards(df):
    '''
    Convert movie list to card style.
    Input:
    - df: pandas DataFrame containing movie information.
    Output:
    - cards: a list of movie cards in a card style format ready for display.
    '''
    cards = []
    for index, row in df.iterrows():
        card = dbc.Card(
            dbc.CardBody([
                html.H6(html.A(row.iloc[0], href=row.iloc[3], target="_blank"), className="card-title"),
                html.P(f"Year: {row.iloc[2]}", className="card-year"),
            ]),
            style=card_style,
            className="mb-3",
        )
        cards.append(card)
    return cards


##### DASHBOARD PART #####

# Setup Dash application
app = Dash(external_stylesheets=[dbc.themes.PULSE])

# Layout of the Dash app
app.layout = dbc.Container([
    html.Br(),
    dbc.Row(html.H1("Comparison of Movie Reviews", style={'color': 'white'}), justify='center', style={'background-color': 'darkred'}),

    # Word Cloud
    dbc.Row(html.H2("Word Cloud"), justify='center', style={'margin-top': '20px'}),
    dbc.Row([
        dbc.Col([
            html.H4("Rotten Tomatoes"),
            html.Img(src=WC_r, style={'width': '100%', 'height': 'auto'}),
            html.P(note_WC_R, style={'textAlign': 'left'}),
        ], width=6),
        dbc.Col([
            html.H4("Douban"),
            html.Img(src=WC_d, style={'width': '100%', 'height': 'auto'}),
            html.P(note_WC_D, style={'textAlign': 'left'}), 
        ], width=6)
    ], justify='center'),

    # LDA Analysis
    dbc.Row(html.H2("LDA Analysis"), justify='center', style={'margin-top': '20px'}),
    dbc.Row(html.P(note_LDA)),
    dbc.Row([
        dbc.Col([
            html.H4("Rotten Tomatoes"),
            html.Img(src=LDA_r, style={'width': '100%', 'height': 'auto'}),
            html.P(note_LDA_R, style={'textAlign': 'left'})
        ], width=6),
        dbc.Col([
            html.H4("Douban"),
            html.Img(src=LDA_d, style={'width': '100%', 'height': 'auto'}),
            html.P(note_LDA_D, style={'textAlign': 'left'})
        ], width=6),
    ], justify='center'),

    # Sentiment Analysis
    dbc.Row(html.H2("Sentiment Analysis"), justify='center', style={'margin-top': '20px'}),
    dbc.Row(html.P(note_SA)),
    dbc.Row([
        dbc.Col([
            html.H4("Rotten Tomatoes"),
            html.Img(src=SA_r, style={'width': '100%', 'height': 'auto'}),
            html.P(note_SA_R, style={'textAlign': 'left'}),
        ], width=6),
        dbc.Col([
            html.H4("Douban"),
            html.Img(src=SA_d, style={'width': '100%', 'height': 'auto'}),
            html.P(note_SA_D, style={'textAlign': 'left'}), 
        ], width=6)
    ], justify='center'),

    # Timeline
    dbc.Row(html.H2("Time Line"), justify='center', style={'margin-top': '20px'}),
    dbc.Row([
        dbc.Col([
            html.H4("Rotten Tomatoes"),
            html.Img(src=TL_r, style={'width': '100%', 'height': 'auto'}),
        ], width=6),
        dbc.Col([
            html.H4("Douban"),
            html.Img(src=TL_d, style={'width': '100%', 'height': 'auto'}),
        ], width=6)
    ], justify='center'),


    # APPENDIX
    dbc.Row(html.H2("APPENDIX"), style={'margin-top': '20px', 'font-weight': 'bold'}),

    # List of Films from Rotten Tomatoes
    dbc.Row(html.H3("List of Films from Rotten Tomatoes"), justify='center', style={'margin-top': '20px'}),
    dbc.Row(generate_movie_cards(df_r)),

    # List of Films from Douban
    dbc.Row(html.H3("List of Films from Douban"), justify='center', style={'margin-top': '20px'}),
    dbc.Row(generate_movie_cards(df_d)),

    # Reviews from RT
    dbc.Row(html.H3("Sample Reviews (Rotten Tomatoes)"), justify='center', style={'margin-top': '20px'}),
    dbc.Row([
        dcc.Dropdown(
            id='movie-dropdown-rt',
            options=[{'label': movie, 'value': movie} for movie in df_rcom['Movie Title'].unique()],
            value=None,
            placeholder="Select a Movie Title"
        )
    ]),
    dbc.Row([
        dash_table.DataTable(
            id='datatable-interactivity-rt',
            columns=[{"name": i, "id": i} for i in df_rcom.columns],
            data=df_rcom.to_dict('records'),
            filter_action='none',
            page_size=10,
            style_cell={'maxWidth': '100px', 'overflow': 'auto', 'textAlign': 'left'},
        )
    ]),

    # Reviews from DB
    dbc.Row(html.H3("Sample Reviews (Douban)"), justify='center', style={'margin-top': '20px'}),
    dbc.Row([
        dcc.Dropdown(
            id='movie-dropdown-db',
            options=[{'label': movie, 'value': movie} for movie in df_dcom['name'].unique()],
            value=None,
            placeholder="Select a Movie Title"
        )
    ]),
    dbc.Row([
        dash_table.DataTable(
            id='datatable-interactivity-db',
            columns=[{"name": i, "id": i} for i in df_dcom.columns],
            data=df_dcom.to_dict('records'),
            filter_action='none',
            page_size=10,
            style_cell={'maxWidth': '100px', 'overflow': 'auto', 'textAlign': 'left'},
        )
    ]),

    html.Br(),

    dbc.Row("Sources: Douban and Rotten Tomatoes Websites"),
], fluid=True, style={'text-align': 'center'})


##### CALLBACK #####

# Callback to update data table for Rotten Tomatoes
@app.callback(
    Output('datatable-interactivity-rt', 'data'),
    [Input('movie-dropdown-rt', 'value')]
)
def update_table_rt(selected_movie):
    if selected_movie is not None:
        filtered_data = df_rcom[df_rcom['Movie Title'] == selected_movie]
        return filtered_data.to_dict('records')
    else:
        return df_rcom.to_dict('records')

# Callback to update data table for Douban reviews
@app.callback(
    Output('datatable-interactivity-db', 'data'),
    [Input('movie-dropdown-db', 'value')]
)
def update_table_db(selected_movie):
    if selected_movie is not None:
        filtered_data = df_dcom[df_dcom['name'] == selected_movie]
        return filtered_data.to_dict('records')
    else:
        return df_dcom.to_dict('records')


##### MAIN #####

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
