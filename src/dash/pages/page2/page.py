import dash_bootstrap_components as dbc
import iris
from dash import dcc
from layout import covidTimeline

# Set filter Country selector
country_selector = dcc.Dropdown(
    iris.sql.exec("select location from Data.Covid19 WHERE continent != ''").dataframe()['location'],
    multi=True,
    id='country_selector')


def getLayout():
    return [dbc.Row(dcc.Graph(figure=covidTimeline.getFigure(), className='dash-block'))]
