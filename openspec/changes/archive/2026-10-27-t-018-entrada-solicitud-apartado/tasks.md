## 1. Preparación
- [x] 1.1 Decidir el canal de entrada (formulario de n8n o Telegram)

## 2. Flujo
- [x] 2.1 Recibir y validar la solicitud
- [x] 2.2 `POST /api/apartados` y aviso a Marisa en dudosos
- [x] 2.3 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 3. Pruebas
- [x] 3.1 Probar solicitud válida, incompleta y repetida

## 4. Entrega
- [x] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [x] 4.2 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [x] 5.1 Validar: `openspec validate t-018-entrada-solicitud-apartado --strict`
- [x] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-018-entrada-solicitud-apartado`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [x] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
