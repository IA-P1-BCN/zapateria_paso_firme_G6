# proteccion-datos Specification

## Purpose
Documenta la autenticación del webhook de entrada y las transmisiones de datos a servicios externos para reducir riesgos de acceso no autorizado y facilitar un tratamiento responsable de los datos personales.

## Requirements

### Requirement: Webhook autenticado

El webhook SHALL validar la cabecera `X-Webhook-Token` frente al valor configurado en `WEBHOOK_TOKEN` antes de procesar el evento. El token SHALL viajar en la cabecera y SHALL NOT incluirse en la URL ni en el workflow exportado como valor literal.

#### Scenario: Sin clave

- **WHEN** llega un evento sin la cabecera `X-Webhook-Token`
- **THEN** se rechaza la petición y no se procesa el evento

#### Scenario: Clave incorrecta

- **WHEN** llega un evento con una cabecera `X-Webhook-Token` que no coincide con `WEBHOOK_TOKEN`
- **THEN** se rechaza la petición y no se procesa el evento

#### Scenario: Clave válida

- **WHEN** llega un evento con una cabecera `X-Webhook-Token` que coincide con `WEBHOOK_TOKEN`
- **THEN** el webhook acepta la petición para su procesamiento

### Requirement: Datos enviados documentados

El README SHALL documentar los datos transmitidos a cada servicio externo, la finalidad de cada transmisión y las precauciones aplicables al tratamiento de datos personales.

#### Scenario: Revisión de servicios externos

- **WHEN** se revisa la documentación de privacidad del README
- **THEN** se identifican los servicios externos, las categorías de datos que reciben y la finalidad del envío

#### Scenario: Tratamiento de datos personales

- **WHEN** un flujo transmite datos personales a un proveedor externo
- **THEN** la documentación advierte de esa transmisión y recomienda limitar los datos a los necesarios y revisar las condiciones y la base jurídica aplicable
