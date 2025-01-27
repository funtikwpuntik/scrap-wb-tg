import csv

def dict_to_data(data: dict) -> str:
    """
    Сборка текста для отправки в телеграмм
    :param data:
    :return:
    """
    options = '\n- '.join([f"{item['name']}: {item['value']}" for item in data['options']])
    return (f"Артикул: {data['_article_id']}\n"
            f"Название: {data['title']}\n"
            f"Категория: {data['category']}\n"
            f"Цена: {data['price']}\n"
            f"Характеристики: {options}\n\n"
            f"Описание: {data['description']}\n\n"
            f"Рейтинг: {data['rating']}\n"
            f"Кол-во отзывов: {data['feedbacks']}\n")



def to_csv(data: list[list]):
    """
    Создание csv файла
    :param data:
    :return:
    """
    with open('data.csv', 'w', newline='') as csvfile:
        f = csv.writer(csvfile, delimiter=',',)

        f.writerows(data)


