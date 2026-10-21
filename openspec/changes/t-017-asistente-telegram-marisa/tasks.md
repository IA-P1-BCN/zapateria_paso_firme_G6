## 1. Preparación
- [ ] 1.1 Decidir bot y guardar el id de chat de Marisa en una variable

## 2. Flujo
- [ ] 2.1 Trigger de Telegram con comprobación del chat
- [ ] 2.2 Consultas: apartado de X, resumen del día
- [ ] 2.3 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 3. Pruebas
- [ ] 3.1 Probar chat autorizado y no autorizado

## 4. Entrega
- [ ] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [ ] 4.2 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [ ] 5.1 Validar: `openspec validate t-017-asistente-telegram-marisa --strict`
- [ ] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-017-asistente-telegram-marisa`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
