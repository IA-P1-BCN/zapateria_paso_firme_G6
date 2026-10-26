## Decisiones
1. **Hora:** día 1 a las 08:00, zona `Europe/Madrid`. A confirmar.
2. **Mes anterior:** `desde` = día 1, `hasta` = último día del mes anterior, calculados en Madrid.
3. **Recaudado:** `GET /api/ventas` y `GET /api/abonos` con `desde`/`hasta`; ventas y abonos por separado y total. Sumas en céntimos.
4. **Pendiente total:** suma de `pendiente` de los apartados `activo` ahora. `GET /api/apartados/resumen` solo da conteos por estado, no importes.
5. **Apartados nuevos:** `fecha` del apartado dentro del mes.
6. **Liquidados del mes:** la app no guarda la fecha en que se liquidó; se toma la fecha del último abono (`GET /api/apartados/{id}`) de los apartados `liquidado`.
7. **Vencidos del mes:** la `fecha` del vale (`GET /api/vales`) dentro del mes.
