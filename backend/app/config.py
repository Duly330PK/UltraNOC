import os
class Settings:
    PROJECT_NAME = "UltraNOC"
    DB_URL = os.getenv("DATABASE_URL", "postgresql://root:root@localhost/ultranoc")
settings = Settings()