from dash import Dash, html, dcc, Input, Output

app = Dash(__name__, suppress_callback_exceptions=True)

# Sidebar
sidebar = html.Div([
    dcc.Link("Dashboard", href="/"),
    html.Br(),
    dcc.Link("Tabla", href="/tabla"),
    html.Br(),
    dcc.Link("Admin", href="/admin"),
])

# Layout principal
app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div(sidebar, style={"width": "20%", "float": "left"}),
    html.Div(id="contenido", style={"margin-left": "20%"})
])

# Páginas
def login():
    return html.Div([
        html.H2("Login"),
        dcc.Input(placeholder="Usuario"),
        dcc.Input(type="password", placeholder="Contraseña"),
        html.Button("Entrar")
    ])

def dashboard():
    return html.H2("Dashboard")

def tabla():
    return html.H2("Tabla de datos")

def admin():
    return html.H2("Panel de administración")

# Router
@app.callback(
    Output("contenido", "children"),
    Input("url", "pathname")
)
def render(path):
    if path == "/":
        return dashboard()
    elif path == "/tabla":
        return tabla()
    elif path == "/admin":
        return admin()
    else:
        return login()

app.run(debug=False)