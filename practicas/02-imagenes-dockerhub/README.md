# Práctica 2 · Crea imágenes y súbelas a Docker Hub y GitHub

> **Enunciado (Aules, "Crea imatges DockerHub"):** cuatro Dockerfiles (nginx y Apache, en Alpine y en Debian). Cada uno instala una herramienta y copia un index. Comparar los tamaños, subir las imágenes a Docker Hub y los Dockerfiles a GitHub (repositorio `practica-dockerfile-1`, con un README que tenga tu nombre y la comparación de tamaños).

| Carpeta | Imagen que se crea | Base | Herramienta | Puerto |
|---|---|---|---|---|
| [`ex1`](ex1/Dockerfile) | `tuusuario/web-nginx:1.0` | `nginx:1.27-alpine` (Alpine) | nano | 8081 |
| [`ex2`](ex2/Dockerfile) | `tuusuario/web-apache:1.0` | `httpd:2.4.62` (Debian) | curl | 8082 |
| [`ex3`](ex3/Dockerfile) | `tuusuario/web-nginx:2.0` | `nginx:1.26` (Debian) | nano | 8083 |
| [`ex4`](ex4/Dockerfile) | `tuusuario/web-apache:2.0` | `httpd:2.4-alpine` (Alpine) | curl | 8084 |

Cambia `tuusuario` por tu usuario de Docker Hub.

## Paso a paso

### 1. Crear las carpetas y entrar

```bash
mkdir -p ~/docker-imatges/ex1 ~/docker-imatges/ex2 ~/docker-imatges/ex3 ~/docker-imatges/ex4
cd ~/docker-imatges
```

`mkdir -p` crea las cuatro carpetas (y `docker-imatges` si no existe); `cd` entra en ella.

### 2. Un index.html en cada carpeta

Si el profesor os da index, cópialos con `cp`. Si no:

```bash
echo "<h1>Exercici 1</h1>" > ex1/index.html
echo "<h1>Exercici 2</h1>" > ex2/index.html
echo "<h1>Exercici 3</h1>" > ex3/index.html
echo "<h1>Exercici 4</h1>" > ex4/index.html
```

| Parte | Qué significa |
|---|---|
| `echo "texto"` | Escribe un texto. |
| `>` | Lo guarda en un fichero (si ya existe, lo sobrescribe). |

### 3. Los cuatro Dockerfiles

Con `nano ex1/Dockerfile`, `nano ex2/Dockerfile`… (guardar con <kbd>Ctrl</kbd>+<kbd>O</kbd> y <kbd>Enter</kbd>, salir con <kbd>Ctrl</kbd>+<kbd>X</kbd>).

**ex1:** nginx sobre Alpine, con nano.

```dockerfile
FROM nginx:1.27-alpine
RUN apk add --no-cache nano
COPY index.html /usr/share/nginx/html/index.html
```

**ex2:** Apache sobre Debian, con curl.

```dockerfile
FROM httpd:2.4.62
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*
COPY index.html /usr/local/apache2/htdocs/index.html
```

**ex3:** nginx sobre Debian, con nano.

```dockerfile
FROM nginx:1.26
RUN apt-get update && \
    apt-get install -y nano && \
    rm -rf /var/lib/apt/lists/*
COPY index.html /usr/share/nginx/html/index.html
```

**ex4:** Apache sobre Alpine, con curl.

```dockerfile
FROM httpd:2.4-alpine
RUN apk add --no-cache curl
COPY index.html /usr/local/apache2/htdocs/index.html
```

| Parte | Qué significa |
|---|---|
| `FROM imagen:tag` | Imagen base y su versión. *alpine* = una versión mínima de Linux, muy pequeña. |
| `RUN` | Ejecuta un comando **durante el build** (aquí, instalar programas). |
| `apk add --no-cache` | Instala paquetes en Alpine, sin guardar la caché (no hace falta update antes). |
| `apt-get update` | Actualiza la lista de paquetes en Debian (obligatorio antes de install). |
| `apt-get install -y` | Instala en Debian; `-y` responde "sí" solo (si no, el build se para a preguntar). |
| `rm -rf /var/lib/apt/lists/*` | Borra las listas descargadas para que la imagen ocupe menos. |
| `&&` | Encadena comandos en un solo `RUN` (una sola capa). |
| `\` | El comando sigue en la línea de abajo. |
| `/usr/share/nginx/html/` | Carpeta web de **nginx**. |
| `/usr/local/apache2/htdocs/` | Carpeta web de **Apache**. |

Comprueba que cada carpeta tiene sus dos ficheros con `ls ex1 ex2 ex3 ex4`.

### 4. Construir las cuatro imágenes

```bash
docker build -t tuusuario/web-nginx:1.0 ex1
docker build -t tuusuario/web-apache:1.0 ex2
docker build -t tuusuario/web-nginx:2.0 ex3
docker build -t tuusuario/web-apache:2.0 ex4
```

| Parte | Qué significa |
|---|---|
| `-t tuusuario/nombre:tag` | Nombre con tu usuario delante: así se puede subir sin `docker tag`. |
| `ex1`, `ex2`… | El contexto: la carpeta de cada ejercicio (en vez de `.`), porque estás en `~/docker-imatges`. |

Cada build termina con `naming to docker.io/tuusuario/...`. Las de Debian tardan más.

> **Lo que nos pasó:** el build de ex2 y ex3 falló con `/bin/sh: 1: rem-rf: not found` y `exit code: 127`. Era una errata: es `rm -rf`, con espacio. El código 127 significa "comando no encontrado". Además, en ex3 la ruta estaba como `/usr/local/nginx/html/` y es `/usr/share/nginx/html/`. Con esa ruta mal, el build funciona, pero en el navegador sale la página de bienvenida de nginx en lugar de tu index.

### 5. Arrancar un contenedor de cada una

```bash
docker run -d --name web1 -p 8081:80 tuusuario/web-nginx:1.0
docker run -d --name web2 -p 8082:80 tuusuario/web-apache:1.0
docker run -d --name web3 -p 8083:80 tuusuario/web-nginx:2.0
docker run -d --name web4 -p 8084:80 tuusuario/web-apache:2.0
docker ps
```

Cada uno usa un puerto de la VM distinto (8081 a 8084), pero dentro todos escuchan en el 80. `docker ps` tiene que enseñar los cuatro en `Up`.

### 6. Comprobar

En Firefox, `localhost:8081`, `8082`, `8083` y `8084` enseñan Exercici 1, 2, 3 y 4 (**haz captura**). Después:

```bash
docker exec web1 nano --version
docker exec web2 curl --version
docker exec web3 nano --version
docker exec web4 curl --version
```

`docker exec` ejecuta un comando dentro de un contenedor en marcha. Si enseña la versión, la herramienta está instalada dentro de la imagen.

### 7. Comparar tamaños

```bash
docker images
```

Las de **Alpine** (`web-nginx:1.0` y `web-apache:2.0`) ocupan unas decenas de MB. Las de **Debian** (`web-apache:1.0` y `web-nginx:2.0`), unos 150-200 MB. Alpine es una distribución mínima pensada para contenedores (usa musl y BusyBox); Debian trae muchas más librerías y herramientas.

### 8. Subir a Docker Hub

```bash
docker login -u tuusuario
docker push tuusuario/web-nginx:1.0
docker push tuusuario/web-apache:1.0
docker push tuusuario/web-nginx:2.0
docker push tuusuario/web-apache:2.0
```

`login` inicia sesión (`Login Succeeded`); `push` sube cada imagen y termina con `1.0: digest: sha256:...`. Compruébalo en `hub.docker.com/u/tuusuario`: tienen que estar `web-nginx` y `web-apache` con las etiquetas `1.0` y `2.0` (**haz captura**).

Si da `denied`, a la imagen le falta tu usuario delante (`docker tag web-nginx:1.0 tuusuario/web-nginx:1.0`) o no has hecho login.

### 9. Subir a GitHub desde la web

Hazlo en el Firefox **de la VM**, porque los ficheros están ahí.

1. github.com → **+** (arriba a la derecha) → **New repository** → nombre `practica-dockerfile-1` → **Public** → marca **Add a README file** → **Create repository**.
2. **Add file** → **Upload files** → abre Archivos → `docker-imatges` y **arrastra** las carpetas `ex1`, `ex2`, `ex3` y `ex4` a Firefox. Arrástralas: así se mantienen las carpetas. El botón *choose your files* solo deja elegir ficheros sueltos.
3. Comprueba que salen 8 ficheros → mensaje `Pràctica Dockerfile 1` → **Commit changes**.
4. Pulsa `README.md` → lápiz (**Edit this file**) → pega el texto de abajo con tus datos → **Commit changes**.

```text
# Pràctica Dockerfile 1

Alumne: Nom Cognom

| Imatge | Base | Mida |
|---|---|---|
| tuusuario/web-nginx:1.0 | nginx:1.27-alpine | XX MB |
| tuusuario/web-apache:1.0 | httpd:2.4.62 (Debian) | XX MB |
| tuusuario/web-nginx:2.0 | nginx:1.26 (Debian) | XX MB |
| tuusuario/web-apache:2.0 | httpd:2.4-alpine | XX MB |

Les imatges basades en Alpine ocupen molt menys que les basades en Debian.
Alpine és una distribució mínima pensada per a contenidors (usa musl i BusyBox),
mentre que Debian porta moltes més llibreries i eines.
```

<details>
<summary>La misma subida desde la terminal, con git</summary>

```bash
git config --global user.name "Nom Cognom"
git config --global user.email "el-teu-correu@exemple.com"
git init
git add .
git commit -m "Pràctica Dockerfile 1"
git branch -M main
git remote add origin https://github.com/tuusuariogithub/practica-dockerfile-1.git
git push -u origin main
```

Para este método, el repositorio de GitHub se crea **sin** README. Si git pide contraseña, la de GitHub no vale: usa un token (GitHub → Settings → Developer settings → Personal access tokens).

</details>

### 10. Limpiar

```bash
docker rm -f web1 web2 web3 web4
```

## Copia y pega

```text
PRÁCTICA 2 · CREA IMÁGENES Y SÚBELAS A DOCKER HUB Y GITHUB

1) Crear las carpetas y entrar
   mkdir -p ~/docker-imatges/ex1 ~/docker-imatges/ex2 ~/docker-imatges/ex3 ~/docker-imatges/ex4
   cd ~/docker-imatges
     mkdir -p -> crea las carpetas (y las intermedias)
     cd       -> entra en la carpeta

2) Un index.html en cada carpeta
   echo "<h1>Exercici 1</h1>" > ex1/index.html   (igual con ex2, ex3 y ex4)
     echo "texto" -> escribe un texto
     >            -> lo guarda en un fichero

3) Los cuatro Dockerfiles (nano ex1/Dockerfile ...)
   ex1 (nginx + Alpine + nano):
     FROM nginx:1.27-alpine
     RUN apk add --no-cache nano
     COPY index.html /usr/share/nginx/html/index.html
   ex2 (Apache + Debian + curl):
     FROM httpd:2.4.62
     RUN apt-get update && \
         apt-get install -y curl && \
         rm -rf /var/lib/apt/lists/*
     COPY index.html /usr/local/apache2/htdocs/index.html
   ex3 (nginx + Debian + nano):
     FROM nginx:1.26
     RUN apt-get update && \
         apt-get install -y nano && \
         rm -rf /var/lib/apt/lists/*
     COPY index.html /usr/share/nginx/html/index.html
   ex4 (Apache + Alpine + curl):
     FROM httpd:2.4-alpine
     RUN apk add --no-cache curl
     COPY index.html /usr/local/apache2/htdocs/index.html

     FROM imagen:tag     -> imagen base y su versión (alpine = Linux mínimo)
     RUN                 -> ejecuta un comando durante el build (instalar programas)
     apk add --no-cache  -> instala en Alpine (sin update antes, sin guardar caché)
     apt-get update      -> actualiza la lista de paquetes en Debian (obligatorio antes de install)
     apt-get install -y  -> instala en Debian; -y responde "sí" solo
     rm -rf /var/lib/apt/lists/* -> borra las listas descargadas (imagen más pequeña)
                            OJO: es "rm -rf" con espacio. Si pones "rem-rf" da "not found" y exit code 127
     &&                  -> encadena comandos en un solo RUN
     \                   -> sigue el comando en la línea de abajo
     /usr/share/nginx/html/     -> carpeta web de nginx (OJO: share, no local)
     /usr/local/apache2/htdocs/ -> carpeta web de Apache

4) Construir las cuatro imágenes
   docker build -t tuusuario/web-nginx:1.0  ex1
   docker build -t tuusuario/web-apache:1.0 ex2
   docker build -t tuusuario/web-nginx:2.0  ex3
   docker build -t tuusuario/web-apache:2.0 ex4
     -t tuusuario/nombre:tag -> nombre con mi usuario delante (así se puede subir sin docker tag)
     ex1, ex2...             -> contexto: la carpeta de cada ejercicio (en vez de ".")

5) Arrancar un contenedor de cada una
   docker run -d --name web1 -p 8081:80 tuusuario/web-nginx:1.0
   docker run -d --name web2 -p 8082:80 tuusuario/web-apache:1.0
   docker run -d --name web3 -p 8083:80 tuusuario/web-nginx:2.0
   docker run -d --name web4 -p 8084:80 tuusuario/web-apache:2.0
   docker ps   -> los cuatro en Up
     -p 8081:80 -> puerto de la VM : puerto del contenedor (nginx y Apache escuchan en el 80)

6) Comprobar
   Firefox: localhost:8081, 8082, 8083, 8084 -> Exercici 1, 2, 3, 4
   docker exec web1 nano --version
   docker exec web2 curl --version
     docker exec -> ejecuta un comando dentro de un contenedor en marcha
     si enseña la versión -> la herramienta está instalada en la imagen

7) Comparar tamaños
   docker images
     Alpine (web-nginx:1.0, web-apache:2.0) -> mucho más pequeñas
     Debian (web-apache:1.0, web-nginx:2.0) -> más grandes
     Alpine es una distribución mínima para contenedores; Debian lleva muchas más librerías

8) Subir a Docker Hub
   docker login -u tuusuario
   docker push tuusuario/web-nginx:1.0
   docker push tuusuario/web-apache:1.0
   docker push tuusuario/web-nginx:2.0
   docker push tuusuario/web-apache:2.0
     login -> inicia sesión (Login Succeeded)
     push  -> sube la imagen. Si da "denied": falta mi usuario en el nombre o no hice login
     Comprobar en hub.docker.com/u/tuusuario (web-nginx y web-apache, tags 1.0 y 2.0)

9) Subir a GitHub desde la web
   github.com -> + -> New repository -> practica-dockerfile-1 · Public · Add a README file -> Create repository
   Add file -> Upload files -> ARRASTRAR ex1, ex2, ex3, ex4 desde Archivos -> Commit changes
     arrastrar -> mantiene las carpetas con su Dockerfile e index dentro
   README.md -> lápiz -> nombre + tabla de tamaños + explicación Alpine/Debian -> Commit changes
     commit -> guardar los cambios en el repositorio con un mensaje

10) Limpiar
   docker rm -f web1 web2 web3 web4
     rm -f -> borra los contenedores aunque estén en marcha
```
