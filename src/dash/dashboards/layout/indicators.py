import dash_bootstrap_components as dbc
from dash import dcc
import plotly.graph_objects as go
import iris

query = ("""SELECT
    location, 
    CAST(total_cases AS int) as total_cases,
    CAST(total_deaths as int) as total_deaths,
    CAST(total_vaccinations AS int) as total_vaccinations
    FROM Data.Covid19 WHERE continent != ''""")

df = (iris.sql.exec(query).dataframe().rename(columns={
    "total_cases": "Total cases",
    "total_deaths": "Total deaths",
    "total_vaccinations": "Total vaccinations"
}))


def getFigure(countries):

    data = df[df['location'].isin(countries)] if countries else df

    fig1 = go.Figure(go.Indicator(
        value=data['Total cases'].sum(),
        number={"font": {"size": 28}},
        title={"text": "<span style='font-size:16px;color:gray'>Total cases</span>"},
    ))

    fig2 = go.Figure(go.Indicator(
        value=data['Total deaths'].sum(),
        number={"font": {"size": 28}},
        title={"text": "<span style='font-size:16px;color:gray'>Total deaths</span>"},
    ))

    fig3 = go.Figure(go.Indicator(
        value=data['Total vaccinations'].sum(),
        number={"font": {"size": 28}},
        title={"text": "<span style='font-size:16px;color:gray'>Total vaccinations</span>"},
    ))

    return [
        dbc.Col(dcc.Graph(figure=fig1, className='dash-block'), width=4, style={'padding': '0 5px 0 5px'}),
        dbc.Col(dcc.Graph(figure=fig2, className='dash-block'), width=4, style={'padding': '0 5px 0 5px'}),
        dbc.Col(dcc.Graph(figure=fig3, className='dash-block'), width=4, style={'padding': '0 5px 0 5px'})
    ]
