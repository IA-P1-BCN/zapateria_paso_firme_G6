## 1. Decisiones previas
- [ ] 1.1 Decidir la forma de pago de las transferencias (decisión abierta del diseño) y anotarla
- [ ] 1.2 Confirmar contra la app (seed) a qué apartado corresponde cada uno de los 9 correos
- [ ] 1.3 Crear las credenciales `Correo entrada` y `Modelo IA`

## 2. Entrada y filtro
- [ ] 2.1 Disparador de correo (IMAP) o lectura de los `.eml` de `data/correos/` en desarrollo
- [ ] 2.2 Filtro previo: descartar sin `Importe` y `Ordenante`
- [ ] 2.3 Evitar duplicados (marcar leído y guardar `Message-ID`)

## 3. Extracción
- [ ] 3.1 Prompt que devuelve JSON `{ordenante, importe, concepto}` para los dos formatos
- [ ] 3.2 Validar y convertir el importe en un nodo Code

## 4. Reglas
- [ ] 4.1 Llamar a `SUB - Buscar apartado` con ordenante y concepto
- [ ] 4.2 Nodo de reglas: único, activo, importe <= pendiente, plazo; si no → dudoso o rechazo
- [ ] 4.3 `POST /api/apartados/{id}/abonos` con la forma de pago decidida
- [ ] 4.4 Aviso a Marisa en dudosos y rechazos, con motivo y candidatos
- [ ] 4.5 Asignar `08 - Error Workflow` como flujo de error (Ajustes del workflow)

## 5. Pruebas
- [ ] 5.1 Pasar los 9 correos y rellenar la tabla de resultados reales en el README
- [ ] 5.2 Guardar capturas de cada resultado como evidencia

## 6. Entrega
- [ ] 6.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [ ] 6.2 No guardar ninguna clave del modelo de IA en el JSON
- [ ] 6.3 Anotar en la sección propia de `docs/ai-log.md`

## 7. Cierre del change (obligatorio al terminar)
- [ ] 7.1 Validar: `openspec validate t-008-flujo-03-abonos-a-distancia --strict`
- [ ] 7.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-008-flujo-03-abonos-a-distancia`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 7.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
