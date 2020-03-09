import os

TITLE = os.getenv("TITLE", "OJ backend")
VERSION = "0.0.1"
DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://postgres:password@localhost:5432/oj")
PASSWORD_SALT = os.getenv("PASSWORD_SALT", "mjUSyfaZw5A=")
JWT_KEY = os.getenv("JWT_KEY", "031d9dba928bfcbe908efa0f9eced79bcf8a47c8a2d9c453ccb7fe7a3162a46f")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_SECONDS = 60 * 24 * 8
ALLOWED_EXTENSIONS = ["zip", "tar", "c"]
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
