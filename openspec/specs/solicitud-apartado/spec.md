# solicitud-apartado Specification

## Purpose
Un cliente pide un apartado desde casa con un formulario (`Solicitudes de apartado`): la solicitud se guarda como pendiente en la tabla de n8n `solicitudes_apartado` sin tocar la app, y el apartado se crea cuando la tienda confirma en un formulario protegido (`Confirmar solicitud de apartado`) que se ha pagado el abono inicial. Flujos en `workflows/`; puesta en marcha y resultados, en el README.

## Requirements

### Requirement: Solicitud incompleta no se guarda
El flujo SHALL NOT guardar una solicitud si falta nombre, modelo o talla, o si el teléfono o el correo no son válidos; SHALL avisar a Marisa.

#### Scenario: Solicitud incompleta
- **WHEN** falta el producto o el cliente, o el teléfono o el correo no son válidos
- **THEN** no se guarda nada y se avisa a Marisa

### Requirement: Solicitud duplicada no se guarda
El flujo SHALL NOT guardar una solicitud repetida (misma persona, modelo, talla y día); SHALL avisar a Marisa.

#### Scenario: Solicitud repetida
- **WHEN** se recibe dos veces la misma solicitud en el mismo día
- **THEN** no se guarda de nuevo y se avisa a Marisa

### Requirement: Solicitud pendiente hasta el abono inicial
El flujo SHALL guardar cada solicitud válida como pendiente sin crear nada en la app, y SHALL crear el apartado solo cuando la tienda confirme el pago del abono inicial con el precio, el abono y la forma de pago.

#### Scenario: Solicitud recibida
- **WHEN** un cliente envía una solicitud completa
- **THEN** queda guardada como pendiente con un número de solicitud
- **AND** no se crea ningún apartado en la app y se avisa a Marisa

#### Scenario: Confirmación con abono por debajo del mínimo
- **WHEN** la tienda confirma una solicitud con un abono inicial de 3 €
- **THEN** no se crea el apartado y Marisa recibe el motivo
