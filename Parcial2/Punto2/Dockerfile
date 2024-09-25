FROM python:3.8-slim

# Instalar dependencias
RUN pip install Flask tensorflow keras
RUN pip install Pillow==8.4.0

# Copiar los archivos del proyecto
COPY . /app
WORKDIR /app

# Exponer puerto
EXPOSE 5000

# Iniciar la aplicación
CMD ["python", "app.py"]
