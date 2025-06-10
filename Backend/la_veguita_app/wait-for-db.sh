#!/bin/sh

echo "Esperando a que PostgreSQL arranque en $DB_HOST:$DB_PORT..."

# Espera hasta que el puerto esté listo
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "PostgreSQL está listo. Ejecutando el servidor Django..."

exec "$@"
