# T-017 · Asistente de Telegram para Marisa

**Historia:** HU-12 · **Responsable:** Charlotte · **Tamaño:** M · **Fecha límite:** sin fecha (extra: si hay tiempo)
**Depende de:** T-001, T-002, T-003, T-016 (misma base de flujo con agente de IA)

## Por qué
Marisa quiere tener las cifras de su negocio al momento desde el móvil, preguntando por Telegram en lenguaje natural: "¿cuánto se recaudó esta semana?", "¿qué apartados vencen este mes?".

## Qué cambia
- Flujo `Asistente Marisa`: bot de Telegram propio (`Telegram Marisa`) que solo atiende a Marisa.
- Un nodo **AI Agent** (modelo gratuito de Groq, credencial `Modelo IA`) con tres herramientas de solo lectura sobre la API de la tienda: recaudado, vencimientos y buscar apartado.
- Memoria corta de conversación (últimos 4 intercambios) para entender preguntas de seguimiento como "¿y la semana pasada?".
- Variable `TELEGRAM_CHAT_ID_MARISA` en `.env` (sin valor en `.env.example`).

## Fuera de alcance
- Registrar o modificar datos desde el chat (abonar, vencer, crear apartados).
- Atender a clientes (T-016).

## Impacto
Usa Telegram, la credencial `Tienda API` y la API de lectura (`GET /api/abonos`, `/api/ventas`, `/api/apartados`). Extra (nivel Avanzado/Experto): se construye con los niveles Esencial y Medio cerrados.
