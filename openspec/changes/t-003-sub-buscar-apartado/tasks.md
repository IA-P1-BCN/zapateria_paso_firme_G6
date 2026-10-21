## 1. Preparación
- [ ] 1.1 Revisar con la API real cómo devuelve `GET /api/apartados?estado=activo` (cabecera `X-Total-Count`)
- [ ] 1.2 Escribir 6 entradas de prueba: `JORGE M.`, `LAURA O.`, `ROMERO D`, `LUCIA GOMEZ`, `#2`, un nombre que no existe

## 2. Sub-workflow
- [ ] 2.1 Crear `SUB - Buscar apartado` con *Execute Workflow Trigger* (`id`, `texto`)
- [ ] 2.2 Rama `id`: `GET /api/apartados/{id}` (credencial `Tienda API`), 404 → `ninguno`
- [ ] 2.3 Rama `texto`: traer apartados `activo` y filtrar en un nodo Code (normalizar, trozos, puntuación)
- [ ] 2.4 Devolver siempre la salida normalizada del diseño

## 3. Pruebas
- [ ] 3.1 Ejecutar las 6 entradas y comparar con lo esperado
- [ ] 3.2 Probar con un payload de ejemplo (URL de test) y enseñar el resultado antes de publicar

## 4. Entrega
- [ ] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [ ] 4.2 Documentar el contrato en el README
- [ ] 4.3 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [ ] 5.1 Validar: `openspec validate t-003-sub-buscar-apartado --strict`
- [ ] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-003-sub-buscar-apartado`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
