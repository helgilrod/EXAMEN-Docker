# Examen · Descargar una imagen y hacerla funcionar

> **Lo que piden:** te dan el nombre de una imagen (nginx, httpd, mysql…). Hay que descargarla, hacerla funcionar, decir qué comandos se usan y entrar por el puerto que se le asigna para ver el resultado.

## Paso a paso (ejemplo con nginx)

### 1. Buscarla

```bash
docker search nginx
```

```text
NAME                              DESCRIPTION                                     STARS     OFFICIAL
nginx                             Official build of Nginx.                        21422     [OK]
nginx/nginx-ingress               NGINX and  NGINX Plus Ingress Controllers fo…   124
```

La que pone `[OK]` en OFFICIAL es la oficial. Su página en hub.docker.com explica el puerto y las variables que necesita.

### 2. Descargarla

```bash
docker pull nginx
```

```text
Using default tag: latest
latest: Pulling from library/nginx
```

Sin etiqueta descarga `latest`. Para una versión concreta: `docker pull nginx:1.27`.

### 3. Comprobar que la tienes

```bash
docker images
```

### 4. Averiguar en qué puerto escucha por dentro

```bash
docker image inspect -f '{{.Config.ExposedPorts}}' nginx
```

```text
map[80/tcp:{}]
```

Ese 80 es el que va a la **derecha** del `-p`.

### 5. Arrancarla publicando el puerto

```bash
docker run -d --name web -p 8080:80 nginx
```

| Parte | Qué significa |
|---|---|
| `-d` | En segundo plano. |
| `--name web` | El nombre del contenedor. |
| `-p 8080:80` | Puerto de la VM : puerto del contenedor. |
| `nginx` | La imagen. |

Con puerto aleatorio: `docker run -d --name web -P nginx` (P mayúscula).

### 6. Comprobar que sigue en marcha

```bash
docker ps
```

Si no aparece, se ha parado: `docker ps -a` lo enseña como `Exited (1)` y `docker logs web` dice por qué.

### 7. Ver qué puerto tiene asignado

```bash
docker port web
```

```text
80/tcp -> 0.0.0.0:8080
```

Con `-P` (aleatorio) salió, por ejemplo, `80/tcp -> 0.0.0.0:32768`. El número de la derecha es el que pones en el navegador. También sale en la columna PORTS de `docker ps`.

### 8. Entrar por ese puerto

En Firefox, `http://localhost:8080` (o el que te diera `docker port`). Con nginx sale **Welcome to nginx!**; con httpd, **It works!** (**haz captura**).

### 9. Respuesta: qué comandos he usado

```bash
docker search nginx                          # buscar la imagen
docker pull nginx                            # descargarla (latest)
docker images                                # comprobar que está
docker run -d --name web -p 8080:80 nginx    # crear y arrancar el contenedor
docker ps                                    # comprobar que está en marcha
docker port web                              # ver el puerto asignado
docker logs web                              # ver su salida si algo falla
# navegador: http://localhost:8080
```

## Imágenes más probables (todas probadas)

| Imagen | Puerto interno | Variables obligatorias | `docker run` | Cómo comprobarlo |
|---|---|---|---|---|
| `nginx` | 80 | — | `docker run -d --name web -p 8080:80 nginx` | Navegador: **Welcome to nginx!** |
| `httpd` | 80 | — | `docker run -d --name apache -p 8081:80 httpd` | Navegador: **It works!** |
| `tomcat` | 8080 | — | `docker run -d --name tomcat -p 8888:8080 tomcat` | Da 404 al principio (ver abajo). Después, página de Tomcat |
| `mysql:8.0` | 3306 | `MYSQL_ROOT_PASSWORD` | `docker run -d --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=1234 mysql:8.0` | `docker exec -it mysql mysql -uroot -p1234 -e "SHOW DATABASES;"` |
| `mariadb` | 3306 | `MARIADB_ROOT_PASSWORD` | `docker run -d --name mariadb -p 3307:3306 -e MARIADB_ROOT_PASSWORD=1234 mariadb` | `docker exec -it mariadb mariadb -uroot -p1234 -e "SELECT VERSION();"` |
| `postgres` | 5432 | `POSTGRES_PASSWORD` | `docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=1234 postgres` | `docker exec -it postgres psql -U postgres -c "SELECT version();"` |
| `mongo` | 27017 | — | `docker run -d --name mongo -p 27017:27017 mongo` | `docker exec -it mongo mongosh --eval "db.runCommand({ping: 1})"` → `{ ok: 1 }` |
| `redis` | 6379 | — | `docker run -d --name redis -p 6379:6379 redis` | `docker exec -it redis redis-cli ping` → `PONG` |
| `phpmyadmin` | 80 | `PMA_HOST` (el MySQL) | `docker run -d --name phpmyadmin --network red-db -p 8082:80 -e PMA_HOST=mysql phpmyadmin` | Navegador: login (root / 1234) |

## Errores típicos (mensajes reales)

- **Base de datos sin su variable:** el contenedor se para con `Exited (1)`. `docker logs` dice, con mysql: `[ERROR] [Entrypoint]: Database is uninitialized and password option is not specified`. Con postgres: `Error: Database is uninitialized and superuser password is not specified. You must specify POSTGRES_PASSWORD`. Solución: `docker rm -f nombre` y repetir el run con `-e`.
- **Tomcat da 404:** la imagen trae la carpeta `webapps` vacía. Copia las aplicaciones de ejemplo y espera unos 10 segundos: `docker exec tomcat sh -c 'cp -r webapps.dist/* webapps/'`.
- **phpMyAdmin o WordPress no encuentran el MySQL:** tienen que estar en la misma red. Crea antes `docker network create red-db` y arranca los dos contenedores con `--network red-db`.
- **Si piden persistencia,** monta un volumen en la carpeta de datos: mysql y mariadb `/var/lib/mysql`; postgres `/var/lib/postgresql`; mongo `/data/db`; redis `/data`. Por ejemplo: `-v mysqlVol:/var/lib/mysql`.

## Copia y pega

```text
EXAMEN · DESCARGAR UNA IMAGEN, HACERLA FUNCIONAR Y ENTRAR POR SU PUERTO

   docker search nginx                          -> buscar la imagen ([OK] = oficial)
   docker pull nginx                            -> descargarla (sin tag = latest)
   docker images                                -> comprobar que está
   docker image inspect -f '{{.Config.ExposedPorts}}' nginx   -> map[80/tcp:{}] = escucha en el 80
   docker run -d --name web -p 8080:80 nginx    -> crear y arrancar el contenedor
   docker ps                                    -> comprobar que está en Up
   docker port web                              -> 80/tcp -> 0.0.0.0:8080 (el puerto asignado)
   Firefox: http://localhost:8080               -> entrar por ese puerto
   docker logs web                              -> ver qué pasa si algo falla

Puerto aleatorio: docker run -d --name web -P nginx   (P mayúscula)
   docker port web -> 80/tcp -> 0.0.0.0:32768 -> entrar por localhost:32768

Si se para nada más arrancar (Exited (1)): docker logs nombre
   bases de datos -> falta la contraseña: docker rm -f nombre y repetir el run con -e
   mysql    -e MYSQL_ROOT_PASSWORD=1234
   mariadb  -e MARIADB_ROOT_PASSWORD=1234
   postgres -e POSTGRES_PASSWORD=1234
Tomcat da 404: docker exec tomcat sh -c 'cp -r webapps.dist/* webapps/'  y esperar 10 s
```
