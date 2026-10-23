# T-004 · Flujo 01 · Confirmación de apartado

**Historia:** HU-01 · **Responsable:** Leandro (`Leandroletoile`) · **Tamaño:** S · **Fecha límite:** 2026-10-24

**Depende de:** T-001, T-002

## Why

Cuando alguien aparta unos zapatos quiere tener claro qué ha apartado, cuánto ha pagado, cuánto falta y hasta cuándo. Hoy se avisa a mano o no se avisa.

## What Changes

- Workflow `01 - Confirmación de apartado`, llamado desde la rama `apartado.creado` de `00 - Entrada tienda`.
- Mensaje al cliente con los datos que da la app.
- Variante para un apartado que nace liquidado.

## Fuera de alcance

- Recibos de abonos posteriores (T-005).
- Recordatorios de plazo (T-009).

## Impacto

Usa `SUB - Enviar notificación`. Sustituye al sub-workflow vacío de la rama `apartado.creado` en `00 - Entrada tienda`.
