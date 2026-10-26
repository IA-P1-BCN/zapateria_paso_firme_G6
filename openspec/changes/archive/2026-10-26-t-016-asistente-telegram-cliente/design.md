## Decisiones
1. **Bot y token:** bot propio de clientes (`pasofirme_clientes_bot`), distinto del de Marisa (T-017). El token vive solo en la credencial de n8n `Telegram Clientes`, nunca en el repo.
2. **El saldo y las fechas vienen de la app**, nunca de lo que diga el modelo. El modelo copia `pendiente`, `fecha_limite` e `id` tal como los devuelve la API; no calcula importes.
3. **"Asistente" = el flujo completo.** La identificación y el acceso a los datos son nodos deterministas; la IA solo redacta la respuesta (decisión 7).
4. **Identificación en dos pasos (dos factores):**
   1. La clienta comparte su contacto con el botón de Telegram. Solo vale si `contact.user_id` es el de quien lo envía (`¿El contacto es suyo?`); un contacto ajeno se rechaza. Se guardan las 9 últimas cifras del teléfono.
   2. Escribe el número de uno de sus apartados (puede ir dentro de una frase). Solo se acepta si ese `id` pertenece a un apartado de ese teléfono.
5. **Sesión en una Data Table** `clientes_telegram` (`chat_id`, `telefono`, `verificado_en`), de 10 minutos de inactividad. Estados: `sin_sesion`, `esperando_apartado`, `activa`. Cada mensaje de una sesión activa la renueva. `/salir` la borra.
6. **Si no se puede identificar, no se dan datos** y se ofrece contactar con la tienda. Los grupos se ignoran (solo chat privado).
7. **Papel de la IA (AI Agent, Groq `openai/gpt-oss-20b`, temperatura 0.2):**
   - Solo se ejecuta con la sesión `activa` o recién verificada.
   - Su única herramienta, `Consultar mis apartados`, hace `GET /api/apartados` con `q` fijo = teléfono de la sesión (no lo elige el modelo). Así nunca puede ver apartados de otras personas.
   - Ve `id, producto, estado, pendiente, fecha_limite` de todos los estados; por defecto habla solo de los `activo`, y de `liquidado`/`vencido` solo si se le pregunta, sin hablar de deuda.
   - No decide dinero (descuentos, reembolsos, cancelaciones): remite a la tienda.
   - Si el modelo falla (límite de Groq, caída), la salida de error envía un mensaje fijo y remite a la tienda.
8. **Duplicación de petición asumida:** la verificación consulta la API (seguridad, nodos) y la herramienta del agente la vuelve a consultar (respuesta). Se prefiere a dejar que el agente use datos de otro nodo, porque así la herramienta no puede salirse del teléfono de la sesión.
9. **Dos flujos conviven en el repo para la comparativa antes/después:** `Asistente cliente` (solo nodos, respuesta con plantilla fija) y `Asistente cliente con agente IA`. Usan el mismo bot, y Telegram solo admite un webhook por bot: **solo uno puede estar activo a la vez.**
10. **Datos que salen de la tienda:** Telegram recibe producto, pendiente y fecha límite de la clienta, y el modelo de Groq recibe esos mismos campos. Se documentará en el README (T-020).

## Mejoras futuras (fuera de este change)
- **Agente "puro"** que gestione también la identificación con herramientas (`pedir_contacto`, `verificar_apartado`…), con comprobación de sesión dentro de cada herramienta. Se descarta ahora por seguridad: una herramienta sin filtro de teléfono podría exponer a todos los clientes.
- **Memoria de conversación** (Simple Memory con clave `chat_id`) para preguntas de seguimiento. Riesgos: mezclar clientes si la clave no es el `chat_id`, importes desfasados y recuerdos tras caducar la sesión.
- **Primer mensaje en el idioma de la clienta:** hoy es un mensaje fijo en español (no pasa por el modelo para no abrir la puerta a datos sin identificar).
- Modelo mayor (`gpt-oss-120b`) si el pequeño falla en reglas condicionales.
