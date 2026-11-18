# Extra · Más ejercicios de Docker Compose

> **No es una tarea de Aules.** Son ejercicios de Compose de la lista de prácticas de clase: Prestashop + MySQL, añadir phpMyAdmin, y una configuración base con preproducción y producción. Sirven para practicar redes, variables y ficheros que se sobrescriben.

| Carpeta | Ejercicio | Puertos |
|---|---|---|
| [`a-prestashop`](a-prestashop/docker-compose.yml) | Prestashop + MySQL 5.7 en la red `prestashop-net` | 8080 (web), 3307 (MySQL) |
| [`b-phpmyadmin`](b-phpmyadmin/docker-compose.yml) | Lo mismo + phpMyAdmin | 9200 |
| [`c-entornos`](c-entornos/) | nginx base + preproducción + producción | 9003, 9004 |

---

## 5A · Prestashop + MySQL 5.7

**Enunciado:** pasar a un `docker-compose.yml` estos tres comandos:

```bash
docker network create prestashop-net
docker run -it --name contenidor_mysql --network prestashop-net -e MYSQL_ROOT_PASSWORD=admin -p 3307:3306 -d mysql:5.7
docker run -it --name contenidor_prestashop --network prestashop-net -e DB_SERVER=contenidor_mysql -p 8080:80 -d prestashop/prestashop
```

> **Errata del enunciado:** el original llama al contenedor `contenerdor_mysql` y luego pone `DB_SERVER=contenidor-mysql`. `DB_SERVER` tiene que ser **idéntico** al nombre del contenedor de MySQL; si no, Prestashop no encuentra la base de datos. Aquí los dos son `contenidor_mysql`.

### 1. Carpeta

```bash
mkdir -p ~/docker/prestashop
cd ~/docker/prestashop
```

### 2. docker-compose.yml

```yaml
services:
  mysql:
    image: mysql:5.7
    container_name: contenidor_mysql
    environment:
      MYSQL_ROOT_PASSWORD: admin
    ports:
      - "3307:3306"
    networks:
      - prestashop-net
    stdin_open: true
    tty: true

  prestashop:
    image: prestashop/prestashop
    container_name: contenidor_prestashop
    environment:
      DB_SERVER: contenidor_mysql
    ports:
      - "8080:80"
    networks:
      - prestashop-net
    depends_on:
      - mysql
    stdin_open: true
    tty: true

networks:
  prestashop-net:
    name: prestashop-net
```

| En el `docker run` | En el compose |
|---|---|
| `docker network create prestashop-net` | `networks:` abajo del todo, y `networks: - prestashop-net` en cada servicio |
| `--name contenidor_mysql` | `container_name: contenidor_mysql` |
| `-e MYSQL_ROOT_PASSWORD=admin` | `environment: MYSQL_ROOT_PASSWORD: admin` |
| `-p 3307:3306` | `ports: - "3307:3306"` |
| `--network prestashop-net` | `networks: - prestashop-net` |
| `-it` | `stdin_open: true` + `tty: true` |
| `-d` | No se pone: es el `-d` de `docker compose up -d` |
| (orden de arranque) | `depends_on: - mysql`: arranca Prestashop después de MySQL |

- `name: prestashop-net` hace que la red se llame exactamente así; sin él se llamaría `carpeta_prestashop-net`.
- `DB_SERVER` le dice a Prestashop dónde está la base de datos. La contraseña que usa por defecto (`DB_PASSWD`) es `admin`: por eso root tiene `admin`.

### 3. Levantar y comprobar

```bash
docker compose up -d
docker compose ps
docker network ls | grep prestashop
docker compose logs -f prestashop
```

- `ps` tiene que enseñar `contenidor_mysql` y `contenidor_prestashop` en `Up`.
- En `logs -f` espera a ver `resuming normal operations` y sal con <kbd>Ctrl</kbd>+<kbd>C</kbd> (no para nada).

### 4. Instalar Prestashop en el navegador

`http://localhost:8080` te lleva al instalador (`/install`). En el paso de la base de datos pon: servidor `contenidor_mysql`, base de datos `prestashop`, usuario `root`, contraseña `admin` (**haz captura**). Si al final te pide borrar la carpeta install:

```bash
docker exec contenidor_prestashop rm -rf /var/www/html/install
```

---

## 5B · Añadir phpMyAdmin en el puerto 9200

Dentro de `services:` del compose anterior (después de `prestashop` y antes del `networks:` de abajo), añade este servicio. Tiene que empezar con 2 espacios, como `mysql:` y `prestashop:`. El fichero completo está en [`b-phpmyadmin/docker-compose.yml`](b-phpmyadmin/docker-compose.yml).

```yaml
  phpmyadmin:
    image: phpmyadmin
    container_name: contenidor_phpmyadmin
    environment:
      PMA_HOST: contenidor_mysql
    ports:
      - "9200:80"
    networks:
      - prestashop-net
    depends_on:
      - mysql
```

| Clave | Qué significa |
|---|---|
| `PMA_HOST` | El servidor MySQL al que se conecta phpMyAdmin. Tiene que estar en la misma red. |
| `"9200:80"` | phpMyAdmin escucha en el 80 dentro; se entra por el 9200. |

```bash
docker compose config -q
docker compose up -d
```

`config -q` no escribe nada si el fichero está bien. `up -d` solo crea phpMyAdmin; los otros servicios siguen igual.

En `http://localhost:9200` entra con el usuario `root` y la contraseña `admin`. A la izquierda verás la base de datos `prestashop` con sus tablas `ps_...` (**haz captura**). Para limpiar: `docker compose down -v`.

---

## 5C · Base + preproducción + producción

**Enunciado:** un `docker-compose.yml` base con nginx y dos ficheros más, `docker-compose.pre.yml` (puerto 9003, carpeta `PREPRO`) y `docker-compose.pro.yml` (puerto 9004, carpeta `PRO`), que lo sobrescriben.

### 1. Carpetas y los tres index

```bash
mkdir -p ~/docker/entornos/html/PREPRO ~/docker/entornos/html/PRO
cd ~/docker/entornos
echo '<h1>NGINX - CONFIGURACIÓN BASE</h1>' > html/index.html
echo '<h1>NGINX - CONFIGURACIÓN PREPRODUCCIÓN</h1>' > html/PREPRO/index.html
echo '<h1>NGINX - CONFIGURACIÓN PRODUCCIÓN</h1>' > html/PRO/index.html
```

### 2. Los tres ficheros de Compose

`docker-compose.yml`, la base:

```yaml
services:
  web:
    image: nginx
    volumes:
      - ./html:/usr/share/nginx/html
```

`docker-compose.pre.yml`:

```yaml
services:
  web:
    ports:
      - "9003:80"
    volumes:
      - ./html/PREPRO:/usr/share/nginx/html
```

`docker-compose.pro.yml`:

```yaml
services:
  web:
    ports:
      - "9004:80"
    volumes:
      - ./html/PRO:/usr/share/nginx/html
```

- La **base** lleva lo común a todos los entornos (la imagen). No lleva `ports` a propósito: al combinar ficheros, los puertos se **suman** (quedarían los dos), no se reemplazan. Lo he comprobado.
- **pre** y **pro** solo llevan lo que cambia: el puerto y la carpeta.
- `./html/PREPRO:/usr/share/nginx/html` = carpeta de la VM : carpeta web de nginx. Como monta en la misma ruta que la base, la **sustituye**.

### 3. Ver cómo queda el fichero combinado

```bash
docker compose -f docker-compose.yml -f docker-compose.pre.yml config
```

`-f` indica qué ficheros usar; el segundo sobrescribe al primero. `config` enseña el resultado: la carpeta `PREPRO` y el puerto `9003`.

### 4. Levantar los dos entornos a la vez

```bash
docker compose -p pre -f docker-compose.yml -f docker-compose.pre.yml up -d
docker compose -p pro -f docker-compose.yml -f docker-compose.pro.yml up -d
```

`-p pre` y `-p pro` dan un nombre de proyecto distinto a cada entorno. Sin `-p`, el segundo `up` sustituye al primero, porque son el mismo proyecto: también lo he comprobado.

### 5. Comprobar

```bash
docker ps
curl http://localhost:9003
curl http://localhost:9004
```

**Deberías ver:** `pre-web-1` en el 9003 y `pro-web-1` en el 9004, y después:

```text
<h1>NGINX - CONFIGURACIÓN PREPRODUCCIÓN</h1>
<h1>NGINX - CONFIGURACIÓN PRODUCCIÓN</h1>
```

Haz captura en Firefox de los dos.

### 6. Parar cada entorno

```bash
docker compose -p pre -f docker-compose.yml -f docker-compose.pre.yml down
docker compose -p pro -f docker-compose.yml -f docker-compose.pro.yml down
```

---

## Copia y pega

```text
EXTRA · MÁS EJERCICIOS DE DOCKER COMPOSE

---- 5A · PRESTASHOP + MYSQL 5.7 ----
mkdir -p ~/docker/prestashop && cd ~/docker/prestashop
docker-compose.yml:
services:
  mysql:
    image: mysql:5.7
    container_name: contenidor_mysql
    environment:
      MYSQL_ROOT_PASSWORD: admin
    ports:
      - "3307:3306"
    networks:
      - prestashop-net
    stdin_open: true
    tty: true

  prestashop:
    image: prestashop/prestashop
    container_name: contenidor_prestashop
    environment:
      DB_SERVER: contenidor_mysql
    ports:
      - "8080:80"
    networks:
      - prestashop-net
    depends_on:
      - mysql
    stdin_open: true
    tty: true

networks:
  prestashop-net:
    name: prestashop-net

   container_name -> = --name · environment -> = -e · ports -> = -p · networks -> = --network
   stdin_open + tty -> = -it · depends_on -> arranca después de mysql
   networks (abajo) -> = docker network create · name -> nombre exacto de la red
   DB_SERVER = IGUAL que el container_name de MySQL (el enunciado tiene una errata)
docker compose up -d
docker compose ps                    -> los dos en Up
docker compose logs -f prestashop    -> "resuming normal operations" (Ctrl+C para salir)
Firefox localhost:8080 -> instalador: servidor contenidor_mysql · bd prestashop · root / admin

---- 5B · PHPMYADMIN (9200) ----
Añadir dentro de services (2 espacios delante):
  phpmyadmin:
    image: phpmyadmin
    container_name: contenidor_phpmyadmin
    environment:
      PMA_HOST: contenidor_mysql
    ports:
      - "9200:80"
    networks:
      - prestashop-net
    depends_on:
      - mysql
   PMA_HOST -> el MySQL al que se conecta (misma red)
docker compose config -q   -> sin salida = fichero bien
docker compose up -d       -> solo crea phpmyadmin
Firefox localhost:9200 -> root / admin
docker compose down -v

---- 5C · BASE + PRE + PRO ----
mkdir -p ~/docker/entornos/html/PREPRO ~/docker/entornos/html/PRO && cd ~/docker/entornos
echo '<h1>NGINX - CONFIGURACIÓN BASE</h1>' > html/index.html
echo '<h1>NGINX - CONFIGURACIÓN PREPRODUCCIÓN</h1>' > html/PREPRO/index.html
echo '<h1>NGINX - CONFIGURACIÓN PRODUCCIÓN</h1>' > html/PRO/index.html
docker-compose.yml (base):
services:
  web:
    image: nginx
    volumes:
      - ./html:/usr/share/nginx/html
docker-compose.pre.yml:
services:
  web:
    ports:
      - "9003:80"
    volumes:
      - ./html/PREPRO:/usr/share/nginx/html
docker-compose.pro.yml:
services:
  web:
    ports:
      - "9004:80"
    volumes:
      - ./html/PRO:/usr/share/nginx/html
   base sin ports: en los overrides los ports se SUMAN · volúmenes en la misma ruta se SUSTITUYEN
docker compose -f docker-compose.yml -f docker-compose.pre.yml config   -> ver el resultado combinado
docker compose -p pre -f docker-compose.yml -f docker-compose.pre.yml up -d
docker compose -p pro -f docker-compose.yml -f docker-compose.pro.yml up -d
   -f -> qué ficheros (el segundo sobrescribe) · -p -> nombre de proyecto (sin él, pro sustituye a pre)
curl localhost:9003 -> PREPRODUCCIÓN · curl localhost:9004 -> PRODUCCIÓN
docker compose -p pre -f docker-compose.yml -f docker-compose.pre.yml down   (igual con pro)
```
