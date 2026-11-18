FROM nginx:1.26
RUN apt-get update && \
    apt-get install -y nano && \
    rm -rf /var/lib/apt/lists/*
COPY index.html /usr/share/nginx/html/index.html
