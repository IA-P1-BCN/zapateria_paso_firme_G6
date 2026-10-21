## 1. Preparación
- [ ] 1.1 Probar a mano los endpoints (`ventas`, `abonos`, `apartados`, `vales`) con rango de fechas
- [ ] 1.2 Decidir hora y confirmar con Marisa

## 2. Workflow
- [ ] 2.1 Crear `07 - Informe mensual` con *Schedule Trigger* día 1, 08:00 `Europe/Madrid`
- [ ] 2.2 Calcular `desde` y `hasta` del mes anterior
- [ ] 2.3 Pedir ventas, abonos, activos, liquidados y vales
- [ ] 2.4 Nodo Code: sumas en céntimos y conteos
- [ ] 2.5 Llamar a `SUB - Enviar notificación` (destinatario `tienda`)
- [ ] 2.6 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 3. Pruebas
- [ ] 3.1 Ejecutar manualmente con el mes de los datos de prueba y comparar con la app
- [ ] 3.2 Probar un mes vacío

## 4. Entrega
- [ ] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [ ] 4.2 Dejar el flujo sin activar hasta la demo
- [ ] 4.3 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [ ] 5.1 Validar: `openspec validate t-011-flujo-07-informe-mensual --strict`
- [ ] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-011-flujo-07-informe-mensual`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
