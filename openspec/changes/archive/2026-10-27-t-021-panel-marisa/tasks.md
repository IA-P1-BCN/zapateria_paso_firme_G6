## 1. Preparación
- [x] 1.1 Decidir tecnología del panel: webhook de n8n (GET `/webhook/panel-marisa`) con `Respond to Webhook`, protegido con Basic Auth (`Acceso Marisa`).

## 2. Construcción
- [x] 2.1 Consultas a la API (`/api/ventas`, `/api/abonos`, `/api/apartados?estado=activo`) y maqueta móvil en HTML/CSS.
- [x] 2.2 Proteger el acceso con Basic Auth (credencial `Acceso Marisa`); sin sesión devuelve 401.

## 3. Pruebas
- [x] 3.1 Comparar las cifras con el cierre diario: total cobrado hoy = ventas + abonos, desglose por forma de pago, total pendiente de cobro.

## 4. Entrega
- [x] 4.1 Exportado a `workflows/21 - Panel móvil para Marisa.json`; revisado: sin claves ni tokens (solo nombres de credencial).
- [x] 4.2 Anotado en `docs/ai-log.md`.

## 5. Cierre del change (obligatorio al terminar)
- [ ] 5.1 Validar: `openspec validate t-021-panel-marisa --strict`
- [ ] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-021-panel-marisa`.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #38`)
