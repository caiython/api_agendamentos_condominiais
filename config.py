class Config():
    # Database Config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

    # Flask Config
    SECRET_KEY = '123456'

    # Debug Mode
    DEBUG = True

    #Basic Auth
    BASIC_AUTH_USERNAME = 'admin'
    BASIC_AUTH_PASSWORD = '12345'