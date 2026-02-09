"""
Conexión a la base de datos SQLite
Versión simplificada para aplicación de escritorio local
"""

import sqlite3
import os


class Database:
    """Clase para gestionar la conexión a SQLite."""
    
    _db_path = None
    _initialized = False
    
    @classmethod
    def get_db_path(cls):
        """Obtiene la ruta de la base de datos."""
        if cls._db_path is None:
            # Usar ruta en el directorio de datos
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
            os.makedirs(data_dir, exist_ok=True)
            cls._db_path = os.path.join(data_dir, 'gymgraph.db')
        return cls._db_path
    
    @classmethod
    def get_connection(cls):
        """Obtiene una conexión a SQLite."""
        conn = sqlite3.connect(cls.get_db_path())
        conn.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
        conn.execute("PRAGMA foreign_keys = ON")  # Habilitar foreign keys
        return conn
    
    @classmethod
    def dict_from_row(cls, row):
        """Convierte una Row de SQLite a diccionario."""
        if row is None:
            return None
        return dict(row)
    
    @classmethod
    def execute_query(cls, query, params=None, fetch_one=False, fetch_all=True):
        """
        Ejecuta una consulta SELECT.
        """
        # Asegurar que la BD está inicializada
        cls.init_db()
        
        # Convertir sintaxis MySQL a SQLite
        query = cls._convert_query(query)
        
        connection = None
        try:
            connection = cls.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            
            if fetch_one:
                row = cursor.fetchone()
                return cls.dict_from_row(row)
            elif fetch_all:
                rows = cursor.fetchall()
                return [cls.dict_from_row(row) for row in rows]
            return None
        except sqlite3.Error as e:
            print(f"Error en consulta: {e}")
            print(f"Query: {query}")
            raise
        finally:
            if connection:
                connection.close()
    
    @classmethod
    def execute_insert(cls, query, params=None):
        """
        Ejecuta una consulta INSERT.
        """
        cls.init_db()
        query = cls._convert_query(query)
        
        connection = None
        try:
            connection = cls.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            if connection:
                connection.rollback()
            print(f"Error en insert: {e}")
            print(f"Query: {query}")
            raise
        finally:
            if connection:
                connection.close()
    
    @classmethod
    def execute_update(cls, query, params=None):
        """
        Ejecuta una consulta UPDATE o DELETE.
        """
        cls.init_db()
        query = cls._convert_query(query)
        
        connection = None
        try:
            connection = cls.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            connection.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            if connection:
                connection.rollback()
            print(f"Error en update/delete: {e}")
            print(f"Query: {query}")
            raise
        finally:
            if connection:
                connection.close()
    
    @classmethod
    def _convert_query(cls, query):
        """Convierte sintaxis MySQL a SQLite."""
        import re
        
        # Reemplazar %s por ? (placeholders)
        query = query.replace('%s', '?')
        
        # Convertir DATE_SUB(CURDATE(), INTERVAL ? DAY) -> date('now', '-' || ? || ' days')
        # La regex busca el patrón completo con posibles espacios
        query = re.sub(
            r"DATE_SUB\s*\(\s*CURDATE\s*\(\s*\)\s*,\s*INTERVAL\s+\?\s+DAY\s*\)",
            "date('now', '-' || ? || ' days')",
            query,
            flags=re.IGNORECASE
        )
        
        # Convertir DATE_SUB(CURDATE(), INTERVAL ? MONTH) -> date('now', '-' || ? || ' months')
        query = re.sub(
            r"DATE_SUB\s*\(\s*CURDATE\s*\(\s*\)\s*,\s*INTERVAL\s+\?\s+MONTH\s*\)",
            "date('now', '-' || ? || ' months')",
            query,
            flags=re.IGNORECASE
        )
        
        # Convertir CURDATE() -> date('now')
        query = re.sub(r"CURDATE\s*\(\s*\)", "date('now')", query, flags=re.IGNORECASE)
        
        # Convertir NOW() -> datetime('now')
        query = re.sub(r"NOW\s*\(\s*\)", "datetime('now')", query, flags=re.IGNORECASE)
        
        # Convertir ON DUPLICATE KEY UPDATE a INSERT OR REPLACE (simplificado)
        # SQLite usa INSERT OR REPLACE o INSERT ... ON CONFLICT
        if 'ON DUPLICATE KEY UPDATE' in query.upper():
            # Simplificar: quitar la parte ON DUPLICATE KEY UPDATE
            query = re.sub(
                r"\s*ON\s+DUPLICATE\s+KEY\s+UPDATE\s+.*$",
                "",
                query,
                flags=re.IGNORECASE | re.DOTALL
            )
            # Cambiar INSERT a INSERT OR REPLACE
            query = re.sub(r"INSERT\s+INTO", "INSERT OR REPLACE INTO", query, flags=re.IGNORECASE)
        
        return query
    
    @classmethod
    def init_db(cls):
        """Inicializa la base de datos con el esquema."""
        if cls._initialized:
            return
            
        connection = cls.get_connection()
        cursor = connection.cursor()
        
        # Crear tablas
        cursor.executescript('''
            -- Tabla de usuarios
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                birth_date DATE,
                gender TEXT CHECK(gender IN ('male', 'female', 'other')),
                height_cm REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Tabla de ejercicios
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                muscle_group TEXT,
                equipment TEXT,
                created_by INTEGER,
                is_custom INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
            );
            
            -- Planes de entrenamiento
            CREATE TABLE IF NOT EXISTS training_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            
            -- Días de entrenamiento
            CREATE TABLE IF NOT EXISTS training_days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_id INTEGER NOT NULL,
                day_of_week INTEGER NOT NULL,
                name TEXT,
                FOREIGN KEY (plan_id) REFERENCES training_plans(id) ON DELETE CASCADE
            );
            
            -- Ejercicios planificados
            CREATE TABLE IF NOT EXISTS planned_exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                training_day_id INTEGER NOT NULL,
                exercise_id INTEGER NOT NULL,
                order_index INTEGER DEFAULT 0,
                target_sets INTEGER,
                target_reps TEXT,
                notes TEXT,
                FOREIGN KEY (training_day_id) REFERENCES training_days(id) ON DELETE CASCADE,
                FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
            );
            
            -- Sesiones de entrenamiento
            CREATE TABLE IF NOT EXISTS workout_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                training_day_id INTEGER,
                session_date DATE NOT NULL,
                start_time TIME,
                end_time TIME,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (training_day_id) REFERENCES training_days(id) ON DELETE SET NULL
            );
            
            -- Series de entrenamiento
            CREATE TABLE IF NOT EXISTS workout_sets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                exercise_id INTEGER NOT NULL,
                set_number INTEGER NOT NULL,
                weight_kg REAL,
                reps INTEGER,
                rpe INTEGER,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES workout_sessions(id) ON DELETE CASCADE,
                FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
            );
            
            -- Alimentos
            CREATE TABLE IF NOT EXISTS foods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                brand TEXT,
                serving_size REAL DEFAULT 100,
                serving_unit TEXT DEFAULT 'g',
                calories REAL,
                protein_g REAL,
                carbs_g REAL,
                fat_g REAL,
                fiber_g REAL,
                created_by INTEGER,
                is_custom INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
            );
            
            -- Objetivos nutricionales
            CREATE TABLE IF NOT EXISTS nutrition_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                calories_target INTEGER,
                protein_target INTEGER,
                carbs_target INTEGER,
                fat_target INTEGER,
                water_target_ml INTEGER DEFAULT 2000,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            
            -- Registro de alimentos
            CREATE TABLE IF NOT EXISTS food_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                food_id INTEGER NOT NULL,
                log_date DATE NOT NULL,
                meal_type TEXT CHECK(meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
                quantity REAL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE
            );
            
            -- Registro de agua
            CREATE TABLE IF NOT EXISTS water_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                log_date DATE NOT NULL,
                liters REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(user_id, log_date)
            );
            
            -- Medidas corporales
            CREATE TABLE IF NOT EXISTS body_measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                measurement_date DATE NOT NULL,
                weight_kg REAL,
                body_fat_percentage REAL,
                chest_cm REAL,
                waist_cm REAL,
                hips_cm REAL,
                bicep_left_cm REAL,
                bicep_right_cm REAL,
                thigh_left_cm REAL,
                thigh_right_cm REAL,
                calf_left_cm REAL,
                calf_right_cm REAL,
                neck_cm REAL,
                shoulders_cm REAL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            
            -- Registro de sueño
            CREATE TABLE IF NOT EXISTS sleep_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                log_date DATE NOT NULL,
                hours_slept REAL NOT NULL,
                sleep_quality INTEGER CHECK(sleep_quality BETWEEN 1 AND 10),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            
            -- Registro menstrual
            CREATE TABLE IF NOT EXISTS menstrual_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                log_date DATE NOT NULL,
                is_period_day INTEGER DEFAULT 1,
                flow_intensity TEXT CHECK(flow_intensity IS NULL OR flow_intensity IN ('light', 'medium', 'heavy')),
                symptoms TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            
            -- Registro de pasos
            CREATE TABLE IF NOT EXISTS step_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                log_date DATE NOT NULL,
                steps INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(user_id, log_date)
            );
        ''')
        
        # Insertar usuario local por defecto si no existe
        cursor.execute("SELECT id FROM users WHERE id = 1")
        if cursor.fetchone() is None:
            cursor.execute('''
                INSERT INTO users (id, username, email, password_hash, first_name)
                VALUES (1, 'Usuario', 'usuario@local.app', 'local', 'Usuario Local')
            ''')
        
        # Insertar ejercicios por defecto si no existen
        cursor.execute("SELECT COUNT(*) FROM exercises")
        if cursor.fetchone()[0] == 0:
            exercises = [
                ('Press de banca', 'Ejercicio de empuje horizontal para pecho', 'Pecho', 'Barra'),
                ('Press inclinado con mancuernas', 'Enfoque en pecho superior', 'Pecho', 'Mancuernas'),
                ('Aperturas con mancuernas', 'Aislamiento de pecho', 'Pecho', 'Mancuernas'),
                ('Dominadas', 'Ejercicio de tirón vertical', 'Espalda', 'Barra fija'),
                ('Remo con barra', 'Tirón horizontal para espalda', 'Espalda', 'Barra'),
                ('Peso muerto', 'Ejercicio compuesto para espalda baja', 'Espalda', 'Barra'),
                ('Sentadilla', 'Ejercicio compuesto para piernas', 'Piernas', 'Barra'),
                ('Prensa de piernas', 'Ejercicio de empuje para cuádriceps', 'Piernas', 'Máquina'),
                ('Curl de bíceps', 'Aislamiento de bíceps', 'Brazos', 'Mancuernas'),
                ('Extensión de tríceps', 'Aislamiento de tríceps', 'Brazos', 'Polea'),
                ('Press militar', 'Ejercicio de empuje vertical', 'Hombros', 'Barra'),
                ('Elevaciones laterales', 'Aislamiento de deltoides lateral', 'Hombros', 'Mancuernas'),
                ('Plancha', 'Ejercicio isométrico para core', 'Core', 'Peso corporal'),
                ('Crunch abdominal', 'Flexión de tronco', 'Core', 'Peso corporal'),
                ('Zancadas', 'Ejercicio unilateral para piernas', 'Piernas', 'Mancuernas'),
            ]
            cursor.executemany('''
                INSERT INTO exercises (name, description, muscle_group, equipment, is_custom)
                VALUES (?, ?, ?, ?, 0)
            ''', exercises)
        
        # Insertar alimentos por defecto si no existen
        cursor.execute("SELECT COUNT(*) FROM foods")
        if cursor.fetchone()[0] == 0:
            foods = [
                ('Pechuga de pollo', None, 100, 'g', 165, 31, 0, 3.6, 0),
                ('Arroz blanco cocido', None, 100, 'g', 130, 2.7, 28, 0.3, 0.4),
                ('Huevo entero', None, 50, 'g', 78, 6, 0.6, 5, 0),
                ('Plátano', None, 100, 'g', 89, 1.1, 23, 0.3, 2.6),
                ('Avena', None, 100, 'g', 389, 17, 66, 7, 11),
                ('Leche entera', None, 100, 'ml', 61, 3.2, 4.8, 3.3, 0),
                ('Pan integral', None, 100, 'g', 247, 13, 41, 3.4, 7),
                ('Atún en lata', None, 100, 'g', 116, 26, 0, 1, 0),
                ('Almendras', None, 100, 'g', 579, 21, 22, 50, 12),
                ('Brócoli', None, 100, 'g', 34, 2.8, 7, 0.4, 2.6),
                ('Pasta cocida', None, 100, 'g', 131, 5, 25, 1.1, 1.8),
                ('Yogur natural', None, 100, 'g', 59, 10, 3.6, 0.7, 0),
                ('Salmón', None, 100, 'g', 208, 20, 0, 13, 0),
                ('Patata cocida', None, 100, 'g', 77, 2, 17, 0.1, 2.2),
                ('Manzana', None, 100, 'g', 52, 0.3, 14, 0.2, 2.4),
            ]
            cursor.executemany('''
                INSERT INTO foods (name, brand, serving_size, serving_unit, calories, protein_g, carbs_g, fat_g, fiber_g, is_custom)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            ''', foods)
        
        connection.commit()
        connection.close()
        cls._initialized = True
        print(f"✓ Base de datos inicializada en: {cls.get_db_path()}")
