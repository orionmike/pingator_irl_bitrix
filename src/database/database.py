
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DB_FILE

Base = declarative_base()

engine = create_engine(f"sqlite:///{DB_FILE}", echo=False, future=True)

session_maker = sessionmaker(bind=engine)
session = session_maker()
