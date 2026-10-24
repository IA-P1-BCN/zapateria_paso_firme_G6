## 1. Preparación
- [x] 1.1 Copiar los payloads de `abono.registrado` (parcial, liquidado, sin email) de la spec `tienda-webhook`
- [x] 1.2 Escribir los dos textos (recibo y recogida)

## 2. Workflow
- [x] 2.1 Crear `02 - Recibo de abono` con *Execute Workflow Trigger*
- [x] 2.2 Formato de importes y fecha límite (nodo Code)
- [x] 2.3 IF `estado` = `liquidado`
- [x] 2.4 Llamar a `SUB - Enviar notificación`
- [x] 2.5 Conectarlo en la rama `abono.registrado` de `00 - Entrada tienda`
- [x] 2.6 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 3. Pruebas
- [x] 3.1 Probar los 3 payloads
- [x] 3.2 Registrar un abono real desde la app y comprobar el correo
- [x] 3.3 Comprobar que crear un apartado NO genera recibo

## 4. Entrega
- [x] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [x] 4.2 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [x] 5.1 Validar: `openspec validate t-005-flujo-02-recibo-abono --strict`
- [x] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-005-flujo-02-recibo-abono`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [x] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
