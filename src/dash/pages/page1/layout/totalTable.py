import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table
import iris

query = ("""SELECT 
    location, 
    CAST(total_cases AS int) as total_cases,
    CAST(total_deaths as int) as total_deaths,
    CAST(total_vaccinations AS int) as total_vaccinations
    FROM Data.Covid19 WHERE continent != ''""")

df = (iris.sql.exec(query).dataframe().sort_values(by=['total_cases'], ascending=False).rename(columns={
    "location": "Location",
    "total_cases": "Total cases",
    "total_deaths": "Total deaths",
    "total_vaccinations": "Total vaccinations"
}))

df.loc[:, "Total cases"] = df["Total cases"].map('{:,d}'.format)
df.loc[:, "Total deaths"] = df["Total deaths"].map('{:,d}'.format)
df.loc[:, "Total vaccinations"] = df["Total vaccinations"].map('{:,d}'.format)


def getFigure(countries):

    data = df[df['Location'].isin(countries)] if countries else df

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(data.columns.map(lambda x: '<b>'+x+'</b>')),
                    fill_color='white',
                    align=['left', 'center'],
                    font_size=14,
                    height=40,
                    line_color='#c1c5c9'),

        cells=dict(values=[data['Location'], data['Total cases'], data['Total deaths'], data['Total vaccinations']],
                   fill_color='white',
                   align=['left', 'center'],
                   height=30,
                   line_color='#dee2e6'))
    ])

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(
            showframe=False,
            showcoastlines=False,
        ),
    )

    return fig
