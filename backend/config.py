import os

class Config:
    """Base configuration"""
    # MySQL Database Configuration
    # Format: mysql+pymysql://username:password@localhost/database_name
    # For special characters in password, use URL encoding (@ = %40)
    
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost/student_erp'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Connection pool configuration for better performance
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 20,
    }
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'erp_secret_key')
    

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/student_erp_test'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
