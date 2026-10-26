## Decisiones
1. **Cada línea se identifica por fecha + importe + referencia** para no duplicar.
2. **Las líneas que no se entienden no se cargan** y van a un informe para Marisa.
   - **Cómo queda (2026-10-26, Anna):** un cobro ya está en la app si su venta lleva su número de operación en el concepto (`Cobro con tarjeta (datáfono, op. N)`, lo pone el propio flujo al cargarlo) o si cuadra con una venta o un abono pagados con tarjeta del mismo día e importe. Se miran también los abonos porque un abono de apartado pagado con tarjeta pasa por el datáfono y no es una venta nueva.
