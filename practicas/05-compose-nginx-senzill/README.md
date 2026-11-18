# Práctica 5 · Docker Compose: nginx sencillo

> **Enunciado (Aules, "Docker-Compose - Nginx senzill"):** Utilitzant Docker-compose, crea una imatge basada en una de Nginx. A més, deurà exposar el port 80 i utilitzar un volum nomenat `nginxVol` que s'associarà amb el directori `/usr/share/nginx/html`.

**Ficheros de esta carpeta:** [`Dockerfile`](Dockerfile) · [`docker-compose.yml`](docker-compose.yml)

## Paso a paso

### 1. Crear la carpeta y entrar

```bash
mkdir -p ~/docker/compose-nginx
cd ~/docker/compose-nginx
```

El nombre de la carpeta es el nombre del **proyecto** de Compose: se pone delante del nombre del volumen y de la red.

### 2. Crear el Dockerfile

```bash
nano Dockerfile
```

```dockerfile
FROM nginx:1.27-alpine
EXPOSE 80
```

| Línea | Qué significa |
|---|---|
| `FROM nginx:1.27-alpine` | Imagen oficial de nginx, en su versión Alpine (más pequeña). |
| `EXPOSE 80` | Documenta que escucha en el 80. |

### 3. Crear docker-compose.yml

```bash
nano docker-compose.yml
```

Se indenta con **espacios**, nunca con tabulador: cada nivel lleva 2 espacios más.

```yaml
services:
  web:
    build: .
    image: nginx-compose:1.0
    container_name: nginx_compose
    ports:
      - "80:80"
    volumes:
      - nginxVol:/usr/share/nginx/html

volumes:
  nginxVol:
```

| Clave | Qué significa | Equivale en `docker run` a |
|---|---|---|
| `services:` | La lista de contenedores del proyecto. | — |
| `web:` | El nombre del servicio (lo eliges tú). | — |
| `build: .` | Construye la imagen con el Dockerfile de esta carpeta. | `docker build .` |
| `image: nginx-compose:1.0` | El nombre de la imagen construida. | `-t nginx-compose:1.0` |
| `container_name:` | El nombre del contenedor. | `--name` |
| `ports: - "80:80"` | Puerto de la VM : puerto del contenedor. | `-p 80:80` |
| `volumes: - nginxVol:/usr/share/nginx/html` | Monta el volumen en la carpeta web de nginx. | `-v nginxVol:/usr/share/nginx/html` |
| `volumes: nginxVol:` (abajo del todo) | Declara el volumen con nombre; Compose lo crea. | `docker volume create` |

Sin Dockerfile también vale: cambia `build: .` por `image: nginx`.

### 4. Validar el fichero

```bash
docker compose config
```

Si está bien, enseña el fichero completo. Si hay un error, te dice la línea; casi siempre es la indentación.

### 5. Levantarlo

```bash
docker compose up -d --build
```

| Parte | Qué significa |
|---|---|
| `up` | Crea la red, el volumen y el contenedor, y lo arranca. |
| `-d` | En segundo plano. |
| `--build` | Construye la imagen antes de arrancar. |

**Deberías ver:**

```text
 Volume compose-nginx_nginxVol Created
 Network compose-nginx_default Created
 Container nginx_compose Created
 Container nginx_compose Started
```

Si el 80 está ocupado en la VM (por ejemplo, porque hay un Apache instalado), cambia a `"8080:80"` y entra por `localhost:8080`.

### 6. Comprobar

```bash
docker compose ps
docker volume ls
```

**Deberías ver:**

```text
NAME            IMAGE               SERVICE   STATUS         PORTS
nginx_compose   nginx-compose:1.0   web       Up 3 seconds   0.0.0.0:80->80/tcp

DRIVER    VOLUME NAME
local     compose-nginx_nginxVol
```

El volumen lleva delante el nombre de la carpeta. Para que se llame exactamente `nginxVol`, añade debajo de `nginxVol:` (al final del fichero) una línea `    name: nginxVol`.

En Firefox, `http://localhost` enseña **Welcome to nginx!** (**haz captura**).

### 7. Demostrar que el volumen guarda los datos

```bash
docker compose exec web sh -c 'echo "<h1>Hola des del volum</h1>" > /usr/share/nginx/html/index.html'
docker compose down
docker compose up -d
curl http://localhost
```

**Deberías ver:** `<h1>Hola des del volum</h1>`

- `exec web sh -c '...'` ejecuta un comando dentro del servicio `web`; aquí, cambiar el index.
- `down` borra el contenedor y la red, pero **no** el volumen. Por eso, al volver a levantarlo, el cambio sigue ahí.

### 8. Limpiar todo, volumen incluido

```bash
docker compose down -v
```

`-v` borra también los volúmenes.

## Copia y pega

```text
PRÁCTICA 5 · DOCKER COMPOSE: NGINX SENCILLO

1) Carpeta
   mkdir -p ~/docker/compose-nginx
   cd ~/docker/compose-nginx
     el nombre de la carpeta = nombre del proyecto de Compose

2) Dockerfile
     FROM nginx:1.27-alpine
     EXPOSE 80
       FROM -> imagen oficial de nginx (Alpine = pequeña) · EXPOSE 80 -> documenta el puerto

3) docker-compose.yml (indentar con ESPACIOS)
services:
  web:
    build: .
    image: nginx-compose:1.0
    container_name: nginx_compose
    ports:
      - "80:80"
    volumes:
      - nginxVol:/usr/share/nginx/html

volumes:
  nginxVol:

     services       -> los contenedores del proyecto
     web            -> nombre del servicio
     build: .       -> construye con el Dockerfile de aquí (= docker build .)
     image          -> nombre de la imagen construida
     container_name -> nombre del contenedor (= --name)
     ports "80:80"  -> puerto de la VM : puerto del contenedor (= -p 80:80)
     volumes (en el servicio) -> monta nginxVol en la carpeta web de nginx (= -v)
     volumes (abajo) -> declara el volumen con nombre

4) Validar:   docker compose config
5) Levantar:  docker compose up -d --build
     up -> crea red, volumen y contenedor y arranca · -d segundo plano · --build construye antes
6) Comprobar:
   docker compose ps   -> nginx_compose Up 0.0.0.0:80->80/tcp
   docker volume ls    -> compose-nginx_nginxVol (prefijo = carpeta; "name: nginxVol" para el nombre exacto)
   Firefox localhost   -> Welcome to nginx! (captura)
7) Persistencia:
   docker compose exec web sh -c 'echo "<h1>Hola des del volum</h1>" > /usr/share/nginx/html/index.html'
   docker compose down     -> borra contenedor y red, NO el volumen
   docker compose up -d
   curl http://localhost   -> <h1>Hola des del volum</h1>
8) Limpiar:   docker compose down -v   (-v borra también el volumen)
```
