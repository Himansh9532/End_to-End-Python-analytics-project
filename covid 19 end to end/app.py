import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

external_stylesheets = [
    {
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC",
        "crossorigin": "anonymous"
    }
]

# Load the data
df = pd.read_csv("state_wise_daily.csv")
Total = df.shape[0]
Active = df[df["Status"] == "Confirmed"].shape[0]
Recovered = df[df["Status"] == "Recovered"].shape[0]
Deceased = df[df["Status"] == "Deceased"].shape[0]

# Define the dropdown options
options = [
    {"label": "All", "value": "All"},
    {"label": "Hospitalized", "value": "Hospitalized"},
    {"label": "Recovered", "value": "Recovered"},
    {"label": "Deceased", "value": "Deceased"},
]
options1 = [
    {"label": "All", "value": "All"},
    {"label": "Mask", "value": "Mask"},
    {"label": "Sanitizer", "value": "Sanitizer"},
    {"label": "Oxygen", "value": "Oxygen"}
]
options2 = [
    {"label": "Red Zone", "value": "Red Zone"},
    {"label": "Blue Zone", "value": "Blue Zone"},
    {"label": "Green Zone", "value": "Green Zone"},
    {"label": "Orange Zone", "value": "Orange Zone"}
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Corona Virus Pandemic", style={"color": "#fff", "text-align": "center"}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases", className="text-light"),
                    html.H4(Total, className="text-light")
                ], className="card-body")
            ], className="card bg-danger")
        ], className="col-md-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases", className="text-light"),
                    html.H4(Active, className="text-light")
                ], className="card-body")
            ], className="card bg-info")
        ], className="col-md-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered Cases", className="text-light"),
                    html.H4(Recovered, className="text-light")
                ], className="card-body")
            ], className="card bg-warning")
        ], className="col-md-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Deaths", className="text-light"),
                    html.H4(Deceased, className="text-light")
                ], className="card-body")
            ], className="card bg-success")
        ], className="col-md-3")
    ], className="row"),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id="plot-graph", options=options1, value="All"),
                    dcc.Graph(id="graph")
                ], className="card-body")
            ], className="card bg-success")
        ], className="col-md-6"),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id="my_dropdown", options=options2, value="Red Zone"),
                    dcc.Graph(id="the_graph")
                ], className="card-body")
            ], className="card")
        ], className="col-md-6")
    ], className="row"),
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(id="picker", options=options, value="All"),
                dcc.Graph(id="bar")
            ], className="card-body")
        ], className="card")
    ], className="col-md-12")
], className="container")

# Define the callback to update the bar chart
@app.callback(Output("bar", "figure"), [Input("picker", "value")])
def update_graph(value):
    if value == "All":
        return {
            "data": [go.Bar(x=df["State"], y=df["Total"])],
            "layout": go.Layout(title="State Total Cases", plot_bgcolor="orange")
        }
    elif value == "Hospitalized":
        return {
            "data": [go.Bar(x=df["State"], y=df["Hospitalized"])],
            "layout": go.Layout(title="State Hospitalized Cases", plot_bgcolor="orange")
        }
    elif value == "Recovered":
        return {
            "data": [go.Bar(x=df["State"], y=df["Recovered"])],
            "layout": go.Layout(title="State Recovered Cases", plot_bgcolor="orange")
        }
    elif value == "Deceased":
        return {
            "data": [go.Bar(x=df["State"], y=df["Deceased"])],
            "layout": go.Layout(title="State Deceased Cases", plot_bgcolor="orange")
        }

# Define the callback to update the line chart
@app.callback(Output("graph", "figure"), [Input("plot-graph", "value")])
def generate_graph(value):
    if value == "All":
        return {
            "data": [go.Scatter(x=df["Status"], y=df["Total"], mode='lines')],
            "layout": go.Layout(title="Commodities Total Count", plot_bgcolor="pink")
        }
    elif value == "Mask":
        return {
            "data": [go.Scatter(x=df["Status"], y=df["Mask"], mode='lines')],
            "layout": go.Layout(title="Commodities Mask Count", plot_bgcolor="pink")
        }
    elif value == "Sanitizer":
        return {
            "data": [go.Scatter(x=df["Status"], y=df["Sanitizer"], mode='lines')],
            "layout": go.Layout(title="Commodities Sanitizer Count", plot_bgcolor="pink")
        }
    elif value == "Oxygen":
        return {
            "data": [go.Scatter(x=df["Status"], y=df["Oxygen"], mode='lines')],
            "layout": go.Layout(title="Commodities Oxygen Count", plot_bgcolor="pink")
        }

# Define the callback to update the pie chart
@app.callback(Output("the_graph", "figure"), [Input("my_dropdown", "value")])
def update_pie_chart(value):
    piechart = px.pie(df, names=value, hole=0.3)
    return (piechart)

if __name__ == '__main__':
    app.run_server(debug=True)
