## ADDED Requirements

### Requirement: Contrato único de notificación
El sub-workflow `SUB - Enviar notificación` SHALL aceptar `destinatario`, `email`, `asunto`, `mensaje` y `contexto`, y SHALL devolver `{enviado, motivo}`.

#### Scenario: Envío a una clienta con correo
- **WHEN** se llama con `destinatario` = `cliente` y un `email` válido
- **THEN** se envía el correo con ese asunto y mensaje
- **AND** devuelve `enviado` = true

#### Scenario: Envío a Marisa
- **WHEN** se llama con `destinatario` = `tienda`
- **THEN** se envía a la dirección configurada en la variable de la tienda
- **AND** devuelve `enviado` = true

### Requirement: Clienta sin correo
El sub-workflow SHALL NOT fallar cuando el cliente no tiene `email`; SHALL avisar a la tienda con el `contexto` y devolver `motivo` = `sin_email`.

#### Scenario: Apartado sin email
- **WHEN** se llama con `destinatario` = `cliente` y `email` vacío o ausente
- **THEN** se envía un aviso a la tienda que indica que no se pudo enviar y a qué apartado se refería
- **AND** devuelve `enviado` = false y `motivo` = `sin_email`

### Requirement: Un fallo de envío no rompe al llamante
Si el servidor de correo falla, el sub-workflow SHALL devolver `enviado` = false y `motivo` = `error_envio` sin lanzar error.

#### Scenario: Servidor de correo caído
- **WHEN** el envío devuelve un error
- **THEN** el flujo que llama sigue ejecutándose
- **AND** recibe `enviado` = false y `motivo` = `error_envio`
