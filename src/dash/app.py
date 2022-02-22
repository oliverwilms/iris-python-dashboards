import dash
import codecs
from flask import Flask, request, make_response, redirect
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import sys
sys.path.append('/opt/irisapp/src/dash/pages/page1')
sys.path.append('/opt/irisapp/src/dash/pages/page2')
import pages.page1.page as page1
import pages.page2.page as page2
import iris

# init server
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

APPPATH = "/opt/irisapp/src/dash"
LOGINCOOKIE = "dash_login"

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#fff",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Dashboards", className="display-6"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Overview", href="/", active="exact", external_link=True),
                dbc.NavLink("Timeline", href="/page-1", active="exact", external_link=True),
                dbc.NavLink("IRIS python usage", href="/page-2", active="exact", external_link=True),
                dbc.NavLink("Logout", href="/logout", active="exact", external_link=True, className='logout-btn', style={
                    'margin-top': '40px',
                })
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


def login_check(func):
    def inner(*args):
        if not bool(request.cookies.get(LOGINCOOKIE)):
            return dcc.Location(pathname="/login", id='page-content')

        return func(*args)

    return inner


content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])
page1.set_callback(app)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
@login_check
def render_page_content(pathname):

    if pathname == "/":
        return html.Div(page1.getLayout())
    elif pathname == "/page-1":
        return html.Div(page2.getLayout())
    elif pathname == "/page-2":
        return dbc.Row([
            html.Iframe(src='/guide-login-jupyter', style={'width': '100%', 'height': '300px'}, className='dash-block'),
            html.Iframe(src='/guide-embedded-jupyter', className='dash-block', style={
                'width': '100%',
                'height': '2190px',
                'margin-top': '20px'
            }),
            html.Iframe(src='/guide-nativeapi-jupyter', className='dash-block', style={
                'width': '100%', 
                'height': '640px',
                'margin-top': '20px'
            })
        ])

    return dcc.Location(pathname="/login", id='page-content')


@app.server.route('/guide-login-jupyter')
def get_guide_login_jupyter():
    return codecs.open(APPPATH + "/pages/page3/guide-login-jupyter.html", 'r').read()


@app.server.route('/guide-embedded-jupyter')
def get_guide_embedded_jupyter():
    return codecs.open(APPPATH + "/pages/page3/guide-embedded-jupyter.html", 'r').read()


@app.server.route('/guide-nativeapi-jupyter')
def get_guide_nativeapi_jupyter():
    return codecs.open(APPPATH + "/pages/page3/guide-nativeapi-jupyter.html", 'r').read()


@app.server.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        if iris.system.Security.Login(request.form['username'], request.form['password']):
            res = make_response(redirect('/'))
            res.set_cookie(LOGINCOOKIE, "1", 3600)
            res.status_code = 200
            return res
        else:
            res = make_response("error")
            res.status_code = 401
            return res

    return codecs.open("/opt/irisapp/src/dash/auth/login.html", 'r').read()


@app.server.route('/logout')
def logout():
    res = make_response(redirect('/login'))
    res.delete_cookie(LOGINCOOKIE)
    return res


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080, debug=True)
