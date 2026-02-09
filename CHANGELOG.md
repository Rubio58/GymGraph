# 📝 CHANGELOG - GymGraph

## [v0.1.0] - 2026-01-27 - Versión Base

### ✨ Funcionalidades Implementadas

#### 🏗️ Arquitectura
- [x] Patrón MVC con Flask
- [x] Pool de conexiones MySQL
- [x] Autenticación de usuarios con contraseñas hasheadas
- [x] Decorador para rutas protegidas

#### 👤 Módulo de Usuario
- [x] Registro e inicio de sesión
- [x] Editar perfil personal
- [x] Gestión de sesiones

#### 🏋️ Módulo de Entrenamiento
- [x] Crear y editar planes de entrenamiento
- [x] Catálogo de 29 ejercicios predefinidos
- [x] Crear ejercicios personalizados
- [x] Registrar sesiones de entrenamiento
- [x] Registrar series con peso, repeticiones y RPE
- [x] Historial de entrenamientos
- [x] Vista HTML: Plans, Workout Session, History
- [x] API REST: `/workout/api/*`

#### 🥗 Módulo de Nutrición
- [x] Base de datos de 28 alimentos predefinidos
- [x] Crear alimentos personalizados
- [x] Buscar alimentos
- [x] Registrar comidas diarias por tipo (desayuno, comida, cena, snacks)
- [x] Seguimiento de agua diaria
- [x] Objetivos nutricionales personalizados
- [x] Cálculo de macros diarios
- [x] Vista HTML: Nutrition, Foods, Goals
- [x] API REST: `/nutrition/api/*`

#### 📏 Módulo de Medidas Corporales
- [x] Registro de peso
- [x] Registro de composición corporal (% grasa)
- [x] Medidas de múltiples grupos musculares
  - Pecho, cintura, cadera
  - Brazos (bíceps izq/der)
  - Piernas (muslos, gemelos izq/der)
  - Cuello, hombros
- [x] Historial de medidas
- [x] Vista HTML: Measurements, New Measurement
- [x] API REST: `/measurement/api/*`

#### 😴 Módulo de Autocuidado
- [x] Registro de sueño (horas y calidad)
- [x] Registro de pasos diarios
- [x] Registro de ciclo menstrual
- [x] Historial de registros personalizados
- [x] Vista HTML: Self-care
- [x] API REST: `/selfcare/api/*`

#### 📊 Dashboard y Visualización
- [x] Dashboard principal con resumen del día
- [x] Gráfica de evolución del peso (Chart.js)
- [x] Integración con Grafana para análisis avanzado
- [x] 4 dashboards de Grafana preconfigurados

#### 🎨 Frontend
- [x] Diseño responsive dark mode
- [x] Navegación intuitiva
- [x] Formularios con validación
- [x] Alertas y notificaciones
- [x] Estilos CSS modulares
- [x] JavaScript para interactividad

#### 🐳 Infraestructura
- [x] Dockerfile para la aplicación
- [x] Docker Compose (MySQL + Grafana + Flask)
- [x] Esquema SQL con 18 tablas
- [x] Scripts de inicio (Linux/Mac/Windows)
- [x] Archivo .env.example para configuración

#### 📚 Documentación
- [x] README.md completo
- [x] QUICKSTART.md para inicio rápido
- [x] Comentarios en código
- [x] Docstrings en funciones

### 🗄️ Base de Datos

**Tablas creadas:**
- `users` - Usuarios del sistema
- `exercises` - Catálogo de ejercicios
- `training_plans` - Planes de entrenamiento
- `training_days` - Días del plan
- `planned_exercises` - Ejercicios por día
- `workout_sessions` - Sesiones realizadas
- `workout_sets` - Series de cada sesión
- `foods` - Catálogo de alimentos
- `recipes` - Recetas personalizadas
- `recipe_ingredients` - Ingredientes de recetas
- `nutrition_goals` - Objetivos nutricionales
- `food_logs` - Registro diario de alimentos
- `water_logs` - Registro de agua
- `body_measurements` - Medidas corporales
- `sleep_logs` - Registro de sueño
- `menstrual_logs` - Registro menstrual
- `step_logs` - Registro de pasos
- `custom_logs` - Registros personalizados

### 📋 API REST

**29 endpoints implementados:**
- 6 endpoints de autenticación
- 11 endpoints de entrenamiento
- 9 endpoints de nutrición
- 4 endpoints de medidas
- 5 endpoints de autocuidado

### ⚠️ Limitaciones Conocidas

- [ ] Autenticación: Sin roles de usuario (todos son usuarios normales)
- [ ] Recetas: No completamente integradas con food logs
- [ ] Gráficas: Solo gráficas básicas en dashboard (Grafana para avanzadas)
- [ ] Notificaciones: Sin sistema de alertas automáticas
- [ ] Email: No hay validación de email
- [ ] Backup: Sin sistema de copias de seguridad automáticas
- [ ] Escalado: No optimizado para miles de usuarios

### 🔄 Próximas Fases (Según Plan Original)

**Fase 3.1 - Selección Tecnológica (Completada)**
- Justificación de Python/Flask ✓
- Análisis de Grafana ✓

**Fase 4.2-4.4 - Desarrollo (Completada)**
- Configuración del entorno ✓
- Implementación BD ✓
- Backend (lógica) ✓
- Frontend (interfaz) ✓

**Fase 5 - Integración del Sistema (Pendiente)**
- Pruebas de persistencia
- Pruebas de flujo de datos
- Pruebas de actualización en tiempo real

**Fase 6 - Gestión y Documentación (En progreso)**
- Reuniones semanales
- Documentación técnica

**Fase 7 - Evaluación y Cierre**
- Testing completo
- Despliegue final
- Guía de usuario

### 🚀 Mejoras Futuras

- [ ] Autenticación OAuth (Google, GitHub)
- [ ] Exportar datos (PDF, CSV, Excel)
- [ ] Sincronización con wearables
- [ ] Notificaciones push
- [ ] App móvil (React Native/Flutter)
- [ ] Análisis predictivo con ML
- [ ] Comunidad y seguimiento social
- [ ] Integración con Spotify para entrenamientos

---

## Versiones Anteriores

### v0.0.0 (2026-01-27)
- Inicialización del proyecto
- Creación de estructura base
