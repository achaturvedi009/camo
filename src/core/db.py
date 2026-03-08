from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import os

DB_DIR = "data"
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "profiles.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

Base = declarative_base()

class ProfileModel(Base):
    __tablename__ = 'profiles'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    icon = Column(String, default="🦊")
    tags = Column(String, default="")  # Comma-separated or JSON
    os_type = Column(String, default="windows")
    camoufox_version = Column(String, nullable=True)
    fingerprint = Column(JSON, nullable=True)

    proxy_enabled = Column(Boolean, default=False)
    proxy_type = Column(String, nullable=True)
    proxy_host = Column(String, nullable=True)
    proxy_port = Column(Integer, nullable=True)
    proxy_username = Column(String, nullable=True)
    proxy_password = Column(String, nullable=True)

    status = Column(String, default="idle")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_used = Column(DateTime, nullable=True)

class CamoufoxVersionModel(Base):
    __tablename__ = 'camoufox_versions'

    version = Column(String, primary_key=True)
    installed = Column(Boolean, default=False)
    install_path = Column(String, nullable=True)
    is_default = Column(Boolean, default=False)
    installed_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
