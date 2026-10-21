# T-012 · Migración del Excel de Marisa

**Historia:** HU-10 · **Responsable:** Anna (`costanna`) · **Tamaño:** L · **Fecha límite:** 2026-10-28
**Depende de:** T-001

## Por qué
Marisa lleva los apartados y las ventas del mes en hojas de Excel. Antes de dejar el Excel hay que pasar sus datos a la app sin perder nada y sin inventar nada.

## Qué cambia
- Workflow `Migración Excel` que lee `data/excel_actual_apartados.csv` y `data/excel_actual_ventas.csv`.
- Normalización de fechas, importes y nombres.
- Carga en la app por su API respetando sus reglas.
- Informe a Marisa de lo que no se cargó y por qué.

## Fuera de alcance
- Repetir la migración cada día.
- Corregir los datos del Excel.

## Impacto
Escribe en la app: apartados, abonos y ventas. **Solo se ejecuta una vez y sobre una base limpia.**
