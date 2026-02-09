@echo off
REM GymGraph - Script de inicio para Windows

echo 🏋️  GymGraph - Iniciando aplicación...

REM Verificar que Python está disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado
    exit /b 1
)

REM Verificar dependencias
echo 📦 Verificando dependencias...
python -m pip install -q -r requirements.txt

REM Crear .env si no existe
if not exist ".env" (
    echo ⚙️  Creando archivo .env...
    copy .env.example .env
    echo ℹ️  Se ha creado .env. Ajusta las credenciales de MySQL si es necesario.
)

REM Iniciar la aplicación
echo 🚀 Iniciando Flask en http://localhost:5000...
python run.py
