# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pathlib import Path

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Welcome to my house pricing app!

            For all your house pricing needs (as long as you live in Ames, Iowa)

            """
        ),

        #dcc.Link(hred = 'https://github.com/ppmorgoun/lambda-unit-2-build-week'),

        dcc.Link(dbc.Button('Predict my house!', color='primary'), href='/predictions'),

        dcc.Markdown(
            """
        

        
            See the source code here:

            """
        ),

        dcc.Link(dbc.Button('Github', color='primary'), href='https://github.com/ppmorgoun/lambda-unit-2-build-week')
    ],
    md=4,
)

data_path = Path('../../data/project')
X = pd.read_csv(data_path/'X_train_engineered.csv', index_col = 'Id')
y = pd.read_csv(data_path/'y_train_engineered.csv', index_col = 'Id')
my_data = pd.concat([X, y], axis=1)

fig = px.scatter(my_data, x="TotalSF", y="SalePrice", color="OverallQual")

#fig = px.scatter(gapminder.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
 #          hover_name="country", log_x=True, size_max=60)

col_options = [dict(label=x, value=x) for x in my_data.columns]
dimensions = ['x', 'y', 'color', 'facet_col', 'facet_row']

column2 = dbc.Col(
    [
        html.Div(
            [html.P([d + ':', dcc.Dropdown(id=d, options=col_options)]) for d in dimensions]
        ),
        dcc.Graph(id = 'graph',
        figure=px.scatter(my_data))
    ]
)

@app.callback(Output('graph', 'figure'),
              [Input(d, 'value') for d in dimensions])
def cb(x, y, color, facet_col, facet_row):
    return px.scatter(my_data, x = x, y = y, color = color, facet_col = facet_col, facet_row = facet_row)

layout = dbc.Row([column1])