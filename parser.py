import requests
from bs4 import BeautifulSoup
import csv


def string_filtering(stroka):
    """
    Функция фильтрации строки. Переводится в нижний регистр, удаляются все знаки кроме русских и пробела
    :param stroka: входная строка
    :return: выходная строка после фильтрации
    """
    stroka = stroka.lower()
    stroka = stroka.replace("ё", "е")
    answer = ''
    for symbol in stroka:
        if ord(symbol) == 32 or 1072 <= ord(symbol) <= 1103:
            answer += symbol
    answer = answer.replace("  ", " ")
    return answer


# Открываем файл для записи
with open('songs.csv', 'w', newline="") as file:
    writer = csv.writer(file)
    writer.writerow(['Исполнитель', 'Название песни', 'Текст'])

    website = "https://www.litprichal.ru/"
    prefix = "teksty-pesen/"
    performers = ['korol-i-shut', 'vladimir-vysockij', 'smeshariki', 'ddt', 'yurij-shatunov',
                  'ruki-vverhhahaha', 'viktor-coj']
    performers_rus = ['Король и шут', 'Владимир Высоцкий', 'Смешарики', 'ДДТ', 'Юрий Шатунов',
                      'Руки вверх', 'Виктор Цой']

    for performer in performers:
        count = 1
        while count <= 5:
            response = requests.get(website + prefix + performer + '/p' + str(count) + '/')
            main_page = BeautifulSoup(response.text, 'html.parser')
            list_songs = main_page.findAll("a", "blueBig")
            for song in list_songs:
                response = requests.get(website + song.get("href"))
                song_page = BeautifulSoup(response.text, 'html.parser')
                title_song = song_page.find("b", "m153")
                text_song = song_page.find("div", "m207")
                try:
                    text = " ".join(text_song.stripped_strings)
                    text = text[:text.rfind("@") - 1]
                    text = string_filtering(text)
                    title = " ".join(title_song.stripped_strings)
                    title = string_filtering(title)
                    writer.writerow([performers_rus[performers.index(performer)], title, text])
                except:
                    print("Ошибка в ссылке - ", website + song.get("href"))
            if performer == performers[2] or \
                    (count == 2 and performer == performers[4]) or \
                    (count == 3 and performer == performers[6]):
                break
            count += 1
        print("Обработаны песни ", performers_rus[performers.index(performer)])
