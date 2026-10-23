# T-009 · Flujo 06 · Recordatorios y vencimientos

**Historia:** HU-06 y HU-07 · **Responsable:** Charlotte (`Charlottedoulcet`) · **Tamaño:** L · **Fecha límite:** 2026-10-28
**Depende de:** T-001, T-002

## Por qué
Los apartados tienen un plazo de 90 días. Hoy nadie avisa a la clienta de que se acerca la fecha ni se cierra el apartado cuando pasa: los zapatos quedan bloqueados sin que Marisa se dé cuenta.

## Qué cambia
- Workflow programado `06 - Recordatorios y vencimientos` (cada mañana).
- Recordatorio a la clienta 7 días y 1 día antes de `fecha_limite`.
- Vencimiento de los apartados activos con la fecha pasada, con aviso a la clienta (incluye su vale) y lista a Marisa de los zapatos que vuelven a la venta.

## Fuera de alcance
- Cobrar o renegociar plazos.
- Mensajes por otros canales (T-016).

## Impacto
Usa `SUB - Enviar notificación`. Escribe en la app: `POST /api/apartados/{id}/vencer`. La app emite `apartado.vencido`; el `00 - Entrada tienda` NO debe actuar sobre él (ver decisión 5).
