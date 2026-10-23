## 1. Preparación
- [x] 1.1 Leer la spec `tienda-webhook` y copiar los payloads de `apartado.creado` (normal, liquidado, sin email)
- [x] 1.2 Escribir los dos textos del mensaje (normal y liquidado) en español claro

## 2. Workflow
- [x] 2.1 Crear `01 - Confirmación de apartado` con *Execute Workflow Trigger*
- [x] 2.2 Nodo Code que da formato a importes y fechas
- [x] 2.3 IF `estado` = `liquidado` → texto de recogida; si no → texto de confirmación
- [x] 2.4 Llamar a `SUB - Enviar notificación` (destinatario `cliente`, `contexto` con el nº de apartado)
- [x] 2.5 Conectarlo en la rama `apartado.creado` de `00 - Entrada tienda`
- [x] 2.6 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 3. Pruebas
- [x] 3.1 Probar los 3 payloads (normal, liquidado, sin email)
- [x] 3.2 Crear un apartado real en la app y ver llegar el correo (flujo publicado)

## 4. Entrega
- [x] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [x] 4.2 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [x] 5.1 Validar: `openspec validate t-004-flujo-01-confirmacion-apartado --strict`
- [x] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-004-flujo-01-confirmacion-apartado`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [x] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
