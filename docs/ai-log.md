# Bitácora de uso de IA

Se anota cada uso relevante de un agente: qué herramienta y modelo, qué se pidió, qué salió, qué se corrigió a mano y qué se aprendió. **También cuando la IA se equivoca.** Sin claves ni datos personales reales.

## Plantilla
```
### AAAA-MM-DD · T-XXX · <tema>
- Herramienta / modelo:
- Qué se pidió:
- Qué salió:
- Qué se corrigió a mano:
- Aprendizaje:
```

## Entradas

### 2026-10-21 · T-000 · Specs de base leyendo el código de la app
- Herramienta / modelo: Claude Code (Sonnet 5.5).
- Qué se pidió: describir cómo funciona hoy la app (API, webhook y reglas de apartado) como specs verificables.
- Qué salió: `tienda-api`, `tienda-webhook` y `reglas-apartado`, validadas con `openspec validate --specs`.
- Qué se corrigió a mano: pendiente de revisión por la pareja contra la app.
- Aprendizaje: la guía de la app simplifica un detalle (los errores de validación devuelven `detail` como lista, no como texto); hay que fiarse del código y no de la guía. La búsqueda `q` es por subcadena y no ignora acentos, así que el flujo 3 debe buscar por trozos. Al vencer, la app devuelve `{apartado, vale}`.

### 2026-10-21 · T-000 · Reglas para los agentes y herramientas
- Herramienta / modelo: Claude Code (Sonnet 5.5).
- Qué se pidió: `AGENTS.md` y `CLAUDE.md` con prohibiciones y convenciones de n8n, e instalar OpenSpec, `n8n-mcp` y n8n-skills.
- Qué salió: ocho prohibiciones (sin credenciales en JSON, no recalcular importes, la IA no decide dinero…), forma de trabajo con OpenSpec y archivado obligatorio de cada change.
- Qué se corrigió a mano: se decidió que documentos y tickets van en español y commits y PR en inglés, con el ID del ticket como scope.
- Aprendizaje: Claude Code no lee `AGENTS.md` por sí solo; `CLAUDE.md` lo importa con `@AGENTS.md`.

### 2026-10-21 · T-000 · Creación masiva de tickets: la IA se equivocó
- Herramienta / modelo: Claude Code (Sonnet 5.5).
- Qué se pidió: 22 tickets de GitHub, uno por change, como sub-issue de su historia, con etiquetas, tamaño y fecha.
- Qué salió: los 22 tickets (#17…#39), pero el script tenía fallos: `declare -A` (no existe en el bash de macOS), un tipo `Date` que la API rechaza, y algunos tickets quedaron sin estado ni tamaño porque el proyecto ya los había añadido solo.
- Qué se corrigió a mano: se detectó al comprobar el tablero y se repasó ticket por ticket.
- Aprendizaje: comprobar siempre el resultado en GitHub después de una operación masiva; crear de uno en uno con pausa evita bloqueos.

### 2026-10-22 · T-003 · SUB - Buscar apartado
- Herramienta / modelo: Claude Code (Opus 5.5).
- Qué se pidió: construir el sub-workflow de búsqueda tolerante (por `id` o por texto) siguiendo el change de T-003.
- Qué salió: la lógica de normalizar, trocear y puntuar se probó primero en Node contra los apartados reales de la API (12 casos y empates sintéticos) y después dentro de n8n con un flujo de prueba temporal: 12 casos correctos, también los liquidados (`ninguno`) y el id inexistente (404 → `ninguno`).
- Qué se corrigió a mano: (1) la expresión `[̀-ͯ]` para quitar acentos se rompía al incrustar el código en el JSON del flujo; se cambió por `\p{M}`. (2) El export por CLI de n8n incluía el bloque `shared` con el nombre y el correo de la dueña de la instancia; se dejó solo lo que exporta el botón *Download*. (3) Se probó primero llamando al sub-workflow desde otro flujo, pero n8n 2.x solo ejecuta sub-workflows publicados; como publicar requiere permiso, la prueba pasó el JSON del sub-workflow en línea.
- Aprendizaje: un 401 o 500 de la tienda no debe convertirse en `ninguno` (el flujo 3 acabaría preguntando a Marisa por cada pago), así que el sub-workflow lanza error en esos casos. Para que el flujo 3 lo llame, `SUB - Buscar apartado` tendrá que estar publicado en la instancia que tenga activo el flujo 3.

### 2026-10-22 · T-001 · Entrada única `00 - Entrada tienda`
- Herramienta / modelo: Claude Code (Sonnet 5.5), en modo mentor: la IA explicó y verificó, Charlotte construyó el flujo en n8n.
- Qué se pidió: un plan paso a paso del ticket, los payloads de ejemplo de los eventos y la configuración del Webhook y del Switch, con explicación del porqué de cada ajuste.
- Qué salió: cinco payloads en `data/eventos/` (los cuatro eventos más uno inventado, `foo.bar`), copiados de la spec `tienda-webhook`; el Webhook (`POST /tienda`, respuesta inmediata) con un Switch por `$json.body.evento` y una salida de reserva; cinco nodos NoOp como destinos. Probado con los cinco payloads en la URL de test y después con un apartado real creado en la app, con el flujo publicado: llegó por `apartado.creado`.
- Qué se corrigió a mano: (1) la tarea 2.3 pedía "sub-workflows vacíos"; se usaron nodos NoOp, que T-004, T-005 y T-010 sustituirán por *Execute Workflow*. (2) La tarea 4.1 y los comandos de la IA usaban `00-entrada-tienda.json`, pero `AGENTS.md` y el flujo de Anna usan el nombre del flujo; se dejó `workflows/00 - Entrada tienda.json` y se corrigió `tasks.md`. (3) La convención de nombres de nodo no estaba escrita en ningún sitio: se tomó de `SUB - Buscar apartado` (T-003) y se añadió a `AGENTS.md`. (4) VS Code reformateó un payload al guardarlo; se descartó ese cambio.
- Aprendizaje: el Webhook guarda el JSON recibido dentro de `body`, así que se lee `$json.body.evento`, no `$json.evento`. La URL de test (`/webhook-test/`) acepta una sola llamada por cada clic en *Execute*; la de producción exige el flujo publicado. La rama `apartado.vencido` no hace nada a propósito: el flujo 06 es quien llama a `vencer`, y si la rama también avisara, el cliente recibiría el mensaje dos veces. Las rutas con espacios hay que escribirlas entre comillas en el terminal.

### 2026-10-22 · T-002 · SUB - Enviar notificación
- Herramienta / modelo: Claude Code (Sonnet 5.5), en modo mentor: la IA explicó y verificó con capturas, Charlotte construyó el flujo en n8n.
- Qué se pidió: un plan paso a paso del ticket, los datos de prueba de los 4 casos y la comprobación del JSON exportado.
- Qué salió: `SUB - Enviar notificación` con Switch por `destinatario`, un IF de email vacío, tres nodos de envío con *Continuar en error (salida de error)* y tres nodos que devuelven `{enviado, motivo}`. Probado con cliente con email, cliente sin email (campo ausente), tienda, un email inválido y un `destinatario` desconocido. El JSON exportado no lleva `pinData`, claves ni direcciones reales (solo `carmen@example.com`).
- Qué se corrigió a mano: (1) la IA dijo primero que el Switch admite varias condiciones por regla; no es así (una por regla), y se mantuvo Switch + IF. (2) El Switch descartaba en silencio un `destinatario` desconocido; se añadió salida de reserva hacia `error_envio` y el escenario a la spec. (3) El caso 4 de la tarea 3.1 pedía romper la credencial; se probó con un email inválido para no tocar la credencial compartida. (4) Un primer envío a `carmen@example.com` rebotó en el buzón compartido: Gmail aceptó el envío y luego devolvió el rechazo. (5) `EMAIL_TIENDA` estaba vacío dentro del contenedor hasta rellenar el `.env` y volver a levantar Docker.
- Aprendizaje: sin salida de reserva, un Switch descarta en silencio lo que no encaja. `$env` no se previsualiza en el editor pero funciona al ejecutar. Hay que quitar los datos fijados (*pinned*) antes de exportar. Pendiente de acordar con el equipo: `EMAIL_TIENDA` es a la vez remitente y buzón de la tienda.

### 2026-10-23 · T-007 · 08 - Error Workflow
- Herramienta / modelo: Claude Code (Sonnet 5.5), en modo mentor: la IA explicó y verificó con capturas, Charlotte construyó el flujo en n8n.
- Qué se pidió: un plan paso a paso del ticket, el código del nodo que arma el aviso y oculta secretos, y la comprobación del JSON exportado.
- Qué salió: `08 - Error Workflow` con *Error Trigger*, un nodo Code (`Preparar aviso`) que arma el texto y sustituye por `[oculto]` los valores de `X-API-Key`, `Authorization`, tokens y contraseñas, y una llamada a `SUB - Enviar notificación` con destinatario `tienda`. Probado con un flujo desechable que falla a propósito con `X-API-Key: abc123`: llegó el correo con el flujo, el nodo, el enlace y `[oculto]` en lugar de la clave. El JSON exportado no lleva `pinData`, claves ni direcciones reales.
- Qué se corrigió a mano: (1) la tarea 3.1 pedía asignar `08` a todos los flujos; `08` llama a `SUB - Enviar notificación`, así que asignárselo podría crear un bucle de avisos. Se acordó dejarlo sin flujo de error y se añadió la excepción a la spec, al diseño y a las tareas. (2) La tarea 3.1 tampoco decía que los JSON de otros flujos no deben re-exportarse con el id de `08` de una sola instancia; se aclaró en `tasks.md`.
- Aprendizaje: el flujo de errores no se lanza al ejecutar a mano; hace falta un flujo publicado y una llamada real (por ejemplo un webhook). Un sub-workflow que usa `08` no debe asignárselo, por el riesgo de bucle. El id de `08` es propio de cada instancia de n8n, así que cada persona debe elegirlo de nuevo en *Settings → Error workflow* tras importar un flujo.
