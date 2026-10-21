# T-007 · Flujo 08 · Error Workflow

**Historia:** HU-05 · **Responsable:** Charlotte (`Charlottedoulcet`) · **Tamaño:** S · **Fecha límite:** 2026-10-25
**Depende de:** T-001, T-002

## Por qué
Si una automatización falla y nadie se entera, se descubre semanas después que algo dejó de funcionar. Marisa quiere un aviso cuando pase.

## Qué cambia
- Workflow `08 - Error Workflow` con *Error Trigger*.
- Aviso a Marisa con nombre del flujo, paso que falló y error, sin datos sensibles.
- Regla: todos los flujos lo asignan como su flujo de error.

## Fuera de alcance
- Reintentos automáticos o recuperación de datos.
- Alertas a otros canales.

## Impacto
Todos los flujos (T-004 en adelante) deben asignarlo en sus ajustes: está como tarea en cada ticket.
