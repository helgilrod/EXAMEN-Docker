FROM python:3.15
ENV HOST=0.0.0.0
WORKDIR /app
# Primer només requirements.txt: si no canvia, Docker reutilitza la capa del pip install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3", "app.py"]
