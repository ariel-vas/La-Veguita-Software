Build y Push de front
La-Veguita-Software\FrontEnd\nuxt-app1> docker build -t motihc/la-veguita-frontend:latest .
La-Veguita-Software\FrontEnd\nuxt-app1> docker push motihc/la-veguita-frontend:latest      

Build y Push de back
La-Veguita-Software\Backend\la_veguita_app> docker build -t motihc/la-veguita-backend:latest .
La-Veguita-Software\Backend\la_veguita_app> docker push motihc/la-veguita-backend:latest

En el servidor se necesita tener solo el docker-compose.yml
-> docker-compose up --build

Para cerrarlo y borrar toda la cache
-> docker-compose down --rmi all

Solo para cerrarlo y abrirlo desde cero
-> docker system prune -f
-> docker-compose down --volumes