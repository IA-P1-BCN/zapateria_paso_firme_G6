## 1. Preparación
- [x] 1.1 Leer los dos CSV y listar los problemas (fechas, importes, nombres, duplicados)
- [x] 1.2 Confirmar con Marisa los casos dudosos
- [x] 1.3 Preparar una base limpia (`SEED=0` o volumen nuevo)

## 2. Lectura y limpieza
- [x] 2.1 Flujo con *Read Binary File* / *Extract from File* de los dos CSV
- [x] 2.2 Nodo Code de normalización (fechas, importes, nombres)
- [x] 2.3 Ignorar la fila de total

## 3. Agrupación
- [x] 3.1 Agrupar por cliente + teléfono + modelo + talla
- [x] 3.2 Marcar los dudosos (abono inicial < 5 €)
- [x] 3.3 Detectar ventas que son abonos y deducir `forma_pago`

## 4. Carga
- [x] 4.1 Crear cliente/apartado con su fecha original
- [x] 4.2 Cargar abonos en orden cronológico
- [x] 4.3 Cargar las ventas restantes
- [x] 4.4 Comprobar `pendiente` contra la columna `resta`
- [x] 4.5 Hacerla idempotente

## 5. Informe y pruebas
- [x] 5.1 Enviar el informe de no cargados a Marisa
- [x] 5.2 Ejecutar dos veces y comprobar que no duplica
- [x] 5.3 Comparar los totales con el Excel

## 6. Entrega
- [x] 6.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [x] 6.2 Documentar en el README cómo ejecutarla (una sola vez)
- [x] 6.3 Anotar en la sección propia de `docs/ai-log.md`

## 7. Cierre del change (obligatorio al terminar)
- [x] 7.1 Validar: `openspec validate t-012-migracion-excel --strict`
- [x] 7.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-012-migracion-excel`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [x] 7.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
