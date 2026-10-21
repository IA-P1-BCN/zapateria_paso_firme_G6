## 1. Preparación
- [ ] 1.1 Leer la spec `tienda-webhook` y copiar los payloads de `apartado.creado` (normal, liquidado, sin email)
- [ ] 1.2 Escribir los dos textos del mensaje (normal y liquidado) en español claro

## 2. Workflow
- [ ] 2.1 Crear `01 - Confirmación de apartado` con *Execute Workflow Trigger*
- [ ] 2.2 Nodo Code que da formato a importes y fechas
- [ ] 2.3 IF `estado` = `liquidado` → texto de recogida; si no → texto de confirmación
- [ ] 2.4 Llamar a `SUB - Enviar notificación` (destinatario `cliente`, `contexto` con el nº de apartado)
- [ ] 2.5 Conectarlo en la rama `apartado.creado` de `00 - Entrada tienda`
- [ ] 2.6 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 3. Pruebas
- [ ] 3.1 Probar los 3 payloads (normal, liquidado, sin email)
- [ ] 3.2 Crear un apartado real en la app y ver llegar el correo (flujo publicado)

## 4. Entrega
- [ ] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [ ] 4.2 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [ ] 5.1 Validar: `openspec validate t-004-flujo-01-confirmacion-apartado --strict`
- [ ] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-004-flujo-01-confirmacion-apartado`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
