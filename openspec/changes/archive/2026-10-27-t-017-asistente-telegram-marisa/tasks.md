## 1. Preparación

- [x] 1.1 Crear el bot `Telegram Marisa` en BotFather y la credencial de Telegram en n8n
- [x] 1.2 Obtener el `chat_id` de Marisa y guardarlo en `.env` como `TELEGRAM_CHAT_ID_MARISA` (pasarlo a n8n en `docker-compose.yml`, y añadirlo vacío a `.env.example` y al README)

## 2. Flujo

- [x] 2.1 Telegram Trigger y nodo `¿Es Marisa en chat privado?` con rechazo fijo
- [x] 2.2 Herramienta `Recaudado` (periodo → abonos + ventas, suma por forma de pago en un Code)
- [x] 2.3 Herramienta `Vencimientos` (periodo → activos filtrados por `fecha_limite` en un Code)
- [x] 2.4 Herramienta `Buscar apartado`
- [x] 2.5 AI Agent (Groq `Modelo IA`): prompt con pasos explícitos y mensaje fijo si el modelo falla
- [x] 2.6 Memoria corta (Simple Memory, ventana 4, clave `chat.id`) y regla de volver a consultar la herramienta
- [x] 2.7 Enviar respuesta por Telegram
- [x] 2.8 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 3. Pruebas

- [x] 3.1 Chat ajeno y mensaje de grupo: rechazo o silencio, sin consultar la API
- [x] 3.2 "¿Cuánto se recaudó esta semana / hoy?" y comparar con la app
- [x] 3.3 "¿Qué apartados vencen este mes?" y comparar con la app
- [x] 3.4 Buscar un apartado por cliente
- [x] 3.5 Petición de escritura ("cancela el 12"): rechazada
- [x] 3.6 Modelo caído (nombre de modelo falso): mensaje fijo
- [x] 3.7 Seguimiento: "¿cuánto se recaudó este mes?" y luego "¿y la semana pasada?" vuelve a llamar a la herramienta

## 4. Entrega

- [x] 4.1 Exportar a `workflows/Asistente Marisa.json` y revisar que el JSON no contiene claves, tokens ni el `chat_id`
- [x] 4.2 Anotar en la sección propia de `docs/ai-log.md` y documentar el flujo en el README

## 5. Cierre del change (obligatorio al terminar)

- [x] 5.1 Validar: `openspec validate t-017-asistente-telegram-marisa --strict`
- [x] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-017-asistente-telegram-marisa`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [x] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
