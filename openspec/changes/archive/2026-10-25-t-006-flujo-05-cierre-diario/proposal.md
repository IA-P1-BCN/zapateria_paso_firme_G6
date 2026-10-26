# T-006 · Flujo 05 · Cierre diario

**Historia:** HU-04 · **Responsable:** Leandro (`Leandroletoile`) · **Tamaño:** M · **Fecha límite:** 2026-10-25
**Depende de:** T-001, T-002

## Por qué
Marisa cierra la caja a mano sumando ventas y cobros con calculadora. El resumen automático le ahorra el trabajo y evita errores.

## Qué cambia
- Workflow programado `05 - Cierre diario` (cada noche).
- Resumen con ventas directas, abonos y total, por forma de pago.
- Mensaje claro cuando no hubo movimientos.

## Fuera de alcance
- Cuadrar con el datáfono o el banco (T-019).
- Informe mensual (T-011).

## Impacto
Usa `SUB - Enviar notificación`. Lee `GET /api/ventas` y `GET /api/abonos`.
