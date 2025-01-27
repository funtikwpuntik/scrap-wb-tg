from sqlalchemy import create_engine, select, insert

from db_models import Photos
from loggers import error_logger


@error_logger
class Storage:
    """
    Взаимодействие с бд
    """
    def __init__(self):
        self.engine = create_engine("sqlite+pysqlite:///database.db", echo=True)
        self.session = self.engine.connect()

    def get_photo_ids(self, article_id: int):
        """
        Получение id изображений
        :param article_id: артикул ВБ
        :return:
        """
        data = self.session.execute(
            select(Photos.photo_id).where(Photos.article_id == article_id)
        ).mappings().all()
        self.session.close()
        return data

    def add_photo_ids(self, article_id: int, photo_ids: list):
        """
        Сохранение изображений
        :param article_id: артикул ВБ
        :param photo_ids: id изображений телеграмма
        :return:
        """
        self.session.execute(
            insert(Photos), [{'article_id': article_id, 'photo_id': photo_id} for photo_id in photo_ids]
        )
        self.session.commit()
        self.session.close()