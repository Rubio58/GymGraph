# 🚀 QUICKSTART - GymGraph

## Inicio rápido

### Opción 1: Docker (Recomendado)
```bash
docker-compose up -d
```
Accede a:
- App: http://localhost:5000
- Grafana: http://localhost:3000 (admin/admin)

### Opción 2: Desarrollo local

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
start.bat
```

**Manual:**
```bash
python3 -m pip install -r requirements.txt
cp .env.example .env
python3 run.py
```

La aplicación estará en: http://localhost:5000

---

## Primeros pasos

1. **Registrarse**: Clic en "Registrarse" (esquina superior derecha)
2. **Crear una cuenta** con usuario y contraseña
3. **Iniciar sesión**
4. **Explorar los módulos**:
   - 🏋️ **Entrenamiento**: Crear planes y registrar sesiones
   - 🥗 **Nutrición**: Buscar alimentos y registrar comidas
   - 📏 **Medidas**: Registrar peso y medidas corporales
   - 😴 **Autocuidado**: Sueño, pasos y ciclo menstrual

---

## Solución de problemas

### "python: command not found"
Usa `python3` en su lugar:
```bash
python3 run.py
```

### "No connection to MySQL"
- Verifica que MySQL está corriendo
- Comprueba las credenciales en `.env`
- Si usas Docker: `docker-compose up -d db`

### Base de datos no inicializada
```bash
# Linux/Mac
mysql -u root -p < database/schema.sql

# Docker
docker-compose exec db mysql -u gymgraph_user -p -D gymgraph_db < database/schema.sql
```

### Puerto 5000 en uso
```bash
# Busca qué proceso usa el puerto 5000
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Usa otro puerto en run.py:
# app.run(host='0.0.0.0', port=8000, debug=True)
```

---

## Estructura rápida

| Carpeta | Contenido |
|---------|-----------|
| `app/controllers/` | Rutas y lógica de negocio |
| `app/models/` | Acceso a base de datos |
| `templates/` | Vistas HTML |
| `static/` | CSS, JavaScript |
| `database/` | Esquema SQL |

---

## Comandos útiles

```bash
# Ver logs en tiempo real (Docker)
docker-compose logs -f app

# Detener aplicación
docker-compose down

# Resetear base de datos
docker-compose down -v  # Elimina volúmenes

# Ejecutar con Python sin Docker
python3 run.py
```

---

¿Preguntas? Revisa [README.md](README.md) para más detalles.
