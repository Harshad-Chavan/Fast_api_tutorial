from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Local sqlite3
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
# Local postgres
SQLALCHEMY_DATABASE_URL = "postgresql://postgres@localhost/TodoApplicationDatabase"

# Create a engine that will connect to the database
# conect args is needed for sqlite3
# engine = create_engine(url=SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# engine for postgres
engine = create_engine(url=SQLALCHEMY_DATABASE_URL)

# create a session that will be binded to the engine created earlier
# instance of a database
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# this will allow us to create Models
Base = declarative_base()
