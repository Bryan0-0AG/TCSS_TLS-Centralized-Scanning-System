import dash
from dashboard.layout import crear_layout
from dashboard.callbacks import registrar_callbacks


def crear_app() -> dash.Dash:
    app = dash.Dash(__name__)
    app.layout = crear_layout()
    registrar_callbacks(app)
    return app
