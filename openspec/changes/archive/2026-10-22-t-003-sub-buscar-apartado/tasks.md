## 1. Preparación
- [x] 1.1 Revisar con la API real cómo devuelve `GET /api/apartados?estado=activo` (cabecera `X-Total-Count`)
- [x] 1.2 Escribir 6 entradas de prueba: `JORGE M.`, `LAURA O.`, `ROMERO D`, `LUCIA GOMEZ`, `#2`, un nombre que no existe

## 2. Sub-workflow
- [x] 2.1 Crear `SUB - Buscar apartado` con *Execute Workflow Trigger* (`id`, `texto`)
- [x] 2.2 Rama `id`: `GET /api/apartados/{id}` (credencial `Tienda API`), 404 → `ninguno`
- [x] 2.3 Rama `texto`: traer apartados `activo` y filtrar en un nodo Code (normalizar, trozos, puntuación)
- [x] 2.4 Devolver siempre la salida normalizada del diseño

## 3. Pruebas
- [x] 3.1 Ejecutar las 6 entradas y comparar con lo esperado
- [x] 3.2 Probar con un payload de ejemplo (URL de test) y enseñar el resultado antes de publicar

## 4. Entrega
- [x] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [x] 4.2 Documentar el contrato en el README
- [x] 4.3 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [x] 5.1 Validar: `openspec validate t-003-sub-buscar-apartado --strict`
- [x] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-003-sub-buscar-apartado`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [x] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
