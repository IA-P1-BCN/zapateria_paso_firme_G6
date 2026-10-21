# T-022 · Despliegue en la nube

**Historia:** HU-16 · **Responsable:** sin asignar · **Tamaño:** L · **Fecha límite:** sin fecha (extra: si hay tiempo)
**Depende de:** T-001, T-020

## Por qué
Hoy n8n corre en el ordenador de cada persona. Para que Marisa use los flujos hace falta un servidor siempre encendido.

## Qué cambia
- n8n y la app desplegados en la nube con HTTPS.
- Copias de seguridad.
- Validación automática de los JSON de los workflows en CI.

## Fuera de alcance
- Alta disponibilidad.

## Impacto
Infraestructura nueva; las credenciales se recrean allí con los mismos nombres. Extra (nivel Avanzado/Experto): se construye solo si el nivel Esencial y Medio están cerrados y queda tiempo.
