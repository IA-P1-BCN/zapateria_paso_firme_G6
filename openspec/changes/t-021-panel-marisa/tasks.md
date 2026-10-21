## 1. Preparación
- [ ] 1.1 Decidir tecnología del panel (página de n8n u otra)

## 2. Construcción
- [ ] 2.1 Consultas a la API y maqueta móvil
- [ ] 2.2 Proteger el acceso

## 3. Pruebas
- [ ] 3.1 Comparar las cifras con el cierre diario

## 4. Entrega
- [ ] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [ ] 4.2 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [ ] 5.1 Validar: `openspec validate t-021-panel-marisa --strict`
- [ ] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-021-panel-marisa`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
