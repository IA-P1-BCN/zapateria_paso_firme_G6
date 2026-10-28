## ADDED Requirements

### Requirement: Resumen de hoy en el móvil
El panel SHALL mostrar lo cobrado hoy y los apartados próximos a vencer.

#### Scenario: Panel abierto
- **WHEN** Marisa abre el panel en el móvil
- **THEN** ve el total de hoy y la lista de apartados por vencer

### Requirement: Acceso protegido
El panel SHALL requerir autenticación.

#### Scenario: Sin sesión
- **WHEN** alguien abre el panel sin iniciar sesión
- **THEN** no ve ningún dato
