# venta-grande Specification

## Purpose
Define cuándo se debe notificar a Marisa una venta registrada que alcanza o supera el umbral configurable.

## Requirements

### Requirement: Aviso de venta grande
El flujo SHALL enviar a Marisa un aviso con concepto, importe y forma de pago cuando `datos.importe` sea mayor o igual que el umbral configurado.

#### Scenario: Importe por encima
- **WHEN** llega `venta.registrada` con `importe` = 120 y el umbral es 80
- **THEN** Marisa recibe un aviso con concepto, `120,00 €` y forma de pago

#### Scenario: Importe igual al umbral
- **WHEN** `importe` = 80 y el umbral es 80
- **THEN** Marisa recibe el aviso

### Requirement: Ventas normales
El flujo SHALL NOT enviar nada cuando el importe es menor que el umbral.

#### Scenario: Importe por debajo
- **WHEN** llega `venta.registrada` con `importe` = 45 y el umbral es 80
- **THEN** no se envía ningún mensaje

### Requirement: Umbral configurable
El umbral SHALL leerse de una variable de configuración.

#### Scenario: Cambio de umbral
- **WHEN** se cambia la variable a 50
- **THEN** una venta de 60 € dispara el aviso sin editar el flujo
