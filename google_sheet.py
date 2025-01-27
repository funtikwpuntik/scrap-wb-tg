import gspread_asyncio
from google.oauth2.service_account import Credentials
from loggers import error_logger

@error_logger
class GoogleSheet:
    """
    Класс взаимодействия с google аблицами
    """
    def __init__(self, table_key: str):
        self.credentials_file = "service.json"
        self.agcm = gspread_asyncio.AsyncioGspreadClientManager(self._get_credentials)
        self.table_key = table_key

    def _get_credentials(self):
        """
        Получение настроек авторизации
        :return:
        """
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_file(self.credentials_file, scopes=scopes)
        return creds

    async def open_spreadsheet(self, table_key: str):
        """
        Открыть таблицу по ключу
        :param table_key: ключ таблицы
        :return:
        """
        agc = await self.agcm.authorize()
        spreadsheet = await agc.open_by_key(table_key)
        return spreadsheet

    async def get_worksheet(self, table_key: str, worksheet_index: int = 0):
        """
        Получение конкретного листа из таблицы.
        :param table_key: ключ таблицы
        :param worksheet_index: индекс листа
        :return:
        """
        spreadsheet = await self.open_spreadsheet(table_key)
        worksheet = await spreadsheet.get_worksheet(worksheet_index)
        return worksheet

    async def check_article(self, article_id: int):
        """
        Проверка наличия артикула в таблице
        :param article_id: артикул ВБ
        :return:
        """
        ws = await self.get_worksheet(self.table_key, 0)
        row = await ws.find(str(article_id), in_column=1)
        return row

    async def update_values(self, data: dict):
        """
        Метод добавления/обновление данных в таблицу
        :param data: словарь с данными
        :return:
        """
        ws = await self.get_worksheet(self.table_key, 0)
        update_data = [item if type(item) != list else ', '.join(str(i) for i in item) for key, item in data.items()]
        row = await self.check_article(update_data[0])
        if row:
            await ws.update([update_data], f'A{row.row}:I{row.row}')
            return 'update'
        await ws.append_row(update_data)
        return 'add'


    async def get_values(self):
        """
        Получение данных с таблицы для экспорта в csv
        :return:
        """
        ws = await self.get_worksheet(self.table_key, 0)
        list_values = await ws.get_all_values()
        return list_values