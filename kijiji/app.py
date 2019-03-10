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

df = pd.read_json('test/unclean_data.json', orient='records')

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict("rows"),
)

if __name__ == '__main__':
    app.run_server(debug=True)
