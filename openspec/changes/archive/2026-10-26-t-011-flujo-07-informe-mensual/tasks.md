## 1. Preparación
- [x] 1.1 Probar a mano los endpoints (`ventas`, `abonos`, `apartados`, `vales`) con rango de fechas
- [x] 1.2 Decidir hora y confirmar con Marisa

## 2. Workflow
- [x] 2.1 Crear `07 - Informe mensual` con *Schedule Trigger* día 1, 08:00 `Europe/Madrid`
- [x] 2.2 Calcular `desde` y `hasta` del mes anterior
- [x] 2.3 Pedir ventas, abonos, activos, liquidados y vales
- [x] 2.4 Nodo Code: sumas en céntimos y conteos
- [x] 2.5 Llamar a `SUB - Enviar notificación` (destinatario `tienda`)
- [x] 2.6 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 3. Pruebas
- [x] 3.1 Ejecutar manualmente con el mes de los datos de prueba y comparar con la app
- [x] 3.2 Probar un mes vacío

## 4. Entrega
- [x] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [x] 4.2 Dejar el flujo sin activar hasta la demo
- [x] 4.3 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [x] 5.1 Validar: `openspec validate t-011-flujo-07-informe-mensual --strict`
- [x] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-011-flujo-07-informe-mensual`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [x] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
