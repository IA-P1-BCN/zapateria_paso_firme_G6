## ADDED Requirements

### Requirement: Cargar solo lo que falta
El flujo SHALL registrar las líneas del CSV que no existan ya en la app.

#### Scenario: Línea nueva
- **WHEN** una línea del CSV no existe en la app
- **THEN** se registra como venta con forma de pago `tarjeta`

#### Scenario: Línea ya registrada
- **WHEN** la línea ya existe
- **THEN** no se crea otra venta

### Requirement: Informe de líneas dudosas
El flujo SHALL informar a Marisa de las líneas que no pudo interpretar.

#### Scenario: Línea ilegible
- **WHEN** una línea no tiene importe válido
- **THEN** no se carga y aparece en el informe
