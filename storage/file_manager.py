import json
import pandas as pd

from config import RUTA_CSV, RUTA_JSON, COLUMNAS_CSV


# ── CSV ────────────────────────────────────────────────────────────────────────

def leer_csv() -> pd.DataFrame:
    """Devuelve el DataFrame del CSV. Lo crea vacío si no existe."""
    if RUTA_CSV.exists() if hasattr(RUTA_CSV, "exists") else __import__("os").path.exists(RUTA_CSV):
        return pd.read_csv(RUTA_CSV)
    df = pd.DataFrame(columns=COLUMNAS_CSV)
    df.to_csv(RUTA_CSV, index=False)
    return df


def guardar_csv(df: pd.DataFrame) -> None:
    df.to_csv(RUTA_CSV, index=False)


# ── JSON ───────────────────────────────────────────────────────────────────────

def leer_dominios() -> list[str]:
    """Devuelve la lista de dominios registrados. Crea el archivo si no existe."""
    import os
    if os.path.exists(RUTA_JSON):
        with open(RUTA_JSON, "r") as f:
            contenido = f.read().strip()
            return json.loads(contenido) if contenido else []
    _guardar_dominios([])
    return []


def _guardar_dominios(dominios: list[str]) -> None:
    with open(RUTA_JSON, "w") as f:
        json.dump(dominios, f, indent=2)


def agregar_dominio_json(dominio: str) -> bool:
    """Añade el dominio a la lista JSON. Devuelve True si fue nuevo."""
    dominios = leer_dominios()
    if dominio in dominios:
        return False
    dominios.append(dominio)
    _guardar_dominios(dominios)
    return True


def eliminar_dominio_json(dominio: str) -> None:
    dominios = leer_dominios()
    if dominio in dominios:
        dominios.remove(dominio)
        _guardar_dominios(dominios)


# ── CSV: operaciones por fila ──────────────────────────────────────────────────

def upsert_dominio_csv(dominio: str, nueva_data: dict) -> None:
    """Inserta o actualiza la fila del dominio en el CSV."""
    df = leer_csv()
    filtro = df[df["Dominio"] == dominio]

    if filtro.empty:
        df = pd.concat([df, pd.DataFrame([nueva_data])], ignore_index=True)
    else:
        idx = filtro.index[0]
        fila = filtro.iloc[0]
        if any(fila[col] != nueva_data[col] for col in nueva_data):
            for col, val in nueva_data.items():
                df.at[idx, col] = val

    guardar_csv(df)


def eliminar_dominio_csv(dominio: str) -> None:
    df = leer_csv()
    df = df[df["Dominio"] != dominio]
    guardar_csv(df)
