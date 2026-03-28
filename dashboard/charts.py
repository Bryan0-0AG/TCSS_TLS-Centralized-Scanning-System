import plotly.express as px
import pandas as pd

from config import COLORES_RIESGO, COLORES_TABLA
from storage.file_manager import leer_csv


def obtener_info_actualizada() -> dict:
    """
    Lee el CSV y construye todos los datos que necesita el dashboard:
    contadores, figuras Plotly y datos para la tabla.
    """
    df = leer_csv()

    # ── Gráfica de torta ──────────────────────────────────────────────────────
    conteo = df["Riesgo"].value_counts().reset_index()
    conteo.columns = ["Riesgo", "Cantidad"]
    fig_torta = px.pie(
        conteo,
        names="Riesgo",
        values="Cantidad",
        title="Distribución de riesgos",
        color="Riesgo",
        color_discrete_map=COLORES_RIESGO,
    )

    # ── Gráfica de barras ─────────────────────────────────────────────────────
    df_validos = df[df["Días restantes"] > 0].copy()
    fig_barras = px.bar(
        df_validos,
        x="Dominio",
        y="Días restantes",
        title="Días hasta vencimiento del certificado",
        color="Riesgo",
        color_discrete_map=COLORES_RIESGO,
        text="Días restantes",
    )
    fig_barras.update_traces(textposition="outside")

    # ── Estilo condicional de la tabla ────────────────────────────────────────
    estilo_tabla = [
        {"if": {"filter_query": f'{{Riesgo}} = "{r}"'}, "backgroundColor": c}
        for r, c in COLORES_TABLA.items()
    ]

    return {
        "dominios_escaneados":       str(len(df)),
        "cantidad_riesgo_bajo":      str(len(df[df["Riesgo"] == "BAJO"])),
        "cantidad_requieren_atencion": str(len(df[df["Riesgo"].isin(["ALTO", "CRITICO"])])),
        "fig_torta":                 fig_torta,
        "fig_barras":                fig_barras,
        "tabla_data":                df.to_dict("records"),
        "tabla_columns":             [{"name": c, "id": c} for c in df.columns],
        "estilo_tabla":              estilo_tabla,
    }
