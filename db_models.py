import os

from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    pass



class Photos(Base):
    """
    Описание таблицы для хранения id изображений телеграма, чтобы каждый раз
    не скачивать заново
    """
    __tablename__ = 'photos'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    article_id: Mapped[int] = mapped_column(unique=False)
    photo_id: Mapped[str] = mapped_column(String(128))



# создание файла базы данных, если отсутствует
if not os.path.exists('database.db'):
    engine = create_engine("sqlite+pysqlite:///database.db", echo=True)
    Base.metadata.create_all(engine)

