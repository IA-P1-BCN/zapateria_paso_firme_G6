## 1. Preparación
- [ ] 1.1 Confirmar el umbral con Marisa y crear la variable (o `$env`)
- [ ] 1.2 Copiar los payloads de `venta.registrada` (por encima, igual, por debajo)

## 2. Workflow
- [ ] 2.1 Crear `04 - Venta grande` con *Execute Workflow Trigger*
- [ ] 2.2 IF `importe >= umbral`
- [ ] 2.3 Llamar a `SUB - Enviar notificación` (destinatario `tienda`)
- [ ] 2.4 Conectarlo en la rama `venta.registrada` de `00 - Entrada tienda`
- [ ] 2.5 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 3. Pruebas
- [ ] 3.1 Probar los 3 payloads y un cambio de umbral
- [ ] 3.2 Registrar una venta real desde la app

## 4. Entrega
- [ ] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [ ] 4.2 Apuntar la variable en la lista del README
- [ ] 4.3 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [ ] 5.1 Validar: `openspec validate t-010-flujo-04-venta-grande --strict`
- [ ] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-010-flujo-04-venta-grande`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
