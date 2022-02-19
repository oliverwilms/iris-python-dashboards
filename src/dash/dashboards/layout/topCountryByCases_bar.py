import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
import iris

query = ("""SELECT location,
    CAST(total_cases AS int) as total_cases,
    CAST(total_deaths AS int) as total_deaths,
    CAST(total_vaccinations as int) as total_vaccinations
    FROM Data.Covid19 WHERE continent != ''""")

df = (iris.sql.exec(query).dataframe().sort_values(by=['total_cases'], ascending=False).rename(columns={
        'location': 'Location',
        'total_cases': 'Total cases',
        'total_deaths': 'Total deaths',
        'total_vaccinations': 'Total vaccinations'}))


def getFigure(countries):

    data = df[df['Location'].isin(countries)] if countries else df

    fig = px.bar(
        data.head(10),
        x="Location",
        y=["Total cases", 'Total deaths', 'Total vaccinations'],
        barmode="group",
        title="Top 10 Countries",
        text_auto='.2s'
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(l=50, r=50, t=70, b=50),
        plot_bgcolor='#fff',
        title_font_size=14,
        legend=dict(
            orientation="h",
            yanchor="top",
            xanchor="right",
            x=1,
            y=1.12,
            title_text=None
        )
    )

    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')

    return fig
