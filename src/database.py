from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

class DatabaseConfig(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=DatabaseConfig):
    def __init__(self):
        self.url = "postgresql://user:password@db/appdb"

engine = create_engine(Config().url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()