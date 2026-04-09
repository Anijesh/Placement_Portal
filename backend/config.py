class Config:
    SECRET_KEY = "super-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///placement.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "jwt-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = 3600

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/1"
    CACHE_DEFAULT_TIMEOUT = 300