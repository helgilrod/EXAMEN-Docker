# Trampas comprobadas

## Trampas

Las he comprobado una a una en Docker. Las primeras vienen de errores de las diapositivas; las demás, de las prácticas.

| Dónde | Lo que pone o parece | Lo que funciona |
|---|---|---|
| Tema 2 | `-n nom` · `-rm` | `--name nom` · `--rm` |
| Tema 3 | `docker commit nom_imatge nom_contenidor` | `docker commit contenedor imagen:tag` |
| Tema 4 | `CMD [“nginx”, “-g”, “daemon:off;”]` | `CMD ["nginx", "-g", "daemon off;"]` |
| Tema 4 | `apt-get install nginx` | `apt-get install -y nginx` (sin `-y` el build se para) |
| Tema 4 | `-t nom:tag.` · `–no-cache` | `-t nom:tag .` (con espacio) · `--no-cache` |
| Tema 4 | `CMD [“java” “-jar” ...]` | `CMD ["java", "-jar", "/opt/app.jar"]` |
| Tema 5 | `image:` dentro de `build:` | Error `additional properties 'image' not allowed`. Va al mismo nivel que `build:` |
| Tema 5 | `labels: - run: "11"` | Error `unexpected type map`. Usa `- "run=11"` o `run: "11"` sin guion |
| Tema 5 | "`down` borra volúmenes e imágenes" | Solo borra contenedores y redes. Añade `-v` y `--rmi all` |
| Tema 5 | `external: name: red` | Funciona, pero está obsoleto. Usa `name: red` + `external: true` |
| Tema 5 | `docker-compose` (v1) | En tu VM: `docker compose` (con espacio). La línea `version:` solo da un aviso |
| Tema 5 | `depends_on` "espera al servicio" | Solo espera a que el contenedor arranque. Para esperar a que esté listo: `wait-for-it` o `healthcheck` + `condition: service_healthy` |
| Práctica 4 | `mysql` + `--default-authentication-plugin=...` | `mysql:latest` (versión 26) muere con `unknown variable`. Usa `mysql:8.0` |
| Práctica 4 | `-v infoWordpress:/var/www/html` | Así crea un **volumen** llamado infoWordpress. Para la carpeta: `-v "$(pwd)/infoWordpress":/var/www/html` |
| Prácticas 3, 5 y 6 | Salir del contenedor con `exit` | Para el contenedor y todo lo que tenía en marcha. Sal con <kbd>Ctrl</kbd>+<kbd>P</kbd> <kbd>Ctrl</kbd>+<kbd>Q</kbd> |
| Práctica 3 | El contenedor creado con `commit` "ya tiene" los servidores | La imagen guarda `CMD /bin/bash`: arráncalos a mano (`service nginx start`, `httpd -k start`) |
| Práctica 6 | `npm install -g express` y `node index.js` | `Cannot find module 'express'`. Pasa `-e NODE_PATH=/usr/local/lib/node_modules` o haz `npm install` en el proyecto |
| Práctica 8 | `COPY my.conf /etc/mysql/conf.d/` con `bind-address=0.0.0.0` | MySQL ignora los ficheros que no son `.cnf`, y `mysql.conf.d/` se lee después. Pon `--bind-address=0.0.0.0` en el `mysqld` del script |
| Práctica 8 | `mysql -o ... XOU DATABASES` | `mysql -u ...` · `SHOW DATABASES;`. `-h localhost` usa el socket local: pon `-h 127.0.0.1` o `0.0.0.0` |
| Práctica 8 | `docker logs` sale vacío | El MySQL de Ubuntu escribe en `/var/log/mysql/error.log`: `docker exec nom grep "ready" /var/log/mysql/error.log` |
| Práctica 8 | "permisos de escritura" al script | Hace falta permiso de **ejecución**: `chmod +x` |
| Práctica 9 | `node:17-alpine` + Next.js actual | Next 14 o superior necesita Node 18 o más. Crea el proyecto con `create-next-app@13` |
| Práctica 9 | Proyecto `MultiStageExample` | npm no acepta mayúsculas: créalo en minúsculas y renombra la carpeta |
| Prestashop | `--name contenerdor_mysql` y `DB_SERVER=contenidor-mysql` | El enunciado tiene una errata: `DB_SERVER` tiene que ser **idéntico** al nombre del contenedor o del servicio |
| Práctica 12 | Puertos en la base y en el override | Los `ports` se **suman** (quedan los dos). Los volúmenes con el mismo destino se sustituyen |
| Práctica 12 | Levantar pre y pro a la vez | Sin `-p pre` / `-p pro`, el segundo `up` recrea el contenedor del primero |
| Práctica 15 | `host: "localhost"` en `src/db.js` | Dentro del contenedor web, localhost es él mismo: cámbialo a `database` |
| Prácticas 15 y 16 | `wait-for-it.sh` descargado | Llega sin permiso de ejecución y necesita bash: `chmod +x` y, en Alpine, `apk add bash` |
| Práctica 17 | `ENV HOST=0.0.0.0` "abre" la app | Solo sirve si `app.py` lee esa variable (`app.run(host=os.environ["HOST"])`). Si Flask escucha en 127.0.0.1, desde fuera no responde aunque pongas `-p` |
| Práctica 16 | El frontend llama a `http://backend:3000` | Si la llamada la hace el **navegador**, está fuera de Docker: usa `localhost:3000` (el puerto publicado) |
