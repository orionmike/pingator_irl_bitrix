
from config import DB_FILE
from database.database import Base, engine
from database.models import UrlResponce

if __name__ == "__main__":

    if DB_FILE.exists():
        UrlResponce.__table__.drop(engine)

    Base.metadata.create_all(engine)
