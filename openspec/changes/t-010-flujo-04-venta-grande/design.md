## Decisiones
1. **El umbral vive en una variable** (`UMBRAL_VENTA_GRANDE`), nunca dentro del flujo. Valor inicial propuesto: **80 €** (a confirmar con Marisa).
2. **Variables de n8n o `$env`:** las Variables de n8n son de pago en algunas ediciones; si no están, se usa `$env` (en `docker-compose.yml`) y se documenta.
3. **Comparación con `>=`.** El importe viene de la app, no se recalcula.
4. **Debajo del umbral no se hace nada** (ni siquiera un mensaje).
