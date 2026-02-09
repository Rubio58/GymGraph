# 💪 GymGraph

**Aplicación de escritorio para el seguimiento personal de fitness, nutrición y bienestar.**

*Proyecto universitario por: Huilin Jin, Arkaitz Cambra y Andrés Salamanca*

---

## 📋 Descripción

GymGraph es una aplicación local que centraliza el registro y análisis de:
- 🏋️ **Entrenamientos**: Ejercicios, series, pesos y repeticiones
- 🥗 **Nutrición**: Calorías, macronutrientes y consumo de agua
- 📏 **Medidas corporales**: Peso, medidas musculares, grasa corporal
- 😴 **Autocuidado**: Sueño, pasos y ciclo menstrual

> **Nota**: Esta aplicación está diseñada para uso personal en tu ordenador. No requiere registro ni inicio de sesión.

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| Backend | Python 3.11 + Flask |
| Base de datos | MySQL 8.0 |
| Visualización | Grafana |
| Frontend | HTML5 + CSS3 + JavaScript |
| Contenedores | Docker + Docker Compose |

## 🚀 Instalación y Ejecución

### Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/)
- Git

### Opción 1: Con Docker (Recomendado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/gymgraph.git
cd gymgraph

# 2. Copiar archivo de configuración
cp .env.example .env

# 3. Iniciar todos los servicios
docker-compose up -d

# 4. Verificar que los contenedores están corriendo
docker-compose ps
```

Una vez iniciado:
- **Aplicación web**: http://localhost:5000
- **Grafana**: http://localhost:3000 (usuario: `admin`, contraseña: `admin`)

### Opción 2: Desarrollo local (sin Docker)

```bash
# Linux/Mac
chmod +x start.sh
./start.sh

# O manualmente:
python3 -m pip install -r requirements.txt
cp .env.example .env
python3 run.py

# Windows
start.bat

# O manualmente:
python -m pip install -r requirements.txt
copy .env.example .env
python run.py
```

**Requisitos locales:**
- Python 3.8+
- MySQL 8.0+ (si no usas Docker)
- Los comandos `python` o `python3` en el PATH

**Nota:** Si usas una base de datos local, asegúrate de:
1. Tener MySQL corriendo
2. Crear la base de datos: `mysql -u root -p < database/schema.sql`
3. Configurar credenciales en `.env`

## 📁 Estructura del Proyecto

```
GymGraph/
├── app/
│   ├── __init__.py          # Factory de la aplicación Flask
│   ├── controllers/          # Controladores (rutas y lógica)
│   │   ├── main_controller.py
│   │   ├── auth_controller.py
│   │   ├── workout_controller.py
│   │   ├── nutrition_controller.py
│   │   ├── measurement_controller.py
│   │   └── selfcare_controller.py
│   └── models/               # Modelos (acceso a BD)
│       ├── database.py
│       ├── user.py
│       ├── workout.py
│       ├── nutrition.py
│       └── measurements.py
├── templates/                # Vistas HTML (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── auth/
│   ├── workout/
│   ├── nutrition/
│   ├── measurement/
│   └── selfcare/
├── static/                   # Archivos estáticos
│   ├── css/style.css
│   └── js/main.js
├── database/
│   └── schema.sql           # Esquema de base de datos
├── grafana/                  # Configuración de Grafana
│   ├── provisioning/
│   └── dashboards/
├── config.py                 # Configuración de la aplicación
├── run.py                    # Punto de entrada
├── requirements.txt          # Dependencias Python
├── Dockerfile               # Imagen Docker de la app
├── docker-compose.yml       # Orquestación de servicios
└── README.md
```

## 🎯 Funcionalidades

### Módulo de Entrenamiento
- ✅ Crear planes de entrenamiento semanales
- ✅ Catálogo de ejercicios predefinidos + personalizados
- ✅ Registrar sesiones con series, peso y repeticiones
- ✅ Historial de entrenamientos

### Módulo de Nutrición
- ✅ Base de datos de alimentos con macros
- ✅ Registro diario de comidas
- ✅ Seguimiento de agua
- ✅ Objetivos nutricionales personalizados

### Módulo de Medidas
- ✅ Registro de peso y composición corporal
- ✅ Medidas de múltiples grupos musculares
- ✅ Historial y evolución

### Módulo de Autocuidado
- ✅ Registro de horas de sueño
- ✅ Seguimiento de pasos diarios
- ✅ Registro de ciclo menstrual

### Visualización (Grafana)
- ✅ Gráfica de evolución del peso
- ✅ Gráfica de calorías semanales
- ✅ Gráfica de pasos
- ✅ Indicadores de sueño

## 🔌 API REST

La aplicación expone una API REST para cada módulo:

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/workout/api/exercises` | GET | Listar ejercicios |
| `/workout/api/sessions` | POST | Iniciar sesión de entrenamiento |
| `/workout/api/sessions/{id}/sets` | POST | Registrar serie |
| `/nutrition/api/foods` | GET | Buscar alimentos |
| `/nutrition/api/logs` | POST | Registrar alimento consumido |
| `/nutrition/api/water` | POST | Registrar agua |
| `/measurement/api/measurements` | GET/POST | Medidas corporales |
| `/selfcare/api/sleep` | GET/POST | Registro de sueño |
| `/selfcare/api/steps` | GET/POST | Registro de pasos |

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=app tests/
```

## 📊 Diagramas

### Arquitectura MVC

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│ Controller  │────▶│   Model     │
│   (HTML)    │◀────│  (Flask)    │◀────│  (MySQL)    │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Grafana   │
                    │  (Gráficas) │
                    └─────────────┘
```

### Esquema de Base de Datos

Las tablas principales son:
- `users` - Usuarios del sistema
- `exercises`, `training_plans`, `workout_sessions`, `workout_sets` - Entrenamiento
- `foods`, `food_logs`, `water_logs`, `nutrition_goals` - Nutrición
- `body_measurements` - Medidas corporales
- `sleep_logs`, `step_logs`, `menstrual_logs` - Autocuidado

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Añadir nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

---

**GymGraph** - Desarrollado con ❤️ por Huilin Jin, Arkaitz Cambra y Andrés Salamanca
