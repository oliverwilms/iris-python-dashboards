import numpy as np
import plotly.express as px
import pandas as pd

data = pd.read_csv('/opt/irisapp/src/dash/pages/page2/covid_19_data.csv', index_col='SNo')

data['ObservationDate'] = pd.to_datetime(data['ObservationDate'])
data['Confirmed'] = data['Confirmed'].astype('int')
data['Deaths'] = data['Deaths'].astype('int')
data['Recovered'] = data['Recovered'].astype('int')
data.loc[(data['Country/Region'] == ' Azerbaijan'), 'Country/Region'] = 'Azerbaijan'
data.loc[(data['Country/Region'] == 'US'), 'Country/Region'] = 'United States'
data.loc[(data['Country/Region'] == "('St. Martin',)"), 'Country/Region'] = 'St Martin'
data.loc[(data['Country/Region'] == "UK"), 'Country/Region'] = 'United Kingdom'
data.loc[(data['Country/Region'] == "Bahamas, The"), 'Country/Region'] = 'Bahamas'
covid_data = data.groupby(['Country/Region', 'ObservationDate']).sum().reset_index()
covid_data = covid_data.sort_values(['ObservationDate'])
covid_data['ObservationDate'] = covid_data['ObservationDate'].astype('str')


def getFigure():
    fig = px.choropleth(covid_data, locations="Country/Region",
                        color=np.log10(covid_data["Confirmed"]),
                        hover_name="Country/Region",
                        hover_data=["Confirmed", 'Deaths', 'Recovered'],
                        locationmode="country names",
                        animation_frame='ObservationDate',
                        color_continuous_midpoint=3,
                        color_continuous_scale=px.colors.sequential.thermal)

    fig.update_layout(margin=dict(l=20, r=0, b=0, t=70, pad=0), paper_bgcolor="white", height=700,
                      title_text='Number of daily COVID-19 cases worldwide', font_size=18)

    return fig
