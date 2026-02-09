# 📦 Distribución de GymGraph

## Para usuarios: Descargar y ejecutar

### Windows
1. Descarga `GymGraph.exe`
2. Haz doble clic para ejecutar
3. Abre http://localhost:5000 en tu navegador
4. ¡Listo!

### Linux / Mac
Descarga el archivo binario correspondiente y ejecuta:
```bash
chmod +x GymGraph
./GymGraph
```

---

## Para desarrolladores: Compilar el ejecutable

### Requisitos
- Python 3.8+
- PyInstaller: `pip install pyinstaller`

### Generar .exe para Windows

#### Opción 1: En Windows (recomendado)
```bash
python build_exe.py
```
El archivo `dist/GymGraph.exe` estará listo para compartir.

#### Opción 2: Construcción remota
Si construyes desde Linux/Mac pero necesitas un .exe de Windows, puedes:
1. Usar GitHub Actions (ver `.github/workflows/`)
2. Compilar con Wine/CrossBuild
3. Usar un servidor Windows

### Tamaño del ejecutable
- `GymGraph.exe`: ~60-80 MB (includes Python runtime + dependencias)

### Distribución
1. Sube a GitHub Releases
2. Comparte el link de descarga
3. Los usuarios descargan y ejecutan directamente

---

## Troubleshooting

### "Windows protected your PC"
Windows SmartScreen puede bloquear el ejecutable. Los usuarios deben:
1. Hacer clic en "Más información"
2. Seleccionar "Ejecutar de todas formas"

### El puerto 5000 está en uso
```
Error: Address already in use
```
Edita `run.py` y cambia el puerto:
```python
app.run(host='0.0.0.0', port=8000, debug=True)
```

### No se abre el navegador automáticamente
Accede manualmente a http://localhost:5000

---

## Próximas mejoras
- [ ] Auto-actualización integrada
- [ ] Iconos personalizados
- [ ] Instalador MSI para Windows
- [ ] Firma de código para evitar advertencias
