"""Valida los flujos exportados de n8n (T-022).

Falla si un JSON no es válido o si lleva algo que parece una clave. Solo avisa de lo que conviene
revisar pero no es un secreto (flujo publicado, sin flujo de errores, identificador de la instancia).

Uso: python .github/scripts/validar_flujos.py workflows
"""

import json
import re
import sys
from pathlib import Path

# Claves con formato conocido: no deben aparecer nunca en un export.
PATRONES_CLAVE = {
    "clave de Groq": re.compile(r"gsk_[A-Za-z0-9]{20,}"),
    "clave tipo OpenAI": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    "token de bot de Telegram": re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b"),
    "clave privada": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "URL con usuario y contraseña": re.compile(r"[a-z][a-z0-9+.-]*://[^/\s:@\"]+:[^/\s@\"]+@"),
}
# Campos que en un nodo no pueden llevar un valor escrito: o una expresión (={{ ... }}) o nada.
CAMPOS_SENSIBLES = re.compile(r"^(password|passwd|apiKey|api_key|secret|clientSecret|accessToken|token)$", re.I)
# Flujos que no llevan "08 - Error Workflow": él mismo y el sub-workflow que usa (evita un bucle de avisos).
SIN_FLUJO_DE_ERRORES = {"08 - Error Workflow", "SUB - Enviar notificación"}


def campos_con_valor(obj, ruta=""):
    """Devuelve las rutas de campos sensibles que tienen un valor escrito (no una expresión)."""
    encontrados = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            r = f"{ruta}.{k}" if ruta else k
            if CAMPOS_SENSIBLES.match(k) and isinstance(v, str) and v.strip() and not v.startswith("="):
                encontrados.append(r)
            encontrados += campos_con_valor(v, r)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            encontrados += campos_con_valor(v, f"{ruta}[{i}]")
    return encontrados


def revisar(fichero: Path):
    errores, avisos = [], []
    texto = fichero.read_text(encoding="utf-8")
    try:
        flujo = json.loads(texto)
    except json.JSONDecodeError as e:
        return [f"no es un JSON válido ({e})"], avisos

    if not isinstance(flujo, dict) or not isinstance(flujo.get("nodes"), list) or not isinstance(flujo.get("connections"), dict):
        errores.append("no parece un export de n8n (faltan 'nodes' o 'connections')")
        return errores, avisos

    for nombre, patron in PATRONES_CLAVE.items():
        if patron.search(texto):
            errores.append(f"contiene algo que parece una {nombre}")

    for nodo in flujo["nodes"]:
        nombre_nodo = nodo.get("name", "?")
        for tipo, cred in (nodo.get("credentials") or {}).items():
            extra = set(cred) - {"id", "name"} if isinstance(cred, dict) else {"(formato raro)"}
            if extra:
                errores.append(f"nodo «{nombre_nodo}»: la credencial {tipo} lleva más que su nombre ({', '.join(sorted(extra))})")
        for ruta in campos_con_valor(nodo.get("parameters") or {}):
            errores.append(f"nodo «{nombre_nodo}»: el campo {ruta} tiene un valor escrito; debe ir en una credencial o variable")

    nombre = flujo.get("name", fichero.stem)
    if flujo.get("active"):
        avisos.append("se exportó publicado (active: true); al importarlo conviene revisarlo antes de publicarlo")
    if nombre not in SIN_FLUJO_DE_ERRORES and not (flujo.get("settings") or {}).get("errorWorkflow"):
        avisos.append("no tiene asignado '08 - Error Workflow'")
    if (flujo.get("meta") or {}).get("instanceId"):
        avisos.append("lleva el identificador de la instancia de n8n (meta.instanceId)")
    return errores, avisos


def main(carpeta: str) -> int:
    ficheros = sorted(Path(carpeta).glob("*.json"))
    if not ficheros:
        print(f"No hay flujos en {carpeta}")
        return 1
    total_errores = 0
    for f in ficheros:
        errores, avisos = revisar(f)
        estado = "ERROR" if errores else ("aviso" if avisos else "ok")
        print(f"[{estado}] {f.name}")
        for e in errores:
            print(f"    ✗ {e}")
            # Anotación para que GitHub lo marque en la PR
            print(f"::error file={f.as_posix()}::{e}")
        for a in avisos:
            print(f"    · {a}")
            print(f"::warning file={f.as_posix()}::{a}")
        total_errores += len(errores)
    print(f"\n{len(ficheros)} flujos revisados, {total_errores} errores.")
    return 1 if total_errores else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "workflows"))
