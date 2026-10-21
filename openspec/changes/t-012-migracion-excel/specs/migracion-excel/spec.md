## ADDED Requirements

### Requirement: Normalizar los datos del Excel
La migración SHALL convertir fechas, importes y nombres a los formatos de la app antes de cargar.

#### Scenario: Formatos distintos
- **WHEN** una fila tiene fecha `7/9/26`, importe `15€` y cliente `carmen ruiz`
- **THEN** se carga con fecha `2026-09-07`, importe 15 y cliente `Carmen Ruiz`

#### Scenario: Sin teléfono
- **WHEN** una cliente no tiene teléfono
- **THEN** se carga igualmente

### Requirement: Agrupar filas en apartados y abonos
La migración SHALL agrupar las filas por cliente, modelo y talla, y crear el apartado con la primera fila y un abono por cada fila siguiente.

#### Scenario: Cuatro filas del mismo apartado
- **WHEN** hay 4 filas de la misma persona, modelo y talla
- **THEN** se crea 1 apartado y 3 abonos en orden de fecha

### Requirement: Respetar las reglas de la app
La migración SHALL NOT cargar los casos que la app rechazaría, y SHALL incluirlos en el informe en lugar de forzarlos.

#### Scenario: Abono inicial menor de 5 €
- **WHEN** el abono inicial es de 4 €
- **THEN** no se carga el apartado ni sus abonos
- **AND** aparece en el informe con el motivo

### Requirement: No duplicar ventas y abonos
La migración SHALL NOT cargar como venta las filas de ventas que corresponden a abonos de apartados.

#### Scenario: Abono inicial en la hoja de ventas
- **WHEN** una venta se llama `abono inicial apartado`
- **THEN** no se carga como venta
- **AND** se usa para deducir la forma de pago del abono

### Requirement: Ignorar totales a mano
La migración SHALL ignorar la fila `TOTAL SEPTIEMBRE (a mano)`.

#### Scenario: Fila de total
- **WHEN** se lee esa fila
- **THEN** no se carga

### Requirement: Ejecución repetible
Ejecutar la migración dos veces SHALL NOT duplicar registros.

#### Scenario: Segunda ejecución
- **WHEN** se vuelve a ejecutar con los mismos archivos
- **THEN** no se crean apartados, abonos ni ventas nuevos

### Requirement: Informe de lo no cargado
La migración SHALL enviar a Marisa un informe con lo que no se cargó, el motivo y las suposiciones hechas.

#### Scenario: Informe final
- **WHEN** termina la migración
- **THEN** Marisa recibe las filas dudosas y las formas de pago supuestas
