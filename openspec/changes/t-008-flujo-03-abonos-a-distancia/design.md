## Decisiones
1. **La IA solo extrae texto a campos.** Todo lo que implica dinero (¿qué apartado? ¿se registra? ¿el importe cabe?) lo deciden nodos deterministas con las reglas de la spec.
2. **Filtro previo sin IA:** se descartan los correos que no tienen `Importe` y `Ordenante` (publicidad) antes de gastar una llamada al modelo.
3. **El importe se valida en código:** `10,00 EUR` → `10`. Si no es un número positivo, el pago es dudoso.
4. **Dos formatos de correo:** Bizum (`Importe: 10,00 EUR`) y transferencia (`Importe .......... 12,00 EUR`). El mismo prompt debe extraer ambos.
5. **Sin duplicados:** cada correo se procesa una vez (se marca como leído y se guarda el `Message-ID`).
6. **Errores de la app:** si `POST /abonos` devuelve 422, se avisa a Marisa con el motivo. `detail` puede ser texto o lista: se tratan los dos.
7. **DECISIÓN ABIERTA:** la app solo acepta `efectivo`, `tarjeta` y `bizum`; no existe `transferencia`. Propuesta: registrar las transferencias como `bizum` (pago a distancia) y decirlo en el aviso; alternativa: pedir a Marisa. A decidir antes de construir.

## Los 9 correos de `data/correos/` y qué regla prueba cada uno
| Correo | Qué prueba | Resultado esperado* |
|---|---|---|
| 01 Bizum Carmen Ruiz García, `zuecos`, 10 € | nombre completo | registra si hay un único apartado activo |
| 02 Bizum `JORGE M.`, `apartado 2 bota`, 20 € | nombre abreviado y número engañoso en el concepto | busca por `jorge`; el `2` no se usa como id sin comprobarlo |
| 03 Transferencia Lucía Gómez Pérez, `Liquidar mocasines`, 12 € | otro formato de correo; concepto que puede no coincidir | registra solo si es único y el importe cabe |
| 04 Bizum `LAURA O.`, `deportivas`, 15 € | apellido abreviado | un único candidato o dudoso |
| 05 Bizum `ROMERO D`, sin concepto, 10 € | sin concepto | **dudoso**: no registra, pregunta |
| 06 Bizum Paula Ramos León, `zapatillas running perdón por el retraso`, 20 € | ruido en el concepto | el texto extra no impide encontrar el apartado |
| 07 Transferencia Antonio Fernández Soto, `botas`, 25 € | cliente desconocido | **dudoso**: no registra, pregunta |
| 08 Publicidad del banco | no es un pago | se ignora |
| 09 Bizum Silvia Cortés, `abono sandalias`, 5 € | importe mínimo | registra si cabe; si supera lo pendiente, rechazo |

\* El resultado final depende de los apartados cargados en la app (seed): confirmar cada caso contra la app antes de cerrar el ticket.
