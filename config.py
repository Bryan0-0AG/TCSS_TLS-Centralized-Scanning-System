import os
import pytz

# ── Rutas ─────────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV  = os.path.join(ROOT, "storage", "TLS.SCAN_Dominios.csv")
RUTA_JSON = os.path.join(ROOT, "storage" ,"Dominios_registrados.json")

# ── Zona horaria ──────────────────────────────────────────────────────────────
ZONA_HORARIA = pytz.timezone("America/Bogota")

# ── Clasificación de cifrados ─────────────────────────────────────────────────
CIFRADOS_INSEGUROS = ["RC4", "DES", "3DES", "MD5", "NULL", "EXPORT"]
CIFRADOS_MODERADOS = ["AES128", "SHA1"]
CIFRADOS_SEGUROS   = ["AES256", "CHACHA20", "SHA256"]

# ── Colores para el dashboard ─────────────────────────────────────────────────
COLORES_RIESGO = {
    "BAJO":    "#2ecc71",
    "MEDIO":   "#f39c12",
    "ALTO":    "#d3721e",
    "CRITICO": "#e74c3c",
}

COLORES_TABLA = {
    "BAJO":    "#a8e6cf",
    "MEDIO":   "#ffd3b6",
    "ALTO":    "#ffaaa5",
    "CRITICO": "#ff8b94",
}

# ── Columnas del CSV ──────────────────────────────────────────────────────────
COLUMNAS_CSV = [
    "Dominio",
    "Escaneado en",
    "Version TLS",
    "Días restantes",
    "Emisor de certificado TLS",
    "Protocolo de cifrado",
    "Riesgo",
    "Observaciones",
]
