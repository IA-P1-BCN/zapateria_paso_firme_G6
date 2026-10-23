## Decisiones
1. **Error Workflow de n8n** (Error Trigger) en vez de comprobar errores nodo a nodo: cubre cualquier fallo no previsto.
2. **El aviso lleva:** nombre del workflow, nombre del nodo que falló, mensaje de error, hora y enlace a la ejecución.
3. **Se limpian los textos**: se sustituyen por `[oculto]` los valores de cabeceras `X-API-Key`, `Authorization`, tokens y contraseñas que puedan aparecer en el mensaje de error.
4. **Ni `08` ni `SUB - Enviar notificación` se asignan el flujo de error**: `08` llama a ese sub-workflow, así que un fallo suyo volvería a lanzar `08` y haría un bucle. Si el envío del aviso falla, queda en las ejecuciones de n8n.
5. **El id de `08` es propio de cada instancia de n8n**: no se versiona en los JSON de otros flujos. Cada persona lo elige en *Settings → Error workflow* tras importar.
