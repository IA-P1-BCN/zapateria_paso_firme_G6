## Decisiones
1. **`abono.registrado` trae el apartado actualizado más `importe`.** `datos.importe` es lo abonado ahora; `datos.pendiente` ya incluye ese abono.
2. **El abono inicial NO genera este evento** (solo `apartado.creado`); por eso no hay recibo duplicado al dar de alta.
3. **Un solo flujo para abonos de cualquier origen:** tienda, pantalla o flujo 3.
