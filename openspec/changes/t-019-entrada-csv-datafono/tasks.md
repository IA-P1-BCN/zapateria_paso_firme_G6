## 1. Preparación
- [ ] 1.1 Conseguir un CSV de ejemplo del datáfono (datos ficticios)

## 2. Flujo
- [ ] 2.1 Leer y normalizar el CSV
- [ ] 2.2 Comparar con las ventas existentes
- [ ] 2.3 Registrar las nuevas e informar de las dudosas
- [ ] 2.4 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 3. Pruebas
- [ ] 3.1 Ejecutar dos veces y comprobar que no duplica

## 4. Entrega
- [ ] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [ ] 4.2 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [ ] 5.1 Validar: `openspec validate t-019-entrada-csv-datafono --strict`
- [ ] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-019-entrada-csv-datafono`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
