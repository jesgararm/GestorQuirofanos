class Config():
    SECRET_KEY = 'gestorQuirofanosUBU'
class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'ubutfg'
    MYSQL_DB = 'gestor_quirofanos'

config = {
    'development': DevelopmentConfig
}