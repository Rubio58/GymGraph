#!/bin/bash
# GymGraph - Script de inicio

set -e

echo "🏋️  GymGraph - Iniciando aplicación..."

# Verificar que Python 3 está disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

# Verificar dependencias
echo "📦 Verificando dependencias..."
python3 -m pip install -q -r requirements.txt 2>/dev/null || true

# Crear .env si no existe
if [ ! -f ".env" ]; then
    echo "⚙️  Creando archivo .env..."
    cp .env.example .env
    echo "ℹ️  Se ha creado .env. Ajusta las credenciales de MySQL si es necesario."
fi

# Iniciar la aplicación
echo "🚀 Iniciando Flask en http://localhost:5000..."
python3 run.py
