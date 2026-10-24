# recibo-abono Specification

## Purpose
TBD - created by archiving change t-005-flujo-02-recibo-abono. Update Purpose after archive.

## Requirements

### Requirement: Recibo de cada abono
El flujo SHALL enviar al cliente un recibo con el importe pagado y lo que queda pendiente cuando llega `abono.registrado`.

#### Scenario: Abono parcial
- **WHEN** llega `abono.registrado` con `importe` = 20, `pendiente` = 39.90 y `estado` = `activo`
- **THEN** el recibo muestra `20,00 €` pagados y `39,90 €` pendientes

### Requirement: Apartado liquidado
El flujo SHALL cambiar el mensaje para avisar de que ya puede recoger sus zapatos si `datos.estado` es `liquidado`.

#### Scenario: Último abono
- **WHEN** llega `abono.registrado` con `pendiente` = 0 y `estado` = `liquidado`
- **THEN** el mensaje dice que ya puede recoger sus zapatos

### Requirement: Cliente sin correo
El flujo SHALL NOT fallar si no hay `email`; SHALL avisar a la tienda.

#### Scenario: Sin email
- **WHEN** llega `abono.registrado` sin `email`
- **THEN** la tienda recibe un aviso y la ejecución termina sin error
