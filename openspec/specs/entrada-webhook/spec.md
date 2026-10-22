# entrada-webhook Specification

## Purpose
TBD - created by archiving change t-001-base-webhook-credenciales. Update Purpose after archive.

## Requirements

### Requirement: Entrada única de eventos
El workflow `00 - Entrada tienda` SHALL recibir por `POST /webhook/tienda` los eventos de la app y derivar cada uno a su flujo según `$json.body.evento`.

#### Scenario: Evento conocido
- **WHEN** llega `apartado.creado`, `abono.registrado`, `venta.registrada` o `apartado.vencido`
- **THEN** el Switch lo envía a la rama de ese evento con `datos` intactos

#### Scenario: Evento desconocido
- **WHEN** llega un `evento` no previsto
- **THEN** no se ejecuta ningún flujo y el workflow no falla

### Requirement: Respuesta inmediata
El workflow SHALL responder 200 a la app antes de procesar el evento.

#### Scenario: Flujo lento
- **WHEN** el flujo de destino tarda más de 5 segundos
- **THEN** la app ya ha recibido el 200

### Requirement: Credenciales sin valores en el repositorio
Los workflows exportados SHALL referenciar las credenciales solo por nombre.

#### Scenario: Exportar el workflow
- **WHEN** se exporta `00 - Entrada tienda` a `workflows/`
- **THEN** el JSON no contiene claves ni tokens
