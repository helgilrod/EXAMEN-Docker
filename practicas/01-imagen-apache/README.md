# Práctica 1 · Crear una imagen de un contenedor Apache

> **Enunciado (Aules):** Crea una imatge amb un Dockerfile, basada en la imatge oficial `httpd`. Anomena-la `la-meua-web` amb el tag `v1`. Copia el index que vos adjunte dins la ruta de la imatge `/usr/local/apache2/htdocs/`. Comprova que funciona utilitzant `-p 4000:80`.
>
> Además, la subimos a Docker Hub (es lo que piden en el examen).

**Ficheros de esta carpeta:** [`Dockerfile`](Dockerfile) · [`index.html`](index.html) (uno de ejemplo; en la práctica se usa el que da el profesor).

Cambia `tuusuario` por tu usuario de Docker Hub.

## Resumen: la práctica entera en orden

```bash
mkdir -p ~/docker/ex01
cd ~/docker/ex01
cp ~/Descargas/index.html .
nano Dockerfile
docker build -t la-meua-web:v1 .
docker run -d --name la-meua-web -p 4000:80 la-meua-web:v1
docker ps
# Firefox: http://localhost:4000
docker tag la-meua-web:v1 tuusuario/la-meua-web:v1
docker login -u tuusuario
docker push tuusuario/la-meua-web:v1
```

## Paso a paso

### 0. Comprobar que Docker funciona

```bash
docker ps
```

| Parte | Qué significa |
|---|---|
| `docker` | El cliente de Docker: le pasa la orden al daemon, el servicio que hace el trabajo. |
| `ps` | Lista los contenedores en marcha. Si sale la cabecera, aunque esté vacía, Docker funciona. |

Si sale `permission denied ... docker.sock`, tu usuario no puede usar Docker. Ejecuta `sudo usermod -aG docker $USER`, cierra sesión y vuelve a entrar. Otra opción es poner `sudo` delante de cada comando.

### 1. Crear la carpeta de la práctica y entrar

```bash
mkdir -p ~/docker/ex01
cd ~/docker/ex01
```

| Parte | Qué significa |
|---|---|
| `mkdir` | Crea una carpeta. |
| `-p` | Crea también las carpetas intermedias y no da error si ya existen. |
| `~` | Tu carpeta personal (`/home/tuusuario`). |
| `cd` | Entra en la carpeta: todo lo que hagas después se hace ahí. |

Esta carpeta es el **contexto** del build: el Dockerfile solo puede copiar lo que hay aquí dentro.

### 2. Copiar el index.html del profesor

```bash
ls ~/Descargas
cp ~/Descargas/index.html .
```

| Parte | Qué significa |
|---|---|
| `ls ~/Descargas` | Enseña lo que hay en Descargas, para ver dónde quedó el index que bajaste de Aules. |
| `cp origen destino` | Copia un fichero. |
| `.` | "La carpeta en la que estoy" (`~/docker/ex01`). |

Si la VM está en inglés, la carpeta es `~/Downloads`; en valenciano, `~/Baixades`.

### 3. Crear el Dockerfile

```bash
nano Dockerfile
```

Pega con <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd>, guarda con <kbd>Ctrl</kbd>+<kbd>O</kbd> y <kbd>Enter</kbd>, y sal con <kbd>Ctrl</kbd>+<kbd>X</kbd>. Se llama exactamente `Dockerfile`: con D mayúscula y sin extensión.

```dockerfile
FROM httpd:2.4
COPY index.html /usr/local/apache2/htdocs/
```

| Parte | Qué significa |
|---|---|
| `FROM` | La imagen de la que partes (imagen base). Siempre es la primera línea. |
| `httpd` | La imagen oficial de Apache HTTP Server en Docker Hub. |
| `:2.4` | El tag: la versión. Sin tag usaría `latest` (la última). |
| `COPY origen destino` | Copia un fichero de tu carpeta (el contexto) dentro de la imagen. |
| `index.html` | El fichero que copias, que está en tu carpeta. |
| `/usr/local/apache2/htdocs/` | La carpeta que sirve Apache en esta imagen: lo que pones ahí se ve en la web. Con la `/` final, el fichero se copia dentro con el mismo nombre. |

Para comprobarlo: `ls` tiene que enseñar `Dockerfile  index.html`, y `cat Dockerfile` enseña el contenido.

### 4. Construir la imagen

```bash
docker build -t la-meua-web:v1 .
```

| Parte | Qué significa |
|---|---|
| `docker build` | Crea una imagen siguiendo el Dockerfile. |
| `-t` | El nombre (tag) que tendrá la imagen. |
| `la-meua-web` | El nombre de la imagen (lo pide el enunciado). |
| `:v1` | El tag, la versión (lo pide el enunciado). |
| `.` | El contexto: la carpeta actual. Sin el punto, el comando falla. |

**Deberías ver, al final:**

```text
naming to docker.io/library/la-meua-web:v1 done
```

`docker.io/library/` significa que es una imagen local, sin usuario de Docker Hub. Con `docker images` la ves en la lista.

### 5. Arrancar el contenedor con el puerto 4000

```bash
docker run -d --name la-meua-web -p 4000:80 la-meua-web:v1
```

| Parte | Qué significa |
|---|---|
| `docker run` | Crea un contenedor a partir de una imagen y lo arranca. |
| `-d` | En segundo plano: te devuelve el prompt y el contenedor sigue funcionando. |
| `--name la-meua-web` | El nombre del contenedor, con dos guiones. |
| `-p 4000:80` | **Puerto de la VM : puerto del contenedor.** Lo que llega al 4000 de la VM va al 80 del contenedor, donde escucha Apache. |
| `la-meua-web:v1` | La imagen que acabas de construir. Siempre va al final. |

Devuelve un ID largo: es el identificador del contenedor.

```bash
docker ps
```

**Deberías ver:**

```text
CONTAINER ID   IMAGE            COMMAND              STATUS        PORTS                  NAMES
828d82a4c116   la-meua-web:v1   "httpd-foreground"   Up 5 seconds  0.0.0.0:4000->80/tcp   la-meua-web
```

| Columna | Qué significa |
|---|---|
| CONTAINER ID | El identificador corto del contenedor. |
| IMAGE | De qué imagen se ha creado. |
| COMMAND | El proceso que ejecuta: `httpd-foreground` es Apache en primer plano. |
| STATUS | `Up` = en marcha. `Exited` = parado. |
| PORTS | `0.0.0.0:4000->80/tcp`: el 4000 de la VM va al 80 del contenedor. |
| NAMES | El nombre que le diste con `--name`. |

### 6. Comprobar que funciona

En Firefox, dentro de la VM: `http://localhost:4000`. Tiene que salir el index del profesor (**haz captura**). Desde la terminal también puedes usar `curl http://localhost:4000`.

| Parte | Qué significa |
|---|---|
| `localhost` | La propia máquina donde estás: la VM. |
| `:4000` | El puerto que publicaste con `-p`. |

### 7. Ponerle tu usuario de Docker Hub

```bash
docker tag la-meua-web:v1 tuusuario/la-meua-web:v1
docker images
```

| Parte | Qué significa |
|---|---|
| `docker tag` | Le pone otro nombre a una imagen que ya existe. No la copia ni la vuelve a construir. |
| `la-meua-web:v1` | El nombre que ya tiene. |
| `tuusuario/la-meua-web:v1` | El nombre nuevo. Docker Hub solo deja subir imágenes que empiezan por tu usuario. |

En `docker images` salen dos líneas con **el mismo ID**: es una sola imagen con dos nombres.

### 8. Iniciar sesión en Docker Hub

```bash
docker login -u tuusuario
```

Te pide la contraseña; al escribirla no se ve nada, es normal. **Deberías ver:** `Login Succeeded`. Si tienes la verificación en dos pasos, la contraseña no vale: usa un token (hub.docker.com → Account settings → Personal access tokens).

### 9. Subir la imagen

```bash
docker push tuusuario/la-meua-web:v1
```

| Parte | Qué significa |
|---|---|
| `docker push` | Sube la imagen a Docker Hub. Si el repositorio no existe, lo crea. |
| `tuusuario/la-meua-web:v1` | La imagen que subes: usuario, nombre y tag. |

**Deberías ver, al final:** `v1: digest: sha256:... size: ...`. El *digest* es la huella única de la imagen subida.

### 10. Comprobar en Docker Hub

Abre `https://hub.docker.com/r/tuusuario/la-meua-web` → pestaña **Tags**: aparece `v1` (**haz captura**). Desde cualquier ordenador, `docker pull tuusuario/la-meua-web:v1` la descarga.

## Si algo falla

| Error | Qué pasa y cómo se arregla |
|---|---|
| `permission denied ... docker.sock` | Tu usuario no puede usar Docker: `sudo usermod -aG docker $USER` y vuelve a iniciar sesión, o usa `sudo`. |
| `failed to read dockerfile` | No estás en la carpeta (`cd ~/docker/ex01`) o el fichero no se llama exactamente `Dockerfile`. |
| `"/index.html": not found` | El index no está en la carpeta: repite el `cp` del paso 2. |
| `port is already allocated` | Algo ya usa el 4000: mira `docker ps` y bórralo, o usa `-p 4001:80`. |
| `Conflict. The container name "/la-meua-web" is already in use` | Queda un contenedor de antes: `docker rm -f la-meua-web` y repite el run. |
| `push access denied` | La imagen no lleva tu usuario exacto (paso 7) o no has hecho login (paso 8). |

## Copia y pega

```text
PRÁCTICA 1 · IMAGEN DE APACHE (la-meua-web:v1)

1) Crear la carpeta y entrar
   mkdir -p ~/docker/ex01
   cd ~/docker/ex01
     mkdir -> crea una carpeta
     -p    -> crea también las carpetas intermedias y no da error si ya existe
     ~     -> tu carpeta personal
     cd    -> entra en la carpeta

2) Copiar el index.html del profesor
   cp ~/Descargas/index.html .
     cp -> copia un fichero (origen destino)
     .  -> la carpeta en la que estoy

3) Crear el Dockerfile
   nano Dockerfile
     FROM httpd:2.4
     COPY index.html /usr/local/apache2/htdocs/

     FROM httpd:2.4  -> parte de la imagen oficial de Apache (httpd), versión 2.4
     COPY            -> copia un fichero de mi carpeta dentro de la imagen
     /usr/local/apache2/htdocs/ -> la carpeta que sirve Apache: lo que hay ahí se ve en la web

4) Construir la imagen
   docker build -t la-meua-web:v1 .
     docker build -> crea una imagen a partir del Dockerfile
     -t           -> le da nombre:tag
     la-meua-web  -> nombre de la imagen
     v1           -> tag (versión)
     .            -> la carpeta actual (donde están el Dockerfile y el index)

5) Arrancar el contenedor
   docker run -d --name la-meua-web -p 4000:80 la-meua-web:v1
     docker run -> crea y arranca un contenedor a partir de una imagen
     -d         -> en segundo plano
     --name     -> nombre del contenedor
     -p 4000:80 -> puerto de la VM : puerto del contenedor (Apache escucha en el 80)
     la-meua-web:v1 -> la imagen que uso

6) Comprobar que está en marcha
   docker ps
     ps -> lista los contenedores en marcha. Tiene que poner Up y 0.0.0.0:4000->80/tcp

7) Comprobar que funciona
   Firefox: http://localhost:4000
     localhost -> la propia VM
     4000      -> el puerto que publiqué con -p

8) Ponerle mi usuario de Docker Hub
   docker tag la-meua-web:v1 tuusuario/la-meua-web:v1
     docker tag -> le pone otro nombre a la imagen (misma imagen, mismo ID)
     tuusuario/ -> Docker Hub solo deja subir imágenes con tu usuario delante

9) Iniciar sesión en Docker Hub
   docker login -u tuusuario
     login -> inicia sesión en Docker Hub (pide la contraseña). Sale: Login Succeeded

10) Subir la imagen
   docker push tuusuario/la-meua-web:v1
     push -> sube la imagen a Docker Hub
     Se comprueba en hub.docker.com/r/tuusuario/la-meua-web (pestaña Tags: v1)
```
