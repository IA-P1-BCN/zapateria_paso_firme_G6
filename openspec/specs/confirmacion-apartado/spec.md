# confirmacion-apartado Specification

## Purpose
TBD - created by archiving change t-004-flujo-01-confirmacion-apartado. Update Purpose after archive.

## Requirements

### Requirement: Confirmación al crear un apartado
El flujo SHALL enviar al cliente un mensaje con modelo, talla, precio, abonado, pendiente y fecha límite cuando llega `apartado.creado`.

#### Scenario: Apartado normal
- **WHEN** llega `apartado.creado` con `estado` = `activo` y `email`
- **THEN** se envía un mensaje con modelo, talla, precio, abonado, pendiente y fecha límite con los importes recibidos
- **AND** el mensaje se envía en menos de un minuto

### Requirement: Apartado liquidado desde el alta
El flujo SHALL enviar un mensaje distinto, que avisa de que ya puede recoger sus zapatos, si `datos.estado` es `liquidado`.

#### Scenario: Abono inicial igual al precio
- **WHEN** llega `apartado.creado` con `estado` = `liquidado` y `pendiente` = 0
- **THEN** el mensaje no menciona importe pendiente y dice que puede recoger sus zapatos

### Requirement: Cliente sin correo
El flujo SHALL NOT fallar si el cliente no tiene `email`; SHALL avisar a la tienda a través del sub-workflow de notificaciones.

#### Scenario: Sin email
- **WHEN** llega `apartado.creado` sin `email`
- **THEN** la tienda recibe un aviso con el número y el cliente del apartado
- **AND** la ejecución termina sin error

### Requirement: Importes sin recalcular
El flujo SHALL usar los importes de `datos` sin volver a calcularlos.

#### Scenario: Datos de la app
- **WHEN** `datos.pendiente` = 79.90
- **THEN** el mensaje muestra `79,90 €`
