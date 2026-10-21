## Decisiones
1. **Un solo punto de salida de mensajes.** Alternativa descartada: un nodo de correo en cada flujo (duplicado y distinto manejo de errores).
2. **Canal: correo electrónico.** El briefing acepta correo o Telegram, y los flujos 3 y 7 ya usan correo. El envío es por Gmail o SMTP: falta decidir qué cuenta (una compartida para la demo). Si cambia, solo cambia este sub-workflow.
3. **Contrato de entrada:** `destinatario` (`cliente` o `tienda`), `email` (solo si es cliente), `asunto`, `mensaje` (texto plano), `contexto` (opcional, texto corto que identifica el apartado para el aviso a la tienda).
4. **Contrato de salida:** `{enviado: true|false, motivo: ''|'sin_email'|'error_envio'}`. Nunca lanza error al flujo que llama (continuar en error).
5. **Correo de la tienda en una variable de configuración** (Variables de n8n, o `$env` si la edición de n8n no las incluye), nunca escrito en el flujo.

## Riesgos
- Sin servidor de correo real en desarrollo: se usa un buzón de pruebas (p. ej. una cuenta propia o un servidor SMTP de pruebas) y se documenta en el README.
- Los mensajes no deben llevar claves, tokens ni datos que no hagan falta.
