## ADDED Requirements

### Requirement: Solo Marisa
El asistente SHALL responder únicamente al chat privado autorizado de Marisa, cuyo identificador está en la variable `TELEGRAM_CHAT_ID_MARISA`.

#### Scenario: Chat desconocido
- **WHEN** escribe un chat que no es el de Marisa
- **THEN** recibe un rechazo fijo y no se consulta ni la API ni el modelo

#### Scenario: Mensaje en un grupo
- **WHEN** el bot recibe un mensaje de un grupo, aunque venga de Marisa
- **THEN** no responde ni consulta datos

### Requirement: Respuestas con datos de la API
Las cifras y fechas de la respuesta SHALL proceder de consultas a la API de la tienda mediante las herramientas del agente.

#### Scenario: Recaudado de la semana
- **WHEN** Marisa pregunta "¿cuánto se recaudó esta semana?"
- **THEN** recibe el total de abonos y ventas de lunes a hoy, desglosado por efectivo, tarjeta y bizum, tal como lo suma la herramienta

#### Scenario: Apartados que vencen este mes
- **WHEN** Marisa pregunta "¿qué apartados vencen este mes?"
- **THEN** recibe la lista de apartados `activo` cuya `fecha_limite` cae en el mes, con `id`, cliente, `pendiente` y `fecha_limite` tal como los devuelve la app

#### Scenario: Consulta de un apartado
- **WHEN** Marisa pregunta por un apartado por cliente, id o teléfono
- **THEN** recibe los datos que devuelve la app

### Requirement: El modelo no calcula fechas ni dinero
El modelo SHALL elegir solo el `periodo` de la herramienta y copiar los resultados sin sumar, restar ni redondear.

#### Scenario: Periodo relativo
- **WHEN** Marisa dice "esta semana" o "este mes"
- **THEN** el modelo pasa `esta_semana` o `este_mes` y el rango de fechas lo calcula un nodo determinista

### Requirement: Preguntas de seguimiento
El asistente SHALL usar los últimos mensajes solo para entender la pregunta, y SHALL volver a consultar la herramienta para cada cifra, fecha o apartado.

#### Scenario: Seguimiento de un periodo
- **WHEN** Marisa pregunta "¿cuánto se recaudó este mes?" y después "¿y la semana pasada?"
- **THEN** el asistente llama otra vez a la herramienta con `semana_pasada` y responde con sus datos, sin reutilizar cifras de la respuesta anterior

### Requirement: Solo lectura
El asistente SHALL NOT registrar abonos, vencer apartados, crear ventas ni modificar ningún dato.

#### Scenario: Petición de escritura
- **WHEN** Marisa pide "cancela el apartado 12" o "registra un abono"
- **THEN** se le indica que eso se hace desde la app y no se llama a ninguna ruta de escritura

### Requirement: Fallo del modelo
Si el modelo de IA no responde, el asistente SHALL avisar con un mensaje fijo sin cifras.

#### Scenario: Modelo caído
- **WHEN** la llamada al modelo falla
- **THEN** Marisa recibe "Ahora mismo no puedo responder. Inténtalo de nuevo en unos minutos."
