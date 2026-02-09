#!/usr/bin/env python3
"""
Script para compilar GymGraph a un ejecutable .exe con PyInstaller
Uso: python build_exe.py
"""

import subprocess
import sys
import os
from pathlib import Path

def build_exe():
    """Compilar la aplicación a ejecutable"""
    
    # Rutas
    project_root = Path(__file__).parent
    dist_dir = project_root / "dist"
    
    print("🏗️  Compilando GymGraph a ejecutable...")
    print(f"📁 Proyecto: {project_root}")
    print(f"📦 Salida: {dist_dir}")
    
    # Comando de PyInstaller
    cmd = [
        "pyinstaller",
        "--name=GymGraph",
        "--onefile",  # Un único archivo ejecutable
        "--windowed",  # Sin ventana de consola (opcional, remove para debug)
        "--icon=NONE",
        "--add-data=templates:templates",  # Incluir carpeta templates
        "--add-data=static:static",  # Incluir carpeta static
        "--add-data=database:database",  # Incluir carpeta database
        "--hidden-import=flask",
        "--hidden-import=flask_cors",
        "--collect-all=flask",
        "--collect-all=werkzeug",
        str(project_root / "run.py"),  # Archivo principal
    ]
    
    print(f"\n🔨 Ejecutando: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, cwd=str(project_root))
    
    if result.returncode == 0:
        print("\n✅ ¡Compilación exitosa!")
        exe_path = dist_dir / "GymGraph.exe"
        print(f"📍 Ejecutable: {exe_path}")
        print(f"\n💡 Ahora puedes:")
        print(f"   1. Compartir {exe_path} con tus amigos")
        print(f"   2. Ellos solo necesitan hacer doble clic para ejecutar")
    else:
        print("\n❌ Error durante la compilación")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
