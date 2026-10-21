## ADDED Requirements

### Requirement: Solo los datos del propio cliente
El asistente SHALL responder únicamente con los apartados de la persona identificada.

#### Scenario: Cliente identificado
- **WHEN** una clienta identificada pregunta cuánto le falta
- **THEN** recibe el pendiente de la app de sus apartados

#### Scenario: Cliente no identificado
- **WHEN** alguien no verificado pregunta por un apartado
- **THEN** no se da ningún dato y se le ofrece contactar con la tienda

### Requirement: Cifras de la app, no del modelo
Los importes y fechas de la respuesta SHALL proceder de la API de la tienda.

#### Scenario: Respuesta con saldo
- **WHEN** el asistente responde con un importe
- **THEN** coincide con el `pendiente` de la app
