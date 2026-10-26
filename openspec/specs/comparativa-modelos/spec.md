# comparativa-modelos Specification

## Purpose
Comparativa de dos modelos gratuitos de IA en la extracción de datos de los avisos del banco del flujo 03 (T-008): mismo prompt y mismos correos para los dos, con acierto por campo, validez del JSON, tiempo de respuesta y datos enviados. Flujo: `workflows/Comparativa de modelos.json`; resultados y modelo elegido, en el README.

## Requirements

### Requirement: Misma prueba para ambos modelos
La comparativa SHALL ejecutar el mismo prompt sobre los mismos 9 correos con dos modelos gratuitos distintos.

#### Scenario: Ejecución comparable
- **WHEN** se ejecuta la comparativa
- **THEN** hay 9 resultados por modelo con la misma entrada

### Requirement: Métricas registradas
La comparativa SHALL registrar, por modelo, el acierto de cada campo, la validez del JSON y el tiempo de respuesta.

#### Scenario: Tabla de resultados
- **WHEN** termina la comparativa
- **THEN** el README contiene una tabla con esas tres métricas por modelo

### Requirement: Datos enviados documentados
La comparativa SHALL documentar qué datos se enviaron a cada modelo.

#### Scenario: Privacidad
- **WHEN** se revisa la documentación
- **THEN** indica el texto exacto enviado y que son datos ficticios

### Requirement: Conclusión
La comparativa SHALL terminar con un modelo recomendado y su motivo.

#### Scenario: Modelo elegido
- **WHEN** se cierra el ticket
- **THEN** el README nombra el modelo elegido y por qué
