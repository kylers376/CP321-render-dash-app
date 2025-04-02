# Link to published dashboard: ...

#pip! install numpy pandas Dash plotly
import numpy as np
import pandas as pd
from dash import Dash, dcc, html, callback, Input, Output
import plotly.express as px

"""
Notes:
Linking: Render is a free option for publishing your dashboard on a server, link is in assignment, as well as Youtube tutorial
Data representation: West Germany and Germany should be considered the same country for this assignment
"""

# Step 1: Create a dataset for your dashboard, using the Wiki page info
wc_history = [
    {"Year": 2022, "Winner": "Argentina", "Runner-up": "France"},
    {"Year": 2018, "Winner": "France", "Runner-up": "Croatia"},
    {"Year": 2014, "Winner": "Germany", "Runner-up": "Argentina"},
    {"Year": 2010, "Winner": "Spain", "Runner-up": "Netherlands"},
    {"Year": 2006, "Winner": "Italy", "Runner-up": "France"},
    {"Year": 2002, "Winner": "Brazil", "Runner-up": "Germany"},
    {"Year": 1998, "Winner": "France", "Runner-up": "Brazil"},
    {"Year": 1994, "Winner": "Brazil", "Runner-up": "Italy"},
    {"Year": 1990, "Winner": "Germany", "Runner-up": "Argentina"},
    {"Year": 1986, "Winner": "Argentina", "Runner-up": "Germany"},
    {"Year": 1982, "Winner": "Italy", "Runner-up": "Germany"},
    {"Year": 1978, "Winner": "Argentina", "Runner-up": "Netherlands"},
    {"Year": 1974, "Winner": "Germany", "Runner-up": "Netherlands"},
    {"Year": 1970, "Winner": "Brazil", "Runner-up": "Italy"},
    {"Year": 1966, "Winner": "England", "Runner-up": "Germany"},
    {"Year": 1962, "Winner": "Brazil", "Runner-up": "Czechoslovakia"},
    {"Year": 1958, "Winner": "Brazil", "Runner-up": "Sweden"},
    {"Year": 1954, "Winner": "Germany", "Runner-up": "Hungary"},
    {"Year": 1950, "Winner": "Uruguay", "Runner-up": "Brazil"},
    #WW2
    {"Year": 1938, "Winner": "Italy", "Runner-up": "Hungary"},
    {"Year": 1934, "Winner": "Italy", "Runner-up": "Czechoslovakia"},
    {"Year": 1930, "Winner": "Uruguay", "Runner-up": "Argentina"}

]

#assign to dataframe
history_df = pd.DataFrame(wc_history)

#create another df of winners|wins, for step 2 b and c
wins_df = history_df.groupby("Winner")["Year"].count().reset_index(name = "Wins")

"""
Step 2: Enable user interaction with the dashboard, allowing users to:
a. View all countries that have ever won a World Cup
b. Select a country and view the number of times it has won the World Cup
c. Select a year when a World Cup was organized and view the winner and the runner-up
"""

app = Dash()
server = app.server

app.layout = html.Div([
    html.H1(children='FIFA World Cup History Dashboard', style={'textAlign':'center'}),

    #a
    dcc.Graph(id = "choropleth-content"),

    #b
    html.Div([
        html.Label("Select a country: "),
        dcc.Dropdown(id = "country-input", placeholder = "Select... ", value = wins_df["Winner"][0], options = [{"label": team,"value": team} for team in wins_df["Winner"]]),
        #originally had no default, bit I thought that a default looked a bit better, so I set it to Argentina in the value attribute
        html.Div(id = "country-output")
    ], style = {'marginBottom': '64px'}), #needed a bit more space between the slider and dropdown menu

    #c
    html.Div([
        html.Label("Enter the World Cup year: "),
        dcc.Slider(
            id = "year-input",
            min = 1930,
            max = 2022,
            step = None,
            marks = { #using custom marks, much easier
                1930: '1930',
                1934: '1934',
                1938: '1938',
                1950: '1950',
                1954: '1954',
                1962: '1962',
                1966: '1966',
                1970: '1970',
                1974: '1974',
                1978: '1978',
                1982: '1982',
                1986: '1986',
                1990: '1990',
                1994: '1994',
                1998: '1998',
                2002: '2002',
                2006: '2006',
                2010: '2010',
                2014: '2014',
                2018: '2018',
                2022: '2022'
            },
            value = 2002 #default
        ),
        html.Div(id = "year-output") #collect slider output
    ])
])

#a
@callback(
    Output("choropleth-content", "figure"),
    Input("country-input", "value")
)
def update_graph(country):
    fig = px.choropleth(
        wins_df,
        locations = "Winner",
        locationmode = "country names",
        color = "Wins",
        color_continuous_scale = "Viridis",
        scope = "world",
        title = "World Cup Winners"
    )
    fig.update_geos(showcoastlines = False, fitbounds = "locations")

    #to match map title font with the rest of the dashboard
    fig.update_layout(title_font = dict(family = "Times New Roman", color = "black", size = 24))
    return fig

#b
@callback(
    Output("country-output", "children"),
    Input("country-input", "value")
)
def display_wins(country):
    if country is None: #no country selected yet
        return "Choose a country from the dropdown menu above"
    wins = wins_df[wins_df["Winner"] == country]["Wins"].values[0]
    return f"{country} are {wins}-time World Cup champions"

#c
@callback(
    Output("year-output", "children"), #probably not
    Input("year-input", "value")
)
def display_year_final(year):
    winner = history_df[history_df["Year"] == year]["Winner"].values[0]
    runner = history_df[history_df["Year"] == year]["Runner-up"].values[0]
    return f"In the {year} World Cup, {winner} won against {runner}"

if __name__ == '__main__':
    app.run(debug=True)

# Step 3: Publish your code on a server. Include a link to your published dashboard as a comment at the top of your code. Additionally, include the password if you have password-protected your website
