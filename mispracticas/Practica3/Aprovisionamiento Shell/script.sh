#!/bin/bash

# Actualizar el sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instalar Docker usando el script oficial de Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Iniciar el servicio Docker
sudo systemctl start docker
sudo systemctl enable docker

# Añadir el usuario actual al grupo docker
sudo usermod -aG docker ${USER}

# Crear una red Docker para los microservicios


# Función para construir y ejecutar un microservicio
build_and_run() {
    service=$1
    port=$2
    echo "Construyendo y ejecutando $service..."
    cd /home/vagrant/microWebAppParcial/$service
    docker build -t $service .
    docker run -d --name $service --network microservices-net -p $port:$port $service
	 -e MYSQL_HOST=$MYSQL_HOST \
         -e MYSQL_USER=$MYSQL_USER \
         -e MYSQL_PASSWORD=$MYSQL_PASSWORD \
         -e MYSQL_DB=$MYSQL_DB \
         -p $port:$port ${service,,}
}

export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=root
export MYSQL_DB=myflaskapp

# Construir y ejecutar cada microservicio
build_and_run frontend 5001
build_and_run microusers 5002
build_and_run microproducts 5003
build_and_run microorders 5004

echo "Aprovisionamiento completado. Los microservicios están en ejecución."

# Mostrar los contenedores en ejecución
docker ps
