from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np


data_all = pd.read_csv("data_all_density.csv", sep=";", header=0)

dropdown_options = data_all["location_name"].unique().tolist()
dropdown_options.insert(0, "All locations")


def get_mask(df, low, high, location):
    print(location)
    if location == "All locations":
        mask = (df["Hm0 SWAN"] > low) & (df["Hm0 SWAN"] < high)
    else:
        mask = (df["Hm0 SWAN"] > low) & (df["Hm0 SWAN"] < high) & (df["location_name"] == location)

    return mask


app = Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Graph(id="scatter-plot-windspeed"),
            ],
            style={"width": "49%", "display": "inline-block"},
        ),
        html.Div(
            [
                dcc.Graph(id="radial-scatter-wind"),
            ],
            style={"width": "49%", "display": "inline-block"},
        ),
        html.Div(
            [
                dcc.Graph(id="scatter-plot-waveperiod"),
                html.P("Filter by measured spectral wave height:"),
            ],
            style={"width": "49%", "display": "inline-block"},
        ),
        html.Div(
            [
                dcc.Graph(id="radial-scatter-waves"),
            ],
            style={"width": "49%", "display": "inline-block"},
        ),
        html.Div(
            [
                dcc.RangeSlider(
                    id="range-slider",
                    min=0,
                    max=6,
                    step=0.1,
                    marks={
                        0: "0.0",
                        0.5: "0.5",
                        1: "1.0",
                        1.5: "1.5",
                        2: "2.0",
                        2.5: "2.5",
                        3: "3.0",
                        3.5: "3.5",
                        4: "4.0",
                        4.5: "4.5",
                        5: "5.0",
                        5.5: "5.5",
                        6: "6.0",
                    },
                    value=[0.0, 6.0],
                ),
                dcc.Dropdown(
                    dropdown_options,
                    "All locations",
                    id="selected_location",
                ),
            ],
            style={"width": "98%", "display": "inline-block"},
        ),
    ]
)


@app.callback(
    Output("scatter-plot-windspeed", "figure"),
    Input("range-slider", "value"),
    Input("selected_location", "value"),
)
def update_figure_windspeed(slider_range, location):
    df = data_all
    low, high = slider_range
    mask = get_mask(df, low, high, location)
    fig = px.scatter(
        df[mask],
        x="Wind speed SWAN",
        y="Hm0 SWAN",
        color="density_Hm0_Uwind",
        color_continuous_scale=px.colors.sequential.Hot,
    )
    fig.update_xaxes(range=[0, np.ceil(df["Wind speed SWAN"].max())])
    fig.update_yaxes(range=[0, np.ceil(df["Hm0 SWAN"].max())])
    return fig


@app.callback(
    Output("radial-scatter-wind", "figure"),
    Input("range-slider", "value"),
    Input("selected_location", "value"),
)
def update_figure_radial_wind(slider_range, location):
    df = data_all
    low, high = slider_range
    mask = get_mask(df, low, high, location)
    fig = px.scatter_polar(
        df[mask],
        theta="Wind direction SWAN",
        r="Hm0 SWAN",
        color="density_Hm0_WindDir",
        color_continuous_scale=px.colors.sequential.Hot,
        range_r=[0, np.ceil(df["Hm0 SWAN"].max())],
    )
    return fig


@app.callback(
    Output("scatter-plot-waveperiod", "figure"),
    Input("range-slider", "value"),
    Input("selected_location", "value"),
)
def update_figure_waveperiod(slider_range, location):
    df = data_all
    low, high = slider_range
    mask = get_mask(df, low, high, location)
    fig = px.scatter(
        df[mask],
        x="Tm10 SWAN",
        y="Hm0 SWAN",
        color="density_Hm0_Tmm10",
        color_continuous_scale=px.colors.sequential.Hot,
    )
    fig.update_xaxes(range=[0, np.ceil(df["Tm10 SWAN"].max())])
    fig.update_yaxes(range=[0, np.ceil(df["Hm0 SWAN"].max())])
    return fig


@app.callback(
    Output("radial-scatter-waves", "figure"),
    Input("range-slider", "value"),
    Input("selected_location", "value"),
)
def update_figure_radial_waves(slider_range, location):
    df = data_all
    low, high = slider_range
    mask = get_mask(df, low, high, location)
    fig = px.scatter_polar(
        df[mask],
        theta="Wdir SWAN",
        r="Hm0 SWAN",
        color="density_Hm0_WaveDir",
        color_continuous_scale=px.colors.sequential.Hot,
        range_r=[0, np.ceil(df["Hm0 SWAN"].max())],
    )
    return fig


app.run_server()
