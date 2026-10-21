# T-008 · Flujo 03 · Abonos por Bizum y transferencia

**Historia:** HU-03 · **Responsable:** Anna (`costanna`) · **Tamaño:** L · **Fecha límite:** 2026-10-26
**Depende de:** T-001, T-002, T-003

## Por qué
Marisa revisa los avisos del banco y apunta a mano cada Bizum o transferencia en el apartado correcto. Es lento y se cometen errores. El flujo debe registrar solo y, cuando no esté claro, preguntar.

## Qué cambia
- Workflow `03 - Abonos a distancia` que lee los correos del banco.
- Descarte de lo que no es un pago (publicidad).
- Extracción con IA de `{ordenante, importe, concepto}`.
- Reglas deterministas para registrar, dudar o rechazar.
- Aviso a Marisa en los casos dudosos y rechazados.

## Fuera de alcance
- Comparar dos modelos de IA (T-013).
- Pagos por otros canales.
- Que la IA decida si se registra un pago.

## Impacto
Usa `SUB - Buscar apartado`, `SUB - Enviar notificación` y `POST /api/apartados/{id}/abonos`. El abono registrado dispara `abono.registrado` y con él el recibo del flujo 2.
