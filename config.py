import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = f"postgresql://quickep_admin:MiGoLeOn%40%40_7@quickep-db.postgres.database.azure.com:5432/postgres"
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
