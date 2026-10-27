## ADDED Requirements

### Requirement: Resumen de hoy en el móvil
El panel SHALL mostrar lo cobrado hoy (ventas directas + abonos) y la lista de apartados próximos a vencer en los próximos 7 días.

#### Scenario: Panel abierto
- **WHEN** Marisa abre el panel en el móvil con una sesión válida
- **THEN** ve el total cobrado hoy, el desglose por forma de pago, la lista de apartados por vencer y el total pendiente de cobro

### Requirement: Acceso protegido
El panel SHALL requerir autenticación.

#### Scenario: Sin sesión
- **WHEN** alguien abre el panel sin iniciar sesión
- **THEN** no ve ningún dato (respuesta 401)
