## 1. Preparación
- [x] 1.1 Crear la credencial `Tienda API` (Header Auth, cabecera `X-API-Key`) en n8n
- [x] 1.2 Preparar un payload de ejemplo por evento (4 JSON, más uno de evento desconocido) en `data/eventos/`

## 2. Workflow de entrada
- [x] 2.1 Crear `00 - Entrada tienda`: Webhook POST `tienda` con respuesta 200 inmediata
- [x] 2.2 Añadir el Switch por `$json.body.evento` con 4 ramas y una rama "desconocido"
- [x] 2.3 Conectar cada rama a un nodo NoOp (se sustituye por un *Execute Workflow* real en cada T-xxx); la rama `apartado.vencido` queda sin acción (NoOp)

## 3. Pruebas
- [x] 3.1 Probar con los 4 payloads (URL de test) y con un evento inventado
- [x] 3.2 Publicar y comprobar que la app avisa de verdad (crear un apartado en la app)

## 4. Entrega
- [x] 4.1 Exportar a `workflows/00 - Entrada tienda.json` (el nombre del flujo) y revisar que no hay claves
- [x] 4.2 Escribir la lista de credenciales y variables en el README
- [x] 4.3 Anotar en `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [x] 5.1 Validar: `openspec validate t-001-base-webhook-credenciales --strict`
- [x] 5.2 Archivar con `/opsx:archive` (en OpenCode: `/opsx-archive`) o `openspec archive t-001-base-webhook-credenciales`. Esto mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, que es la fuente de verdad del comportamiento actual.
- [x] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
