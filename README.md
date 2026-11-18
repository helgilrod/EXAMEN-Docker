# EXAMEN Docker

Apuntes y prácticas para el examen práctico de Docker. Todo está explicado paso a paso: qué escribir, qué significa cada parte y qué deberías ver. Cada práctica termina con un bloque para copiar y pegar como chuleta.

Las soluciones se han ejecutado de verdad con Docker 29 y Docker Compose v2 (`docker compose`, con espacio). Las salidas que aparecen como "Deberías ver" son reales.

## Qué entra en el examen

| Parte | Qué piden | Dónde está |
|---|---|---|
| 1 | Imagen de nginx/Apache con Dockerfile → ejecutarla → comprobarla → subirla a Docker Hub → código a GitHub | [Práctica 1](practicas/01-imagen-apache/) y [Práctica 2](practicas/02-imagenes-dockerhub/) |
| 2 | Dockerfile de Python que funcione y ver lo que devuelve | [Práctica 3](practicas/03-imagen-python/) |
| 3 | Descargar una imagen, hacerla funcionar, decir los comandos y entrar por su puerto | [Examen: imagen descargada](practicas/06-examen-imagen-descargada/) |
| 4 | Docker Compose | [Práctica 4](practicas/04-compose-exercicis-basics/) y [Práctica 5](practicas/05-compose-nginx-senzill/) |
| 5 | Preguntas de teoría ("¿qué comando usarías para…?") | [Preguntas de teoría](apuntes/preguntas-teoria.md) |

## Prácticas paso a paso

| Carpeta | Práctica (tarea de Aules) |
|---|---|
| [`practicas/01-imagen-apache`](practicas/01-imagen-apache/) | Crear una imagen de un contenedor Apache (`la-meua-web:v1`, puerto 4000) y subirla a Docker Hub |
| [`practicas/02-imagenes-dockerhub`](practicas/02-imagenes-dockerhub/) | Crea imágenes en Docker Hub: 4 imágenes (nginx/Apache, Alpine/Debian), Docker Hub y GitHub |
| [`practicas/03-imagen-python`](practicas/03-imagen-python/) | Crea una imagen Docker de Python (`python:3.15`, `HOST=0.0.0.0`, `WORKDIR`) y súbela |
| [`practicas/04-compose-exercicis-basics`](practicas/04-compose-exercicis-basics/) | Exercicis Docker Compose: 5 ejercicios básicos (httpd, puertos, dos servidores, volumen, MariaDB + Adminer) y las 10 respuestas |
| [`practicas/05-compose-nginx-senzill`](practicas/05-compose-nginx-senzill/) | Docker Compose - Nginx senzill: nginx con el volumen `nginxVol` |
| [`practicas/06-examen-imagen-descargada`](practicas/06-examen-imagen-descargada/) | Examen: descargar una imagen y hacerla funcionar (nginx, httpd, mysql, postgres…) |
| [`practicas/extra-compose-prestashop-entornos`](practicas/extra-compose-prestashop-entornos/) | Extra (no es de Aules): Prestashop + MySQL, phpMyAdmin y entornos pre/pro |

Cada carpeta tiene un `README.md` con los pasos y los ficheros ya probados (Dockerfile, docker-compose.yml, app.py…).

## Apuntes

| Fichero | Qué tiene |
|---|---|
| [Chuleta de comandos](apuntes/chuleta-comandos.md) | Imágenes, `docker run`, contenedores, volúmenes y redes, Dockerfile, Compose y "si algo falla" |
| [Trampas](apuntes/trampas.md) | Los errores de las diapositivas y de las prácticas que hacen fallar un ejercicio |
| [Preguntas de teoría](apuntes/preguntas-teoria.md) | 67 preguntas con la respuesta escondida (pulsa para verla) |
| [Curso de pabpereza](apuntes/pabpereza/) | Capítulos 1 a 12 (sin el 11) del Curso de Docker de pabpereza |
| [`chuleta-docker.html`](apuntes/chuleta-docker.html) | Todo lo anterior en una página para descargar, abrir en el navegador e imprimir |

## Cómo estudiar con esto

1. Haz las prácticas 1 a 5 en la máquina virtual, siguiendo su README. La 4 tiene las respuestas para entregar en `respostes.txt`.
2. Repasa la [chuleta](apuntes/chuleta-comandos.md) y las [trampas](apuntes/trampas.md).
3. Pregúntate la [teoría](apuntes/preguntas-teoria.md) sin abrir las respuestas.
4. Practica la [parte 3](practicas/06-examen-imagen-descargada/) con imágenes distintas: nginx, httpd, mysql, postgres.
5. Para el examen, imprime el bloque "Copia y pega" de cada práctica o el [HTML completo](apuntes/chuleta-docker.html).

En todos los comandos, cambia `tuusuario` por tu usuario de Docker Hub.

## Créditos

- Los capítulos de [`apuntes/pabpereza`](apuntes/pabpereza/) son de Pablo Pérez-Aradros ([pabpereza.dev](https://pabpereza.dev)), con licencia Apache 2.0. La licencia y los cambios hechos están en su carpeta.
- El resto (prácticas, chuleta, trampas y preguntas) son apuntes propios.
