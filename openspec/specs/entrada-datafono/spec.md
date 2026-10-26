# entrada-datafono Specification

## Purpose
El flujo `Entrada CSV del datáfono` lee el CSV de cobros con tarjeta del datáfono, lo cuadra con las ventas y los abonos pagados con tarjeta que ya hay en la app y registra como venta con tarjeta los cobros que faltan, sin duplicar; lo que no entiende no lo carga y se lo cuenta a Marisa. Flujo: `workflows/Entrada CSV del datáfono.json`; CSV de ejemplo y resultados, en `data/datafono_octubre.csv` y el README.

## Requirements

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
