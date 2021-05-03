# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pathlib import Path
import numpy as np

# Imports from this application
from app import app

from joblib import load
pipeline = load('assets/model.joblib')

# Import data
data_path = Path('../../data/project')
X = pd.read_csv(data_path/'X_train_engineered.csv', index_col = 'Id')
y = pd.read_csv(data_path/'y_train_engineered.csv', index_col = 'Id')
my_data = pd.concat([X, y], axis=1)


# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Make your predictions here

            """
        , className = 'mb-5'),

        dcc.Markdown(
            """

            #### Total Square Footage: 

            """
        , className = 'mb-4'),
        
        dcc.Slider(
            id = 'total_sf',
            min = 300,
            max = 12000,
            step = 100,
            marks = {n: str(n) for n in range(300, 12050, 500)},
            className = 'mb-2'),

        dcc.Markdown(
            """

            #### Year built: 

            """
        , className = 'mb-4'),
        
        dcc.Input(
            id = 'year',
            placeholder = 'Enter a year:',
            type='text',
            value='',
            className = 'mb-2'),

        dcc.Markdown(
            """

            #### Overall quality of the material and house finish: 

            """
        , className = 'mb-4'),
        
        dcc.Slider(
            id = 'OverallQual',
            min = 0,
            max = 10,
            step = 1,
            marks = {n: str(n) for n in range(0, 11, 1)},
            className = 'mb-2'),

    ],
    md=4,
)

column2 = dbc.Col(
    [
        html.H2('Predicted sales price:', className='mb-5'), 
        html.Div(id='prediction-content', className='lead')
    

    ]
)

@app.callback(
    Output('prediction-content', 'children'),
    [Input('total_sf', 'value'), Input('year', 'value'), Input('OverallQual', 'value')],
)
def predict(total_sf, year, OverallQual):
    # total_sf
    mean_row = [X[i].mean() for i in X if i != 'TotalSF']
    arr = X.mean().index == 'TotalSF'
    missing_index = np.where(arr == True)
    mean_row.insert(missing_index[0][0], total_sf)

    # year
    mean_row = np.array(mean_row)
    arr = X.mean().index == 'YearBuilt'
    missing_index = np.where(arr == True)
    np.put(mean_row, missing_index, year)

    # OverallQual  
    arr = X.mean().index == 'OverallQual'
    missing_index = np.where(arr == True)
    np.put(mean_row, missing_index, OverallQual)

    df = pd.DataFrame( 
        data=[mean_row]
    )
    y_pred = pipeline.predict(df)[0]
    y_pred = np.exp(y_pred)
    return f'${y_pred:.0f}'

layout = dbc.Row([column1, column2])