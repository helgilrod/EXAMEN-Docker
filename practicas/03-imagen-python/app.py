import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hola():
    return "Hola des de Python dins de Docker!"


if __name__ == "__main__":
    # HOST ve del Dockerfile (ENV HOST=0.0.0.0). Si no el llig, Flask escolta en 127.0.0.1
    # i des de fora del contenidor no s'hi pot accedir.
    app.run(host=os.environ.get("HOST", "127.0.0.1"), port=5000)
