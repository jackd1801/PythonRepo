# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output 
import plotly.express as px
import pandas as pd
import CPI_data_clean as cdc

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
data = cdc.cpi_data('../Data/CPI_time_series_December_2022.xls')
#inflation = "GENERAL INDEX (CPI)"
#data = data.loc[data['Index'] == inflation]


#fig1 = px.line(data, x="Date", y="CPI", title='General Inflation - Rwanda', color="Level")

##Layout section with components to be displayed
years = data['Date'].dt.year.unique()
marks1 = {i: str(i) for i in years}

app.layout = html.Div(children=[
    html.H1(children='CPI Dashboard'),
    dcc.Dropdown(data.Index.unique(), id='inflation', multi=False, value = "GENERAL INDEX (CPI)"),
    dcc.RangeSlider(min=min(years),
                    max=max(years),
                    step=1,
                    marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                    id='years'),
    html.Div(id = 'output_container', children=[]),
    dcc.Graph(
        id='cpi-fig',
        figure={}
    )
])

@app.callback(
     [Output(component_id='output_container', component_property='children'),
     Output(component_id='cpi-fig', component_property='figure')],
    [Input(component_id='inflation', component_property='value')]
)
def update_graph(inflation):
    print(inflation)
    print(type(inflation))

    container = "The current CPI index is: {}".format(inflation)

    dff = data.copy()
    dff = dff.loc[dff["Index"] == inflation]
    fig = px.line(dff, x="Date", y="CPI", title="{}".format(inflation), color="Level",
                  labels={"Date": "","CPI":"CPI", "Level":"Geography"})
    
    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)