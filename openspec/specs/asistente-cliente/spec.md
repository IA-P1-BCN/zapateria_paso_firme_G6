# asistente-cliente Specification

## Purpose
Asistente de Telegram para clientes: permite consultar el saldo y la fecha límite de sus apartados tras identificarse con su teléfono y número de apartado. Solo lectura.

## Requirements

### Requirement: Solo los datos del propio cliente
El asistente SHALL responder únicamente con los apartados de la persona identificada.

#### Scenario: Cliente identificado
- **WHEN** una clienta identificada pregunta cuánto le falta
- **THEN** recibe el pendiente de la app de sus apartados

#### Scenario: Cliente no identificado
- **WHEN** alguien no verificado pregunta por un apartado
- **THEN** no se da ningún dato y se le ofrece contactar con la tienda

### Requirement: Identificación con teléfono propio y número de apartado
El asistente SHALL identificar a la persona con el contacto que comparte desde Telegram y con el número de un apartado registrado con ese mismo teléfono.

#### Scenario: Contacto ajeno
- **WHEN** alguien envía un contacto cuyo `user_id` no es el suyo
- **THEN** se rechaza y se le pide compartir su propio número

#### Scenario: Apartado de otra persona
- **WHEN** la persona escribe el número de un apartado que no es de su teléfono
- **THEN** no se activa la sesión y no se muestra ningún dato

#### Scenario: Número dentro de una frase
- **WHEN** la persona escribe "es el 27" y el 27 es un apartado de su teléfono
- **THEN** se verifica y se activa la sesión

### Requirement: Sesión de 10 minutos
La sesión SHALL caducar tras 10 minutos de inactividad y poder cerrarse con `/salir`.

#### Scenario: Sesión caducada
- **WHEN** pasan más de 10 minutos sin mensajes y la persona escribe de nuevo
- **THEN** se le vuelve a pedir compartir su número

#### Scenario: Salir
- **WHEN** la persona escribe `/salir`
- **THEN** se borra su sesión y se confirma el cierre

### Requirement: Solo chats privados
El asistente SHALL ignorar los mensajes que no vengan de un chat privado.

#### Scenario: Mensaje en un grupo
- **WHEN** el bot recibe un mensaje de un grupo
- **THEN** no responde ni consulta datos

### Requirement: Cifras de la app, no del modelo
Los importes y fechas de la respuesta SHALL proceder de la API de la tienda.

#### Scenario: Respuesta con saldo
- **WHEN** el asistente responde con un importe
- **THEN** coincide con el `pendiente` de la app

#### Scenario: Sin cálculos del modelo
- **WHEN** el modelo redacta la respuesta
- **THEN** copia `pendiente`, `fecha_limite` e `id` tal como los devuelve la API y no suma, resta ni redondea

### Requirement: El modelo no decide dinero
El asistente SHALL NOT conceder descuentos, reembolsos, cancelaciones ni excepciones.

#### Scenario: Petición de dinero
- **WHEN** la clienta pide un descuento, un reembolso o cancelar un apartado
- **THEN** se le indica que lo gestiona la tienda

### Requirement: Apartados según su estado
El asistente SHALL hablar por defecto solo de los apartados `activo` y mostrar `liquidado` o `vencido` solo si se le pregunta, sin presentarlos como deuda.

#### Scenario: Sin apartados activos
- **WHEN** la clienta no tiene ningún apartado `activo` y no pregunta por otros estados
- **THEN** recibe el aviso de que no tiene apartados activos y se le remite a la tienda por si es un error

#### Scenario: Pregunta por otros apartados con uno solo
- **WHEN** la clienta pregunta si tiene otros apartados y solo tiene uno activo
- **THEN** se le dice que solo tiene ese y se le repite con su número

### Requirement: Fallo del modelo
Si el modelo de IA no responde, el asistente SHALL avisar con un mensaje fijo y remitir a la tienda.

#### Scenario: Modelo caído
- **WHEN** la llamada al modelo falla
- **THEN** la clienta recibe "Ahora mismo no puedo responder. Contacta con la tienda y te ayudarán."
