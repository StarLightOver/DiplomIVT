import cv2
import os.path
from CSVmodule import *

# Целевой год
year = 2019

# Название csv-файла со старшим годом
filename = './data_politics_%d.csv' % year

# Пока есть csv-файлы, ищем
while os.path.exists(filename):
    print('Данные по \"' + filename + '\" загружены.\n')

    # Чтение csv-файла
    data = csv_reader(filename)

    # Для каждой строчки в файле
    for row in data:
        if not os.path.exists(row[-1]):
            print(row)

    # Переход к следующему году
    year -= 1
    filename = './data_politics_%d.csv' % year

