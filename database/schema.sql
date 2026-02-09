-- ============================================
-- GymGraph - Esquema de Base de Datos
-- Autores: Huilin Jin, Arkaitz Cambra, Andrés Salamanca
-- ============================================

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS gymgraph_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gymgraph_db;

-- ============================================
-- TABLA: users (Usuarios)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE,
    gender ENUM('male', 'female', 'other'),
    height_cm DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================
-- TABLAS DE ENTRENAMIENTO
-- ============================================

-- Tabla: exercises (Catálogo de ejercicios)
CREATE TABLE IF NOT EXISTS exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    muscle_group VARCHAR(50),
    equipment VARCHAR(50),
    created_by INT,
    is_custom BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Tabla: training_plans (Planes de entrenamiento)
CREATE TABLE IF NOT EXISTS training_plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabla: training_days (Días de entrenamiento dentro de un plan)
CREATE TABLE IF NOT EXISTS training_days (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plan_id INT NOT NULL,
    day_of_week TINYINT NOT NULL COMMENT '1=Lunes, 7=Domingo',
    name VARCHAR(50) COMMENT 'Ej: Push, Pull, Legs',
    FOREIGN KEY (plan_id) REFERENCES training_plans(id) ON DELETE CASCADE
);

-- Tabla: planned_exercises (Ejercicios planificados por día)
CREATE TABLE IF NOT EXISTS planned_exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    training_day_id INT NOT NULL,
    exercise_id INT NOT NULL,
    order_index INT DEFAULT 0,
    target_sets INT,
    target_reps VARCHAR(20) COMMENT 'Ej: 8-12',
    notes TEXT,
    FOREIGN KEY (training_day_id) REFERENCES training_days(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
);

-- Tabla: workout_sessions (Sesiones de entrenamiento realizadas)
CREATE TABLE IF NOT EXISTS workout_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    training_day_id INT,
    session_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (training_day_id) REFERENCES training_days(id) ON DELETE SET NULL
);

-- Tabla: workout_sets (Series realizadas en una sesión)
CREATE TABLE IF NOT EXISTS workout_sets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    exercise_id INT NOT NULL,
    set_number INT NOT NULL,
    weight_kg DECIMAL(6,2),
    reps INT,
    rpe TINYINT COMMENT 'Rating of Perceived Exertion 1-10',
    is_warmup BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES workout_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
);

-- ============================================
-- TABLAS DE NUTRICIÓN
-- ============================================

-- Tabla: foods (Catálogo de alimentos)
CREATE TABLE IF NOT EXISTS foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(100),
    serving_size DECIMAL(8,2) NOT NULL DEFAULT 100,
    serving_unit VARCHAR(20) NOT NULL DEFAULT 'g',
    calories DECIMAL(8,2) NOT NULL DEFAULT 0,
    protein_g DECIMAL(8,2) DEFAULT 0,
    carbs_g DECIMAL(8,2) DEFAULT 0,
    fat_g DECIMAL(8,2) DEFAULT 0,
    fiber_g DECIMAL(8,2) DEFAULT 0,
    sugar_g DECIMAL(8,2) DEFAULT 0,
    sodium_mg DECIMAL(8,2) DEFAULT 0,
    is_custom BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Tabla: recipes (Recetas personalizadas)
CREATE TABLE IF NOT EXISTS recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    servings INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabla: recipe_ingredients (Ingredientes de recetas)
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT NOT NULL,
    food_id INT NOT NULL,
    quantity DECIMAL(8,2) NOT NULL,
    unit VARCHAR(20) DEFAULT 'g',
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE
);

-- Tabla: nutrition_goals (Objetivos nutricionales)
CREATE TABLE IF NOT EXISTS nutrition_goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    daily_calories INT,
    protein_g INT,
    carbs_g INT,
    fat_g INT,
    water_liters DECIMAL(4,2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabla: food_logs (Registro diario de alimentos)
CREATE TABLE IF NOT EXISTS food_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    food_id INT,
    recipe_id INT,
    log_date DATE NOT NULL,
    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack') NOT NULL,
    quantity DECIMAL(8,2) NOT NULL,
    unit VARCHAR(20) DEFAULT 'g',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE SET NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE SET NULL,
    CHECK (food_id IS NOT NULL OR recipe_id IS NOT NULL)
);

-- Tabla: water_logs (Registro de agua)
CREATE TABLE IF NOT EXISTS water_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    log_date DATE NOT NULL,
    liters DECIMAL(4,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, log_date)
);

-- ============================================
-- TABLAS DE MEDIDAS Y MÉTRICAS
-- ============================================

-- Tabla: body_measurements (Medidas corporales)
CREATE TABLE IF NOT EXISTS body_measurements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    measurement_date DATE NOT NULL,
    weight_kg DECIMAL(5,2),
    body_fat_percentage DECIMAL(4,2),
    chest_cm DECIMAL(5,2),
    waist_cm DECIMAL(5,2),
    hips_cm DECIMAL(5,2),
    bicep_left_cm DECIMAL(5,2),
    bicep_right_cm DECIMAL(5,2),
    thigh_left_cm DECIMAL(5,2),
    thigh_right_cm DECIMAL(5,2),
    calf_left_cm DECIMAL(5,2),
    calf_right_cm DECIMAL(5,2),
    neck_cm DECIMAL(5,2),
    shoulders_cm DECIMAL(5,2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- TABLAS DE AUTOCUIDADO
-- ============================================

-- Tabla: sleep_logs (Registro de sueño)
CREATE TABLE IF NOT EXISTS sleep_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    log_date DATE NOT NULL,
    hours_slept DECIMAL(4,2),
    sleep_quality TINYINT COMMENT '1-10',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, log_date)
);

-- Tabla: menstrual_logs (Registro de ciclo menstrual)
CREATE TABLE IF NOT EXISTS menstrual_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    log_date DATE NOT NULL,
    is_period_day BOOLEAN DEFAULT TRUE,
    flow_intensity ENUM('light', 'medium', 'heavy'),
    symptoms TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, log_date)
);

-- Tabla: step_logs (Registro de pasos)
CREATE TABLE IF NOT EXISTS step_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    log_date DATE NOT NULL,
    steps INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, log_date)
);

-- Tabla: custom_logs (Registros personalizados de autocuidado)
CREATE TABLE IF NOT EXISTS custom_log_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    unit VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS custom_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_type_id INT NOT NULL,
    user_id INT NOT NULL,
    log_date DATE NOT NULL,
    value DECIMAL(10,2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (log_type_id) REFERENCES custom_log_types(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ============================================
CREATE INDEX idx_workout_sessions_user_date ON workout_sessions(user_id, session_date);
CREATE INDEX idx_workout_sets_session ON workout_sets(session_id);
CREATE INDEX idx_food_logs_user_date ON food_logs(user_id, log_date);
CREATE INDEX idx_body_measurements_user_date ON body_measurements(user_id, measurement_date);
CREATE INDEX idx_sleep_logs_user_date ON sleep_logs(user_id, log_date);

-- ============================================
-- DATOS SEMILLA: Usuario local por defecto
-- ============================================
INSERT INTO users (id, username, email, password_hash, first_name) VALUES
(1, 'Usuario', 'usuario@local.app', 'pbkdf2:sha256:600000$local$localpassword', 'Usuario Local');

-- ============================================
-- DATOS SEMILLA: Ejercicios básicos
-- ============================================
INSERT INTO exercises (name, description, muscle_group, equipment, is_custom) VALUES
-- Pecho
('Press de banca', 'Ejercicio de empuje horizontal para pecho', 'Pecho', 'Barra', FALSE),
('Press inclinado con mancuernas', 'Enfoque en pecho superior', 'Pecho', 'Mancuernas', FALSE),
('Aperturas con mancuernas', 'Aislamiento de pecho', 'Pecho', 'Mancuernas', FALSE),
('Fondos en paralelas', 'Ejercicio compuesto para pecho y tríceps', 'Pecho', 'Peso corporal', FALSE),

-- Espalda
('Dominadas', 'Ejercicio de tirón vertical', 'Espalda', 'Barra fija', FALSE),
('Remo con barra', 'Tirón horizontal para espalda', 'Espalda', 'Barra', FALSE),
('Remo con mancuerna', 'Remo unilateral', 'Espalda', 'Mancuerna', FALSE),
('Peso muerto', 'Ejercicio compuesto para espalda baja y piernas', 'Espalda', 'Barra', FALSE),
('Jalón al pecho', 'Tirón vertical en polea', 'Espalda', 'Polea', FALSE),

-- Piernas
('Sentadilla', 'Ejercicio principal de piernas', 'Piernas', 'Barra', FALSE),
('Prensa de piernas', 'Ejercicio de empuje para cuádriceps', 'Piernas', 'Máquina', FALSE),
('Extensión de cuádriceps', 'Aislamiento de cuádriceps', 'Piernas', 'Máquina', FALSE),
('Curl de isquiotibiales', 'Aislamiento de isquiotibiales', 'Piernas', 'Máquina', FALSE),
('Peso muerto rumano', 'Énfasis en isquiotibiales y glúteos', 'Piernas', 'Barra', FALSE),
('Elevación de talones', 'Ejercicio para gemelos', 'Piernas', 'Máquina', FALSE),

-- Hombros
('Press militar', 'Ejercicio principal de hombros', 'Hombros', 'Barra', FALSE),
('Elevaciones laterales', 'Aislamiento de deltoides lateral', 'Hombros', 'Mancuernas', FALSE),
('Elevaciones frontales', 'Aislamiento de deltoides frontal', 'Hombros', 'Mancuernas', FALSE),
('Pájaros', 'Aislamiento de deltoides posterior', 'Hombros', 'Mancuernas', FALSE),

-- Brazos
('Curl de bíceps con barra', 'Ejercicio principal de bíceps', 'Bíceps', 'Barra', FALSE),
('Curl de bíceps con mancuernas', 'Curl unilateral', 'Bíceps', 'Mancuernas', FALSE),
('Curl martillo', 'Énfasis en braquial', 'Bíceps', 'Mancuernas', FALSE),
('Press francés', 'Aislamiento de tríceps', 'Tríceps', 'Barra', FALSE),
('Extensión de tríceps en polea', 'Aislamiento en polea', 'Tríceps', 'Polea', FALSE),
('Fondos en banco', 'Ejercicio para tríceps', 'Tríceps', 'Peso corporal', FALSE),

-- Core
('Plancha', 'Ejercicio isométrico de core', 'Core', 'Peso corporal', FALSE),
('Crunch abdominal', 'Flexión de tronco', 'Core', 'Peso corporal', FALSE),
('Elevación de piernas', 'Ejercicio para abdominales inferiores', 'Core', 'Peso corporal', FALSE),
('Russian twist', 'Rotación de tronco', 'Core', 'Peso corporal', FALSE);

-- ============================================
-- DATOS SEMILLA: Alimentos básicos
-- ============================================
INSERT INTO foods (name, brand, serving_size, serving_unit, calories, protein_g, carbs_g, fat_g, fiber_g, is_custom) VALUES
-- Proteínas
('Pechuga de pollo', 'Genérico', 100, 'g', 165, 31, 0, 3.6, 0, FALSE),
('Salmón', 'Genérico', 100, 'g', 208, 20, 0, 13, 0, FALSE),
('Huevo entero', 'Genérico', 50, 'g', 78, 6, 0.6, 5, 0, FALSE),
('Atún en lata', 'Genérico', 100, 'g', 116, 26, 0, 1, 0, FALSE),
('Carne de res magra', 'Genérico', 100, 'g', 250, 26, 0, 15, 0, FALSE),
('Pechuga de pavo', 'Genérico', 100, 'g', 135, 30, 0, 1, 0, FALSE),

-- Carbohidratos
('Arroz blanco cocido', 'Genérico', 100, 'g', 130, 2.7, 28, 0.3, 0.4, FALSE),
('Arroz integral cocido', 'Genérico', 100, 'g', 112, 2.6, 24, 0.9, 1.8, FALSE),
('Pasta cocida', 'Genérico', 100, 'g', 131, 5, 25, 1.1, 1.8, FALSE),
('Pan integral', 'Genérico', 30, 'g', 69, 3.6, 12, 1.1, 1.9, FALSE),
('Avena', 'Genérico', 40, 'g', 152, 5.3, 27, 2.7, 4, FALSE),
('Patata cocida', 'Genérico', 100, 'g', 77, 2, 17, 0.1, 2.2, FALSE),
('Boniato cocido', 'Genérico', 100, 'g', 86, 1.6, 20, 0.1, 3, FALSE),

-- Grasas
('Aceite de oliva', 'Genérico', 15, 'ml', 120, 0, 0, 14, 0, FALSE),
('Aguacate', 'Genérico', 100, 'g', 160, 2, 9, 15, 7, FALSE),
('Almendras', 'Genérico', 30, 'g', 173, 6, 6, 15, 3.5, FALSE),
('Mantequilla de cacahuete', 'Genérico', 32, 'g', 188, 8, 6, 16, 2, FALSE),

-- Lácteos
('Leche desnatada', 'Genérico', 250, 'ml', 83, 8.3, 12, 0.5, 0, FALSE),
('Yogur griego natural', 'Genérico', 150, 'g', 100, 17, 4, 0.7, 0, FALSE),
('Queso fresco', 'Genérico', 100, 'g', 98, 11, 3.4, 4.3, 0, FALSE),

-- Verduras
('Brócoli', 'Genérico', 100, 'g', 34, 2.8, 7, 0.4, 2.6, FALSE),
('Espinacas', 'Genérico', 100, 'g', 23, 2.9, 3.6, 0.4, 2.2, FALSE),
('Tomate', 'Genérico', 100, 'g', 18, 0.9, 3.9, 0.2, 1.2, FALSE),
('Zanahoria', 'Genérico', 100, 'g', 41, 0.9, 10, 0.2, 2.8, FALSE),

-- Frutas
('Plátano', 'Genérico', 120, 'g', 105, 1.3, 27, 0.4, 3.1, FALSE),
('Manzana', 'Genérico', 150, 'g', 78, 0.4, 21, 0.3, 3.6, FALSE),
('Naranja', 'Genérico', 150, 'g', 70, 1.3, 18, 0.2, 3.6, FALSE),
('Fresas', 'Genérico', 100, 'g', 32, 0.7, 7.7, 0.3, 2, FALSE);
