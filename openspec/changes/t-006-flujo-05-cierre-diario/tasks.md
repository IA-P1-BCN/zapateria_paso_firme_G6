## 1. Preparación
- [ ] 1.1 Probar en el navegador o con curl `GET /api/ventas?desde=…&hasta=…` y `GET /api/abonos?desde=…&hasta=…` con la clave
- [ ] 1.2 Decidir con Marisa la hora (22:00 por defecto)
- [ ] 1.3 Decidir dónde se guarda el histórico de cierres

## 2. Workflow
- [ ] 2.1 Crear `05 - Cierre diario` con *Schedule Trigger* a las 22:00 y zona `Europe/Madrid`
- [ ] 2.2 Calcular `hoy` en Madrid
- [ ] 2.3 Dos nodos HTTP (credencial `Tienda API`): ventas y abonos de hoy
- [ ] 2.4 Nodo Code: sumar en céntimos por forma de pago y total
- [ ] 2.5 IF sin movimientos → mensaje específico
- [ ] 2.6 Guardar el cierre del día en el histórico (sin duplicar si se repite)
- [ ] 2.7 Llamar a `SUB - Enviar notificación` (destinatario `tienda`)
- [ ] 2.8 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 3. Pruebas
- [ ] 3.1 Ejecutar manualmente con datos de ejemplo y comparar con la suma hecha a mano
- [ ] 3.2 Probar un día vacío (cambiando la fecha a un domingo sin datos)
- [ ] 3.3 Comparar con lo que muestra la pantalla de la app

## 4. Entrega
- [ ] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [ ] 4.2 Dejar el flujo sin activar hasta la demo (solo una instancia lo tiene activo)
- [ ] 4.3 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [ ] 5.1 Validar: `openspec validate t-006-flujo-05-cierre-diario --strict`
- [ ] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-006-flujo-05-cierre-diario`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
