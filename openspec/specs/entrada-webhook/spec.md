# entrada-webhook Specification

## Purpose
Entrada unica de eventos de la app por POST /webhook/tienda con autenticacion por token y derivacion por evento.

## Requirements

### Requirement: Entrada única de eventos
El workflow `00 - Entrada tienda` SHALL recibir por `POST /webhook/tienda` los eventos de la app, validar primero la cabecera `X-Webhook-Token` contra `WEBHOOK_TOKEN` y derivar únicamente las solicitudes autenticadas según `$json.body.evento`.

#### Scenario: Evento conocido
- **WHEN** llega `apartado.creado`, `abono.registrado`, `venta.registrada` o `apartado.vencido`
- **THEN** el Switch lo envía a la rama de ese evento con `datos` intactos

#### Scenario: Evento desconocido
- **WHEN** llega un `evento` no previsto
- **THEN** no se ejecuta ningún flujo y el workflow no falla

### Requirement: Respuesta inmediata
El workflow SHALL responder HTTP 202 a las solicitudes autenticadas antes de procesar el evento y HTTP 401 a las solicitudes no autenticadas.

#### Scenario: Flujo lento
- **WHEN** el flujo de destino tarda más de 5 segundos
- **THEN** la app ya ha recibido el HTTP 202

#### Scenario: Token ausente o incorrecto
- **WHEN** la solicitud no incluye `X-Webhook-Token` o el valor no coincide con `WEBHOOK_TOKEN`
- **THEN** el workflow responde HTTP 401 y no deriva el evento a ningún flujo

### Requirement: Credenciales sin valores en el repositorio
Los workflows exportados SHALL referenciar las credenciales solo por nombre.

#### Scenario: Exportar el workflow
- **WHEN** se exporta `00 - Entrada tienda` a `workflows/`
- **THEN** el JSON no contiene claves ni tokens

### Requirement: Webhook autenticado
El workflow `00 - Entrada tienda` SHALL rechazar los eventos sin la cabecera `X-Webhook-Token` correcta cuando `WEBHOOK_TOKEN` esté configurado.

#### Scenario: Sin token válido
- **WHEN** llega un evento sin la cabecera de autenticación o con un token incorrecto
- **THEN** se rechaza y no se ejecuta ningún flujo
