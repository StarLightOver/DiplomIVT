import requests
from bs4 import BeautifulSoup
from CSVmodule import *

# Год
year = '2015'

# Раздел: society, politics
section = 'society'

# Временный костыль для разбиения по месяцам
# month0 = '06'
# month1 = 'июня'

# Адрес странички РИА Новости -
# С заданными временными промежутками от 1 января Х года (20190101) до 31 декабря Х года (20191231) -
# С заданным разделом (politics)
# Полгода - 0630
url = 'https://ria.ru/services/tagsearch/?date_start=' + year + '0101&date=' + year + '1231&tags%5B%5D=' + section

# Список с результатами сбора данных
result = []

# Итератор для названий картинок в файловой системе
i = 0

# Делаем запрос на новый блок новостей, пока не дойдем до начала текущего года (начала следующего года)
while True:

    # Запрос к серверу по url
    request = requests.get(url)

    # Передаем полученный html в bs4-функцию
    soup = BeautifulSoup(request.text, features="lxml")

    # Необходимо найти все div, которые хранят ссылку на новость
    div_list = soup.find_all('div', {'class': 'list-item'})

    # Необходимо найти следующий url: если он ссылается на следующий год, то выйти из цикла
    next_url = soup.find('div', {'class': 'list-items-loaded'})['data-next-url']
    if next_url.partition('date=')[-1][0:4] != year: # or (next_url.partition('date=')[-1][4:6] == month0): # Костыль месяцев
        break

    # Перебираем все элементы div, в которых есть новости с картинками
    for list_item in div_list:

        # Найти тег ресурса-фотографии
        source = list_item.find('source')

        # Если есть фотография - найти осталньую информацию сохранить, иначе - пропустить
        if source is not None:
            # Строчка с данными для одной фотографии
            row = []

            # Источник новости
            row.append('РИА Новости')

            # Ссылка на статью
            link_to_news = list_item.find('a', {'class': 'list-item__image'})['href']
            row.append(link_to_news)

            # Рублика
            row.append('Общество')

            # Название статьи
            title = list_item.find('a', {'class': 'list-item__title'}).contents[0]
            row.append(title)

            # Фотография
            pict = requests.get(source['srcset'])
            file_name = '.\\' + section + '_' + year + '\image_' + str(i) + '.jpg'
            with open(file_name, "wb") as file:
                file.write(pict.content)
            row.append(file_name)

            # Добавляем новую строчку в список
            result.append(row)

            i += 1

    # Вытаскиваем ссылку на следующую страницу
    url = 'https://ria.ru' + next_url

    # Сколько загружено фотографий
    print('Загружено - ', str(i))

# !) Необходимо дособирать статьи с последней страницы
# Перебираем все оставшиеся элементы div, при этом проверяем у каждой статьи год
for list_item in div_list:
    # Найти тег ресурса-фотографии
    source = list_item.find('source')

    data = list_item.find('div', {'class': 'list-item__date'}).text
    if data.split(',')[0].split(' ')[-1] == str(int(year)-1): # or (data.split(',')[0].split(' ')[1] == month1): # Костыль месяцев
        break

    # Если есть фотография - найти осталньую информацию сохранить, иначе - пропустить
    if source is not None:
        # Строчка с данными для одной фотографии
        row = []

        # Источник новости
        row.append('РИА Новости')

        # Ссылка на статью
        link_to_news = list_item.find('a', {'class': 'list-item__image'})['href']
        row.append(link_to_news)

        # Рублика
        row.append('Политика')

        # Название статьи
        title = list_item.find('a', {'class': 'list-item__title'}).contents[0]
        row.append(title)

        # Фотография
        pict = requests.get(source['srcset'])
        file_name = '.\\' + section + '_' + year + '\image_' + str(i) + '.jpg'
        with open(file_name, "wb") as file:
            file.write(pict.content)
        row.append(file_name)

        # Добавляем новую строчку в список
        result.append(row)

        i += 1

# Сколько загружено фотографий
print('Загружено - ', str(i))

# Записываем результаты в файл с указанием аттрибута записи
csv_writer(result, 'data_' + section + '_' + year + '.csv', 'a')

