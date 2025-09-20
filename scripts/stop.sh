#!/bin/bash

# --- Script para detener el entorno de desarrollo y limpiar recursos ---

echo "🛑 Deteniendo los servicios de Docker Compose..."
# Navegamos a la carpeta del docker-compose y ejecutamos el comando down
# El comando 'down' detiene y elimina los contenedores, redes y volúmenes anónimos.
(cd environment/develop && docker-compose down)

echo "🧹 Intentando limpiar el puerto 3306 (MariaDB)..."

# Buscamos el ID del proceso (PID) que esté usando el puerto TCP 3306
PID=$(lsof -ti :3306)

# Verificamos si la variable PID no está vacía
if [ ! -z "$PID" ]; then
    echo "   -> Proceso encontrado con PID: $PID. Terminando..."
    # Forzamos la terminación del proceso
    kill -9 $PID
    echo "   -> Puerto 3306 liberado."
else
    echo "   -> El puerto 3306 ya está libre."
fi

echo "✅ Entorno detenido y limpiado con éxito."