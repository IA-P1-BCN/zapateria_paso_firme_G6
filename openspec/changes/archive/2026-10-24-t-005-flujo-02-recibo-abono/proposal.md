# T-005 · Flujo 02 · Recibo de abono

**Historia:** HU-02 · **Responsable:** Leandro (`Leandroletoile`) · **Tamaño:** S · **Fecha límite:** 2026-10-25
**Depende de:** T-001, T-002

## Por qué
Cada vez que un cliente paga un abono quiere saber cuánto ha pagado y cuánto le queda. Y cuando liquida, quiere saber que ya puede recoger sus zapatos.

## Qué cambia
- Workflow `02 - Recibo de abono`, llamado desde la rama `abono.registrado`.
- Recibo con el importe abonado ahora y el pendiente.
- Mensaje de recogida cuando el apartado queda liquidado.

## Fuera de alcance
- El abono inicial (lo cubre la confirmación del flujo 1).
- Detectar pagos por correo del banco (T-008), aunque su abono también genera este recibo.

## Impacto
Usa `SUB - Enviar notificación`. Recibe también los abonos que registra el flujo 3.
