# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import CPI_data_clean as cdc
import calendar

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
data = cdc.cpi_data('../Data/CPI_time_series_December_2022.xls')
# inflation = "GENERAL INDEX (CPI)"
# data = data.loc[data['Index'] == inflation]


# fig1 = px.line(data, x="Date", y="CPI", title='General Inflation - Rwanda', color="Level")

##Layout section with components to be displayed
years = list(range(2009,2023))
marks1 = {i: str(i) for i in years}
Months = calendar.month_name[1:]
Index = data.Index.unique()

app.layout = html.Div(children=[
    html.H1(children='CPI Dashboard'),
    html.Label('Select item'),
    dcc.Dropdown(Index, id='inflation', multi=False, value=Index[0]),
    html.Label('Select month'),
    dcc.Dropdown(Months, id='month', multi=False, placeholder="All"),
    html.Label('Select geography'),
    dcc.Checklist(options=data.Level.unique(),
                  value=data.Level.unique(),
                  inline=True,
                  id='geography'),
    html.Label('Select range'),
    dcc.RangeSlider(min=min(years),
                    max=max(years),
                    step=1,
                    marks=marks1,
                    tooltip={"placement": "bottom", "always_visible": True},
                    id='years'),
    html.Div(id='output_container', children=[]),
    dcc.Graph(
        id='cpi-fig',
        figure={}
    )
])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='cpi-fig', component_property='figure')],
    [Input(component_id='inflation', component_property='value'),
     Input(component_id='month', component_property='value'),
     Input(component_id='years', component_property='value'),
     Input(component_id='geography', component_property='value')]
)
def update_graph(inflation, month, years, geography):
    print(inflation)
    print(type(inflation))

    container = "The current CPI index is: {}".format(inflation)

    dff = data.copy()
    if month not in Months:
        dff = dff
    else:
        dff = dff[dff['Month']==month]
    dff = dff[dff['Level'].isin(geography)]
    dff = dff.loc[dff["Index"] == inflation]
    fig = px.line(dff, x="Date", y="CPI", title="{}".format(inflation), color="Level",
                  labels={"Date": "", "CPI": "CPI", "Level": "Geography"})
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
        title={'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
    )
    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)
