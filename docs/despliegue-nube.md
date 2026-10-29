# Cómo pusimos la tienda en la nube (T-022), explicado para novatos

Este documento cuenta **qué se hizo, en qué orden y por qué** para publicar la tienda en Internet, y qué quedó preparado para n8n. Está pensado para alguien que nunca ha desplegado nada. Los pasos cortos para repetirlo están en el [README](../README.md#despliegue-en-la-nube-t-022); la referencia de variables y credenciales, en [despliegue.md](despliegue.md).

**Resultado:** la tienda funciona en https://paso-firme-tienda.onrender.com (la API en `/docs`). n8n sigue en el ordenador de cada persona; su paso a la nube está preparado pero pendiente.

---

## 1. Las ideas básicas

| Palabra | Qué significa aquí |
|---|---|
| **Local** | Lo que corre en tu ordenador (`http://localhost:8000`). Solo lo ves tú. |
| **La nube** | Un ordenador de una empresa (Render) que está conectado a Internet y ejecuta nuestra app. Cualquiera con el enlace puede abrirla. |
| **Desplegar** | Copiar la app a ese ordenador y arrancarla allí. |
| **Docker / `Dockerfile`** | El `Dockerfile` es la receta para montar la app (qué Python usar, qué instalar, cómo arrancarla). Con la misma receta la app funciona igual en tu ordenador y en la nube. |
| **Variables de entorno** | Ajustes que se le dan a la app al arrancar sin escribirlos en el código (por ejemplo `API_KEY`). En local están en `.env`; en la nube, en el panel de Render. |
| **Secreto** | Una variable que no puede ver nadie más (claves, contraseñas). Nunca va en el repositorio. |
| **HTTPS** | La versión cifrada de HTTP (el candado del navegador). Render lo pone solo. |
| **Plan gratuito que se duerme** | Render apaga la app si nadie la usa en 15 minutos y la vuelve a encender cuando llega una visita. Por eso la primera carga tarda. |

## 2. Qué opciones miramos y por qué elegimos Render

No teníamos crédito de pago, así que solo valían planes gratuitos. Se miraron tres:

| Servicio | Qué es | ¿Sirve? |
|---|---|---|
| **Render** | Ejecuta contenedores Docker y les da una URL con HTTPS | **Sí, para la tienda.** Usa nuestro `Dockerfile` tal cual. |
| **Vercel** | Ejecuta "funciones": cada petición arranca un trocito de código que se apaga al terminar | **No.** Solo deja escribir en una carpeta temporal: un apartado creado en una petición no existiría en la siguiente. Y n8n necesita estar encendido todo el rato. |
| **Neon** | Base de datos Postgres que se apaga sola cuando no se usa | **Para n8n, sí** (pendiente de decidir). La tienda no puede usarla porque está hecha con SQLite y la app no se modifica. |

**Por qué no "siempre encendido":** un servicio despierto 24 horas gasta todas las horas gratuitas del mes y el proyecto se cae. Por eso no se usa nada que lo mantenga despierto (ni pings a la URL, ni monitores externos, ni tareas programadas). A cambio, la primera visita tras un rato espera unos segundos.

## 3. Lo que se hizo, paso a paso

### Paso 1. Mirar qué necesita la app (sin tocarla)
Antes de desplegar hay que saber cómo arranca la app. Leyendo el `Dockerfile` y `backend/config.py` se vio que:
- arranca con `uvicorn` en el **puerto 8000**;
- lee estas variables: `API_KEY`, `N8N_WEBHOOK_URL`, `WEBHOOK_TOKEN`, `SEED` y `DB_PATH`;
- guarda los datos en un fichero **SQLite** (`tienda.db`);
- si `SEED=1` y la base está vacía, carga **datos de ejemplo**.

Regla del proyecto: `backend/` y `frontend/` **no se tocan**. Todo el despliegue se hace por fuera.

### Paso 2. Describir el despliegue en un fichero (`render.yaml`)
En vez de apuntar los ajustes en un papel, se escribieron en [`render.yaml`](../render.yaml) (Render lo llama *Blueprint*). Así cualquiera puede ver cómo está montado y repetirlo. Dice:
- un servicio web `paso-firme-tienda`, con Docker, plan **free**, región **Frankfurt** (la más cercana) y rama `dev`;
- la ruta `/` como *health check* (Render la abre para saber si la app está viva);
- las variables: `PORT=8000`, `TZ`, `SEED=1` y `API_KEY` marcada como `sync: false`, que significa "**secreto: se rellena a mano en el panel, no aquí**".

El bloque de n8n está en el mismo fichero pero **comentado** (líneas con `#`), para quien lo continúe.

### Paso 3. Crear el servicio en Render
1. Alta en [render.com](https://render.com) con la cuenta de GitHub.
2. **New + → Web Service**. Como el repo es público, se puede usar **Public Git Repository** y pegar su URL, sin pedir permisos a la organización.
3. Rellenar lo mismo que dice `render.yaml`: Docker, rama `dev`, Frankfurt, `./Dockerfile`, plan **Free**, *Health Check Path* `/`.
4. Variables de entorno: `API_KEY` (una **nueva**, inventada solo para la demo; ver la sección 14 de la [guía del equipo](guia-del-equipo.md)), `SEED=1`, `TZ=Europe/Madrid`, `PORT=8000`. `N8N_WEBHOOK_URL` se deja sin poner: sin ella la tienda funciona y no intenta avisar a n8n.
5. **Deploy Web Service**.

### Paso 4. Qué hace Render al desplegar
1. Descarga el repositorio de GitHub (rama `dev`).
2. Sigue el `Dockerfile`: instala Python y las dependencias y copia `backend/` y `frontend/`.
3. Arranca la app con las variables del panel.
4. Abre `/` (*health check*). Si contesta, marca el servicio como **Live** y le da la URL `https://paso-firme-tienda.onrender.com`.

Si algo falla, la pestaña **Logs** del servicio muestra el error.

### Paso 5. Comprobar que funciona
No basta con "la página carga". Se comprobó cada requisito con `curl` (un programa que hace peticiones desde la terminal):

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://paso-firme-tienda.onrender.com/          # 200: la tienda carga
curl -s -o /dev/null -w '%{http_code} %{redirect_url}\n' http://paso-firme-tienda.onrender.com/   # 301 → https: HTTP redirige a HTTPS
curl -s https://paso-firme-tienda.onrender.com/api/apartados                              # 401: sin clave no entra
```

| Prueba | Resultado | Qué demuestra |
|---|---|---|
| `https://…/` | 200, en 22 s | Funciona. Tardó porque estaba dormida (lo normal la primera vez) |
| `http://…/` | 301 hacia `https://` | Requisito de la spec: por HTTP se redirige |
| `/docs` | 200 | La documentación de la API está publicada |
| `/api/apartados` sin clave | 401 | La API está protegida |
| `/api/apartados` con clave | 24 apartados | Se cargaron los datos de ejemplo |

### Paso 6. Validar los flujos en cada PR (CI)
**CI** (integración continua) es una comprobación automática que GitHub ejecuta en cada PR. Se añadió la acción [`Validar flujos`](../.github/workflows/validar-flujos.yml), que ejecuta [`validar_flujos.py`](../.github/scripts/validar_flujos.py) sobre `workflows/`:
- **Falla** (la PR sale en rojo) si un JSON está roto o lleva algo que parece una clave: de Groq, un token de Telegram, una contraseña escrita en un nodo, una credencial con datos o una URL con usuario y contraseña.
- **Avisa** (sin fallar) si un flujo se exportó publicado o no tiene `08 - Error Workflow`.
- No llama a la tienda ni a n8n: no despierta nada ni gasta horas.

Se ve en la PR, en la pestaña **Checks**. En local: `python .github/scripts/validar_flujos.py workflows`.

## 4. Lo que hay que saber de la tienda en la nube

- **Tarda en despertar:** tras 15 minutos sin visitas se duerme y la siguiente tarda unos 30-60 s. No está rota: espera y recarga.
- **Es una demo:** Render gratis no tiene disco permanente. Al dormirse o reiniciarse, el fichero SQLite se pierde y la app vuelve a cargar los datos de ejemplo. Lo que se cree en la demo no se guarda.
- **La clave se ve desde el navegador:** la app le pasa la `API_KEY` a la web (`/config.js`). Por eso es una clave solo para la demo y los datos son ficticios.
- **Cada cambio en `dev` se vuelve a desplegar** (si el servicio está conectado a la rama). Con *Public Git Repository* se puede lanzar a mano con **Manual Deploy**.

## 5. Lo que quedó preparado para n8n (pendiente)

La tienda sola funciona, pero las automatizaciones siguen en el n8n de cada persona. Para llevar n8n a la nube se preparó esto:

**Por qué n8n necesita Neon.** n8n guarda flujos, credenciales y ejecuciones en una base de datos. Si estuviera en el disco de Render, se borraría cada vez que se duerme. Neon es una base Postgres aparte que se apaga sola cuando no se usa, así que no gasta y los datos no se pierden.

**Qué se hizo:**
1. Se creó un proyecto de Neon `paso-firme-n8n` (Frankfurt, Postgres 17, base y usuario `n8n`) en la cuenta de Anna. Quien lo continúe puede pedirle acceso o crear uno propio igual.
2. Se probó **en local** que n8n 2.44.4 arranca contra Neon: se lanzó un contenedor de prueba con las variables `DB_TYPE=postgresdb`, `DB_POSTGRESDB_HOST`, `_DATABASE`, `_USER`, `_PASSWORD` y `DB_POSTGRESDB_SSL_ENABLED=true`, se comprobó que creaba sus tablas y respondía en `/healthz`, y se borró.
3. Se escribió el bloque `paso-firme-n8n` de `render.yaml` (comentado) con todas sus variables.

**Dos detalles importantes:**
- Hay que usar la conexión **directa** de Neon (el *host* sin `-pooler`). La que va con *pooler* puede fallar porque n8n hace migraciones (crea y cambia tablas) al arrancar.
- `N8N_ENCRYPTION_KEY` cifra las credenciales. Render la genera; hay que **guardarla** en un gestor de contraseñas, porque sin ella una copia de la base no sirve.

**Cómo continuar:** descomentar el bloque de n8n (y `N8N_WEBHOOK_URL` y `WEBHOOK_TOKEN` en la tienda) y seguir la parte "n8n en la nube (pendiente)" del README. Al terminar, marcar las tareas 2.1-2.3 del change `t-022-despliegue-cloud` y archivarlo.

**Lo que pasará cuando n8n esté en la nube:**
- El primer aviso de la tienda tras un rato **se perderá**: la tienda espera 5 s y n8n tarda 1-2 min en despertar. Antes de una demo, abre n8n primero.
- Los flujos programados (`05`, `06`, `07`, `Entrada CSV del datáfono`) y el de correo (`03`) se dejan **sin publicar**, salvo que Marisa lo pida.

## 6. Problemas que encontramos

- **Docker Desktop cerrado:** la prueba local de n8n contra Neon falló con `failed to connect to the docker API`. Solución: abrir Docker Desktop y esperar a que arranque.
- **Antivirus que intercepta HTTPS:** en un ordenador con Kaspersky, las conexiones cifradas desde los contenedores fallaban. En local se resolvió dándole a n8n el certificado del antivirus (`NODE_EXTRA_CA_CERTS`, en un `docker-compose.override.yml` que no se sube). En Render no pasa.
- **Un dato mal apuntado:** primero se escribió que Neon gratis da 0,5 GB; el proyecto creado tiene 1 GB y se corrigió.
- **La primera carga tardó 22 s:** no era un error, el servicio estaba dormido.

## 7. Reglas que seguimos (y por qué)

| Regla | Por qué |
|---|---|
| Secretos solo en el panel de Render, nunca en el repo | El repositorio es público |
| Nada que mantenga los servicios despiertos | Los planes gratuitos se agotan y el proyecto se cae |
| No tocar `backend/` ni `frontend/` | La app es la de la tienda; nosotros solo automatizamos alrededor |
| Comprobar cada requisito con una prueba | "Me carga la página" no demuestra que HTTP redirige o que la API está protegida |
| Dejar escrito lo pendiente | Para que otra persona pueda continuar sin preguntar |
