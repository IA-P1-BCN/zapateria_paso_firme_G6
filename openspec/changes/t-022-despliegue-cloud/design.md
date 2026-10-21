## Decisiones
1. **HTTPS obligatorio** (la app enviará eventos por la red).
2. **Secretos solo en variables del servidor**, nunca en el repo.
3. **Copias de seguridad** del volumen de n8n y de la base de la app.
4. **CI mínimo**: validar que los JSON de `workflows/` son válidos y no contienen claves.
