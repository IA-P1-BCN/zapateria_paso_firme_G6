## 1. Preparación

- [x] 1.1 Decidir bot, token y forma de identificar al cliente
- [x] 1.2 Crear la credencial de Telegram en n8n

## 2. Flujo

- [x] 2.1 Trigger de Telegram y búsqueda del cliente
- [x] 2.2 Consulta a la API y respuesta con formato claro
- [x] 2.3 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 3. Pruebas

- [x] 3.1 Probar un cliente identificado, uno no identificado y un cliente sin apartados

## 4. Entrega

- [x] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [x] 4.2 Anotar en la sección propia de `docs/ai-log.md`

## 4b. Agente de IA

- [x] 4b.1 Añadir el AI Agent (Groq) con la herramienta `Consultar mis apartados` (filtrada por el teléfono de la sesión)
- [x] 4b.2 Salida de error con mensaje fijo y prueba con un modelo inexistente
- [x] 4b.3 Probar: lista, "¿otros?", vencidos/liquidados, importe, apartado ajeno
- [x] 4b.4 Exportar a `workflows/Asistente cliente con agente IA.json` (el flujo sin IA se conserva) y anotar en `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)

- [x] 5.1 Validar: `openspec validate t-016-asistente-telegram-cliente --strict`
- [x] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-016-asistente-telegram-cliente`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [x] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
