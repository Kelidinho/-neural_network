#!/bin/bash

# --- Script para iniciar el entorno de desarrollo ---

echo "🚀 Iniciando el entorno de desarrollo..."
echo "-------------------------------------------"

# Primero, ejecutamos el script de limpieza para asegurar un inicio limpio.
./scripts/stop.sh

echo ""
echo "🐳 Levantando los servicios de Docker Compose en segundo plano..."

# Navegamos a la carpeta del docker-compose y ejecutamos el comando up -d
(cd environment/develop && docker compose up -d)

echo "-------------------------------------------"
echo "✅ ¡Entorno de desarrollo iniciado! La base de datos está disponible en el puerto 3306."

