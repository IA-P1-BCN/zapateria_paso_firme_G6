## Decisiones
1. **Un solo punto de salida de mensajes.** Alternativa descartada: un nodo de correo en cada flujo (duplicado y distinto manejo de errores).
2. **Canal: correo electrónico.** El briefing acepta correo o Telegram, y los flujos 3 y 7 ya usan correo. El envío es por SMTP con la cuenta compartida del equipo (`pasofirme.g6@gmail.com`), credencial `Correo salida` (decidido en `docs/guia-del-equipo.md`). Si cambia, solo cambia este sub-workflow.
3. **Contrato de entrada:** `destinatario` (`cliente` o `tienda`), `email` (solo si es cliente), `asunto`, `mensaje` (texto plano), `contexto` (opcional, texto corto que identifica el apartado para el aviso a la tienda).
4. **Contrato de salida:** `{enviado: true|false, motivo: ''|'sin_email'|'error_envio'}`. Nunca lanza error al flujo que llama (continuar en error).
5. **Correo de la tienda en una variable de configuración** (Variables de n8n, o `$env` si la edición de n8n no las incluye), nunca escrito en el flujo.

6. **Destinatario desconocido = `error_envio`.** El Switch tiene salida de reserva para que un `destinatario` mal escrito no se pierda en silencio; devuelve `error_envio` sin añadir un cuarto motivo al contrato.
7. **`EMAIL_TIENDA` es remitente y destinatario de la tienda.** Vale con una sola cuenta compartida; si pasa a ser la dirección real de Marisa, Gmail rechazaría el remitente y habría que añadir una variable aparte (toca `.env.example` y `docker-compose.yml`, a acordar con el equipo).

## Riesgos
- Sin servidor de correo real en desarrollo: se usa un buzón de pruebas (p. ej. una cuenta propia o un servidor SMTP de pruebas) y se documenta en el README.
- Los mensajes no deben llevar claves, tokens ni datos que no hagan falta.
