## 1. Decisiones y credenciales
- [ ] 1.1 Decidir con el equipo qué cuenta de correo (Gmail o SMTP) se usa y anotarlo en el diseño
- [ ] 1.2 Crear la credencial `Correo salida` y la variable con el correo de la tienda (apuntar en la lista del README)

## 2. Sub-workflow
- [ ] 2.1 Crear `SUB - Enviar notificación` con *Execute Workflow Trigger* y los 5 campos del contrato
- [ ] 2.2 Rama cliente con email → enviar correo; rama tienda → enviar a la variable
- [ ] 2.3 Rama cliente sin email → aviso a la tienda con `contexto` y salida `sin_email`
- [ ] 2.4 Activar *Continuar en error* en el nodo de envío y devolver `error_envio`

## 3. Pruebas
- [ ] 3.1 Probar 4 casos: cliente con email, cliente sin email, tienda, servidor caído (credencial mal puesta a propósito)

## 4. Entrega
- [ ] 4.1 Exportar a `workflows/` y revisar que el JSON no contiene claves ni tokens
- [ ] 4.2 Documentar el contrato en el README (para que los demás lo llamen)
- [ ] 4.3 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [ ] 5.1 Validar: `openspec validate t-002-sub-enviar-notificacion --strict`
- [ ] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-002-sub-enviar-notificacion`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
