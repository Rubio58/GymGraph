#!/usr/bin/env python3
"""
Script para compilar GymGraph a ejecutables con PyInstaller
Multiplataforma: Windows (.exe), Linux (binario), macOS (app bundle)
Uso: python build_exe.py [--windows|--linux|--mac|--all]
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


def get_platform():
    """Detectar SO actual"""
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Darwin":
        return "mac"
    else:
        return "linux"


def build_exe(target_platform=None):
    """Compilar la aplicación a ejecutable"""
    
    if target_platform is None:
        target_platform = get_platform()
    
    # Rutas
    project_root = Path(__file__).parent
    dist_dir = project_root / "dist"
    
    print(f"🏗️  Compilando GymGraph para {target_platform.upper()}...")
    print(f"📁 Proyecto: {project_root}")
    print(f"📦 Salida: {dist_dir}")
    
    # Configuración base
    cmd = [
        "pyinstaller",
        "--name=GymGraph",
        "--onefile",  # Un único archivo ejecutable
        "--add-data", f"templates{os.pathsep}templates",
        "--add-data", f"static{os.pathsep}static",
        "--add-data", f"database{os.pathsep}database",
        "--hidden-import=flask",
        "--hidden-import=flask_cors",
        "--collect-all=flask",
        "--collect-all=werkzeug",
    ]
    
    # Configuración específica por SO
    if target_platform == "windows":
        cmd.extend([
            "--windowed",  # Sin ventana de consola
            "--icon=NONE",
        ])
        output_name = "GymGraph.exe"
    elif target_platform == "linux":
        cmd.append("--console")  # Con terminal
        output_name = "GymGraph"
    elif target_platform == "mac":
        cmd.extend([
            "--windowed",
            "--osx-bundle-identifier=com.gymgraph.app",
        ])
        output_name = "GymGraph.app"
    
    cmd.append(str(project_root / "run.py"))
    
    print(f"\n🔨 Ejecutando PyInstaller...\n")
    
    result = subprocess.run(cmd, cwd=str(project_root))
    
    if result.returncode == 0:
        print("\n✅ ¡Compilación exitosa!")
        
        if target_platform == "windows":
            exe_path = dist_dir / "GymGraph.exe"
            print(f"📍 Ejecutable: {exe_path}")
            print(f"\n💡 Para compartir:")
            print(f"   - Envía {exe_path} a tus amigos")
            print(f"   - Ellos hacen doble clic y ¡funciona!")
            
        elif target_platform == "linux":
            exe_path = dist_dir / "GymGraph"
            print(f"📍 Ejecutable: {exe_path}")
            print(f"\n💡 Para usar:")
            print(f"   chmod +x {exe_path}")
            print(f"   ./{exe_path}")
            print(f"\n💡 Para compartir:")
            print(f"   - Comprime: tar -czf GymGraph-linux.tar.gz {exe_path}")
            print(f"   - O simplemente copia el archivo")
            
        elif target_platform == "mac":
            app_path = dist_dir / "GymGraph.app"
            print(f"📍 App: {app_path}")
            print(f"\n💡 Para usar:")
            print(f"   - Doble clic en GymGraph.app")
            print(f"   - O: open {app_path}")
    else:
        print("\n❌ Error durante la compilación")
        sys.exit(1)


def main():
    """Función principal"""
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "--current":
            # Compilar solo para el SO actual
            build_exe(get_platform())
        elif arg == "--all":
            print("🚀 Compilando para TODOS los SO...\n")
            for plat in ["linux", "windows", "mac"]:
                print(f"\n{'='*60}")
                print(f"Compilando para {plat.upper()}")
                print(f"{'='*60}")
                try:
                    build_exe(plat)
                except Exception as e:
                    print(f"⚠️  Error compilando para {plat}: {e}")
        elif arg in ["--windows", "--linux", "--mac"]:
            platform_map = {
                "--windows": "windows",
                "--linux": "linux",
                "--mac": "mac"
            }
            build_exe(platform_map[arg])
        else:
            print("Uso: python build_exe.py [--all|--current|--windows|--linux|--mac]")
            print(f"\nPor defecto: python build_exe.py (compila para todos los SO)")
            sys.exit(1)
    else:
        # Sin argumentos: compilar para TODOS los SO
        print("🚀 Compilando para TODOS los SO...\n")
        for plat in ["linux", "windows", "mac"]:
            print(f"\n{'='*60}")
            print(f"Compilando para {plat.upper()}")
            print(f"{'='*60}")
            try:
                build_exe(plat)
            except Exception as e:
                print(f"⚠️  Error compilando para {plat}: {e}")


if __name__ == "__main__":
    main()
