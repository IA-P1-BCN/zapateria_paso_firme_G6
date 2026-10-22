## 1. Decisiones y credenciales
- [x] 1.1 Decidir con el equipo qué cuenta de correo (Gmail o SMTP) se usa y anotarlo en el diseño
- [x] 1.2 Crear la credencial `Correo salida` y la variable con el correo de la tienda (apuntar en la lista del README)

## 2. Sub-workflow
- [x] 2.1 Crear `SUB - Enviar notificación` con *Execute Workflow Trigger* y los 5 campos del contrato
- [x] 2.2 Rama cliente con email → enviar correo; rama tienda → enviar a la variable
- [x] 2.3 Rama cliente sin email → aviso a la tienda con `contexto` y salida `sin_email`
- [x] 2.4 Activar *Continuar en error* en el nodo de envío y devolver `error_envio`

## 3. Pruebas
- [x] 3.1 Probar 4 casos: cliente con email, cliente sin email, tienda, servidor caído (credencial mal puesta a propósito)

## 4. Entrega
- [x] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [x] 4.2 Documentar el contrato en el README (para que los demás lo llamen)
- [x] 4.3 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [x] 5.1 Validar: `openspec validate t-002-sub-enviar-notificacion --strict`
- [x] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-002-sub-enviar-notificacion`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [x] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
