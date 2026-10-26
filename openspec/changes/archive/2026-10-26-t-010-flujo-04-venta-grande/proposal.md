# T-010 · Flujo 04 · Venta grande

**Historia:** HU-09 · **Responsable:** Leandro (`Leandroletoile`) · **Tamaño:** S · **Fecha límite:** 2026-10-27
**Depende de:** T-001, T-002

## Por qué
Marisa quiere enterarse al momento de las ventas importantes, estén o no ella en la tienda.

## Qué cambia
- Workflow `04 - Venta grande`, llamado desde la rama `venta.registrada`.
- Aviso a Marisa cuando el importe iguala o supera un umbral configurable.

## Fuera de alcance
- Aviso al cliente.
- Alertas para ventas por debajo del umbral.

## Impacto
Usa `SUB - Enviar notificación`. Necesita una variable de configuración con el umbral.
