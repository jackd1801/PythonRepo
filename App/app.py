# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import CPI_data_clean as cdc

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
data = cdc.cpi_data('../Data/CPI_time_series_December_2022.xls')
inflation = "GENERAL INDEX (CPI)"
data = data.loc[data['Index'] == inflation]

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig1 = px.line(data, x="Date", y="CPI", title='General Inflation - Rwanda', color="Level")

app.layout = html.Div(children=[
    html.H1(children='CPI Dashboard'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig1
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)