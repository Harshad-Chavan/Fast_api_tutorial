from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create a engine that will connect to the database
engine = create_engine(url=SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# create a session that will be binded to the engine created earlier
# instance of a database
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# this will allow us to create Models
Base = declarative_base()
