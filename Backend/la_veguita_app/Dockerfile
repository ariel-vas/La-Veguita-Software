# Imagen base
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia requirements e instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código
COPY . .

# Expone el puerto (Django usa 8000 por defecto)
EXPOSE 8000

# Comando para correr el servidor de desarrollo (puedes cambiarlo por gunicorn para prod)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
