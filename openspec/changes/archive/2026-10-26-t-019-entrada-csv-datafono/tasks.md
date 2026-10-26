## 1. Preparación
- [x] 1.1 Conseguir un CSV de ejemplo del datáfono (datos ficticios)

## 2. Flujo
- [x] 2.1 Leer y normalizar el CSV
- [x] 2.2 Comparar con las ventas existentes
- [x] 2.3 Registrar las nuevas e informar de las dudosas
- [x] 2.4 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 3. Pruebas
- [x] 3.1 Ejecutar dos veces y comprobar que no duplica

## 4. Entrega
- [x] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [x] 4.2 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [x] 5.1 Validar: `openspec validate t-019-entrada-csv-datafono --strict`
- [x] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-019-entrada-csv-datafono`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [x] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
