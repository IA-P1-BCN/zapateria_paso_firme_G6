## 1. Revisión
- [x] 1.1 Listar los datos que salen de n8n a servicios externos
- [x] 1.2 Definir autenticación por cabecera y configurar emisor y receptor sin exponer el token en la URL

## 2. Cambios
- [x] 2.1 Añadir autenticación al webhook
- [x] 2.2 Documentar datos y consentimiento en el README

## 3. Pruebas
- [x] 3.1 Probar evento con y sin clave

## 4. Entrega
- [x] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [x] 4.2 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [x] 5.1 Validar: `openspec validate t-020-proteccion-datos --strict`
- [x] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-020-proteccion-datos`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
