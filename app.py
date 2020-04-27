from recommender_func import *

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output , State
import dash_table



# setting up DASH server
app = dash.Dash(
    __name__, external_stylesheets=[
        "https://codepen.io/chriddyp/pen/bWLwgP.css",
    ]
)
server = app.server
app.title = 'Anime Recommnder system'


# app layout
app.layout = html.Div(id='container',children=[
    # header
    html.H1(["Anime recommnder system", ], id='h1'),
    html.H1(["________________________________________________________________________", ], id='h2'),
 
    html.Button(id='top', n_clicks=0, children='Top 5 Items'),
    # html.Div(id='dummy1'),
    dash_table.DataTable(id='dummy1',columns=[{"name": i, "id": i} for i in top_5().columns],
                         style_header={
                             'backgroundColor': 'rgb(30, 30, 30)',
                             'fontWeight': 'bold'
                         },
                        style_cell={
                             'backgroundColor': 'rgb(50, 50, 50)',
                             'color': 'white',
                             'font-family': 'PT Sans',
                             'font-size': '1.4rem',
                         },
                     ),
    html.H1(["________________________________________________________________________", ], id='h3'),
    dcc.Input(
                                placeholder="Enter user ID",
                                id="user_id",
                                style={"width":"22%"},
                                     ),
    html.Button(id='search', n_clicks=0, children='Predict'),
    html.Div(id='dummy2'),
    html.H1(["________________________________________________________________________", ], id='h4')],
    )

    # ------------------------------- CALLBACKS ---------------------------------------- #

@app.callback(Output("dummy1",component_property='data'), [Input("top", "n_clicks")])
def top5(n_clicks):
    return top_5().to_dict('records')

@app.callback(Output("dummy2", "children"), [Input("search", "n_clicks")], [State("user_id", "value")])
def new_search(n_clicks, userid ):
    if not userid:
        return "Please enter user id "
    products = top_5_recommendations(userid)

    return products

if __name__ == '__main__':
    app.run_server(debug = False)