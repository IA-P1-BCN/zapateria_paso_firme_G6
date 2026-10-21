## ADDED Requirements

### Requirement: Webhook autenticado
El webhook SHALL rechazar los eventos sin la clave correcta.

#### Scenario: Sin clave
- **WHEN** llega un evento sin la cabecera de autenticación
- **THEN** se rechaza y no se ejecuta ningún flujo

### Requirement: Datos enviados documentados
El README SHALL listar qué datos personales se envían a cada servicio externo.

#### Scenario: Revisión
- **WHEN** se revisa el README
- **THEN** cada servicio externo tiene su lista de datos
