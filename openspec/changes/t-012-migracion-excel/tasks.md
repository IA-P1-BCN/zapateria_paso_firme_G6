## 1. Preparación
- [ ] 1.1 Leer los dos CSV y listar los problemas (fechas, importes, nombres, duplicados)
- [ ] 1.2 Confirmar con Marisa los casos dudosos
- [ ] 1.3 Preparar una base limpia (`SEED=0` o volumen nuevo)

## 2. Lectura y limpieza
- [ ] 2.1 Flujo con *Read Binary File* / *Extract from File* de los dos CSV
- [ ] 2.2 Nodo Code de normalización (fechas, importes, nombres)
- [ ] 2.3 Ignorar la fila de total

## 3. Agrupación
- [ ] 3.1 Agrupar por cliente + teléfono + modelo + talla
- [ ] 3.2 Marcar los dudosos (abono inicial < 5 €)
- [ ] 3.3 Detectar ventas que son abonos y deducir `forma_pago`

## 4. Carga
- [ ] 4.1 Crear cliente/apartado con su fecha original
- [ ] 4.2 Cargar abonos en orden cronológico
- [ ] 4.3 Cargar las ventas restantes
- [ ] 4.4 Comprobar `pendiente` contra la columna `resta`
- [ ] 4.5 Hacerla idempotente

## 5. Informe y pruebas
- [ ] 5.1 Enviar el informe de no cargados a Marisa
- [ ] 5.2 Ejecutar dos veces y comprobar que no duplica
- [ ] 5.3 Comparar los totales con el Excel

## 6. Entrega
- [ ] 6.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [ ] 6.2 Documentar en el README cómo ejecutarla (una sola vez)
- [ ] 6.3 Anotar en la sección propia de `docs/ai-log.md`

## 7. Cierre del change (obligatorio al terminar)
- [ ] 7.1 Validar: `openspec validate t-012-migracion-excel --strict`
- [ ] 7.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-012-migracion-excel`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 7.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
