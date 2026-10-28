## Decisiones
1. **HTTPS obligatorio** (la app enviará eventos por la red).
2. **Secretos solo en variables del servidor**, nunca en el repo.
3. **Copias de seguridad** del volumen de n8n y de la base de la app.
4. **CI mínimo**: validar que los JSON de `workflows/` son válidos y no contienen claves.

## Decisiones al construirlo (Anna, 2026-10-28)
5. **Render (plan gratuito), sin Vercel; Neon para n8n, pendiente.** No hay crédito de pago. Render ejecuta los contenedores (la tienda con el `Dockerfile` del repo y, más adelante, la imagen oficial de n8n) con HTTPS incluido. Para la base de n8n se propone Neon (escala a cero), pero el equipo aún lo decide: en `render.yaml` el bloque de n8n queda comentado y documentado para quien lo continúe, y de momento solo se despliega la tienda. Vercel solo ejecuta funciones que se apagan tras cada petición: no puede mantener n8n ni el SQLite de la tienda.
6. **Los servicios duermen.** Render gratis los duerme tras 15 min sin visitas y el primero que llega espera 30-60 s (tienda) o 1-2 min (n8n). No se añade nada que los mantenga despiertos. Se avisa en el README y en `render.yaml`.
7. **La tienda desplegada es de demostración.** Render gratis no tiene disco permanente y la app no se toca (no puede pasar a Postgres), así que vuelve a los datos de ejemplo al dormirse o reiniciarse. Por eso no se le hace copia (sustituye a la copia "de la base de la app" de la decisión 3).
8. **Copias sin tareas programadas.** Los flujos están en `workflows/`; la base de n8n tiene el historial de 6 h de Neon (restaurar a un momento) y una copia completa bajo demanda con `pg_dump` (comando en el README). La `N8N_ENCRYPTION_KEY` se guarda aparte, porque sin ella las credenciales de una copia no se pueden leer.
9. **Cuando se despliegue n8n, flujos programados e IMAP sin publicar** (`03`, `05`, `06`, `07`, `Entrada CSV del datáfono`), salvo que Marisa lo pida. Los que responden a una persona (webhook, formularios, panel, Telegram) se publican.
10. **CI sin red:** `.github/scripts/validar_flujos.py` solo lee los JSON (biblioteca estándar de Python). Falla con JSON roto, claves con formato conocido, credenciales con datos o contraseñas escritas en un nodo; solo avisa de flujos exportados publicados, sin `08 - Error Workflow` o con `meta.instanceId`.
