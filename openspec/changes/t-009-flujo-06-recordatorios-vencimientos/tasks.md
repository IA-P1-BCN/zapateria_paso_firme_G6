## 1. Preparación
- [ ] 1.1 Revisar con la API real `GET /api/apartados?estado=activo` y la respuesta de `vencer`
- [ ] 1.2 Preparar datos de prueba con fechas límite pasadas, de mañana y de dentro de 7 días (en un volumen de pruebas, no en el de la demo)
- [ ] 1.3 Decidir con Marisa la hora (09:00 por defecto)

## 2. Recordatorios
- [ ] 2.1 Crear `06 - Recordatorios y vencimientos` con *Schedule Trigger* 09:00 `Europe/Madrid`
- [ ] 2.2 Traer activos y filtrar en Code: hoy+7 y hoy+1
- [ ] 2.3 Evitar repetidos con datos estáticos del workflow
- [ ] 2.4 Llamar a `SUB - Enviar notificación`

## 3. Vencimientos
- [ ] 3.1 Filtrar activos con `fecha_limite` < hoy
- [ ] 3.2 `POST /api/apartados/{id}/vencer` para cada uno, tolerando el 422
- [ ] 3.3 Mensaje a la clienta con vale (código e importe de la respuesta)
- [ ] 3.4 Un mensaje a Marisa con la lista, solo si no está vacía
- [ ] 3.5 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 4. Pruebas
- [ ] 4.1 Ejecutar con los datos de prueba y revisar los envíos
- [ ] 4.2 Ejecutar dos veces seguidas y comprobar que no duplica
- [ ] 4.3 Confirmar que el evento `apartado.vencido` no genera un segundo aviso

## 5. Entrega
- [ ] 5.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [ ] 5.2 Dejar el flujo sin activar hasta la demo
- [ ] 5.3 Anotar en la sección propia de `docs/ai-log.md`

## 6. Cierre del change (obligatorio al terminar)
- [ ] 6.1 Validar: `openspec validate t-009-flujo-06-recordatorios-vencimientos --strict`
- [ ] 6.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-009-flujo-06-recordatorios-vencimientos`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 6.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
