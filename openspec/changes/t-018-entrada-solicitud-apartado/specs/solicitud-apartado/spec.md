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
