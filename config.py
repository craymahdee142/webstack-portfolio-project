#import os
#from dotenv import load_dotenv
#load_dotenv()  # Load environment variables from a .env file


class Config:
    SECRET_KEY = 'd7c4825219dd0809f67ef0ec321534a2c3a961cb2f0b2c9552efb32a875d31f2eab159f3ba0740979dd176d139884502df567d8665b964d3932ca9bd0c06e22a'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.hotel_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    # Email config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'craydee123@gmail.com'
    MAIL_PASSWORD = 'jtsy hxfw ljly vnah'
    
   # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
   # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # For production env
    #from secrets import token_hex
    #SECRET_KEY = os.getenv('SECRET_KEY', token_hex(16))