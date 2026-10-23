## Decisiones
1. **Ejecutar con `SEED=0` o volumen limpio.** El seed de la app trae clientes con los mismos nombres; mezclarlos daría duplicados.
2. **Cada fila repetida por cliente + modelo + talla es un apartado inicial más sus abonos** (la primera es el apartado, las demás son abonos). Se agrupa por cliente (+ teléfono) + modelo + talla.
3. **Datos sucios a normalizar:** fechas `02/09/2026` y `7/9/26`; importes `15€`; nombres `carmen ruiz` (se capitalizan); Ana Torres sin teléfono (se carga igual).
4. **La columna `resta` se usa para validar**: el pendiente que calcula la app debe coincidir. Si no coincide, se informa.
5. **Dudosos no se cargan:** el abono inicial de Lucía Gómez (4 €) es menor que el mínimo de 5 €, la app lo rechazaría. No se carga ni él ni sus abonos posteriores (incluido el `LIQUIDADO` de 41 €), y va al informe.
6. **Ventas del Excel que son abonos de apartados** (`abono inicial apartado`, `Abono Ana Torres mocasin`, `(apartado)`) no se cargan como ventas, para no contarlas dos veces; sirven para deducir la `forma_pago` de ese abono. Si no se puede deducir, se usa `efectivo` y se informa como suposición.
7. **La fila `TOTAL SEPTIEMBRE (a mano)` se ignora.**
8. **Se conserva la fecha original** de cada apartado, abono y venta.
9. **Idempotente:** antes de crear, se comprueba si ya existe (apartado: cliente + producto + fecha; abono: fecha + importe). Si se relanza, no duplica.
10. **Orden cronológico:** los abonos se cargan por fecha para respetar las reglas de la app.
