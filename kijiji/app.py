# # -*- coding: utf-8 -*-
from environs import Env
import dash
import dash_table
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import datetime
from datetime import timedelta, date


def relative_freshness(dates, relative=datetime.datetime.utcnow()):
    ans = (relative - dates)
    res = ans / (relative - max(dates))
    return list(1 - min(res, 1.0))


def delta_ratio_day(date_in, denum):
    now = datetime.date.today()
    i = datetime.datetime.strptime(date_in, "%d-%b-%y").date()
    return 1 - min(abs((now - i).days / denum), 1.0)  # [0,1]


env = Env()
env.read_env()  # read .env file, if it exists
mapbox_access_token = env("MAPBOX_ACCESS_TOKEN")

df = pd.read_json('test/unclean_data.json', orient='records')
df = df.dropna()

app = dash.Dash(__name__)

data = [go.Scattermapbox(
    lat=df['latitude'],
    lon=df['longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(size=8,
                                   color='rgb(0, 0, 172)',
                                   opacity=0.7),
    text=df['price'],
    hoverinfo='text'),

    go.Scattermapbox(
        lat=[45.5001806, 45.5071648],
        lon=[-73.5674628, -73.5828495],
        mode='markers',
        marker=go.scattermapbox.Marker(size=12,
                                       color='rgb(255, 0, 0)',
                                       opacity=[1.0, 0.5]),
        text=['Work', 'Gym'],
        hoverinfo='text'),
]

layout = go.Layout(
    title='Kijiji Rooms',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(lat=45.5071648, lon=-73.5828495),
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
