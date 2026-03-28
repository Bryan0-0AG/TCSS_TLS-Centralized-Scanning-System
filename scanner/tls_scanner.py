import socket
import ssl
from datetime import datetime, UTC

from config import ZONA_HORARIA, CIFRADOS_INSEGUROS, CIFRADOS_MODERADOS


def escanear_tls(dominio: str) -> dict:
    """
    Conecta al dominio por HTTPS (puerto 443) y extrae información
    del certificado TLS. Devuelve un dict con los resultados.
    """
    fecha_escaneo = datetime.now(ZONA_HORARIA).replace(microsecond=0, tzinfo=None)
    nil = "---"
    observaciones = []

    try:
        contexto = ssl.create_default_context()

        with contexto.wrap_socket(socket.socket(), server_hostname=dominio) as conn:
            conn.settimeout(5)
            conn.connect((dominio, 443))

            tls_version  = conn.version()
            certificado  = conn.getpeercert()
            cifrado_info = conn.cipher()

        # ── Fecha de expiración ───────────────────────────────────────────────
        exp_date = datetime.strptime(certificado["notAfter"], "%b %d %H:%M:%S %Y %Z")
        exp_date = exp_date.replace(tzinfo=UTC)
        days_left = (exp_date - datetime.now(UTC)).days

        # ── Emisor ────────────────────────────────────────────────────────────
        emisor = "Desconocido"
        if certificado and "issuer" in certificado:
            emisor = dict(x[0] for x in certificado["issuer"]).get("commonName", "Desconocido")

        # ── Puntaje de riesgo ─────────────────────────────────────────────────
        puntaje = 0

        if tls_version in ("TLSv1", "TLSv1.1"):
            observaciones.append("TLS inseguro (obsoleto)")
            puntaje += 10
        elif tls_version == "TLSv1.2":
            puntaje += 2

        if days_left < 0:
            observaciones.append("Certificado vencido")
            puntaje += 10
        elif days_left <= 7:
            observaciones.append(f"Certificado por vencer ({days_left} días)")
            puntaje += 5
        elif days_left <= 30:
            observaciones.append(f"Certificado por vencer ({days_left} días)")
            puntaje += 3

        nombre_cifrado = cifrado_info[0].replace("TLS_", "")

        if any(palabra in nombre_cifrado for palabra in CIFRADOS_INSEGUROS):
            palabra = next(p for p in CIFRADOS_INSEGUROS if p in nombre_cifrado)
            observaciones.append(f"Cifrado inseguro: {palabra}")
            puntaje += 5
        elif any(palabra in nombre_cifrado for palabra in CIFRADOS_MODERADOS):
            palabra = next(p for p in CIFRADOS_MODERADOS if p in nombre_cifrado)
            observaciones.append(f"Cifrado moderado: {palabra}")
            puntaje += 3

        riesgo = _clasificar_riesgo(puntaje)

        return {
            "scan_date":     fecha_escaneo,
            "version":       tls_version,
            "emisor":        str(emisor),
            "days_left":     int(days_left),
            "cipher_name":   nombre_cifrado,
            "risk":          riesgo,
            "observaciones": observaciones,
        }

    except Exception as e:
        mensaje = (
            "No se pudo conectar correctamente al sitio"
            if str(e) in ("[Errno 11001] getaddrinfo failed", "timed out")
            else "No se encontró información válida del certificado."
        )
        observaciones.append(mensaje)
        return {
            "scan_date":     fecha_escaneo,
            "version":       nil,
            "emisor":        nil,
            "days_left":     None,
            "cipher_name":   nil,
            "risk":          "CRITICO",
            "observaciones": observaciones,
        }


# ── Helpers ────────────────────────────────────────────────────────────────────
def _clasificar_riesgo(puntaje: int) -> str:
    if puntaje >= 10:
        return "CRITICO"
    if puntaje >= 6:
        return "ALTO"
    if puntaje >= 3:
        return "MEDIO"
    return "BAJO"
