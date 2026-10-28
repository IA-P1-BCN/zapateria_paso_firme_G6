# Guía de despliegue y configuración (Paso Firme)

Documento para poner en producción la automatización y cambiar los bots de Telegram a una URL pública sin perder la configuración. Complementa al [README](../README.md) y a [AGENTS.md](../AGENTS.md).

## 1. Servicios y puertos

| Servicio | Local (desarrollo) | Producción (pública) | Interno (entre contenedores) |
|---|---|---|---|
| App de la tienda | `http://localhost:8000` | `https://<tu-dominio>/tienda` (si se expone) | `http://tienda:8000` |
| n8n | `http://localhost:5678` | `https://<tu-dominio>/n8n` o `https://n8n.<tu-dominio>` | `http://n8n:5678` |
| Webhook de eventos | — | `https://<tu-dominio>/webhook/tienda` | `http://n8n:5678/webhook/tienda` |

> Dentro de n8n **nunca** se usa `localhost` para llegar a la tienda: se usa `http://tienda:8000`. La app avisa a n8n en `http://n8n:5678/webhook/tienda` (variable `N8N_WEBHOOK_URL`).

## 2. Variables de entorno (`.env`)

| Variable | Para qué | Ejemplo |
|---|---|---|
| `API_KEY` | Clave de la API de la tienda (cabecera `X-API-Key`) | `UVK7eB_K-...` |
| `N8N_WEBHOOK_URL` | Dónde avisa la app a n8n | `http://n8n:5678/webhook/tienda` (vacío = sin avisos) |
| `SEED` | `1` carga datos de ejemplo al arrancar; `0` arranca vacía | `1` |
| `EMAIL_TIENDA` | Buzón de la tienda (remitente y destinatario de avisos) | `pasofirme.g6@gmail.com` |
| `UMBRAL_VENTA_GRANDE` | Importe a partir del cual una venta es "grande" | `80` |
| `N8N_EDITOR_BASE_URL` | URL pública/base de n8n usada por los flujos para construir enlaces (p. ej. confirmar solicitud) | `http://localhost:5678` (local) / `https://n8n.tu-dominio.com` (producción) |
| `WEBHOOK_TOKEN` | Token que la app envía en `X-Webhook-Token` al avisar a n8n (vacío = no envía avisos) | (vacío por defecto) |
| `TELEGRAM_CHAT_ID_MARISA` | Chat ID de Telegram de Marisa (avisos del asistente) | (obtener con @userinfobot) |

En producción cambia `N8N_EDITOR_BASE_URL` a la URL pública de n8n para que los enlaces enviados a Marisa (formulario de confirmación de solicitud) funcionen fuera de la red local.

## 3. Credenciales de n8n (sin valores)

Crearlas en n8n con **estos nombres exactos** (los flujos las referencian por nombre):

| Nombre | Tipo | Contenido |
|---|---|---|
| `Tienda API` | Header Auth | Cabecera `X-API-Key` con el valor de `API_KEY` |
| `Correo salida` | SMTP | Cuenta de correo de la tienda |
| `Correo entrada` | IMAP | La misma cuenta (para leer avisos del banco) |
| `Modelo IA` | Groq | Clave personal de https://console.groq.com |
| `Acceso Marisa` | Basic Auth | Usuario y contraseña de Marisa (formularios protegidos) |
| `Telegram Marisa` | Telegram API | Token del bot de Telegram de Marisa |

Los valores **nunca** se suben al repositorio.

## 4. Bots de Telegram: pasar a público

1. **Exponer n8n con HTTPS** (reverse proxy: Nginx/Caddy/Traefik o un túnel como Cloudflare Tunnel). n8n debe ser accesible desde Internet en `https://<tu-dominio>`.
2. En n8n, abre el flujo del asistente de Telegram (`Asistente cliente con agente IA`) y **publícalo** en una sola instancia. Al publicar, n8n registra el webhook del bot automáticamente; no lo registres a mano con la API de Telegram para evitar pisarlo.
3. Actualiza `N8N_EDITOR_BASE_URL` a la URL pública y reinicia n8n (`docker compose up -d`).
4. Prueba enviando un mensaje al bot desde Telegram.

> Solo una instancia de n8n debe tener el flujo publicado para evitar duplicados. Si cambias el dominio o el path, vuelve a publicar el flujo para que n8n actualice el webhook.

## 5. Flujos y cómo activarlos

- Importa los JSON de `workflows/` en n8n (menú del flujo → *Import from file*).
- En los nodos *Execute Workflow* (sub-workflows `SUB - …`) vuelve a elegir el sub-workflow: su id interno cambia en cada instancia.
- En cada flujo (salvo `08 - Error Workflow` y `SUB - Enviar notificación`) abre *Settings → Error workflow* y elige `08 - Error Workflow`.
- Publica solo en **una** instancia los flujos programados y los de formularios/webhooks.

Flujos principales: `00 - Entrada tienda`, `01` confirmación, `02` recibo, `03` abonos a distancia, `04` venta grande, `05` cierre diario, `06` recordatorios/vencimientos, `07` informe mensual, `08` error, más `Migración Excel`, `Entrada CSV del datáfono`, `Solicitudes de apartado`, `Confirmar solicitud de apartado`, `Asistente cliente`, `21 - Panel móvil para Marisa`.

## 6. Panel móvil para Marisa (T-021)

- URL: `https://<tu-dominio>/webhook/panel-marisa` (o `http://n8n:5678/webhook/panel-marisa` desde dentro).
- Autenticación: Basic Auth con la credencial `Acceso Marisa`. En producción debe ir **siempre detrás de HTTPS**, porque Basic Auth envía la contraseña en claro.
- La respuesta lleva `Cache-Control: no-store`: las cifras de caja no deben quedar en caché del móvil.
- Muestra: total cobrado hoy (ventas + abonos, desglose por forma de pago), apartados por vencer en 7 días y total pendiente de cobro.

## 7. Seguridad y datos personales

- No subir `.env` ni valores de credenciales.
- Los formularios públicos (solicitud de apartado) quedan vinculados con T-020 para aviso de privacidad y medidas anti-abuso.
- Los datos enviados a modelos de IA se limitan a lo imprescindible (asunto y cuerpo del correo en el flujo 03).

## 8. Copias de seguridad

- Volumen `n8n_data` contiene flujos y credenciales: haz copia periódica (`docker compose down` y backup del volumen, o exporta los JSON a `workflows/`).
- Volumen `tienda_data` contiene la base de datos SQLite de la tienda.
