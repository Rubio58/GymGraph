# 💾 Persistencia de Datos - GymGraph

## ¿Se guardan los datos entre sesiones?

**Sí, absolutamente.** Todos los datos se guardan automáticamente en una base de datos SQLite local.

---

## Cómo funciona

### 📊 Base de datos local
- **Ubicación**: `data/gymgraph.db` (se crea automáticamente al ejecutar la app)
- **Tipo**: SQLite (incluido en Python, no necesita servidor)
- **Ubicación relativa a**: El directorio donde se ejecuta el programa

### 👤 Usuario único
La app usa un **usuario local fijo** (ID = 1) con nombre "Usuario"

Esto significa:
- ✅ No necesitas registrarte
- ✅ Los datos son tuyos exclusivamente
- ✅ Cada vez que abres la app, recupera todos los datos anteriores

---

## Rutas de la BD según instalación

### Ejecutable compilado
```
GymGraph.exe / GymGraph / GymGraph.app
└── (directorio de ejecución)
    └── data/
        └── gymgraph.db
```

### Desarrollo (desde proyecto)
```
/home/cambrita/TiT/GymGraph
└── data/
    └── gymgraph.db
```

---

## Verificar los datos

### Con terminal/CMD
```bash
# Ver la ruta de la BD
cd data
ls -la  # Linux/Mac
dir     # Windows

# Ver tamaño
ls -lh gymgraph.db
```

### Con una herramienta SQL
Puedes usar **SQLite Browser** (gratuito) para inspeccionar los datos:
- Windows: https://sqlitebrowser.org/
- Linux: `sudo apt install sqlitebrowser`
- macOS: `brew install db-browser-for-sqlite`

---

## Estructura de datos

| Tabla | Contiene |
|-------|----------|
| `users` | Perfil del usuario |
| `training_plans` | Tus planes de entrenamiento |
| `training_days` | Días de los planes |
| `workout_sessions` | Sesiones registradas |
| `exercises` | Catálogo de ejercicios |
| `foods` | Catálogo de alimentos |
| `body_measurements` | Medidas (peso, talla, etc) |
| `sleep_logs` | Registros de sueño |
| `step_logs` | Pasos registrados |
| `menstrual_logs` | Ciclo menstrual |
| `nutrition_goals` | Tus objetivos nutricionales |

---

## Ejemplos de uso

### Primero que nada
1. Ejecutas `GymGraph`
2. La app crea automáticamente `data/gymgraph.db`
3. Se crea la BD con todas las tablas

### En la sesión 1
- Registras un entrenamiento
- Añades alimentos
- Guardas medidas

### En la sesión 2 (mañana)
- Abres `GymGraph`
- **Todos los datos de ayer siguen ahí** ✅
- Puedes ver tu historial, gráficos, etc.

---

## Hacer backup

Para guardar una copia de tus datos:

```bash
# Linux/Mac
cp data/gymgraph.db data/gymgraph.db.backup

# Windows
copy data\gymgraph.db data\gymgraph.db.backup
```

O simplemente copia la carpeta `data/` a otro lugar.

---

## Restaurar datos

Si algo sale mal:

```bash
# Linux/Mac
cp data/gymgraph.db.backup data/gymgraph.db

# Windows
copy data\gymgraph.db.backup data\gymgraph.db
```

---

## ⚠️ Casos especiales

### Ejecutable en otra máquina
Si compartes el ejecutable con un amigo:
- Cada ejecución crea su propia BD local
- Los datos de tu amigo son completamente independientes
- Si quieres transferir tus datos, copia el archivo `data/gymgraph.db`

### Mover datos a otra ubicación
```bash
# Copiar todo
cp -r data/ /ruta/nueva/datos/

# O el archivo directamente
cp data/gymgraph.db /ruta/nueva/
```

---

## Sincronización (No disponible actualmente)

Actualmente **no hay sincronización en la nube**. Cada instalación de la app es completamente independiente.

Si necesitas sincronizar entre dispositivos, tendrías que:
1. Hacer backup del `data/` en el dispositivo 1
2. Copiar `data/` al dispositivo 2 manualmente

---

## Conclusión

✅ Los datos **SÍ persisten** entre sesiones
✅ Todo se guarda localmente de forma segura
✅ No necesitas conexión a internet
✅ Total privacidad (todo en tu máquina)
