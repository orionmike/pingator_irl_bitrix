from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class UrlResponce(Base):

    __tablename__ = 'responce'
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    status_code: Mapped[Optional[int]]
    datetime_update: Mapped[datetime] = mapped_column(default=datetime.now())
