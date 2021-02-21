import cv2
import os.path
from CSVmodule import *

# Целевой год
year = 2019

# Название csv-файла со старшим годом
filename = './data_politics_%d.csv' % year

# Конфигурация для классификатора из openCV
face_cascade = cv2.CascadeClassifier('.\haarcascade_face.xml')

# Список, содержащий новости с изображения без "крупного плана"
no_close_up = []

# Индекс изображения
count = 0

# Пока есть csv-файлы, ищем
while os.path.exists(filename):
    print('Данные по \"' + filename + '\" загружены.\n')

    # Чтение csv-файла
    data = csv_reader(filename)

    # Для каждой строчки в файле
    for row in data:
        # Для отбрасывания "битых изображений"
        try:
            # Загружаем картинку
            image = cv2.imread(row[-1])

            # Накладываем фильтр "оттенки серого"
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception:
            print('Warning - ', row)
            continue

        # Функция нахождения лица на изображения
        # grey  - это входное изображение в оттенках серого.
        # scaleFactor - параметр, определяющий размер изображения при каждой шкале изображения.
        # minNeighbors - параметр, указывающий, сколько соседей должно иметь каждый прямоугольник кандидата,
        # чтобы сохранить его. Более высокое число дает более низкие ложные срабатывания.
        # minSize - минимальный размер прямоугольника, который считается лицом.
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=6,
            minSize=(40, 40)
        )

        # Усли необходимо вывести лицо на экран - рисуется синий прямоугольник
        # for [x, y, w, h] in faces:
        #     cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #     roi_gray = gray[y:y + h, x:x + w]
        #     roi_color = image[y:y + h, x:x + w]

        # Если нет "крупного плана", то добавляем в список
        if isinstance(faces, tuple):
            # Сохраняем изображение
            cv2.imwrite('./no_close_up_politics_all_year/image_%d.jpg' % count, image)

            # Изменяем адрес изображения
            row[-1] = './no_close_up_politics_all_year/image_%d.jpg' % count

            # Добавляем строчку в новый список
            no_close_up.append(row)
            count += 1

        # Отображение на экране изображения с распознаным лицом, подходящим под крупный план
        # cv2.imshow('image', image)

    # Запись в файл часть данных за один год
    csv_writer(no_close_up, 'data_no_close_up_politics_all_year.csv', 'a')

    print('Данные по \"' + filename + '\" обработаны.\n')

    # Переход к следующему году
    year -= 1
    filename = './data_politics_%d.csv' % year

# cv2.destroyAllWindows()

