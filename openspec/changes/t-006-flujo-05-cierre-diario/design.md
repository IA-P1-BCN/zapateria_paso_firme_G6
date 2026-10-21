## Decisiones
1. **Hora:** 22:00, zona `Europe/Madrid` fijada en los ajustes del workflow. A confirmar con Marisa.
2. **Fecha de hoy** calculada en Madrid, no en UTC (para que a las 22:00 no cuente otro día).
3. **Las sumas se hacen en céntimos** (enteros) y se muestran al final, para que `0,1 + 0,2` no dé `0,30000000004`.
4. **El abono inicial de un apartado es un abono**, no una venta: sale en la fila de abonos. No se cuenta dos veces (en el Excel antiguo sí aparecía en ventas; ver T-012).
5. **Los importes salen de la app**, el flujo solo suma lo que devuelve.
6. **Se guarda el cierre** (el briefing dice "guarda el cierre"): una fila por día con fecha, ventas, abonos y total por forma de pago. Dónde (Google Sheets u otra herramienta, o una tabla de datos de n8n) está por decidir; no es la app, que no guarda cierres.
