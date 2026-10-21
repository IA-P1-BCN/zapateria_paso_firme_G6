## Decisiones
1. **Error Workflow de n8n** (Error Trigger) en vez de comprobar errores nodo a nodo: cubre cualquier fallo no previsto.
2. **El aviso lleva:** nombre del workflow, nombre del nodo que falló, mensaje de error, hora y enlace a la ejecución.
3. **Se limpian los textos**: se sustituyen por `[oculto]` los valores de cabeceras `X-API-Key`, `Authorization`, tokens y contraseñas que puedan aparecer en el mensaje de error.
4. **El propio `08` no se asigna a sí mismo** (evitar un bucle). Si el envío del aviso falla, queda en las ejecuciones de n8n.
