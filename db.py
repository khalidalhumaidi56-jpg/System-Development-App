import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Add this line - this is what models.py is looking for
Base = declarative_base()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
db_name = os.getenv("DB_NAME")
host = os.getenv("DB_HOST")

if host and host.startswith('/cloudsql'):
    db_url = f"mysql+pymysql://{user}:{password}@/{db_name}?unix_socket={host}"
elif user and password and db_name:
    local_host = host if host else "127.0.0.1"
    db_url = f"mysql+pymysql://{user}:{password}@{local_host}/{db_name}"
else:
    # Fallback to SQLite for local development
    db_url = "sqlite:///./app.db"

engine = create_engine(db_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)