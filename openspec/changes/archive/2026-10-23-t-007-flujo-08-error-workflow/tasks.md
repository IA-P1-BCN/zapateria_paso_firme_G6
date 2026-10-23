## 1. Workflow
- [x] 1.1 Crear `08 - Error Workflow` con *Error Trigger*
- [x] 1.2 Nodo Code que arma el texto (flujo, nodo, error, hora, enlace) y oculta secretos
- [x] 1.3 Llamar a `SUB - Enviar notificación` (destinatario `tienda`)

## 2. Pruebas
- [x] 2.1 Crear un flujo de prueba con un nodo que falla a propósito y asignarle `08`
- [x] 2.2 Comprobar que llega el aviso y que no lleva claves (probar con un error que contenga `X-API-Key: abc`)

## 3. Despliegue
- [x] 3.1 Asignar `08` en tu n8n a los flujos que ya existan (`00`, `SUB - Buscar apartado`), salvo `SUB - Enviar notificación` (bucle). No se re-exportan sus JSON: el id de `08` es propio de cada instancia
- [x] 3.2 Anotar en el README que, tras importar un flujo, hay que elegir `08 - Error Workflow` en *Settings → Error workflow*; y recordar al equipo que cada flujo nuevo debe asignarlo

## 4. Entrega
- [x] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [x] 4.2 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [x] 5.1 Validar: `openspec validate t-007-flujo-08-error-workflow --strict`
- [x] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-007-flujo-08-error-workflow`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [x] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
