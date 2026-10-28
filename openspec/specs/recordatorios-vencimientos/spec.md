# recordatorios-vencimientos Specification

## Purpose
Recordatorios a clientes (7 y 1 dia) y vencimiento por API de apartados fuera de plazo con generacion de vale.

## Requirements

### Requirement: Recordatorio antes del plazo
El flujo SHALL enviar al cliente un recordatorio con el pendiente y la fecha límite cuando `fecha_limite` sea dentro de 7 días y cuando sea dentro de 1 día.

#### Scenario: A 7 días
- **WHEN** el flujo se ejecuta y un apartado activo tiene `fecha_limite` = hoy + 7
- **THEN** el cliente recibe un recordatorio con el pendiente y la fecha límite

#### Scenario: A 1 día
- **WHEN** un apartado activo tiene `fecha_limite` = mañana
- **THEN** el cliente recibe un segundo recordatorio

#### Scenario: Otros días
- **WHEN** `fecha_limite` es dentro de 4 días
- **THEN** no se envía nada

### Requirement: Sin avisos repetidos
El flujo SHALL NOT enviar dos veces el mismo tipo de recordatorio para el mismo apartado.

#### Scenario: Ejecución repetida
- **WHEN** el flujo se ejecuta dos veces el mismo día
- **THEN** el cliente recibe un solo recordatorio por tipo

### Requirement: Vencer los apartados pasados de plazo
El flujo SHALL llamar a `POST /api/apartados/{id}/vencer` para cada apartado activo con `fecha_limite` anterior a hoy.

#### Scenario: Plazo pasado
- **WHEN** un apartado activo tiene `fecha_limite` = ayer
- **THEN** se llama a `vencer` y el apartado pasa a `vencido`
- **AND** se genera un vale

#### Scenario: Apartado ya cerrado
- **WHEN** la app responde 422 al vencer
- **THEN** el flujo continúa con el siguiente apartado sin error

### Requirement: Aviso con el vale
El flujo SHALL avisar al cliente del vencimiento indicando el código y el importe del vale de la respuesta de la app.

#### Scenario: Vencimiento notificado
- **WHEN** la app devuelve `vale` con código `VALE-00016` y 40 €
- **THEN** el cliente recibe un mensaje con `VALE-00016` y `40,00 €`

### Requirement: Lista de zapatos que vuelven a la venta
El flujo SHALL enviar a Marisa una lista con los apartados vencidos hoy, y SHALL NOT enviarla si no hubo ninguno.

#### Scenario: Con vencidos
- **WHEN** se vencieron 2 apartados hoy
- **THEN** Marisa recibe un mensaje con los 2 (cliente, producto, talla)

#### Scenario: Sin vencidos
- **WHEN** no se venció ningún apartado
- **THEN** no se envía el mensaje a Marisa
