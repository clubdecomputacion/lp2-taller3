FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# TODO 1: Completa el comando para ejecutar run.py con python.
#         (En producción real se usaría gunicorn en lugar del servidor
#         de desarrollo de Flask, pero para el taller esto es suficiente.)
CMD ["python", "run.py"]
