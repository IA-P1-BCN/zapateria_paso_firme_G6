# T-001 · Base del webhook y credenciales

**Historia:** transversal (sin HU) · **Responsable:** Charlotte (`Charlottedoulcet`) · **Tamaño:** M · **Fecha límite:** 2026-10-22

## Por qué
La app de la tienda avisa a n8n con un único webhook (`/webhook/tienda`) y 4 eventos. Los flujos 1, 2 y 4 (y los que vengan después) necesitan un punto de entrada común y las mismas credenciales en las tres instancias de n8n. Sin esta base, cada persona montaría su propia entrada y nos pisaríamos.

## Qué cambia
- Un workflow `00 - Entrada tienda` con el Webhook y un Switch por `evento`.
- Cada rama del Switch llama a su flujo como sub-workflow (hasta que exista, un nodo vacío).
- Credenciales con nombre fijo, iguales en las tres instancias.
- Lista de credenciales y variables en el README (sin valores).

## Fuera de alcance
- Autenticar el webhook (HU-14, nivel Avanzado).
- La lógica de cada flujo.

## Impacto
Desbloquea T-002, T-004, T-005 y T-010. No toca `backend/` ni `frontend/`.
