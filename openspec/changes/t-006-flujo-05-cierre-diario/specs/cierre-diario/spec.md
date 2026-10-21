## ADDED Requirements

### Requirement: Resumen nocturno
El flujo SHALL ejecutarse cada noche y enviar a Marisa un resumen con las ventas directas, los abonos y el total del día, separados por forma de pago (`efectivo`, `tarjeta`, `bizum`).

#### Scenario: Día con movimientos
- **WHEN** son las 22:00 y hay ventas y abonos de hoy
- **THEN** Marisa recibe tres bloques: ventas, abonos y total, cada uno con efectivo, tarjeta y bizum
- **AND** los importes coinciden con la suma de los datos de la app

#### Scenario: Forma de pago sin movimientos
- **WHEN** no hay cobros por `bizum` hoy
- **THEN** el resumen muestra `0,00 €` en bizum

### Requirement: Día sin movimientos
El flujo SHALL NOT fallar si no hay ventas ni abonos; SHALL enviar un mensaje que lo diga.

#### Scenario: Domingo cerrado
- **WHEN** las listas de ventas y abonos llegan vacías
- **THEN** Marisa recibe `Hoy no hubo movimientos` y la ejecución termina sin error

### Requirement: Rango de fechas del día
El flujo SHALL pedir a la app ventas y abonos con `desde` y `hasta` iguales a la fecha de hoy en Madrid.

#### Scenario: Cerca de medianoche
- **WHEN** el flujo se ejecuta a las 22:00 hora de Madrid
- **THEN** la fecha consultada es la de ese día en Madrid, no la de UTC
