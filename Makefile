# Makefile para La Veguita

# Variables
FRONT_PATH=FrontEnd/nuxt-app1
BACK_PATH=Backend/la_veguita_app
FRONT_IMAGE=fernandosolispaz/la-veguita-frontend:latest
BACK_IMAGE=fernandosolispaz/la-veguita-backend:latest

.PHONY: all build push deploy migrate

# Build de imágenes
build:
	docker build -t $(FRONT_IMAGE) $(FRONT_PATH)
	docker build -t $(BACK_IMAGE) $(BACK_PATH)

# Push a Docker Hub
push:
	docker push $(FRONT_IMAGE)
	docker push $(BACK_IMAGE)

# Build y Push juntos
publish: build push

# Solo ejecutar docker-compose (para el servidor)
deploy:
	docker-compose up --build -d

# Ejecutar migraciones dentro del contenedor backend (espera a que esté arriba)
migrate:
	docker exec -it la-veguita-software-backend-1 python manage.py migrate

# Todo junto (ideal para tu máquina local antes de ir al servidor)
all: publish

# Limpiar proyecto
down:
	docker-compose down --rmi all