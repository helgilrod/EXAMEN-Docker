# Chuleta de comandos Docker

## Chuleta

La sintaxis general es `docker <objeto> <acción>`: `image`, `container`, `volume`, `network`. Si dudas de una opción, `docker run --help | grep palabra` te la busca.

### Imágenes

| Comando | Qué hace |
|---|---|
| `docker search nginx` | Busca en Docker Hub |
| `docker pull nginx:1.27` | Descarga una versión concreta |
| `docker images` · `docker image ls` | Lista las imágenes locales |
| `docker image ls -a` | Incluye las intermedias y huérfanas |
| `docker image ls -q` | Solo los ID |
| `docker image ls -f dangling=true` | Filtra (aquí, las huérfanas) |
| `docker images "ng*"` | Filtra por nombre con comodín |
| `docker image inspect nginx` | Detalles en JSON (capas, Env, Cmd…) |
| `docker image history nginx` | Capas y la instrucción que creó cada una |
| `docker rmi img1 img2` | Borra imágenes; falla si un contenedor, aunque esté parado, la usa (`-f` fuerza) |
| `docker tag web:1.0 usuari/web:1.0` | Pone otro nombre a la misma imagen |
| `docker login` · `docker push usuari/web:1.0` | Sube la imagen a Docker Hub (el nombre tiene que empezar por tu usuario) |
| `docker commit cont usuari/img:tag` | Crea una imagen a partir de un contenedor (primero el **contenedor**) |
| `docker build -t nom:tag .` | Construye a partir del Dockerfile del contexto `.` |

### docker run

`docker run [OPCIONES] IMAGEN[:TAG] [COMANDO] [ARG...]`. Las opciones van **antes** de la imagen y el comando, **después**.

| Opción | Para qué |
|---|---|
| `-d` | En segundo plano (servidores) |
| `-it` | Interactivo con terminal (bash) |
| `--name web` | Nombre del contenedor (no existe `-n`) |
| `--rm` | Se borra al pararse (dos guiones) |
| `-p 8080:80` | **host:contenedor**. También `127.0.0.1:8080:80` |
| `-P` | Publica todos los `EXPOSE` en puertos aleatorios |
| `-e CLAVE=valor` | Variable de entorno (repite `-e` para cada una) |
| `--env-file fichero.env` | Variables desde un fichero |
| `-v vol:/ruta` | Volumen con nombre |
| `-v "$(pwd)/dir":/ruta` | Carpeta del host (ruta **absoluta**) |
| `--network red` | Lo conecta a una red |
| `--restart always` | `no` · `always` · `on-failure` · `unless-stopped` |
| `-w /app` | Directorio de trabajo |
| `--entrypoint sh` | Sustituye el ENTRYPOINT |
| `... imagen /bin/bash` | Sustituye el CMD (siempre al final) |

### Contenedores

| Comando | Qué hace |
|---|---|
| `docker ps` · `docker ps -a` | En marcha · todos (también los parados) |
| `docker start\|stop\|restart nom` | Cambia el estado |
| `docker kill\|pause\|unpause nom` | Lo mata · lo congela · lo reanuda |
| `docker logs -f nom` | Salida del proceso (`-f` la sigue en directo) |
| `docker exec -it nom bash` | Abre otra shell dentro (en Alpine: `sh`) |
| `docker exec -d nom cmd` | Ejecuta algo dentro en segundo plano |
| `docker attach nom` | Se engancha al proceso principal |
| <kbd>Ctrl</kbd>+<kbd>P</kbd> y luego <kbd>Ctrl</kbd>+<kbd>Q</kbd> | Sale de un `-it` o un `attach` **sin parar** el contenedor |
| `docker cp fich nom:/ruta` | Copia ficheros entre el host y el contenedor (en los dos sentidos) |
| `docker rename vell nou` | Cambia el nombre |
| `docker rm nom` · `docker rm -f nom` | Borra uno parado · lo borra aunque esté en marcha |
| `docker inspect nom` | Todo en JSON: IP, montajes, variables… |
| `docker inspect -f '{{.NetworkSettings.IPAddress}}' nom` | Solo la IP (en la red por defecto) |
| `docker stats` · `docker top nom` | Consumo · procesos |

### Volúmenes y redes

| Tipo | Sintaxis en run | Dónde vive |
|---|---|---|
| Anónimo | `-v /data` | `/var/lib/docker/volumes/<hash>` |
| Con nombre | `-v vol1:/data` | `/var/lib/docker/volumes/vol1` |
| Montado (bind) | `-v /opt/web:/data` | La carpeta del host, tal cual |
| Solo lectura | `-v /opt/web:/data:ro` | El contenedor no puede escribir |

| Comando | Qué hace |
|---|---|
| `docker volume create vol1` | Crea el volumen (el `--name` de las diapositivas sobra) |
| `docker volume ls` · `inspect vol1` | Lista · detalla (Mountpoint) |
| `docker volume rm vol1` | Lo borra (falla si un contenedor lo usa) |
| `docker volume prune` | Borra los volúmenes que no usa nadie |
| `docker network create red1` | Crea una red con DNS: los contenedores se ven por su **nombre** |
| `docker network ls` · `inspect red1` | Lista · qué contenedores tiene |
| `docker network connect red1 nom` | Conecta un contenedor que ya existe |

Un volumen con nombre que está vacío se llena con lo que la imagen tenga en esa ruta la primera vez. Una carpeta montada (bind) **tapa** lo que hubiera en la imagen.

### Dockerfile

| Instrucción | Para qué |
|---|---|
| `FROM img:tag [AS nom]` | Imagen base. La primera instrucción. Con `AS` nombras la etapa |
| `RUN cmd && cmd` | Ejecuta durante el build (cada RUN es una capa) |
| `COPY src dest/` | Copia del contexto. No admite `../` |
| `COPY --from=etapa /a /b` | Copia desde otra etapa (multi-stage) |
| `ADD src dest` | Como COPY, pero acepta URL y descomprime .tar. Mejor COPY |
| `WORKDIR /app` | Directorio para todo lo que viene después (lo crea) |
| `ENV CLAVE=valor` | Variable en el build y en el contenedor |
| `ARG nom=defecto` | Variable solo de build (`--build-arg nom=x`) |
| `EXPOSE 80` | Documenta el puerto. **No** lo publica (eso es `-p`) |
| `VOLUME /var/log` | Punto de montaje (crea un volumen anónimo) |
| `USER nom` | Usuario para RUN, CMD y ENTRYPOINT |
| `LABEL autor="x" version="1.0"` | Metadatos |
| `CMD ["exe","arg"]` | Comando por defecto. Solo cuenta el último |
| `ENTRYPOINT ["exe"]` | Ejecutable fijo. El CMD pasa a ser sus argumentos |

| Dockerfile | `run img` | `run img X` |
|---|---|---|
| `CMD ["date"]` | `date` | `X` |
| `ENTRYPOINT ["echo"]` `CMD ["Hola"]` | `echo Hola` | `echo X` |

Para cambiar el ENTRYPOINT: `docker run --entrypoint /bin/sh img`. La forma exec (`["a","b"]`) usa **comillas rectas** y **comas**. Las comillas tipográficas “ ” no funcionan.

| docker build | Para qué |
|---|---|
| `-t nom:tag` | Nombre (sin él, la imagen queda sin nombre) |
| `-f Dockerfile-alt` | Otro Dockerfile |
| `--build-arg x=1` | Valor de un `ARG` |
| `--no-cache` · `--pull` | Sin caché · vuelve a descargar el FROM |
| `--target etapa` | Para en esa etapa del multi-stage |
| `-q` · `--check` | Solo imprime el ID · revisa el Dockerfile sin construir |

**Plantilla: web estática (nginx)**

```dockerfile
FROM nginx:1.27-alpine
COPY index.html /usr/share/nginx/html/
EXPOSE 80
# Ruta en Apache (imagen httpd): /usr/local/apache2/htdocs/
```

**Plantilla: app Node**

```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

**Plantilla: Ubuntu instalando paquetes**

```dockerfile
FROM ubuntu:24.04
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*
EXPOSE 80
# en primer plano o el contenedor muere al arrancar
CMD ["nginx", "-g", "daemon off;"]
```

**Plantilla: multi-stage**

```dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

**Plantilla: app Python**

```dockerfile
FROM python:3.15
ENV HOST=0.0.0.0
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3", "app.py"]
```

**Subir una imagen a Docker Hub**

```bash
docker login -u <usuari>          # contraseña o token de acceso
docker build -t <usuari>/repo:1.0 .
docker push <usuari>/repo:1.0
# ya construida sin tu usuario delante:
docker tag repo:1.0 <usuari>/repo:1.0
```

Buenas prácticas: une los RUN parecidos con `&&`, borra `/var/lib/apt/lists/*` en el mismo RUN, fija la versión de la imagen base (`ubuntu:24.04` en vez de `latest`), usa un `.dockerignore` (`node_modules`, `.git`) y copia `package.json` antes que el resto del código para aprovechar la caché del `npm install`. En Alpine se usa `apk add --no-cache paquete`; en Debian y Ubuntu, `apt-get update && apt-get install -y paquete`.

### Docker Compose

**docker-compose.yml: plantilla completa**

```yaml
services:
  db:
    image: mysql:8.0
    container_name: db_contenidor
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: appdb
    volumes:
      - db_data:/var/lib/mysql            # con nombre
      - ./init:/docker-entrypoint-initdb.d  # carpeta del host
    ports:
      - "3306:3306"
    restart: always
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-proot"]
      interval: 5s
      retries: 20
    networks:
      - app_net

  web:
    build: ./web                 # carpeta con el Dockerfile
    image: web:1.0               # nombre de la imagen construida
    container_name: web_contenidor
    env_file: .env
    command: npm start
    ports:
      - "8080:3000"
    depends_on:
      db:
        condition: service_healthy   # espera a que esté "healthy"
    networks:
      - app_net

volumes:
  db_data:

networks:
  app_net:
```

| docker run | docker compose |
|---|---|
| `--name x` | `container_name: x` |
| `-p 80:80` | `ports: - "80:80"` |
| `-e A=1` | `environment: A: 1` |
| `--env-file f` | `env_file: f` |
| `-v vol:/d` | `volumes:` + `volumes:` de nivel superior |
| `--network red` | `networks:` + `networks:` de nivel superior |
| `--restart always` | `restart: always` |
| `-it` | `stdin_open: true` + `tty: true` |
| comando al final | `command: ...` |
| `--label run=11` | `labels: - "run=11"` |
| `--entrypoint` · `-w` | `entrypoint:` · `working_dir:` |
| `docker build -t w -f D .` | `build: {context: ., dockerfile: D}` + `image: w` |

| Comando | Qué hace |
|---|---|
| `docker compose up -d` | Crea y arranca todo en segundo plano |
| `docker compose up -d --build` | Reconstruye las imágenes antes (si cambiaste el Dockerfile) |
| `docker compose ps` · `logs -f web` | Estado · logs de un servicio |
| `docker compose exec web sh` | Shell dentro del servicio |
| `docker compose stop` · `start` | Para o arranca sin borrar |
| `docker compose down` | Borra contenedores y red. **No** borra volúmenes ni imágenes |
| `docker compose down -v --rmi all` | Borra también los volúmenes y las imágenes |
| `docker compose config` | Valida y enseña el YAML final (útil con overrides) |
| `-f base.yml -f pro.yml` | Combina ficheros: el segundo sobrescribe al primero |
| `-p nombre` | Nombre del proyecto (por defecto, el de la carpeta) |

> **Nombres en Compose.** Dentro de la red, cada servicio se encuentra por el **nombre del servicio** (`db`) y también por su `container_name`. Los volúmenes y las redes llevan delante el nombre del proyecto (`carpeta_db_data`). Si necesitas el nombre exacto, añade `name: nginxVol` dentro de su definición.
> **Red creada antes con `docker network create`:** declárala como `networks: {red: {external: true}}`.

### Si algo falla

| Síntoma | Causa y solución |
|---|---|
| El contenedor aparece como `Exited` nada más arrancar | Su proceso principal ha terminado. Mira `docker logs nom`. Un `ubuntu` sin `-it` muere enseguida; un servidor tiene que ir en primer plano (`nginx -g "daemon off;"`, `exec mysqld`). |
| `port is already allocated` | Otro contenedor o servicio usa ese puerto del host. Mira `docker ps`, para lo que lo ocupa (por ejemplo `sudo systemctl stop mysql`) o cambia el puerto del host. |
| `The container name "/x" is already in use` | Ya existe uno con ese nombre (quizá parado): `docker rm -f x`. |
| `pull access denied` · `repository does not exist` | El nombre de la imagen está mal escrito, o es tuya y todavía no la has construido. |
| Un contenedor no encuentra al otro | Tienen que estar en la misma red definida por ti (o en el mismo compose). Usa el nombre del contenedor o del servicio, nunca `localhost`. La red `bridge` por defecto no tiene DNS: ahí solo funciona la IP. |
| `permission denied` al ejecutar un script | Le falta el permiso de ejecución: `chmod +x script.sh` en el host o `RUN chmod +x` en el Dockerfile. |
| `no such file or directory` con un script que sí existe | En Alpine falta `bash` (`apk add --no-cache bash`), o el fichero tiene saltos de línea de Windows (CRLF). |
| Cambias el Dockerfile y no se nota | Reconstruye: `docker compose up -d --build` o `docker build --no-cache`. |
| El script de `docker-entrypoint-initdb.d` no se ejecuta | Solo se ejecuta si el volumen de datos está vacío. Bórralo con `docker compose down -v` y vuelve a levantar. |
| Compose avisa de `version is obsolete` | Es solo un aviso. Borra la línea `version:`. |
