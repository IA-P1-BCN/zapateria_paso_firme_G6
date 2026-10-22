## Decisiones
1. **Se piden todos los apartados `activo` y se filtra en un nodo Code.** La app solo ofrece `q` por subcadena (y SQLite no ignora acentos), así que `gomez` no encuentra `Gómez`. Con decenas de apartados activos es barato y fiable. Alternativa descartada: llamar a `q` por cada trozo.
2. **Normalizar** = minúsculas, sin acentos, sin puntuación. Se parte el texto en trozos de 3 letras o más y se ignoran partículas (`de`, `del`, `la`).
3. **Puntuación:** el candidato que coincide con más trozos gana; se devuelven todos los que empatan en el máximo.
4. **Un número en el texto** (`#12`, `apartado 2`) se trata como pista de `id` solo si ese apartado también coincide con algún trozo del nombre; no se confía en él a ciegas.
5. **Salida:** `{resultado: 'unico'|'varios'|'ninguno', candidatos: [{id, cliente, producto, talla, precio, abonado, pendiente, fecha_limite, estado}]}`.
