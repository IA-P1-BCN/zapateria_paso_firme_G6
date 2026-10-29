## Decisiones
1. **Concepto: cuero, costuras y etiquetas.** Fondo de papel kraft claro, superficies color crema, primario cuero, acento verde botella (escaparate) y burdeos para avisos. Las tarjetas llevan un borde discontinuo interior que recuerda a una costura y las etiquetas de estado tienen forma de etiqueta de precio.
2. **Tipografía:** títulos en *Fraunces* (serif cálida, de rótulo de tienda) y texto en *Nunito Sans* (la que ya usa la web, muy legible). Ambas de Google Fonts, que la hoja ya importa.
3. **Solo variables y estilos:** en la web se cambian las variables de `:root` y unos pocos estilos de decoración. Ningún selector nuevo depende de cambiar el HTML.
4. **Accesibilidad:** contraste de texto de al menos 4,5:1 (WCAG AA) en modo claro y oscuro; el modo oscuro se mantiene (cuero oscuro en vez de negro azulado).
5. **Una sola paleta para todo:** los mismos colores (en hexadecimal) en la web, el panel y los formularios (opción *Custom Form Styling* del Form Trigger, que n8n limpia de etiquetas HTML antes de insertarla). Los formularios no tienen modo oscuro en n8n, así que van siempre en claro.
6. **Correos fuera:** todos se envían como texto plano desde `SUB - Enviar notificación` (de Charlotte); darles diseño exigiría cambiar ese sub-workflow. La paleta queda documentada en el README.
7. **El panel solo cambia su `<style>`:** el nodo `Construir panel` calcula y pinta lo mismo; además el gris `#888` en línea (contraste 3,5:1 sobre crema) pasa a `#6a5444`.
