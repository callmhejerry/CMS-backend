from os import getenv
class Config():
    """class for all configuration"""
    SQL_ALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY = getenv('SECRET_KEY') or 'cms_secret_key'
    environment = 'development'


class Development(Config):
    """development environment"""
    SQLALCHEMY_DATABASE_URI = 'mysql://cms_dev:cms_dev_pwd@localhost/church_management_system_dev'


class Testing(Config):
    """testing environment"""
    SQSQLALCHEMY_DATABASE_URI = 'mysql://cms_test:cms_test_pwd@localhost/church_management_system_test'
    environment = 'testing'

class Production(Config):
    """production environment"""
    db = getenv('CMS_DB')
    user = getenv('CMS_USER')
    password = getenv('CMS_PASSWORD')
    host = getenv('DB_HOST')
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(user, password, host, db)
    environment = 'production'
    
config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}
