# Práctica 4 · Docker Compose: primeros pasos

> **Tarea de Aules: "Exercicis Docker Compose"** (PDF *Docker Compose — primers passos*). Cinco ejercicios para arrancar y parar contenidores con un fichero `compose.yaml` en lugar de escribir `docker run` largos. Se entrega un `respostes.txt` con las respuestas a las 10 preguntas.

**Ficheros de esta carpeta:** un `compose.yaml` por ejercicio ([ex1](ex1/compose.yaml), [ex2](ex2/compose.yaml), [ex3](ex3/compose.yaml), [ex4](ex4/compose.yaml), [ex5](ex5/compose.yaml)), el [index de ejemplo del ejercicio 4](ex4/web/index.html) y las [respuestas](respostes.txt).

Todo se ha ejecutado de verdad: las salidas de "Deberías ver" son las reales.

## Las 4 órdenes

| Orden | Qué hace |
|---|---|
| `docker compose up -d` | Crea y arranca los contenedores del `compose.yaml`, en segundo plano. |
| `docker compose ps` | Enseña los contenedores del proyecto en marcha. |
| `docker compose logs` | Enseña lo que han escrito los contenedores. |
| `docker compose down` | Para y **borra** los contenedores y la red del proyecto. |

Todas se ejecutan **dentro de la carpeta** donde está el `compose.yaml`. En YAML, los espacios del principio de cada línea importan: copia el fichero igual, con espacios y nunca con tabuladores.

> **Si el `curl` falla justo después del `up`** con `Connection reset by peer`, o sale vacío, es que el servidor todavía está arrancando. Espera 3 segundos y repítelo. Me pasó en la prueba.

---

## Ejercicio 1 · El primer contenedor con Compose

```bash
mkdir -p ~/compose/ex1
cd ~/compose/ex1
nano compose.yaml
```

```yaml
services:
  web:
    image: httpd:2.4
    ports:
      - "8080:80"
```

| Línea | Qué significa |
|---|---|
| `services:` | La lista de contenedores del proyecto. |
| `web:` | El nombre del servicio. Lo eliges tú. |
| `image: httpd:2.4` | La imagen: Apache 2.4. Equivale a la imagen del `docker run`. |
| `ports: - "8080:80"` | Puerto de tu máquina : puerto del contenedor. Equivale a `-p 8080:80`. |

```bash
docker compose up -d
curl http://localhost:8080
docker compose ps
docker compose down
```

**Deberías ver** con el `curl`:

```text
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<title>It works! Apache httpd</title>
</head>
<body>
<p>It works!</p>
</body>
</html>
```

Y con `docker compose ps`:

```text
NAME        IMAGE       COMMAND              SERVICE   CREATED         STATUS         PORTS
ex1-web-1   httpd:2.4   "httpd-foreground"   web       7 seconds ago   Up 3 seconds   0.0.0.0:8080->80/tcp
```

- **Pregunta 1:** sale la página por defecto de Apache, **"It works!"**.
- **Pregunta 2:** el contenedor se llama **`ex1-web-1`**. Compose lo nombra `<carpeta>-<servicio>-<número>`.

---

## Ejercicio 2 · Cambiar el puerto

```bash
cp -r ~/compose/ex1 ~/compose/ex2
cd ~/compose/ex2
nano compose.yaml
```

Cambia solo `"8080:80"` por `"8081:80"`. `cp -r` copia la carpeta entera, con lo que hay dentro.

```bash
docker compose up -d
curl http://localhost:8081
curl http://localhost:8080
docker compose down
```

**Deberías ver:** el 8081 enseña "It works!" y el 8080 da error:

```text
curl: (7) Failed to connect to localhost port 8080 after 0 ms: Couldn't connect to server
```

- **Pregunta 3:** el 8080 falla porque ya no hay nada escuchando ahí. Este contenedor publica el 8081, y el del ejercicio 1 lo paramos con `down`.
- **Pregunta 4:** en `"8081:80"`, el **8081** es el puerto de tu máquina y el **80** el del contenedor.

---

## Ejercicio 3 · Dos servidores a la vez

```bash
mkdir -p ~/compose/ex3
cd ~/compose/ex3
nano compose.yaml
```

```yaml
services:
  web1:
    image: httpd:2.4
    ports:
      - "8081:80"
  web2:
    image: nginx
    ports:
      - "8082:80"
```

Dos servicios en el mismo fichero: un Apache (`web1`) y un nginx (`web2`). Los dos escuchan en el 80 dentro de su contenedor, pero en tu máquina cada uno tiene un puerto distinto.

```bash
docker compose up -d
curl http://localhost:8081
curl http://localhost:8082
docker compose ps
docker compose down
```

**Deberías ver:** el 8081 enseña "It works!", el 8082 `<title>Welcome to nginx!</title>`, y `ps`:

```text
NAME         IMAGE       COMMAND                  SERVICE   STATUS         PORTS
ex3-web1-1   httpd:2.4   "httpd-foreground"       web1      Up 2 seconds   0.0.0.0:8081->80/tcp
ex3-web2-1   nginx       "/docker-entrypoint.…"   web2      Up 2 seconds   0.0.0.0:8082->80/tcp
```

- **Pregunta 5:** aparecen **2** contenedores, `ex3-web1-1` y `ex3-web2-1`.
- **Pregunta 6:** **no** enseñan la misma página. Apache saca "It works!" y nginx "Welcome to nginx!": cada imagen trae su propia página por defecto.

---

## Ejercicio 4 · Mi página web

```bash
mkdir -p ~/compose/ex4/web
cd ~/compose/ex4
cp ~/Descargas/index.html web/
nano compose.yaml
```

El `cp` pone el index de la tarea dentro de `web/`. Si la VM está en inglés, la carpeta de descargas es `~/Downloads`.

```yaml
services:
  web:
    image: httpd:2.4
    ports:
      - "8080:80"
    volumes:
      - ./web:/usr/local/apache2/htdocs
```

| Línea | Qué significa |
|---|---|
| `volumes:` | Lo que se monta dentro del contenedor. Equivale a `-v`. |
| `./web` | La carpeta `web` que está al lado del `compose.yaml`, en tu máquina. |
| `/usr/local/apache2/htdocs` | La carpeta que sirve Apache dentro del contenedor. |

```bash
docker compose up -d
curl http://localhost:8080
nano web/index.html
curl http://localhost:8080
docker compose down
```

El primer `curl` enseña la página de la tarea. Con el contenedor **en marcha**, cambia algún texto del `index.html`, guarda, y repite el `curl`: sale el texto nuevo. En la prueba:

```text
<h1>La meua pàgina amb Docker Compose</h1>      <- antes
<h1>He canviat el text amb Docker Compose</h1>  <- después, sin reiniciar nada
```

- **Pregunta 7:** **sí**, el cambio se ve enseguida y no hay que reiniciar nada. La carpeta está montada: Apache lee directamente los ficheros de tu máquina.
- **Pregunta 8:** monta la carpeta `./web` de tu máquina dentro del contenedor, en `/usr/local/apache2/htdocs`, que es la que enseña Apache. Lo que pongas en `web/` es lo que se ve en la página.

---

## Ejercicio 5 · Una base de datos con panel web

```bash
mkdir -p ~/compose/ex5
cd ~/compose/ex5
nano compose.yaml
```

```yaml
services:
  db:
    image: mariadb:11
    environment:
      MARIADB_ROOT_PASSWORD: arrel123
      MARIADB_DATABASE: botiga

  adminer:
    image: adminer
    ports:
      - "8090:8080"
```

| Línea | Qué significa |
|---|---|
| `db:` | El servicio de la base de datos, que se llama `db`. |
| `image: mariadb:11` | MariaDB versión 11. |
| `environment:` | Variables de entorno. Equivale a `-e`. |
| `MARIADB_ROOT_PASSWORD: arrel123` | La contraseña de root. Sin ella, MariaDB no arranca. |
| `MARIADB_DATABASE: botiga` | Crea la base de datos `botiga` la primera vez que arranca. |
| `adminer:` | El panel web para gestionar la base de datos. |
| `"8090:8080"` | Adminer escucha en el 8080 dentro; entras por el 8090. |

`db` no tiene `ports`: no hace falta, porque solo le habla Adminer, por dentro de la red que crea Compose.

```bash
docker compose up -d
```

Espera unos 20 segundos y comprueba con `docker compose ps` que salen **los dos** en `Up`.

> **Si `adminer` no aparece en `ps`** (se ha parado), mira `docker compose logs adminer`. Si pone `Failed to listen on [::]:8080`, la VM no tiene IPv6 (me pasó en la prueba). Añade esta línea en el servicio `adminer`, a la altura de `image:`, y haz otra vez `docker compose up -d`:
>
> ```yaml
>     command: php -S 0.0.0.0:8080 -t /var/www/html
> ```

**En el navegador:** abre `http://localhost:8090` si Firefox está dentro de la VM. Si entras desde fuera de la VM, usa la IP de la máquina, que te da `hostname -I`. En el formulario:

| Campo | Valor |
|---|---|
| Sistema | MySQL / MariaDB |
| Servidor | `db` |
| Usuario | `root` |
| Contraseña | `arrel123` |
| Base de datos | `botiga` |

Tras entrar, el título de la página es `Database: botiga - db - Adminer` (comprobado).

**Crear la tabla `productes`:** pulsa **Crear tabla** (*Create table*), ponle de nombre `productes` y añade dos columnas: `nom` de tipo `varchar` con longitud `100`, y `preu` de tipo `decimal` con longitud `10,2`. Después pulsa **Guardar** (*Save*). Haz captura.

También puedes crearla escribiendo SQL: **Comando SQL** (*SQL command*) → pega la sentencia → **Ejecutar**.

```sql
CREATE TABLE productes (nom VARCHAR(100), preu DECIMAL(10,2));
```

Para comprobarlo desde la terminal:

```bash
docker compose exec db mariadb -uroot -parrel123 botiga -e "DESCRIBE productes;"
```

```text
Field	Type	Null	Key	Default	Extra
nom	varchar(100)	YES		NULL
preu	decimal(10,2)	YES		NULL
```

Termina con `docker compose down`. Como no hay volumen, al hacer `down` la base de datos se borra.

- **Pregunta 9:** en "Servidor" ponemos **`db`**, que es el nombre del servicio de la base de datos en el `compose.yaml`. Compose crea una red para el proyecto y, dentro de ella, cada servicio se encuentra por su nombre.
- **Pregunta 10:** la línea **`MARIADB_DATABASE: botiga`**, dentro de `environment` del servicio `db`.

---

## Entrega

Sube a la tarea el fichero [`respostes.txt`](respostes.txt) con las 10 respuestas (en valenciano, listas para entregar).

## Copia y pega

```text
PRÁCTICA 4 · DOCKER COMPOSE: PRIMEROS PASOS

Órdenes (dentro de la carpeta del compose.yaml):
   docker compose up -d   -> crea y arranca los contenedores (en segundo plano)
   docker compose ps      -> contenedores en marcha
   docker compose logs    -> lo que han escrito
   docker compose down    -> para y borra contenedores y red
   YAML: espacios, nunca tabuladores. Si el curl falla justo tras el up: esperar 3 s y repetir

EX1 · mkdir -p ~/compose/ex1 && cd ~/compose/ex1 · nano compose.yaml
services:
  web:
    image: httpd:2.4
    ports:
      - "8080:80"
   services -> los contenedores · web -> nombre del servicio · image -> la imagen
   ports "8080:80" -> puerto de mi máquina : puerto del contenedor (= -p)
   up -d · curl localhost:8080 · ps · down
   P1: "It works!" (página por defecto de Apache)
   P2: ex1-web-1  (carpeta-servicio-número)

EX2 · cp -r ~/compose/ex1 ~/compose/ex2 && cd ~/compose/ex2 · cambiar 8080 por 8081
   up -d · curl localhost:8081 (It works!) · curl localhost:8080 (falla) · down
   P3: falla "Failed to connect ... Couldn't connect to server": nadie escucha en el 8080
       (este publica el 8081 y el de ex1 se paró con down)
   P4: 8081 = puerto de mi máquina · 80 = puerto del contenedor

EX3 · mkdir -p ~/compose/ex3 && cd ~/compose/ex3
services:
  web1:
    image: httpd:2.4
    ports:
      - "8081:80"
  web2:
    image: nginx
    ports:
      - "8082:80"
   dos servicios en el mismo fichero; cada uno con su puerto en mi máquina
   up -d · curl 8081 · curl 8082 · ps · down
   P5: 2 contenedores (ex3-web1-1 y ex3-web2-1)
   P6: no; Apache "It works!" y nginx "Welcome to nginx!" (cada imagen trae su página)

EX4 · mkdir -p ~/compose/ex4/web && cd ~/compose/ex4 · index.html de la tarea dentro de web/
services:
  web:
    image: httpd:2.4
    ports:
      - "8080:80"
    volumes:
      - ./web:/usr/local/apache2/htdocs
   volumes -> monta mi carpeta ./web en la carpeta que sirve Apache (= -v)
   up -d · curl · editar web/index.html SIN parar · curl otra vez · down
   P7: sí, el cambio se ve al momento sin reiniciar (la carpeta está montada)
   P8: monta ./web de mi máquina en /usr/local/apache2/htdocs: Apache enseña lo que hay en web/

EX5 · mkdir -p ~/compose/ex5 && cd ~/compose/ex5
services:
  db:
    image: mariadb:11
    environment:
      MARIADB_ROOT_PASSWORD: arrel123
      MARIADB_DATABASE: botiga

  adminer:
    image: adminer
    ports:
      - "8090:8080"
   environment -> variables (= -e) · MARIADB_ROOT_PASSWORD -> contraseña de root (obligatoria)
   MARIADB_DATABASE: botiga -> crea la base de datos botiga
   adminer -> panel web; "8090:8080" -> entro por el 8090
   up -d · esperar 20 s · ps (los dos en Up)
   Si adminer se para con "Failed to listen on [::]:8080" (sin IPv6), añadir en adminer:
       command: php -S 0.0.0.0:8080 -t /var/www/html
   Firefox localhost:8090 · Sistema MySQL · Servidor db · Usuario root · Contraseña arrel123 · BD botiga
   Crear tabla productes: nom varchar(100) · preu decimal(10,2) -> Guardar
     o Comando SQL: CREATE TABLE productes (nom VARCHAR(100), preu DECIMAL(10,2));
   down
   P9: "db" = el nombre del servicio en el compose.yaml (en la red de Compose se encuentran por nombre)
   P10: MARIADB_DATABASE: botiga

Entrega: respostes.txt con las 10 respuestas
```
