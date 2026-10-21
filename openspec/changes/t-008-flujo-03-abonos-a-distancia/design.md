## Decisiones
1. **La IA solo extrae texto a campos.** Todo lo que implica dinero (¿qué apartado? ¿se registra? ¿el importe cabe?) lo deciden nodos deterministas con las reglas de la spec.
2. **Filtro previo sin IA:** se descartan los correos que no tienen `Importe` y `Ordenante` (publicidad) antes de gastar una llamada al modelo.
3. **El importe se valida en código:** `10,00 EUR` → `10`. Si no es un número positivo, el pago es dudoso.
4. **Dos formatos de correo:** Bizum (`Importe: 10,00 EUR`) y transferencia (`Importe .......... 12,00 EUR`). El mismo prompt debe extraer ambos.
5. **Sin duplicados:** cada correo se procesa una vez (se marca como leído y se guarda el `Message-ID`).
6. **Errores de la app:** si `POST /abonos` devuelve 422, se avisa a Marisa con el motivo. `detail` puede ser texto o lista: se tratan los dos.
7. **DECISIÓN ABIERTA:** la app solo acepta `efectivo`, `tarjeta` y `bizum`; no existe `transferencia`. Propuesta: registrar las transferencias como `bizum` (pago a distancia) y decirlo en el aviso; alternativa: pedir a Marisa. A decidir antes de construir.

## Los 9 correos de `data/correos/` y qué debe pasar con cada uno
Según el briefing; los correos están pensados para los apartados de ejemplo de la app.

| Correo | Qué debe pasar |
|---|---|
| 01 Bizum Carmen Ruiz, 10 € | El nombre coincide con un único apartado activo: se registra el abono |
| 09 Bizum Silvia Cortés, 5 € | Igual que el 01: se registra |
| 02 Bizum `JORGE M.` | Ordenante abreviado, pero el concepto trae el nº de apartado: se encuentra por el número y se comprueba con el nombre |
| 03 Transferencia Lucía Gómez | Paga justo lo que falta: el apartado queda **liquidado** (y el cliente recibe el aviso de recogida del flujo 2) |
| 04 Bizum `LAURA O.` | Paga **más** de lo pendiente: la app lo rechaza, no se registra y se avisa a Marisa |
| 05 Bizum `ROMERO D`, sin concepto | Solo apellido e inicial: se pregunta a Marisa antes de registrar nada |
| 06 Bizum Paula Ramos | El apartado está **fuera de plazo**: no se puede abonar, se avisa a Marisa |
| 07 Transferencia Antonio Fernández | No coincide con ningún cliente: se pregunta a Marisa |
| 08 Publicidad del banco | No es un pago: se ignora |
