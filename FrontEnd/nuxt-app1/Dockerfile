# Etapa de desarrollo para Nuxt 3
FROM node:20

# Establece el directorio de trabajo
WORKDIR /app

# Copia archivos
COPY package*.json ./
COPY . .

# Instala dependencias
RUN npm install

# Construye la aplicación
RUN npm run build

# Expone el puerto
EXPOSE 3000

# Comando para iniciar la app en producción
CMD ["npm", "run", "start"]
