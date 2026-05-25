from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Note: This is an example URL. Change the username, password, host, port, and db name.
DATABASE_URL = "postgresql://postgres:iamgroot@localhost:5432/tutOne"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a sessionmaker which will be used to create session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Modern SQLAlchemy 2.0 Base class
class Base(DeclarativeBase):
    pass
