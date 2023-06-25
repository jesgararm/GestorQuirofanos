class Config():
    SECRET_KEY = 'gestorQuirofanosUBU'
    

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'ubutfg'
    MYSQL_DB = 'gestor_quirofanos'
    
'''    
class DevelopmentConfig(Config):
    DEBUG = False
    MYSQL_HOST = 'gestor-quirofanos.cjyrpxu1dtey.eu-north-1.rds.amazonaws.com'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'gestorquirofanos'
    MYSQL_DB = 'gestor_quirofanos'
'''
config = {
    'development': DevelopmentConfig
}