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

app = dash.Dash(__name__)

app.layout = html.Div([

    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
    ),

    dcc.Graph(
        id='basic-interactions',
        figure={
            'data': [
                {
                    'x': [1, 2, 3, 4],
                    'y': [4, 1, 3, 5],
                    'text': ['a', 'b', 'c', 'd'],
                    'customdata': ['c.a', 'c.b', 'c.c', 'c.d'],
                    'name': 'Trace 1',
                    'mode': 'markers',
                    'marker': {'size': 12}
                },
                {
                    'x': [1, 2, 3, 4],
                    'y': [9, 4, 1, 4],
                    'text': ['w', 'x', 'y', 'z'],
                    'customdata': ['c.w', 'c.x', 'c.y', 'c.z'],
                    'name': 'Trace 2',
                    'mode': 'markers',
                    'marker': {'size': 12}
                }
            ],
            'layout': {
                'clickmode': 'event+select'
            }
        }
    ),
])


if __name__ == '__main__':
    app.run_server(debug=True)
