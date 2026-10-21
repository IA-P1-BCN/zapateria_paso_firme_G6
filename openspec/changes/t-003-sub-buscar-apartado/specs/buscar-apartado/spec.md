## ADDED Requirements

### Requirement: Búsqueda por identificador
El sub-workflow SHALL buscar por `id` con `GET /api/apartados/{id}` cuando se le da un identificador, admitiendo el prefijo `#`.

#### Scenario: Id que existe
- **WHEN** se llama con `id` = `12`
- **THEN** devuelve `resultado` = `unico` con ese apartado

#### Scenario: Id que no existe
- **WHEN** se llama con un `id` sin apartado (404 de la app)
- **THEN** devuelve `resultado` = `ninguno` sin lanzar error

### Requirement: Búsqueda por texto tolerante
El sub-workflow SHALL normalizar el texto y coincidir por trozos del nombre sin distinguir mayúsculas ni acentos.

#### Scenario: Nombre abreviado
- **WHEN** el texto es `JORGE M.` y existe un apartado activo de `Jorge Martín`
- **THEN** devuelve ese apartado como candidato `unico`

#### Scenario: Sin acentos
- **WHEN** el texto es `LUCIA GOMEZ` y el cliente se guarda como `Lucía Gómez`
- **THEN** hay coincidencia

#### Scenario: Varios con el mismo nombre
- **WHEN** dos apartados activos de la misma persona o de personas con el mismo nombre coinciden por igual
- **THEN** devuelve `resultado` = `varios` con todos los empatados

#### Scenario: Sin coincidencias
- **WHEN** ningún apartado activo coincide
- **THEN** devuelve `resultado` = `ninguno` y `candidatos` vacío

### Requirement: Solo apartados que pueden recibir abonos
El sub-workflow SHALL buscar por defecto solo entre apartados `activo`.

#### Scenario: Apartado ya liquidado
- **WHEN** el único apartado de esa persona está `liquidado`
- **THEN** devuelve `ninguno`
