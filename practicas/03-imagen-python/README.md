# Práctica 3 · Crea una imagen Docker de Python

> **Enunciado (Aules, "Crea imatge Docker Python"):** Crea una imatge Docker partint d'una imatge `python:3.15` a la qual heu d'executar el fitxer `app.py`. Recordeu que heu d'instal·lar les llibreries que hi han al `requirements.txt`. El Dockerfile ha de tenir una variable d'entorn anomenada `HOST=0.0.0.0`. Heu d'utilitzar `WORKDIR` també. Per a executar l'aplicació de python ho farem amb `python3 app.py`. Després creeu un repo en Docker Hub i pugeu la imatge.

**Ficheros de esta carpeta:** [`Dockerfile`](Dockerfile) · [`app.py`](app.py) · [`requirements.txt`](requirements.txt) · [`.dockerignore`](.dockerignore). El `app.py` es una web Flask de ejemplo: en la práctica se usan los ficheros del profesor.

Cambia `tuusuario` por tu usuario de Docker Hub.

## Paso a paso

### 1. Crear la carpeta y poner dentro los ficheros del profesor

```bash
mkdir -p ~/docker/python
cd ~/docker/python
cp ~/Descargas/app.py ~/Descargas/requirements.txt .
```

`cp a b .` copia los dos ficheros a la carpeta actual.

### 2. Mirar qué hace app.py: puerto y variable HOST

```bash
grep -n -E "Flask|HOST|port=|app.run|input\(" app.py
```

| Si sale… | Significa |
|---|---|
| `Flask` o `app.run` | Es una **web**: hay que publicar el puerto con `-p`. |
| `port=5000` | El puerto de la app: va en `EXPOSE` y a la derecha del `-p`. Si no pone ninguno, Flask usa el 5000. |
| `host=os.environ.get("HOST"...)` | La app lee la variable `HOST` del Dockerfile. Si **no** la lee, escucha solo dentro del contenedor y desde fuera no responde. |
| nada de lo anterior | Es un **script**: se ejecuta, imprime y termina (mira el paso 6B). |
| `input(` | Pide datos por teclado: hay que ejecutarlo con `-it`. |

Con el `app.py` de ejemplo, **deberías ver:**

```text
14:    # HOST ve del Dockerfile (ENV HOST=0.0.0.0). Si no el llig, Flask escolta en 127.0.0.1
16:    app.run(host=os.environ.get("HOST", "127.0.0.1"), port=5000)
```

### 3. Crear el Dockerfile

```bash
nano Dockerfile
```

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

| Línea | Qué significa |
|---|---|
| `FROM python:3.15` | Imagen oficial de Python 3.15. |
| `ENV HOST=0.0.0.0` | Crea la variable de entorno `HOST`. `0.0.0.0` = escuchar en todas las interfaces (así se puede entrar desde fuera del contenedor). |
| `WORKDIR /app` | Crea la carpeta `/app` y trabaja dentro: lo que viene después se hace ahí. |
| `COPY requirements.txt .` | Copia la lista de librerías a `/app`. |
| `RUN pip install --no-cache-dir -r requirements.txt` | Instala las librerías durante el build. `--no-cache-dir` no guarda la caché de pip (imagen más pequeña). |
| `COPY . .` | Copia todo lo de tu carpeta a `/app`. |
| `EXPOSE 5000` | Documenta el puerto. No lo publica: eso lo hace `-p`. |
| `CMD ["python3", "app.py"]` | El comando que se ejecuta al arrancar el contenedor. Comillas rectas y comas. |

`requirements.txt` se copia **antes** que el código por la caché: si solo cambias el código, Docker reutiliza la capa del `pip install` y el build es mucho más rápido. Si no hay `requirements.txt`, quita esas dos líneas.

### 4. Construir la imagen

```bash
docker build -t tuusuario/app-python:1.0 .
```

Con tu usuario delante ya se puede subir a Docker Hub sin `docker tag`. La primera vez tarda, porque `python:3.15` ocupa 1,65 GB.

### 5. Arrancar el contenedor (si es una web)

```bash
docker run -d --name app-python -p 5000:5000 tuusuario/app-python:1.0
```

`-p 5000:5000` = puerto de la VM : puerto de la app.

### 6A. Comprobar la web

```bash
docker logs app-python
curl http://localhost:5000
docker exec app-python printenv HOST
docker exec app-python pwd
```

**Deberías ver:**

```text
 * Running on all addresses (0.0.0.0)
Hola des de Python dins de Docker!
0.0.0.0
/app
```

| Comando | Qué comprueba |
|---|---|
| `docker logs` | Lo que ha escrito el contenedor. `all addresses (0.0.0.0)` = la app ha leído `HOST`. |
| `curl` / Firefox `localhost:5000` | Que la web responde (**haz captura**). |
| `docker exec … printenv HOST` | El valor de la variable del Dockerfile. |
| `docker exec … pwd` | El directorio de trabajo: el `WORKDIR`. |

Si `docker logs` pone `Running on http://127.0.0.1:5000` en lugar de `all addresses`, la app no lee `HOST` y desde fuera no responderá: lo he comprobado. Revisa el `app.run(host=...)`.

### 6B. Si app.py es un script que solo imprime

```bash
docker run --rm tuusuario/app-python:1.0
```

`--rm` borra el contenedor al acabar. El script imprime y termina. Por ejemplo, con este script:

```python
import os
import platform

nom = os.environ.get("NOM", "món")
print(f"Hola, {nom}!")
print(f"Python {platform.python_version()} dins d'un contenidor")
print("Suma 2 + 3 =", 2 + 3)
```

**Deberías ver:**

```text
Hola, món!
Python 3.15.2 dins d'un contenidor
Suma 2 + 3 = 5
```

- Si lo arrancas con `-d`, `docker ps -a` lo enseña como `Exited (0)`. Es **normal**: ha terminado bien. Lo que imprimió se ve con `docker logs nombre`.
- Si usa `input()` y lo ejecutas sin `-it`, da `EOFError: EOF when reading a line`. Ejecútalo con `docker run --rm -it ...`.
- Para un script no hacen falta `ENV HOST`, `EXPOSE` ni `-p`.

### 7. Crear el repositorio en Docker Hub (lo pide el enunciado)

hub.docker.com → **Repositories** → **Create a repository** → nombre `app-python` (en minúsculas) → **Public** → **Create**.

### 8. Subir la imagen

```bash
docker login -u tuusuario
docker push tuusuario/app-python:1.0
```

Termina con `1.0: digest: sha256:...`. Compruébalo en `hub.docker.com/r/tuusuario/app-python`, pestaña **Tags** (**haz captura**). Si da `denied`: falta tu usuario en el nombre o no has hecho login.

### 9. Limpiar

```bash
docker rm -f app-python
```

## Copia y pega

```text
PRÁCTICA 3 · IMAGEN DOCKER DE PYTHON (y subirla a Docker Hub)

1) Carpeta y ficheros del profesor
   mkdir -p ~/docker/python
   cd ~/docker/python
   cp ~/Descargas/app.py ~/Descargas/requirements.txt .
     cp a b . -> copia los dos ficheros a la carpeta actual

2) Mirar el puerto y si app.py lee HOST
   grep -n -E "Flask|HOST|port=|app.run|input\(" app.py
     grep -> busca texto dentro de un fichero (-n enseña el número de línea)
     port=5000 -> el puerto que va en EXPOSE y a la derecha del -p
     host=os.environ.get("HOST") -> la app lee la variable HOST (si no, desde fuera no responde)
     sin Flask/app.run -> es un script: imprime y termina

3) Dockerfile (nano Dockerfile)
     FROM python:3.15
     ENV HOST=0.0.0.0
     WORKDIR /app
     COPY requirements.txt .
     RUN pip install --no-cache-dir -r requirements.txt
     COPY . .
     EXPOSE 5000
     CMD ["python3", "app.py"]

     FROM python:3.15 -> imagen oficial de Python 3.15
     ENV HOST=0.0.0.0 -> variable de entorno HOST (0.0.0.0 = escuchar en todas las interfaces)
     WORKDIR /app     -> crea /app y trabaja dentro
     COPY requirements.txt . -> copia la lista de librerías
     RUN pip install -r requirements.txt -> instala las librerías en el build
     COPY . .         -> copia el resto del código
                         (requirements antes que el código = aprovecha la caché)
     EXPOSE 5000      -> documenta el puerto (no lo publica)
     CMD ["python3", "app.py"] -> lo que se ejecuta al arrancar el contenedor

4) Construir
   docker build -t tuusuario/app-python:1.0 .
     -t usuario/nombre:tag -> con el usuario ya se puede subir
     . -> la carpeta actual

5) Arrancar (web)
   docker run -d --name app-python -p 5000:5000 tuusuario/app-python:1.0
     -p 5000:5000 -> puerto de la VM : puerto de la app

6) Comprobar
   docker logs app-python               -> Running on all addresses (0.0.0.0)
   curl http://localhost:5000           -> Hola des de Python dins de Docker!
   docker exec app-python printenv HOST -> 0.0.0.0 (la variable del Dockerfile)
   docker exec app-python pwd           -> /app (el WORKDIR)
   Firefox: localhost:5000 (captura)
     docker logs -> lo que ha escrito el contenedor
     docker exec -> ejecuta un comando dentro del contenedor
   Si es un script: docker run --rm tuusuario/app-python:1.0 -> enseña lo que imprime
     Exited (0) en docker ps -a = terminó bien (es normal). Con input() hay que usar -it

7) Crear repositorio en Docker Hub
   hub.docker.com -> Repositories -> Create a repository -> app-python · Public -> Create

8) Subir
   docker login -u tuusuario
   docker push tuusuario/app-python:1.0
     Comprobar en hub.docker.com/r/tuusuario/app-python (Tags: 1.0)
```
