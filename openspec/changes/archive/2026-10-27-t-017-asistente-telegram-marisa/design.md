## Flujo
```
Telegram Trigger (bot de Marisa)
  → ¿Es Marisa en chat privado?  ── no → rechazo fijo, fin (sin API, sin IA)
  → AI Agent (Groq `Modelo IA`)
        ├─ Recaudado        (abonos + ventas de un periodo)
        ├─ Vencimientos     (apartados activos que vencen en un periodo)
        └─ Buscar apartado  (por nombre, id o teléfono)
  → Enviar respuesta por Telegram
  (si el modelo falla → mensaje fijo)
```

## Decisiones
1. **Bot propio.** Un bot solo admite un webhook y el de clientes (T-016) ya usa el suyo.
2. **Solo responde a Marisa.** Un nodo determinista compara `chat.id` con `$env.TELEGRAM_CHAT_ID_MARISA` y exige `chat.type = private` antes del agente. Si no coincide, ni la API ni el modelo se tocan.
3. **El modelo no calcula fechas.** Las herramientas reciben un `periodo` (`hoy`, `esta_semana`, `este_mes`) y un nodo Code calcula `desde` y `hasta` (semana de lunes a domingo, zona Europe/Madrid).
4. **El modelo no suma dinero.** Un nodo Code suma los `importe` tal como los devuelve la app, por forma de pago (`efectivo`, `tarjeta`, `bizum`); el modelo solo copia los totales. No se recalculan `abonado`, `pendiente` ni `precio`.
5. **Vencimientos.** La app no filtra por fecha límite: la herramienta pide los `activo` y filtra `fecha_limite` en un Code.
6. **Solo lectura.** Las herramientas son `GET`; ninguna escribe, abona ni vence.
7. **Modelo.** Groq `gpt-oss-20b`, temperatura 0.2, pasos explícitos y frases literales en el prompt (aprendizaje de T-016). Si falla con las preguntas de prueba, `gpt-oss-120b`.
8. **Fallo del modelo.** Mensaje fijo, sin cifras.
9. **Memoria corta.** Simple Memory con ventana de 4 intercambios y clave de sesión `chat.id`, para las preguntas de seguimiento. El prompt prohíbe reutilizar cifras, fechas o nombres de respuestas anteriores: cada consulta de dinero, fechas o apartados vuelve a llamar a la herramienta.
