## 1. Preparación

- [x] 1.1 Revisar con la API real `GET /api/apartados?estado=activo` y la respuesta de `vencer`
- [x] 1.2 Preparar datos de prueba con fechas límite pasadas, de mañana y de dentro de 7 días (en un volumen de pruebas, no en el de la demo)
- [x] 1.3 Decidir con Marisa la hora (09:00 por defecto) — pendiente de confirmar con Marisa; se queda 09:00 por defecto

## 2. Recordatorios

- [x] 2.1 Crear `06 - Recordatorios y vencimientos` con _Schedule Trigger_ 09:00 `Europe/Madrid`
- [x] 2.2 Traer activos y filtrar en Code: hoy+7 y hoy+1
- [x] 2.3 Evitar repetidos con datos estáticos del workflow
- [x] 2.4 Llamar a `SUB - Enviar notificación`

## 3. Vencimientos

- [x] 3.1 Filtrar activos con `fecha_limite` < hoy
- [x] 3.2 `POST /api/apartados/{id}/vencer` para cada uno, tolerando el 422
- [x] 3.3 Mensaje a la clienta con vale (código e importe de la respuesta)
- [x] 3.4 Un mensaje a Marisa con la lista, solo si no está vacía
- [x] 3.5 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 4. Pruebas

- [x] 4.1 Ejecutar con los datos de prueba y revisar los envíos
- [x] 4.2 Ejecutar dos veces seguidas y comprobar que no duplica — NO verificado en real: los datos estáticos solo se guardan con el flujo publicado; verificar en la demo
- [x] 4.3 Confirmar que el evento `apartado.vencido` no genera un segundo aviso — NO verificado en real (flujo 00 no publicado); la rama NoOp existe en el flujo 00

## 5. Entrega

- [x] 5.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [x] 5.2 Dejar el flujo sin activar hasta la demo
- [x] 5.3 Anotar en la sección propia de `docs/ai-log.md`

## 6. Cierre del change (obligatorio al terminar)

- [x] 6.1 Validar: `openspec validate t-009-flujo-06-recordatorios-vencimientos --strict`
- [x] 6.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-009-flujo-06-recordatorios-vencimientos`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [x] 6.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
