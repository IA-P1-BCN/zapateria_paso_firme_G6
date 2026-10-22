# AGENTS.md — Zapatería Paso Firme (automatizaciones n8n)

Reglas para cualquier agente de IA (Claude Code, OpenCode, Codex…) y para las personas que trabajan en este repo. Si algo de aquí contradice una spec de `openspec/specs/`, gana la spec y se avisa de la contradicción.

## Qué es este proyecto
Automatizaciones con **n8n** alrededor de una app ya existente de la zapatería (FastAPI + SQLite + frontend). **La app NO se programa ni se modifica**: n8n la consulta y actúa sobre ella por su API.

Usuaria final: **Marisa**, dueña de la tienda. Los clientes reciben mensajes; Marisa recibe avisos y resúmenes.

Alcance actual: nivel **Esencial + Medio** (flujos 1, 2, 3, 5, 8, 4, 6, 7, migración del Excel y comparativa de dos modelos gratuitos). Avanzado y Experto quedan fuera hasta nuevo aviso.

## Negocio (lo que no se discute)
- Un **apartado** reserva un producto con un abono inicial mínimo de **5 €** y un plazo de **90 días**.
- Formas de pago: `efectivo`, `tarjeta`, `bizum`.
- Estados: `activo` → `liquidado` (automático al llegar pendiente a 0) o `vencido` (solo cuando alguien llama a `POST /api/apartados/{id}/vencer`).
- Al vencer, la app genera un **vale** (`VALE-00016`) por lo abonado.
- Detalle completo y verificable: `openspec/specs/reglas-apartado/`, `tienda-api/` y `tienda-webhook/`. Vocabulario: `docs/ontologia.md`.

## Servicios y direcciones
| Qué | Desde tu navegador | Desde dentro de n8n |
|---|---|---|
| App de la tienda | http://localhost:8000 | `http://tienda:8000` |
| n8n | http://localhost:5678 | — |
| Webhook (producción) | — | la app avisa a `http://n8n:5678/webhook/tienda` |

- Dentro de n8n NUNCA se usa `localhost` para llegar a la tienda.
- La app autentica con la cabecera `X-API-Key` (valor de `API_KEY` en `.env`). En n8n va en una credencial **Header Auth**, nunca escrita en un nodo.
- Webhook: URL de producción solo con el flujo **publicado**; `/webhook-test/tienda` solo mientras se construye.
- Cada persona ejecuta su propia instancia de n8n (`docker compose up -d`). Solo UNA instancia debe tener activo cada flujo programado.

## Convenciones de n8n
- **Nombres de flujo:** `01 - Confirmación de apartado`, `02 - Recibo de abono`… (número del briefing). Sub-workflows: `SUB - Enviar notificación`, `SUB - Buscar apartado`. Flujo de errores: `08 - Error Workflow`.
- **Nombres de nodo:** en español, sin el tipo de nodo en el nombre (nada de `HTTP Request1` ni `Switch`). Verbo en infinitivo si el nodo actúa (`Preparar entrada`, `Puntuar candidatos`), sustantivo si va a buscar un dato (`Apartado por id`), y pregunta con `¿ ?` si es un IF (`¿Busca por id?`). El flujo de errores (T-007) avisa a Marisa con el nombre del nodo que falló, así que tiene que decir qué hacía.
- **Un solo webhook** `/webhook/tienda` y un **Switch** por `$json.body.evento`. Los datos están en `$json.body.datos`.
- **Sub-workflows** para lo que se repite (enviar mensaje, buscar apartado). No copiar nodos entre flujos.
- **Credenciales:** mismo nombre en las dos instancias (ver lista en el README, sin valores).
- **Variables** para valores que cambian (por ejemplo el importe de "venta grande"): nunca fijos dentro del flujo.
- **Control de errores:** todo flujo tiene asignado `08 - Error Workflow` como flujo de error.
- **Exportación:** cada flujo se guarda como `workflows/<nombre>.json` (export de n8n) y se versiona en Git.

## Reglas para agentes (prohibiciones)
1. **No poner credenciales, claves ni tokens** en ningún JSON, spec, log ni commit. Los flujos solo referencian credenciales por nombre.
2. **No recalcular importes**: se usan `abonado`, `pendiente`, `precio` tal como los devuelve la app.
3. **No decidir dinero con IA.** El modelo solo extrae datos (por ejemplo ordenante, importe y concepto de un correo); las reglas (registrar, dudar, rechazar) son nodos deterministas.
4. **No publicar ni activar flujos** sin que lo pida una persona.
5. **No tocar `backend/` ni `frontend/`.**
6. **Antes de cada flujo, probar con un payload de ejemplo** (los de `tienda-webhook` y `data/correos/`) y enseñar el resultado.
7. **Si un caso es dudoso, no se registra nada y se pregunta a Marisa** (aviso), nunca se adivina.
8. **No inventar datos personales**: los de prueba son ficticios.

## Equipo y reparto
| Persona | GitHub | Tickets |
|---|---|---|
| Charlotte | `Charlottedoulcet` | `T-001`, `T-002`, `T-007`, `T-009`, `T-011` |
| Anna | `costanna` | `T-003`, `T-008`, `T-012`, `T-013` (con Charlotte) |
| Leandro | `Leandroletoile` | `T-004`, `T-005`, `T-006`, `T-010` |
| Todos | — | `T-000`, `T-014`, `T-015` |

Cada flujo es un JSON distinto en `workflows/`, así que no se pisan. Puntos compartidos (`AGENTS.md`, `README.md`, `docs/ai-log.md`): `ai-log.md` tiene una sección por persona; `AGENTS.md` y el README los toca una sola persona por PR. Cada PR la revisa alguien distinto de su autor.

## Calendario (entrega: jueves 29 de octubre de 2026, 23:59)
| Cuándo | Qué |
|---|---|
| Mié 21 – jue 22 | PR de setup (`T-000`), Docker en los tres equipos, `T-001` y `T-002`; contratos de los sub-workflows en sus specs |
| Vie 23 – lun 26 | Nivel Esencial: flujos 1, 2, 3, 5 y 8 (`T-003` a `T-008`) |
| Lun 26 (tarde) | **Puerta de control**: 5 flujos mergeados, 8 correos OK, demo alta → abonos → liquidación, AGENTS.md y bitácora al día |
| Mar 27 – mié 28 | Nivel Medio: `T-009` a `T-013` |
| Jue 29 | Cierre (`T-014`, `T-015`): evidencias, README, retrospectiva. **Objetivo: entregar antes de las 18:00**, el resto es margen |

## Forma de trabajo (SDD)
1. **Spec primero**: cada flujo es un *change* de OpenSpec (`openspec/changes/<nombre>/`) con propuesta, diseño, spec y tareas. Se valida con `openspec validate`.
2. Una persona valida la spec contra el briefing y la app **antes** de construir.
3. Se construye en n8n siguiendo las tareas del change y se exporta a `workflows/`.
4. **Al terminar, archivar el change (obligatorio):** `openspec validate <change> --strict` y luego `/opsx:archive` (OpenCode: `/opsx-archive`; o `openspec archive <change>`). Esto mueve el change a `openspec/changes/archive/` y pasa sus *ADDED Requirements* a `openspec/specs/`, que es lo que describe cómo funciona el sistema hoy. El archivo va en la misma PR del flujo. Está como última sección de cada `tasks.md` y de cada ticket.
5. Una rama y una PR por flujo, desde `dev`. **Nunca commits directos a `main` ni a `dev`.**
6. La otra persona revisa la PR (y `/codex:review` si hay créditos).

## Git: commits, ramas y PRs (en inglés)
- **Commits y títulos de PR en inglés**, formato Conventional Commits. El **scope es el ID del ticket de trabajo** (no el nombre del flujo): `feat(T-004): add appointment confirmation flow`.
- Tipos habituales: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`.
- **Rama:** `<tipo>/<ID-ticket>-<descripcion-corta>`, por ejemplo `feat/T-004-confirmation-flow`.
- La PR va hacia `dev` y enlaza el issue de GitHub en la descripción (`Closes #31`).
- **Dos clases de tickets:** las **historias de usuario** (`HU-01`…`HU-16`) y los **tickets de trabajo** `T-000`, `T-001`… (uno por change/flujo). Se nombran siempre por su ID (`HU-03`, `T-004`), no por el número de GitHub.
- Cada ticket de trabajo es **sub-issue** de su HU (así GitHub muestra el % de avance de la HU) y su cuerpo contiene todo el change (propuesta, diseño, tareas como checklist). Si no existe el ticket, se crea antes de empezar.

## Qué agente hace qué
El briefing recomienda OpenCode con modelos gratuitos y permite IA de pago si se delimita su alcance para no pisar el trabajo del equipo. Aquí:
- **OpenCode (modelos gratuitos):** agente principal para generar y depurar flujos de n8n.
- **Claude Code (de pago):** specs, tickets, documentos y revisión de PR. No edita flujos que está construyendo otra persona.
- Cada persona trabaja en su rama y sus tickets; el agente solo toca los archivos del ticket en curso.
- Los sub-workflows se llaman por identificador interno, que cambia entre instancias de n8n: tras importar un flujo, volver a elegirlos en los nodos *Execute Workflow*.

## Bitácora de IA
Cada vez que se usa un agente para algo relevante se anota en `docs/ai-log.md`: qué herramienta y modelo, qué se pidió, qué salió, qué se corrigió a mano y qué se aprendió. Se anota también cuando la IA se equivoca.

## Idioma
Todos los documentos (este archivo, specs, ontología, issues, README) en **español**. **Excepción: commits y títulos/descripciones de PR en inglés** (ver sección Git). Los identificadores técnicos (`SHALL`, `WHEN/THEN`, nombres de campos de la API) se dejan como están.

## Comandos útiles
Ver `CLAUDE.md` (sección Commands).
