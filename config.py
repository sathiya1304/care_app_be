import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', '')}"
        f"@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}"
        f"/{os.getenv('DB_NAME', 'care_analysedb')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY", "")
    ADMIN_MOBILE = os.getenv("ADMIN_MOBILE", "9876543210")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
