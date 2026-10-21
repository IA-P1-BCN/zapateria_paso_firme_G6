## ADDED Requirements

### Requirement: Servicio accesible con HTTPS
El despliegue SHALL exponer n8n y la tienda solo por HTTPS.

#### Scenario: Acceso por HTTP
- **WHEN** se accede por HTTP
- **THEN** se redirige o se rechaza

### Requirement: Copias de seguridad
El despliegue SHALL hacer copias periódicas de los datos de n8n y de la app.

#### Scenario: Restauración
- **WHEN** se restaura la última copia
- **THEN** los flujos y los datos vuelven a estar disponibles

### Requirement: Validación en CI
El repositorio SHALL validar en cada PR que los JSON de `workflows/` son válidos y sin claves.

#### Scenario: JSON con clave
- **WHEN** una PR añade un JSON con un token
- **THEN** la validación falla
