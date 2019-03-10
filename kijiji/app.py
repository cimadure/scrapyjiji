# # -*- coding: utf-8 -*-
# import os
# import dash
#
# app = dash.Dash(__name__)
# server = app.server
#
# # Running the server
# if __name__ == '__main__':
#     app.run_server(debug=True)


import dash
import dash_table
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

df = pd.read_json('test/unclean_data.json', orient='records')
df = df.dropna()

app = dash.Dash(__name__)

app.layout = html.Div([

    dcc.Graph(
        id='basic-interactions',
        figure={
            'data': [
                {
                    'x': df['latitude'],
                    'y': df['longitude'],
                    'text': df['title'],
                    'customdata': df['price'],
                    'name': 'Kijiji',
                    'mode': 'markers',
                    'marker': {'size': 12}
                },
            ],
            'layout': {
                'clickmode': 'event+select'
            }
        }
    ),

    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
    ),


])


if __name__ == '__main__':
    app.run_server(debug=True)
