## 1. Preparación
- [ ] 1.1 Crear la credencial `Tienda API` (Header Auth, cabecera `X-API-Key`) en n8n
- [ ] 1.2 Preparar un payload de ejemplo por evento (4 JSON)

## 2. Workflow de entrada
- [ ] 2.1 Crear `00 - Entrada tienda`: Webhook POST `tienda` con respuesta 200 inmediata
- [ ] 2.2 Añadir el Switch por `$json.body.evento` con 4 ramas y una rama "desconocido"
- [ ] 2.3 Conectar cada rama a un sub-workflow vacío (se sustituye por el real en cada T-xxx)

## 3. Pruebas
- [ ] 3.1 Probar con los 4 payloads (URL de test) y con un evento inventado
- [ ] 3.2 Publicar y comprobar que la app avisa de verdad (crear un apartado en la app)

## 4. Entrega
- [ ] 4.1 Exportar a `workflows/00-entrada-tienda.json` y revisar que no hay claves
- [ ] 4.2 Escribir la lista de credenciales y variables en el README
- [ ] 4.3 Anotar en `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [ ] 5.1 Validar: `openspec validate t-001-base-webhook-credenciales --strict`
- [ ] 5.2 Archivar con `/opsx:archive` (en OpenCode: `/opsx-archive`) o `openspec archive t-001-base-webhook-credenciales`. Esto mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, que es la fuente de verdad del comportamiento actual.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
