## ADDED Requirements

### Requirement: Crear apartado desde una solicitud
El flujo SHALL crear el apartado en la app cuando la solicitud cumple las reglas.

#### Scenario: Solicitud válida
- **WHEN** llega una solicitud completa con abono inicial de 10 €
- **THEN** se crea el apartado en la app

#### Scenario: Solicitud incompleta
- **WHEN** falta el producto o el cliente
- **THEN** no se crea nada y se avisa a Marisa

### Requirement: Sin duplicados
El flujo SHALL NOT crear dos apartados para la misma solicitud.

#### Scenario: Solicitud repetida
- **WHEN** se recibe dos veces la misma solicitud
- **THEN** solo se crea un apartado

### Requirement: Solicitud pendiente hasta el abono inicial
El flujo SHALL guardar cada solicitud válida como pendiente sin crear nada en la app, y SHALL crear el apartado solo cuando la tienda confirme el pago del abono inicial con el precio, el abono y la forma de pago.

#### Scenario: Solicitud recibida
- **WHEN** un cliente envía una solicitud completa
- **THEN** queda guardada como pendiente con un número de solicitud
- **AND** no se crea ningún apartado en la app y se avisa a Marisa

#### Scenario: Confirmación con abono por debajo del mínimo
- **WHEN** la tienda confirma una solicitud con un abono inicial de 3 €
- **THEN** no se crea el apartado y Marisa recibe el motivo
