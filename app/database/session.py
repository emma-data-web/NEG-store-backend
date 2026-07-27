from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import Settings

engine = create_engine(Settings.DATABASE_URL, 
pool_size=5,
max_overflow=10,
pool_pre_ping=True,
connect_args={"check_same_thread": False})
SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)