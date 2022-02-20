import dash_bootstrap_components as dbc
import iris
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from layout import worldmap, piecases, topCountryByCases_bar, totalTable, indicators

# Set filter Country selector
country_selector = dcc.Dropdown(
    iris.sql.exec("select location from Data.Covid19 WHERE continent != ''").dataframe()['location'],
    multi=True,
    id='country_selector')


def getLayout():
    return [
        dbc.Row(html.H1("Covid19 analytics"), className='mb-1'),
        # Filter
        dbc.Row([
            dbc.Col([
                html.H6('Select country'),
                html.Div(country_selector)
            ], width=7)
        ]),

        # Row 1 dashboards
        dbc.Row([
            # World map
            dbc.Col([
                dcc.Graph(id='worldmap-covid', className='dash-block')
            ], width=7, style={'margin': '20px 0 0 0'}),

            # Total table and indicators
            dbc.Col([
                dbc.Row(id='indicators', style={'height': '110px'}),
                dbc.Row(dcc.Graph(id='total-table', className='dash-block'), style={
                    'padding': '0 5px 0 5px',
                    'bottom': '0',
                    'margin-top': '20px'
                })
            ], width=5, style={'margin': '20px 0 0 0'})

        ]),

        # Row 2 dashboards
        dbc.Row([
            dbc.Col(dcc.Graph(id='top-country-by-cases', className='dash-block'), width=7, style={
                'margin': '20px 0 0 0'
            }),
            dbc.Col(dcc.Graph(id='pie-cases', className='dash-block'), width=5, style={
                'margin': '20px 0 0 0',
                'padding': '0 5px 0 5px'
            })
        ])
    ]


def set_callback(app):
    @app.callback(Output('top-country-by-cases', 'figure'), Input('country_selector', 'value'))
    def dash1(countries):
        return topCountryByCases_bar.getFigure(countries)

    @app.callback(Output('worldmap-covid', 'figure'), Input('country_selector', 'value'))
    def dash2(countries):
        return worldmap.getFigure(countries)

    @app.callback(Output('total-table', 'figure'), Input('country_selector', 'value'))
    def dash3(countries):
        return totalTable.getFigure(countries)

    @app.callback(Output('indicators', 'children'), Input('country_selector', 'value'))
    def dash4(countries):
        return indicators.getFigure(countries)

    @app.callback(Output('pie-cases', 'figure'), Input('country_selector', 'value'))
    def dash5(countries):
        return piecases.getFigure(countries)
