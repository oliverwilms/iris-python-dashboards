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

    fig = go.Figure(data=[go.Pie(
        labels=['Total vaccinations', 'Total deaths', 'Total cases'],
        textinfo='label+percent',
        values=[data['Total vaccinations'].sum(), data['Total deaths'].sum(), data['Total cases'].sum()],
    )])

    fig.update_layout(title_text="Count by type")

    return fig
