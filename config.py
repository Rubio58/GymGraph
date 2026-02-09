"""
Configuración de la aplicación GymGraph
Aplicación de escritorio local con SQLite
"""

import os


class Config:
    """Configuración base de la aplicación."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gymgraph-local-app-secret-key'
    
    # SQLite - Base de datos local (no requiere configuración externa)
    # La base de datos se crea automáticamente en la carpeta 'data/'


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True


class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
