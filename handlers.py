from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, InputMediaDocument
import os
from aiogram.utils.media_group import MediaGroupBuilder
from dotenv import load_dotenv
from bot import bot
from article import Article
from google_sheet import GoogleSheet
from loggers import error_logger
from photo import Photo
from utils import dict_to_data, to_csv

load_dotenv()
router = Router()


TABLE_KEY = os.environ['TABLE_KEY']

# Команда start, она же выдает токен при активации бота
@router.message(Command('start'))
async def start(message: Message):
    await message.answer(f'Привет! Отправь мне артикул вб, я соберу данные в удобном формате.')

@error_logger
@router.message(Command('exp'))
async def exp(message: Message):
    """
    Реализация команды получения csv файла таблицы
    :param message:
    :return:
    """
    ans_message = await message.answer('Загрузка...')
    gc = GoogleSheet(TABLE_KEY)
    data = await gc.get_values()
    to_csv(data)
    file = InputMediaDocument(media=FSInputFile(filename='data.csv', path='data.csv'))
    await ans_message.edit_media(media=file)

@error_logger
@router.message()
async def check_article(message: Message):
    """
    Обработка артикула, отправленного в телеграме
    :param message:
    :return:
    """
    ans_message = await message.answer('Загрузка...')
    try:
        art = Article(message.text)
    except ValueError as ex:
        await ans_message.edit_text(text=str(ex))
        return

    await art.scrap_wb()
    if art.available:
        data = art.get_data
        text = dict_to_data(data=data)

        await ans_message.edit_text(text=text)
        try:
            gc = GoogleSheet(TABLE_KEY)
            type_article = await gc.update_values(art.get_data)
        except Exception as ex:
            await message.answer(text='Ошибка подключение к google, таблица не обновлена')
            return

        photo = Photo()
        media_group = MediaGroupBuilder(caption='')
        if type_article == 'add':
            filenames = await photo.download_photos(data['images'])
            for filename in filenames[:10]: # Ограничение по фотографиям, т.к в телеграме больше 10 нельзя отправить
                image = FSInputFile(path=filename, filename=filename)
                media_group.add_photo(media=image)

            raw_photo_data = await bot.send_media_group(chat_id=message.chat.id, media=media_group.build())

            photo_ids = [i.photo[-1].file_id for i in raw_photo_data]
            photo.add_photo_ids(article_id=data['_article_id'], photo_ids=photo_ids)

        elif type_article == 'update':

            photo_ids = photo.get_photo_ids(data['_article_id'])
            for photo_id in photo_ids[:10]:
                media_group.add_photo(media=photo_id['photo_id'])

            await bot.send_media_group(chat_id=message.chat.id, media=media_group.build())

    else:
        await ans_message.edit_text('Нет данных')