## ADDED Requirements

### Requirement: Solo Marisa
El asistente SHALL responder únicamente al chat autorizado de Marisa.

#### Scenario: Chat desconocido
- **WHEN** escribe un chat que no es el de Marisa
- **THEN** recibe un rechazo y no se consulta la API

### Requirement: Consultas con datos de la app
Las respuestas SHALL salir de consultas a la API de la tienda.

#### Scenario: Consulta de un apartado
- **WHEN** Marisa pregunta por un apartado
- **THEN** recibe los datos que devuelve la app
