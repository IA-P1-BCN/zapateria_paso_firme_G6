## ADDED Requirements

### Requirement: Descartar lo que no es un pago
El flujo SHALL ignorar los correos que no contienen un importe y un ordenante.

#### Scenario: Publicidad del banco
- **WHEN** llega el correo `08_publicidad_banco`
- **THEN** no se llama al modelo ni a la API y la ejecución termina sin acción

### Requirement: Extracción de datos del pago
El flujo SHALL extraer `ordenante`, `importe` y `concepto` de los correos de Bizum y de transferencia, y SHALL validar en código que `importe` es un número positivo.

#### Scenario: Bizum
- **WHEN** llega el correo 01 con `Importe: 10,00 EUR`
- **THEN** se obtiene `importe` = 10, `ordenante` = `CARMEN RUIZ GARCIA` y `concepto` = `zuecos`

#### Scenario: Transferencia
- **WHEN** llega el correo 03 con `Importe .......... 12,00 EUR`
- **THEN** se obtiene `importe` = 12 y el ordenante y concepto del correo

#### Scenario: Importe ilegible
- **WHEN** el importe extraído no es un número positivo
- **THEN** el pago se trata como dudoso

### Requirement: Registro automático solo si está claro
El flujo SHALL registrar el abono mediante `POST /api/apartados/{id}/abonos` únicamente cuando haya un único apartado activo candidato, el importe no supere lo pendiente y el plazo esté vigente; la decisión SHALL tomarla un nodo de reglas, no el modelo de IA.

#### Scenario: Un único apartado claro
- **WHEN** el buscador devuelve `unico` y `importe` <= `pendiente`
- **THEN** se registra el abono
- **AND** la app emite `abono.registrado` y el cliente recibe su recibo (T-005)

### Requirement: Pagos dudosos: preguntar, no registrar
El flujo SHALL NOT registrar nada y SHALL preguntar a Marisa cuando haya varios apartados posibles, ninguno, falte el concepto o el cliente sea desconocido.

#### Scenario: Sin concepto
- **WHEN** llega el correo 05 (sin concepto)
- **THEN** no se registra nada y Marisa recibe el ordenante, el importe y los candidatos

#### Scenario: Cliente desconocido
- **WHEN** llega el correo 07 y ningún apartado coincide
- **THEN** no se registra nada y se avisa a Marisa

#### Scenario: Varios posibles
- **WHEN** el buscador devuelve `varios`
- **THEN** no se registra nada y Marisa recibe la lista de candidatos

### Requirement: Rechazos por regla de negocio
El flujo SHALL NOT registrar y SHALL avisar a Marisa con el motivo cuando el importe supere lo pendiente o el apartado esté fuera de plazo.

#### Scenario: Importe mayor que lo pendiente
- **WHEN** el pago es de 25 € y `pendiente` es 10 €
- **THEN** no se registra el abono
- **AND** el aviso a Marisa indica el motivo

#### Scenario: Error de la app
- **WHEN** la app responde 422 al registrar el abono
- **THEN** Marisa recibe el texto del error, sea `detail` un texto o una lista

### Requirement: Un correo se procesa una sola vez
El flujo SHALL NOT procesar dos veces el mismo correo.

#### Scenario: Reejecución
- **WHEN** el flujo se ejecuta otra vez con el mismo correo en el buzón
- **THEN** no se crea un segundo abono
