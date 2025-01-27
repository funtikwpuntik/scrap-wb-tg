from typing import Dict
import aiohttp
from aiohttp.web_exceptions import HTTPNotFound

from utils.loggers import error_logger

@error_logger
class Article:
    """
    Описаны методы для взаимодействия с WB
    """

    def __init__(self, article_id):
        self._available = False
        self.article_id = article_id

    @property
    def article_id(self):
        return self._article_id

    @property
    def available(self):
        return self._available

    @article_id.setter
    def article_id(self, article_id):
        if isinstance(article_id, str):
            if not article_id.isdigit():
                raise ValueError("Артикул должен быть целым, положительным числом, например: 12345678")
        self._article_id = int(article_id)

    @staticmethod
    def get_host(vol: int):
        """
        Метод для получения хоста
        :param vol:
        :return:
        """
        if 0 <= vol <= 143:
            return '01'
        if vol <= 287:
            return '02'
        if vol <= 431:
            return '03'
        if vol <= 719:
            return '04'
        if vol <= 1007:
            return '05'
        if vol <= 1061:
            return '06'
        if vol <= 1115:
            return '07'
        if vol <= 1169:
            return '08'
        if vol <= 1313:
            return '09'
        if vol <= 1601:
            return '10'
        if vol <= 1655:
            return '11'
        if vol <= 1919:
            return '12'
        if vol <= 2045:
            return '16'
        if vol <= 2189:
            return '14'
        if vol <= 2405:
            return '15'
        if vol <= 2621:
            return '16'
        if vol <= 2837:
            return '17'
        if vol <= 3053:
            return '18'
        if vol <= 3269:
            return '19'
        if vol <= 3485:
            return '20'

        return '21'

    def _get_url(self, article: int, s: str or int = 'info'):
        """
        Метод для генерации ссылки на информацию и изображения
        :param article: артикул ВБ
        :param s: флаг для скачивания изображений
        :return:
        """
        vol, part = int(article / 1e5), int(article / 1e3)
        host = self.get_host(vol)
        return (f"https://basket-{host}.wbbasket.ru/vol{vol}/part{part}/{article}"
                f"{'/info/ru/card.json' if s == 'info' else f'/images/big/{s}.webp'}")

    async def scrap_wb(self):
        """
        Парсинг данных в 2 захода (информация на разных эндпоитах)
        :return:
        """
        async with aiohttp.ClientSession() as session:
            first_url = self._get_url(article=self._article_id)

            async with session.get(url=first_url) as r:

                if r.status == 404:
                    raise HTTPNotFound(text=first_url)

                first_data = await r.json()

            second_url = f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={self._article_id}'
            async with session.get(url=second_url) as r:

                if r.status == 404:
                    raise HTTPNotFound(text=second_url)

                second_data = await r.json()

                if len(second_data['data']['products']) == 0:
                    raise IndexError(f'Нет данных\turl: {second_url}')

        self._available = True

        return self._add_data(fd=first_data, sd=second_data['data']['products'][0])

    def _add_data(self, fd: Dict, sd: Dict):
        """
        Добавляет полученные значения как атрибуты класса
        :param fd: Первая часть данных
        :param sd: Вторая часть данных
        :return:
        """
        data = {
            'title': fd['imt_name'],
            'category': fd['subj_name'],
            'price': sd['salePriceU'] // 100,
            'images': [self._get_url(self._article_id, num) for num in range(1, fd['media']['photo_count'] + 1)],
            'options': fd['options'],
            'description': fd['description'].replace('\n', ' '),
            'rating': float(sd['reviewRating']),
            'feedbacks': sd['nmFeedbacks'],
        }

        for key, value in data.items():
            setattr(self, key, value)
        return data

    @property
    def get_data(self):
        """
        Возвращает словарь атрибутов (кроме _available)
        :return:
        """
        return {k: v for k, v in self.__dict__.items() if not isinstance(v, bool)}
