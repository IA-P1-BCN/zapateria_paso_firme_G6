# Guía del equipo: puesta en marcha y dónde está cada cosa

Para las tres personas del equipo. Se hace **una vez por persona**, en su propio ordenador. Cada persona ejecuta su propia instancia de n8n.

## 1. Qué hay en el repositorio

| Qué | Dónde |
|---|---|
| Enunciado del briefing | `README.md` |
| Guía de la app de la tienda | `docs/guia-de-la-app.md` |
| Reglas para personas y agentes de IA | `AGENTS.md` (Claude Code lo lee desde `CLAUDE.md`) |
| Specs de cómo funciona la app hoy | `openspec/specs/` (`tienda-api`, `tienda-webhook`, `reglas-apartado`) |
| Un change por cada flujo o tarea | `openspec/changes/<nombre>/` (propuesta, diseño, spec, tareas) |
| Vocabulario del negocio | `docs/ontologia.md` |
| Mapa del proceso (hoy y automatizado) | `docs/proceso-apartado-hoy.mmd` y `docs/proceso-apartado-automatizado.mmd` |
| Flujos de n8n exportados | `workflows/` (un JSON por flujo) |
| Bitácora de uso de IA | `docs/ai-log.md` (una sección por persona) |
| Tickets | Tablero de GitHub (proyecto 41): `HU-01`…`HU-16` y `T-000`…`T-022` |

Nota: el briefing habla de una carpeta `specs/`. Nosotros usamos `openspec/specs` y `openspec/changes`, que es lo mismo con la herramienta OpenSpec.

## 2. Poner en marcha (cada persona)

1. Abre Docker Desktop.
2. Copia las variables: `cp .env.example .env`.
3. Rellena el `.env` (ver sección 3). **El `.env` no se sube nunca a Git.**
4. `docker compose up -d` (tienda en http://localhost:8000, n8n en http://localhost:5678).
5. Crea tu cuenta de n8n en http://localhost:5678.
6. Crea las credenciales de la sección 4.

## 3. Variables del `.env`

| Variable | Qué es | Valor |
|---|---|---|
| `API_KEY` | Clave de la app de la tienda | La eliges tú; puede ser distinta en cada persona |
| `N8N_WEBHOOK_URL` | Dónde avisa la app a n8n | La que indica `.env.example` |
| `SEED` | Datos de ejemplo al arrancar | Dejar el valor de `.env.example` |
| `EMAIL_TIENDA` | Dirección de correo de la tienda (avisos a la tienda) | La dirección del buzón compartido del equipo; se pasa en privado |
| `UMBRAL_VENTA_GRANDE` | Importe en € a partir del cual una venta es "grande" | `80` |

Si falta alguna de las dos últimas en tu `.env.example`, añádelas. En `.env.example` **`EMAIL_TIENDA` va vacío** (el repositorio es público); el valor real solo va en tu `.env`.

Dentro de un flujo se leen así: `{{ $env.UMBRAL_VENTA_GRANDE }}` y `{{ $env.EMAIL_TIENDA }}`. Para que `$env` funcione, `docker-compose.yml` ya incluye `N8N_BLOCK_ENV_ACCESS_IN_NODE=false`.

## 4. Credenciales de n8n (mismos nombres para todos)

Los flujos solo guardan el **nombre** de la credencial, nunca el valor. Por eso los nombres deben ser idénticos en las tres instancias. Se crean en n8n → Credentials.

| Nombre | Tipo | Datos |
|---|---|---|
| `Tienda API` | Header Auth | Nombre de cabecera `X-API-Key`; valor = el `API_KEY` de tu `.env` |
| `Correo salida` | SMTP | Host `smtp.gmail.com`, puerto `465`, SSL activado; usuario = buzón compartido; contraseña = contraseña de aplicación |
| `Correo entrada` | IMAP | Host `imap.gmail.com`, puerto `993`, SSL activado; mismos usuario y contraseña de aplicación |
| `Modelo IA` | Groq | Tu propia clave de https://console.groq.com (cada persona crea la suya) |

Contraseña de aplicación de Gmail: se crea en la cuenta de Google con la verificación en dos pasos activada (Seguridad → Contraseñas de aplicaciones). Se comparte **en privado** (mensaje directo o gestor de contraseñas), nunca en el chat de una IA, en GitHub ni en un fichero del repositorio.

## 5. Qué no se sube nunca a Git

- `.env` y cualquier clave, token o contraseña.
- Valores de credenciales dentro de un JSON de flujo (revisar el export antes de subirlo).
- La dirección real del buzón en documentos o en `.env.example`.

## 6. Cómo trabajamos (resumen; el detalle está en `AGENTS.md`)

1. Coge un ticket `T-XXX` de tu lista y léelo entero: su cuerpo es el change completo.
2. Rama desde `dev`: `feat/T-004-confirmation-flow`.
3. Construye el flujo en n8n siguiendo las tareas y pruébalo con un payload de ejemplo.
4. Exporta el flujo a `workflows/` y revisa que no lleve claves.
5. Commits en inglés con el ticket como scope: `feat(T-004): add appointment confirmation flow`.
6. PR hacia `dev` en inglés, con `Closes #N`. La revisa otra persona.
7. Archiva el change (`/opsx:archive` o `openspec archive <change>`) en la misma PR.
8. Anota en `docs/ai-log.md` lo relevante del uso de IA, también los errores.

Solo **una instancia** debe tener activo un flujo programado o el que lee el correo (flujo 3); si no, el mismo abono se registraría varias veces.

## 7. Reparto

| Persona | Tickets |
|---|---|
| Charlotte | `T-001`, `T-002`, `T-007`, `T-009`, `T-011` |
| Anna | `T-003`, `T-008`, `T-012`, `T-013` (con Charlotte) |
| Leandro | `T-004`, `T-005`, `T-006`, `T-010` |
| Todos | `T-000`, `T-014`, `T-015` |

Entrega: **jueves 29 de octubre de 2026, 23:59** (objetivo: antes de las 18:00). Puerta de control el lunes 26 por la tarde.

## 8. Decisiones abiertas

- Forma de pago de las transferencias (la app solo admite `efectivo`, `tarjeta` y `bizum`).
- Dónde guardar el histórico de cierres diarios (T-006).
- Horas de los flujos programados: cierre 22:00, recordatorios 09:00, informe el día 1 a las 08:00.
