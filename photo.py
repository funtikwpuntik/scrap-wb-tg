import aiohttp
import os

from loggers import error_logger
from storage import Storage

@error_logger
class Photo:
    """
    Взаимодействие с изображениями
    """
    def __init__(self):
        self.filenames = []
        self.storage = Storage()

    async def download_photos(self, urls: list):
        """
        Скачивания изображений
        :param urls: ссылки на изображения
        :return:
        """
        async with aiohttp.ClientSession() as session:
            for url in urls[:10]:
                async with session.get(url=url) as r:
                    filename = url.split('/')[-4] + '_' + url.split('/')[-1]
                    with open(filename, 'wb') as f:
                        f.write(await r.read())

                    self.filenames.append(filename)
        return self.filenames

    def get_photo_ids(self, article_id: int):
        """
        Получение id уже загруженных изображений в телеграмм
        :param article_id: артикул ВБ
        :return:
        """
        return self.storage.get_photo_ids(article_id=article_id)

    def add_photo_ids(self, article_id: int, photo_ids: list):
        """
        Сохранение id загруженных изображений
        :param article_id: артикул ВБ
        :param photo_ids: id изображений в телеграмме
        :return:
        """
        return self.storage.add_photo_ids(article_id=article_id, photo_ids=photo_ids)

    def __del__(self):
        for filename in self.filenames:
            os.remove(filename)