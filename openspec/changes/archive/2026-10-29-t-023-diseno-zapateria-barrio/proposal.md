# T-023 · Diseño de zapatería de barrio

**Historia:** ninguna (mejora visual transversal) · **Responsable:** Anna · **Tamaño:** M · **Fecha límite:** jueves 29 de octubre
**Depende de:** T-018, T-021

## Por qué
Todo lo que ven Marisa y sus clientes tiene un aspecto genérico de aplicación (verde azulado, letra de sistema). Paso Firme es una zapatería de barrio: la web, el panel, los formularios y los correos deberían parecerlo y reconocerse como de la misma tienda.

## Qué cambia
- Una identidad visual común: papel kraft, cuero, verde botella y un toque burdeos; títulos con letra de rótulo (serif) y detalles de costura y de etiqueta de precio.
- La web de la tienda (`frontend/`): **solo la hoja de estilos** (`frontend/css/styles.css`). No se tocan el HTML ni el JavaScript, así que funciona exactamente igual.
- Lo nuestro en n8n: el panel de Marisa (T-021) y los formularios de solicitud y confirmación de apartado (T-018), con el texto del botón en castellano («Enviar solicitud», «Confirmar apartado») en vez del «Submit» que pone n8n.
- Una sección «Identidad visual» en el README con la paleta y las fuentes.

## Fuera de alcance
- Cambiar textos (salvo el botón de los formularios), campos o comportamiento de la web o de los flujos.
- Los correos: son texto plano y los envía `SUB - Enviar notificación` (de Charlotte), así que no tienen diseño propio. La paleta queda documentada en el README por si se quieren pasar a HTML.
- Logotipo o imágenes de marca nuevas.

## Impacto
Toca `frontend/css/styles.css`, que `AGENTS.md` pide no tocar («No tocar `backend/` ni `frontend/`») y que es de Alexandra Zambrano. Anna da permiso explícito para cambiar **solo el aspecto**; se avisa en la PR para que el equipo lo valide. Si el equipo no lo acepta, la parte de `frontend/` se quita sin afectar al resto.
