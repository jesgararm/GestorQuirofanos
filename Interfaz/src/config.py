class Config():
    SECRET_KEY = 'gestorQuirofanosUBU'
class DevelopmentConfig(Config):
    DEBUG = True
    MY_SQL_HOST = 'localhost'
    MY_SQL_USER = 'root'
    MY_SQL_PASSWORD = 'ubutfg'
    MY_SQL_DB = 'gestor_quirofanos'

config = {
    'development': DevelopmentConfig
}