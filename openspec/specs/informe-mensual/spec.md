# informe-mensual Specification

## Purpose
Informe mensual a Marisa con recaudacion, pendiente de cobro y apartados nuevos, liquidados y vencidos.

## Requirements

### Requirement: Informe del mes anterior
El flujo SHALL enviar a Marisa el día 1 de cada mes un informe del mes anterior con lo recaudado en ventas, lo recaudado en abonos y el total.

#### Scenario: Mes con actividad
- **WHEN** es día 1 y hubo movimientos el mes anterior
- **THEN** Marisa recibe ventas, abonos y total del mes anterior, coincidiendo con la suma de la app

#### Scenario: Primer día de enero
- **WHEN** es el 1 de enero
- **THEN** el informe cubre diciembre del año anterior

### Requirement: Pendiente total
El informe SHALL incluir el pendiente total de los apartados activos, calculado sumando el `pendiente` de cada uno.

#### Scenario: Varios activos
- **WHEN** hay 3 apartados activos con pendientes 10, 20 y 30
- **THEN** el informe indica `60,00 €` pendientes

### Requirement: Apartados del mes
El informe SHALL indicar cuántos apartados se crearon, se liquidaron y vencieron en el mes anterior.

#### Scenario: Cuentas del mes
- **WHEN** se crearon 5, se liquidaron 3 y venció 1 en el mes
- **THEN** el informe indica 5, 3 y 1

### Requirement: Mes sin actividad
El flujo SHALL NOT fallar si el mes no tuvo movimientos.

#### Scenario: Mes vacío
- **WHEN** no hay ventas ni abonos
- **THEN** el informe muestra ceros y la ejecución termina sin error
