# 📦 Distribución de GymGraph

## Para usuarios: Descargar y ejecutar

### Windows
1. Descarga `GymGraph.exe` (60-80 MB)
2. Haz doble clic para ejecutar
3. Abre http://localhost:5000 en tu navegador
4. ¡Listo!

### Linux
1. Descarga `GymGraph` (11 MB)
2. Abre terminal en la carpeta de descarga
3. Ejecuta:
```bash
chmod +x GymGraph
./GymGraph
```
4. Abre http://localhost:5000 en tu navegador

### macOS
1. Descarga `GymGraph.app`
2. Doble clic para ejecutar (o arrastra a Aplicaciones)
3. Abre http://localhost:5000 en tu navegador

---

## Para desarrolladores: Compilar ejecutables

### Requisitos
- Python 3.8+
- PyInstaller: `pip install pyinstaller`

### Compilar para tu SO actual
```bash
python build_exe.py
```

### Compilar para un SO específico
```bash
# Solo Windows
python build_exe.py --windows

# Solo Linux
python build_exe.py --linux

# Solo macOS
python build_exe.py --mac
```

### Compilar para todos los SO
```bash
python build_exe.py --all
```
⚠️ Nota: Necesitas tener compiladores/herramientas específicas para cada SO.

### Tamaños típicos
- **Windows .exe**: 60-80 MB
- **Linux binario**: 10-15 MB
- **macOS app**: 70-90 MB

### Distribución
1. **GitHub Releases**: Crea una release en GitHub y sube los ejecutables
2. **Carpeta compartida**: Dropbox, Google Drive, etc.
3. **Compresión**: Comprimir para reducir tamaño si es necesario

#### Ejemplo: Preparar distribución
```bash
# Crear carpeta de distribución
mkdir -p releases/v1.0

# Linux
cp dist/GymGraph releases/v1.0/GymGraph-linux
tar -czf releases/v1.0/GymGraph-linux.tar.gz releases/v1.0/GymGraph-linux

# Windows (generar en Windows)
cp dist/GymGraph.exe releases/v1.0/GymGraph-windows.exe

# Comprimir todo
cd releases/v1.0
zip -r GymGraph-v1.0-all.zip *.exe *.tar.gz
```

---

## Troubleshooting

### "Windows protected your PC"
Windows SmartScreen puede bloquear el ejecutable. Los usuarios deben:
1. Hacer clic en "Más información"
2. Seleccionar "Ejecutar de todas formas"

**Solución permanente**: Firmar el código (requiere certificado)

### "Permission denied" en Linux
```bash
chmod +x GymGraph
./GymGraph
```

### El puerto 5000 está en uso
```
Error: Address already in use
```
Edita `run.py` y cambia el puerto:
```python
app.run(host='0.0.0.0', port=8000, debug=True)
```
Luego recompila.

### No se abre el navegador automáticamente
Accede manualmente a http://localhost:5000

### Librerias no encontradas en Linux
En algunas distribuciones de Linux puede faltar `libssl` o `libcrypto`:
```bash
# Ubuntu/Debian
sudo apt-get install libssl-dev

# CentOS/RHEL
sudo yum install openssl-devel
```

---

## Automatización: GitHub Actions

Puedes crear un flujo de GitHub Actions para compilar automáticamente:

```yaml
name: Build Executables
on: [push, release]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt pyinstaller
      - run: python build_exe.py
      - uses: actions/upload-artifact@v3
        with:
          name: ${{ runner.os }}-executable
          path: dist/
```

---

## Próximas mejoras
- [ ] Auto-actualización integrada
- [ ] Iconos personalizados (.ico, .icns)
- [ ] Instalador MSI para Windows
- [ ] DMG para macOS
- [ ] Firma de código para evitar advertencias
- [ ] Notarizacion en macOS
