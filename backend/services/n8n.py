"""SERVICIO · Avisar a n8n por webhook cuando pasa algo en la tienda."""

import json
import logging
import urllib.request

import config

log = logging.getLogger("tienda")


def avisar(evento, datos):
    """Envía el evento autenticado a n8n. Si n8n no responde, la tienda sigue funcionando."""
    if not config.N8N_WEBHOOK_URL:
        return

    if not config.WEBHOOK_TOKEN:
        log.warning("No se pudo avisar a n8n (%s): falta WEBHOOK_TOKEN", evento)
        return

    cuerpo = json.dumps(
        {"evento": evento, "datos": datos},
        default=str,
    ).encode()

    cabeceras = {
        "Content-Type": "application/json",
        "X-Webhook-Token": config.WEBHOOK_TOKEN,
    }

    peticion = urllib.request.Request(
        config.N8N_WEBHOOK_URL,
        data=cuerpo,
        headers=cabeceras,
        method="POST",
    )

    try:
        urllib.request.urlopen(peticion, timeout=5)
    except Exception as e:
        log.warning("No se pudo avisar a n8n (%s): %s", evento, e)
