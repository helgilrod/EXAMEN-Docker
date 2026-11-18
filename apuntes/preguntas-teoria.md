# Preguntas de teoría

Pregúntate cada una antes de abrir la respuesta. Los comandos se han ejecutado y, donde aparece, la salida es la real.

Mostrar todas las respuestas

### Conceptos

<details>
<summary>¿Qué diferencia hay entre una imagen y un contenedor?</summary>

La imagen es una plantilla de solo lectura, hecha de capas. El contenedor es una instancia en ejecución de esa imagen, con su propia capa de escritura. De una imagen puedes crear muchos contenedores.

</details>

<details>
<summary>¿Qué diferencia hay entre un contenedor y una máquina virtual?</summary>

La VM lleva un sistema operativo completo sobre un hipervisor: ocupa GB y arranca en minutos. El contenedor comparte el kernel del host: ocupa MB y arranca en segundos. A cambio, aísla menos que una VM.

</details>

<details>
<summary>¿Cómo funciona Docker por dentro (arquitectura)?</summary>

Cliente-servidor. El cliente (el comando `docker`) envía las órdenes al daemon (`dockerd`), que crea, ejecuta y distribuye los contenedores. Las imágenes se descargan de un registro (Docker Hub).

</details>

<details>
<summary>¿Qué es Docker Hub?</summary>

El registro público de imágenes. Las oficiales no llevan usuario (`nginx`); las de los usuarios, sí (`usuari/imatge`).

</details>

<details>
<summary>¿Qué es una etiqueta (tag) y qué pasa si no la pones?</summary>

Es la versión de la imagen: `nombre:tag`, por ejemplo `ubuntu:24.04`. Si no la pones, Docker usa `latest`.

</details>

<details>
<summary>¿Qué es un Dockerfile?</summary>

Un fichero de texto con las instrucciones para construir una imagen (`FROM`, `RUN`, `COPY`, `CMD`…). Se construye con `docker build`.

</details>

<details>
<summary>¿Qué es el contexto de un build?</summary>

La carpeta que se envía al build: el `.` de `docker build -t x .`. `COPY` solo puede coger ficheros de ahí; `COPY ../algo` falla.

</details>

<details>
<summary>¿Qué es una capa de una imagen?</summary>

Cada instrucción del Dockerfile que cambia ficheros (`RUN`, `COPY`…) crea una capa. Se guardan en caché y se reutilizan. Se ven con `docker history imagen`.

</details>

<details>
<summary>¿Qué es un volumen y para qué sirve?</summary>

Almacenamiento fuera del contenedor para que los datos no se pierdan al borrarlo. Puede ser anónimo (`-v /data`), con nombre (`-v vol:/data`) o una carpeta del host (`-v /ruta:/data`).

</details>

### Imágenes

<details>
<summary>Quieres descargar la última imagen de Ubuntu. ¿Qué comando usas?</summary>

`docker pull ubuntu`, que es lo mismo que `docker pull ubuntu:latest`. Salida real:

```text
Using default tag: latest
latest: Pulling from library/ubuntu
```

</details>

<details>
<summary>¿Y una versión concreta, por ejemplo Ubuntu 24.04?</summary>

`docker pull ubuntu:24.04`

</details>

<details>
<summary>¿Cómo buscas una imagen en Docker Hub desde la terminal?</summary>

`docker search nginx`. La oficial tiene `[OK]` en la columna OFFICIAL.

</details>

<details>
<summary>¿Cómo ves las imágenes que tienes descargadas?</summary>

`docker images` o `docker image ls`. Solo los ID: `docker images -q`.

</details>

<details>
<summary>¿Cómo ves los detalles de una imagen (puertos, variables, comando)?</summary>

`docker image inspect nginx`. Solo los puertos: `docker image inspect -f '{{.Config.ExposedPorts}}' nginx` → `map[80/tcp:{}]`.

</details>

<details>
<summary>¿Cómo ves las capas de una imagen?</summary>

`docker history nginx`

</details>

<details>
<summary>¿Cómo borras una imagen? ¿Qué pasa si un contenedor la usa?</summary>

`docker rmi nginx`. Si un contenedor la usa (aunque esté parado), falla. Error real:

```text
conflict: unable to delete alumne/web-nginx:1.0 (must be forced) - container 006a4a7d11f9 is using its referenced image
```

Borra antes el contenedor, o fuerza con `docker rmi -f`.

</details>

<details>
<summary>¿Cómo borras las imágenes que no se usan?</summary>

`docker image prune` (las que no tienen nombre). Con `-a`, todas las que no usa ningún contenedor.

</details>

<details>
<summary>¿Cómo le pones otro nombre o etiqueta a una imagen?</summary>

`docker tag web-nginx:1.0 usuari/web-nginx:1.0`. No copia nada: es otro nombre para la misma imagen (mismo ID).

</details>

<details>
<summary>¿Cómo creas una imagen a partir de un contenedor?</summary>

`docker commit contenedor usuari/imagen:tag`. Primero va el contenedor y después el nombre de la imagen nueva.

</details>

### Contenedores

<details>
<summary>Arranca nginx en segundo plano, llamado "web", en el puerto 8080 de tu máquina</summary>

`docker run -d --name web -p 8080:80 nginx`

</details>

<details>
<summary>¿Qué pasa si haces docker run de una imagen que no tienes?</summary>

La descarga de Docker Hub automáticamente (`Unable to find image 'x' locally`) y después crea el contenedor.

</details>

<details>
<summary>¿Cómo arrancas un Ubuntu y entras en su terminal?</summary>

`docker run -it ubuntu bash`. `-i` mantiene la entrada abierta; `-t` da una terminal.

</details>

<details>
<summary>¿Cómo haces que el contenedor se borre solo al pararse?</summary>

Con `--rm`: `docker run --rm imagen`.

</details>

<details>
<summary>¿Cómo ves los contenedores en marcha? ¿Y todos?</summary>

`docker ps` enseña los que están en marcha; `docker ps -a`, todos, también los parados.

</details>

<details>
<summary>¿Cómo paras, arrancas y reinicias un contenedor?</summary>

`docker stop web`, `docker start web`, `docker restart web`. Para congelarlo: `pause` / `unpause`. Para matarlo: `kill`.

</details>

<details>
<summary>¿Cómo borras un contenedor? ¿Y si está en marcha?</summary>

`docker rm web`. Si está en marcha, falla. Error real:

```text
cannot remove container "enmarcha": container is running: stop the container before removing or force remove
```

Páralo antes o usa `docker rm -f web`.

</details>

<details>
<summary>¿Cómo borras todos los contenedores parados?</summary>

`docker container prune`. Todo lo que no se usa (contenedores, redes, imágenes huérfanas): `docker system prune`.

</details>

<details>
<summary>¿Cómo ves lo que ha escrito un contenedor (su salida)?</summary>

`docker logs web`. En directo: `docker logs -f web`.

</details>

<details>
<summary>¿Cómo entras en un contenedor que ya está en marcha?</summary>

`docker exec -it web bash`. En imágenes Alpine no hay bash: usa `sh`.

</details>

<details>
<summary>¿Cómo sales de un contenedor sin pararlo?</summary>

<kbd>Ctrl</kbd>+<kbd>P</kbd> y luego <kbd>Ctrl</kbd>+<kbd>Q</kbd>. Con `exit` se para si es su proceso principal.

</details>

<details>
<summary>¿Cómo copias un fichero de tu máquina a un contenedor?</summary>

`docker cp index.html web:/usr/share/nginx/html/`. Al revés también funciona: `docker cp web:/ruta/fichero .`

</details>

<details>
<summary>¿Cómo ves toda la información de un contenedor, por ejemplo su IP?</summary>

`docker inspect web`. Solo la IP: `docker inspect -f '{{.NetworkSettings.IPAddress}}' web`.

</details>

<details>
<summary>¿Cómo pasas una variable de entorno a un contenedor?</summary>

`-e CLAVE=valor`, una por variable: `docker run -e MYSQL_ROOT_PASSWORD=1234 mysql:8.0`. Desde un fichero: `--env-file fichero.env`.

</details>

<details>
<summary>¿Cómo ves cuánta CPU y memoria usan los contenedores?</summary>

`docker stats`. Los procesos de uno en concreto: `docker top web`.

</details>

<details>
<summary>¿Cómo le cambias el nombre a un contenedor?</summary>

`docker rename viejo nuevo`

</details>

### Puertos

<details>
<summary>¿Qué significa -p 8080:80?</summary>

Puerto de tu máquina : puerto del contenedor. Lo que llega al 8080 del host va al 80 del contenedor.

</details>

<details>
<summary>¿Qué hace EXPOSE en un Dockerfile? ¿Publica el puerto?</summary>

No. Solo documenta en qué puerto escucha la app. Para entrar desde fuera hace falta `-p` (o `-P`) en el run.

</details>

<details>
<summary>¿Qué diferencia hay entre -p y -P?</summary>

`-p 8080:80` eliges el puerto. `-P` publica todos los puertos del `EXPOSE` en puertos aleatorios del host (por ejemplo 32768).

</details>

<details>
<summary>¿Cómo sabes qué puerto tiene asignado un contenedor?</summary>

`docker port web` → `80/tcp -> 0.0.0.0:32768`. También en la columna PORTS de `docker ps`.

</details>

<details>
<summary>¿Cómo sabes en qué puerto escucha una imagen por dentro?</summary>

`docker image inspect -f '{{.Config.ExposedPorts}}' imagen`, o en su página de Docker Hub.

</details>

<details>
<summary>Te sale "port is already allocated". ¿Qué pasa?</summary>

Otro contenedor o programa ya usa ese puerto del host. Cambia el de la izquierda (`-p 8081:80`) o para lo que lo ocupa.

</details>

### Dockerfile y build

<details>
<summary>¿Cómo construyes una imagen a partir de un Dockerfile?</summary>

`docker build -t nombre:tag .`, con el punto final (el contexto).

</details>

<details>
<summary>¿Y si el Dockerfile tiene otro nombre?</summary>

`docker build -f MiDockerfile -t nombre:tag .`

</details>

<details>
<summary>¿Qué diferencia hay entre RUN y CMD?</summary>

`RUN` se ejecuta durante el **build** (instalar paquetes) y crea una capa. `CMD` es lo que se ejecuta al **arrancar el contenedor**. Si hay varios CMD, solo cuenta el último.

</details>

<details>
<summary>¿Qué diferencia hay entre CMD y ENTRYPOINT?</summary>

El comando que pongas al final de `docker run` sustituye al `CMD`. `ENTRYPOINT` es fijo, y el CMD pasa a ser sus argumentos. Con `ENTRYPOINT ["echo"]` y `CMD ["Hola"]`: `docker run img` → `echo Hola`; `docker run img Adeu` → `echo Adeu`.

</details>

<details>
<summary>¿Qué diferencia hay entre COPY y ADD?</summary>

Los dos copian ficheros a la imagen. `ADD` además acepta URLs y descomprime .tar. Se recomienda `COPY`.

</details>

<details>
<summary>¿Para qué sirve WORKDIR?</summary>

Fija el directorio de trabajo para las instrucciones que vienen después (RUN, COPY, CMD…) y lo crea si no existe.

</details>

<details>
<summary>¿Qué diferencia hay entre ENV y ARG?</summary>

`ENV` crea una variable que existe en el build y también en el contenedor. `ARG` solo existe durante el build y se le da valor con `--build-arg nombre=valor`.

</details>

<details>
<summary>¿Por qué se copia requirements.txt (o package.json) antes que el resto del código?</summary>

Por la caché. Si solo cambias el código, Docker reutiliza la capa del `pip install` (o `npm install`) y el build es mucho más rápido.

</details>

<details>
<summary>¿Cómo construyes sin usar la caché?</summary>

`docker build --no-cache -t nombre .`

</details>

<details>
<summary>¿Para qué sirve .dockerignore?</summary>

Lista los ficheros que no se envían al build (`node_modules`, `.git`…), así no acaban dentro de la imagen.

</details>

<details>
<summary>¿Qué es un multi-stage build?</summary>

Un Dockerfile con varios `FROM`. Las primeras etapas compilan, y la última copia solo el resultado con `COPY --from=etapa`. La imagen final es la del último FROM y ocupa mucho menos.

</details>

### Docker Hub y GitHub

<details>
<summary>¿Qué comandos usas para subir una imagen a Docker Hub?</summary>

`docker login` → `docker tag imagen usuari/imagen:tag` (si no lleva tu usuario) → `docker push usuari/imagen:tag`.

</details>

<details>
<summary>El push da "push access denied" o "denied". ¿Por qué?</summary>

La imagen no lleva tu usuario de Docker Hub delante, o no has hecho `docker login`.

</details>

<details>
<summary>¿Cómo descargas tu imagen en otro ordenador?</summary>

`docker pull usuari/imagen:tag`, o directamente `docker run`, que la descarga si no la tiene.

</details>

<details>
<summary>¿Qué se sube a Docker Hub y qué a GitHub?</summary>

A Docker Hub va la **imagen** ya construida. A GitHub, el **código**: Dockerfile, index.html, app.py, README.

</details>

<details>
<summary>¿Qué comandos usas para subir un proyecto a GitHub?</summary>

`git init` → `git add .` → `git commit -m "missatge"` → `git branch -M main` → `git remote add origin URL` → `git push -u origin main`.

</details>

<details>
<summary>Al hacer git push te pide contraseña y no la acepta. ¿Por qué?</summary>

GitHub no acepta la contraseña de la cuenta en la terminal: hay que usar un token personal (Settings → Developer settings → Personal access tokens).

</details>

### Volúmenes y redes

<details>
<summary>¿Cómo creas, listas, inspeccionas y borras un volumen?</summary>

`docker volume create vol1` · `docker volume ls` · `docker volume inspect vol1` · `docker volume rm vol1`

</details>

<details>
<summary>¿Cómo montas un volumen con nombre? ¿Y una carpeta de tu máquina?</summary>

Con nombre: `-v vol1:/var/lib/mysql`. Carpeta: `-v "$(pwd)/web":/usr/share/nginx/html` (ruta absoluta).

</details>

<details>
<summary>¿Se borra el volumen al borrar el contenedor?</summary>

No. Los volúmenes con nombre se quedan hasta que haces `docker volume rm` (o `docker compose down -v`).

</details>

<details>
<summary>¿Cómo haces que dos contenedores se comuniquen?</summary>

Crea una red (`docker network create red1`) y arráncalos con `--network red1`. Dentro de esa red se encuentran por su nombre de contenedor.

</details>

### Docker Compose

<details>
<summary>¿Qué es Docker Compose?</summary>

Una herramienta para definir y arrancar varios contenedores a la vez desde un fichero YAML (`docker-compose.yml`).

</details>

<details>
<summary>¿Cómo levantas, ves, paras y borras un proyecto de Compose?</summary>

`docker compose up -d` · `docker compose ps` · `docker compose stop` · `docker compose down` (con `-v` borra también los volúmenes).

</details>

<details>
<summary>Has cambiado el Dockerfile y Compose no lo nota. ¿Qué haces?</summary>

`docker compose up -d --build`

</details>

<details>
<summary>¿Cómo ves los logs de un servicio de Compose?</summary>

`docker compose logs -f nombre_servicio`

</details>

### Sistema

<details>
<summary>¿Cómo compruebas que Docker está bien instalado?</summary>

`docker run hello-world` → la segunda línea dice `Hello from Docker!`. La versión: `docker --version`; información general: `docker info`.

</details>
