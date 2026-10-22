# T-003 · SUB · Buscar apartado

**Historia:** HU-03 · **Responsable:** Anna (`costanna`) · **Tamaño:** S · **Fecha límite:** 2026-10-24
**Depende de:** T-001

## Por qué
El flujo 3 (y los asistentes de Telegram) necesitan encontrar el apartado de una persona a partir de un nombre escrito de cualquier manera (`JORGE M.`, `ROMERO D`, `GOMEZ`). La búsqueda `q` de la app es por subcadena exacta y falla con abreviaturas y acentos; hay que resolverlo una vez, aparte.

## Qué cambia
- Sub-workflow `SUB - Buscar apartado` que recibe un `id` o un `texto` y devuelve candidatos normalizados.
- Búsqueda por trozos del nombre, sin depender de mayúsculas ni acentos.

## Fuera de alcance
- Decidir si el pago se registra (lo hace el flujo 3).
- Usar IA: la búsqueda es determinista.

## Impacto
Lo usa T-008 (y T-016/T-017 si se hacen). Solo lee de la API; no modifica nada.
