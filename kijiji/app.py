# # -*- coding: utf-8 -*-
from environs import Env
import dash
import dash_table
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

env = Env()
env.read_env()  # read .env file, if it exists
mapbox_access_token = env("MAPBOX_ACCESS_TOKEN")

df = pd.read_json('test/unclean_data.json', orient='records')
df = df.dropna()

app = dash.Dash(__name__)

data = [go.Scattermapbox(
    lat=list(df['latitude']),
    lon=list(df['longitude']),
    mode='markers',
    marker=go.scattermapbox.Marker(size=8,
                                   color='rgb(242, 177, 172)',
                                   opacity=0.7),
    text=df['price'],
    hoverinfo='text'
)]

layout = go.Layout(
    title='Kijiji Rooms',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(lat=45.92, lon=-73.07),
        pitch=1,
        zoom=10,
        style='light'
    ),
)

fig = go.Figure(data=data, layout=layout)

app.layout = html.Div(children=[
                                html.H1(children='Hello Scraper'),

                                html.Div(children='''
                                    Dash: A web application framework for Python.
                                '''),
                                dcc.Graph(
                                    id='example-graph',
                                    figure=fig),

                                dash_table.DataTable(
                                    id='table',
                                    columns=[{"name": i, "id": i} for i in df.columns],
                                    data=df.to_dict("rows"),
                                ),
                                ])

if __name__ == '__main__':
    app.run_server(debug=True)
