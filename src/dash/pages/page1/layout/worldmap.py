import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import iris

query = "SELECT iso_code, location, CAST(total_cases AS int) as total_cases FROM Data.Covid19 WHERE continent != ''"

df = (iris.sql.exec(query).dataframe().sort_values(by=['total_cases'], ascending=False).rename(columns={
        'total_cases': 'Total cases'}))


def getFigure(countries):

    data = df[df['location'].isin(countries)] if countries else df

    fig = go.Figure(data=go.Choropleth(
            locations=data['iso_code'],
            text=data['location'],
            z=data['Total cases'],
            colorscale='Blues',
            colorbar_title="Total cases",
    ))

    fig.update_layout(
            margin=dict(l=40, r=0, t=10, b=10),
            geo=dict(
                    showframe=False,
                    showcoastlines=False,
            ),
    )

    return fig
