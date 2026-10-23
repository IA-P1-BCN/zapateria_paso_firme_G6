# 👟 Zapatería Paso Firme · Automatizaciones con n8n (G6)

**[Español](#-español)** · **[English](#-english)**

---

## 🇪🇸 Español

### Qué es

Paso Firme es una zapatería de barrio cuyo servicio estrella son los **apartados**: el cliente reserva unos zapatos con un abono inicial (mínimo 5 €) y los paga poco a poco en un plazo de 90 días. La tienda ya tiene una app (FastAPI + SQLite) donde se registran apartados, abonos y ventas.

Este repositorio **no modifica la app**: construye con **n8n** todo lo que pasa a su alrededor (avisar a los clientes, registrar los pagos que llegan por Bizum o transferencia, cerrar la caja, recordar vencimientos, informar a Marisa, la dueña). El enunciado completo del proyecto está en [ENUNCIADO.md](ENUNCIADO.md).

### Flujos

| # | Flujo | Disparador | Ticket | Responsable |
|---|---|---|---|---|
| — | Base del webhook y credenciales | Webhook `/webhook/tienda` | T-001 | Charlotte |
| — | `SUB - Enviar notificación` | Llamado por otros flujos | T-002 | Charlotte |
| — | `SUB - Buscar apartado` | Llamado por otros flujos | T-003 | Anna |
| 1 | Confirmación de apartado | Evento `apartado.creado` | T-004 | Leandro |
| 2 | Recibo de abono | Evento `abono.registrado` | T-005 | Leandro |
| 5 | Cierre diario | Programado, 22:00 | T-006 | Leandro |
| 8 | Error Workflow | Error en cualquier flujo | T-007 | Charlotte |
| 3 | Abonos a distancia (Bizum y transferencia) | Correo del banco (IMAP) | T-008 | Anna |
| 6 | Recordatorios y vencimientos | Programado, 09:00 | T-009 | Charlotte |
| 4 | Venta grande | Evento `venta.registrada` | T-010 | Leandro |
| 7 | Informe mensual | Programado, día 1 a las 08:00 | T-011 | Charlotte |
| — | Migración del Excel de Marisa | Manual, una sola vez | T-012 | Anna |
| — | Comparativa de dos modelos gratuitos | — | T-013 | Anna y Charlotte |

El estado de cada ticket está en el [tablero Kanban](https://github.com/orgs/IA-P1-BCN/projects/41). Alcance: niveles **Esencial** y **Medio** del enunciado.

### Cómo funciona

| Pieza | Desde el navegador | Desde dentro de n8n |
|---|---|---|
| App de la tienda | http://localhost:8000 (API en `/docs`) | `http://tienda:8000` |
| n8n | http://localhost:5678 | — |
| Webhook de eventos | — | la app avisa a `http://n8n:5678/webhook/tienda` |

- La app avisa a n8n por **un único webhook**; un nodo **Switch** reparte por `evento` (`apartado.creado`, `abono.registrado`, `venta.registrada`…).
- n8n consulta y actúa sobre la app por su **API REST** con la cabecera `X-API-Key`.
- Los importes (`abonado`, `pendiente`, `precio`) los calcula siempre la app; los flujos no los recalculan.
- En el flujo 3 la IA **solo extrae** ordenante, importe y concepto del correo. Registrar, dudar o rechazar lo deciden nodos deterministas. Si algo es dudoso, no se registra nada y se pregunta a Marisa.

### 🚀 Cómo empezar

Necesitas [Git](https://git-scm.com/) y [Docker Desktop](https://www.docker.com/products/docker-desktop/) abiertos. Cada persona del equipo tiene **su propia instancia de n8n**.

```bash
git clone https://github.com/IA-P1-BCN/zapateria_paso_firme_G6.git paso-firme
cd paso-firme
cp .env.example .env        # y rellena los valores (ver tabla de variables)
docker compose up -d        # tienda en :8000, n8n en :5678
```

1. Abre http://localhost:5678 y crea tu cuenta local de n8n.
2. Crea las credenciales de la tabla siguiente, **con estos nombres exactos**.
3. Importa los flujos de [`workflows/`](workflows/) (menú del flujo → *Import from file*).
4. En los flujos que llaman a un sub-workflow (`SUB - …`), vuelve a elegirlo en el nodo *Execute Workflow*: su identificador interno cambia en cada instancia.
5. En cada flujo (salvo `08 - Error Workflow` y `SUB - Enviar notificación`), abre *Settings → Error workflow* y elige `08 - Error Workflow`: su identificador también cambia en cada instancia.

Para pararlo: `docker compose down`. Para borrar también los datos: `docker compose down -v`.

### Variables y credenciales (sin valores)

| Variable del `.env` | Para qué |
|---|---|
| `API_KEY` | Clave que la app exige en la cabecera `X-API-Key` |
| `N8N_WEBHOOK_URL` | Dónde avisa la app a n8n (valor de `.env.example`) |
| `SEED` | `1` carga datos de ejemplo al arrancar; `0` arranca vacía (migración) |
| `EMAIL_TIENDA` | Buzón de la tienda: recibe los avisos a Marisa y es también el remitente de los correos |
| `UMBRAL_VENTA_GRANDE` | Importe en € a partir del cual una venta es "grande" (por defecto `80`) |

Dentro de un flujo se leen con `{{ $env.NOMBRE }}`.

| Credencial de n8n | Tipo | Qué lleva |
|---|---|---|
| `Tienda API` | Header Auth | Cabecera `X-API-Key` con el valor de `API_KEY` |
| `Correo salida` | SMTP | Cuenta de correo de la tienda |
| `Correo entrada` | IMAP | La misma cuenta, para leer los avisos del banco |
| `Modelo IA` | Groq | Clave personal de https://console.groq.com |

Los flujos solo guardan el **nombre** de la credencial. El `.env` y los valores de las credenciales no se suben nunca al repositorio.

### Contratos de los sub-workflows

#### `SUB - Buscar apartado` (T-003)

Busca el apartado de una persona a partir de un identificador o de un nombre escrito de cualquier manera (`JORGE M.`, `LUCIA GOMEZ`). Solo lee de la API y solo devuelve apartados en estado `activo`.

**Entrada** (*Execute Workflow*):

| Campo | Tipo | Ejemplo | Nota |
|---|---|---|---|
| `id` | número o texto | `12`, `#12` | Si es válido, se busca por id y se ignora `texto` |
| `texto` | texto | `JORGE M. apartado 2 bota` | Normalmente ordenante + concepto del pago |

**Salida:**

```json
{
  "resultado": "unico | varios | ninguno",
  "candidatos": [
    { "id": 2, "cliente": "Jorge Martín", "producto": "Bota alta mujer", "talla": "36",
      "precio": 119, "abonado": 40, "pendiente": 79, "fecha_limite": "2027-01-15", "estado": "activo" }
  ]
}
```

- El texto se compara sin mayúsculas, acentos ni puntuación, por trozos de 3 letras o más (`de`, `del`, `la`… se ignoran). Gana el apartado que coincide con más trozos; si empatan varios, `varios`.
- Un número en el texto (`#2`, `apartado 2`) solo se usa si ese apartado también coincide con algún trozo del nombre.
- Un id inexistente (404) o un apartado no activo devuelve `ninguno`. Cualquier otro error de la app (401, 500) **lanza error**, para no confundirlo con "no encontrado".
- Para que otro flujo lo llame, el sub-workflow tiene que estar **publicado** en esa instancia de n8n.

#### `SUB - Enviar notificación` (T-002)

Envía un correo de texto a una clienta o a la tienda (Marisa). Lo usan los flujos que avisan por correo. Usa la credencial `Correo salida` y la variable `EMAIL_TIENDA`. **Nunca lanza error al flujo que lo llama**: el resultado dice si se envió.

**Entrada** (*Execute Workflow*):

| Campo | Tipo | Ejemplo | Nota |
|---|---|---|---|
| `destinatario` | texto | `cliente`, `tienda` | `tienda` envía a `EMAIL_TIENDA` |
| `email` | texto | `carmen@example.com` | Solo para `cliente`; puede venir vacío o no venir |
| `asunto` | texto | `Tu apartado en Paso Firme` | |
| `mensaje` | texto | `Hola Carmen, hemos registrado tu apartado.` | Texto plano |
| `contexto` | texto | `Apartado 25 - Carmen Ruiz` | Opcional; identifica el apartado en el aviso a la tienda |

**Salida:**

```json
{ "enviado": true, "motivo": "" }
```

| `enviado` | `motivo` | Cuándo |
|---|---|---|
| `true` | `""` | Correo enviado a la clienta o a la tienda |
| `false` | `sin_email` | `cliente` sin `email`: no se envía a la clienta y se avisa a la tienda con el `contexto` |
| `false` | `error_envio` | Falló el servidor de correo, o `destinatario` no es `cliente` ni `tienda` |

- Quien lo llama no tiene que capturar errores: mira `enviado` y, si es `false`, `motivo`.
- Para que otro flujo lo llame, el sub-workflow tiene que estar **publicado** en esa instancia de n8n.

### Estructura del repositorio

| Ruta | Qué hay |
|---|---|
| `workflows/` | Flujos de n8n exportados en JSON, uno por flujo |
| `openspec/specs/` | Cómo funciona hoy el sistema (API, webhook, reglas del apartado) |
| `openspec/changes/` | Un change de OpenSpec por ticket: propuesta, diseño, spec y tareas |
| `docs/` | [Guía de la app](docs/guia-de-la-app.md), [guía del equipo](docs/guia-del-equipo.md), [ontología](docs/ontologia.md), mapas del proceso y [bitácora de IA](docs/ai-log.md) |
| `data/` | Excel antiguo de Marisa (CSV) y correos de ejemplo del banco |
| `backend/`, `frontend/` | App de la tienda (no se modifica) |
| `AGENTS.md` | Reglas para personas y agentes de IA |
| `ENUNCIADO.md` | Enunciado original del proyecto |

### Forma de trabajo

- **Gitflow:** `main` ← `dev` ← ramas `feat/T-XXX-…`. Las PR van siempre a `dev`, con revisión de otra persona.
- **Spec primero:** cada flujo es un change de OpenSpec; al terminar se archiva en la misma PR.
- Commits y PR en inglés con el ticket como scope: `feat(T-003): …`. Documentación en español.
- El uso de IA se anota en [`docs/ai-log.md`](docs/ai-log.md), errores incluidos. Detalle completo en [AGENTS.md](AGENTS.md).

### Equipo

| Persona | GitHub |
|---|---|
| Charlotte | [@Charlottedoulcet](https://github.com/Charlottedoulcet) |
| Leandro | [@Leandroletoile](https://github.com/Leandroletoile) |
| Anna | [@costanna](https://github.com/costanna) |

---

## 🇬🇧 English

### What it is

Paso Firme is a neighbourhood shoe shop whose key service is **layaway** (*apartado*): the customer reserves a pair of shoes with a down payment (at least €5) and pays the rest in instalments within 90 days. The shop already has an app (FastAPI + SQLite) to record layaways, payments and sales.

This repository **does not change the app**. It uses **n8n** to automate everything around it: notifying customers, recording payments that arrive by Bizum or bank transfer, closing the till, reminding customers of deadlines and reporting to Marisa, the owner. The full project brief (in Spanish) is in [ENUNCIADO.md](ENUNCIADO.md).

### Workflows

| # | Workflow | Trigger | Ticket | Owner |
|---|---|---|---|---|
| — | Webhook base and credentials | Webhook `/webhook/tienda` | T-001 | Charlotte |
| — | `SUB - Enviar notificación` (send notification) | Called by other workflows | T-002 | Charlotte |
| — | `SUB - Buscar apartado` (find layaway) | Called by other workflows | T-003 | Anna |
| 1 | Layaway confirmation | `apartado.creado` event | T-004 | Leandro |
| 2 | Payment receipt | `abono.registrado` event | T-005 | Leandro |
| 5 | Daily close | Scheduled, 22:00 | T-006 | Leandro |
| 8 | Error Workflow | Error in any workflow | T-007 | Charlotte |
| 3 | Remote payments (Bizum and transfer) | Bank email (IMAP) | T-008 | Anna |
| 6 | Reminders and expiries | Scheduled, 09:00 | T-009 | Charlotte |
| 4 | Large sale alert | `venta.registrada` event | T-010 | Leandro |
| 7 | Monthly report | Scheduled, 1st of the month at 08:00 | T-011 | Charlotte |
| — | Migration of Marisa's spreadsheet | Manual, run once | T-012 | Anna |
| — | Comparison of two free AI models | — | T-013 | Anna and Charlotte |

Ticket status lives on the [Kanban board](https://github.com/orgs/IA-P1-BCN/projects/41). Scope: the brief's **Essential** and **Intermediate** levels.

### How it works

| Piece | From your browser | From inside n8n |
|---|---|---|
| Shop app | http://localhost:8000 (API at `/docs`) | `http://tienda:8000` |
| n8n | http://localhost:5678 | — |
| Event webhook | — | the app calls `http://n8n:5678/webhook/tienda` |

- The app notifies n8n through **a single webhook**; a **Switch** node routes on `evento` (`apartado.creado`, `abono.registrado`, `venta.registrada`…).
- n8n reads from and acts on the app through its **REST API**, using the `X-API-Key` header.
- Amounts (`abonado`, `pendiente`, `precio`) always come from the app; workflows never recalculate them.
- In workflow 3, AI **only extracts** payer, amount and reference from the email. Deterministic nodes decide whether to record, ask or reject. When in doubt, nothing is recorded and Marisa is asked.

### 🚀 Getting started

You need [Git](https://git-scm.com/) and [Docker Desktop](https://www.docker.com/products/docker-desktop/) running. Each team member runs **their own n8n instance**.

```bash
git clone https://github.com/IA-P1-BCN/zapateria_paso_firme_G6.git paso-firme
cd paso-firme
cp .env.example .env        # then fill in the values (see the variables table)
docker compose up -d        # shop on :8000, n8n on :5678
```

1. Open http://localhost:5678 and create your local n8n account.
2. Create the credentials in the table below, **with these exact names**.
3. Import the workflows from [`workflows/`](workflows/) (workflow menu → *Import from file*).
4. In workflows that call a sub-workflow (`SUB - …`), pick it again in the *Execute Workflow* node: its internal ID differs on every instance.
5. In every workflow (except `08 - Error Workflow` and `SUB - Enviar notificación`), open *Settings → Error workflow* and pick `08 - Error Workflow`: its ID also differs on every instance.

To stop: `docker compose down`. To also delete the data: `docker compose down -v`.

### Variables and credentials (no values)

| `.env` variable | Purpose |
|---|---|
| `API_KEY` | Key the app requires in the `X-API-Key` header |
| `N8N_WEBHOOK_URL` | Where the app notifies n8n (value from `.env.example`) |
| `SEED` | `1` loads sample data on start; `0` starts empty (migration) |
| `EMAIL_TIENDA` | Shop mailbox: receives the alerts to Marisa and is also the sender of the emails |
| `UMBRAL_VENTA_GRANDE` | Amount in € from which a sale counts as "large" (default `80`) |

Inside a workflow they are read with `{{ $env.NAME }}`.

| n8n credential | Type | Contents |
|---|---|---|
| `Tienda API` | Header Auth | `X-API-Key` header with the `API_KEY` value |
| `Correo salida` | SMTP | Shop email account |
| `Correo entrada` | IMAP | Same account, to read bank notifications |
| `Modelo IA` | Groq | Personal key from https://console.groq.com |

Workflows only store the credential **name**. The `.env` file and credential values are never committed.

### Sub-workflow contracts

#### `SUB - Buscar apartado` (T-003)

Finds a person's layaway from an ID or from a name written in any form (`JORGE M.`, `LUCIA GOMEZ`). It only reads from the API and only returns layaways whose status is `activo`.

**Input** (*Execute Workflow*):

| Field | Type | Example | Note |
|---|---|---|---|
| `id` | number or text | `12`, `#12` | If valid, the search is by ID and `texto` is ignored |
| `texto` | text | `JORGE M. apartado 2 bota` | Usually the payment's payer + reference |

**Output:**

```json
{
  "resultado": "unico | varios | ninguno",
  "candidatos": [
    { "id": 2, "cliente": "Jorge Martín", "producto": "Bota alta mujer", "talla": "36",
      "precio": 119, "abonado": 40, "pendiente": 79, "fecha_limite": "2027-01-15", "estado": "activo" }
  ]
}
```

- Text is compared ignoring case, accents and punctuation, in chunks of 3+ letters (`de`, `del`, `la`… are skipped). The layaway matching the most chunks wins; a tie returns `varios`.
- A number in the text (`#2`, `apartado 2`) is only used if that layaway also matches part of the name.
- A missing ID (404) or a non-active layaway returns `ninguno`. Any other app error (401, 500) **raises an error**, so it is never mistaken for "not found".
- To be called from another workflow, the sub-workflow must be **published** on that n8n instance.

#### `SUB - Enviar notificación` (T-002)

Sends a plain-text email to a customer or to the shop (Marisa). Used by the workflows that notify by email. It uses the `Correo salida` credential and the `EMAIL_TIENDA` variable. It **never raises an error to its caller**: the result says whether the email was sent.

**Input** (*Execute Workflow*):

| Field | Type | Example | Note |
|---|---|---|---|
| `destinatario` | text | `cliente`, `tienda` | `tienda` sends to `EMAIL_TIENDA` |
| `email` | text | `carmen@example.com` | Only for `cliente`; may be empty or missing |
| `asunto` | text | `Tu apartado en Paso Firme` | |
| `mensaje` | text | `Hola Carmen, hemos registrado tu apartado.` | Plain text |
| `contexto` | text | `Apartado 25 - Carmen Ruiz` | Optional; identifies the layaway in the alert to the shop |

**Output:**

```json
{ "enviado": true, "motivo": "" }
```

| `enviado` | `motivo` | When |
|---|---|---|
| `true` | `""` | Email sent to the customer or to the shop |
| `false` | `sin_email` | `cliente` without `email`: nothing is sent to the customer and the shop is alerted with the `contexto` |
| `false` | `error_envio` | The mail server failed, or `destinatario` is neither `cliente` nor `tienda` |

- The caller does not need to catch errors: it checks `enviado` and, if `false`, `motivo`.
- To be called from another workflow, the sub-workflow must be **published** on that n8n instance.

### Repository layout

| Path | Contents |
|---|---|
| `workflows/` | n8n workflows exported as JSON, one per workflow |
| `openspec/specs/` | How the system works today (API, webhook, layaway rules) |
| `openspec/changes/` | One OpenSpec change per ticket: proposal, design, spec and tasks |
| `docs/` | [App guide](docs/guia-de-la-app.md), [team guide](docs/guia-del-equipo.md), [ontology](docs/ontologia.md), process maps and [AI log](docs/ai-log.md) (in Spanish) |
| `data/` | Marisa's old spreadsheet (CSV) and sample bank emails |
| `backend/`, `frontend/` | Shop app (not modified) |
| `AGENTS.md` | Rules for people and AI agents |
| `ENUNCIADO.md` | Original project brief |

### How we work

- **Gitflow:** `main` ← `dev` ← `feat/T-XXX-…` branches. PRs always target `dev` and are reviewed by someone else.
- **Spec first:** each workflow is an OpenSpec change, archived in the same PR when done.
- Commits and PRs in English with the ticket as scope: `feat(T-003): …`. Documentation in Spanish.
- AI usage is logged in [`docs/ai-log.md`](docs/ai-log.md), mistakes included. Full details in [AGENTS.md](AGENTS.md).

### Team

| Person | GitHub |
|---|---|
| Charlotte | [@Charlottedoulcet](https://github.com/Charlottedoulcet) |
| Leandro | [@Leandroletoile](https://github.com/Leandroletoile) |
| Anna | [@costanna](https://github.com/costanna) |
