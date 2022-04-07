import os
from exif import Image
from os.path import getmtime
from datetime import datetime as dt
import shutil
from os import path





def list_files(path_input):
    """_summary_

    Args:
        path_input (str): путь до обрабатываемой папки

    Returns:
        list: список всех путей до файлов
    """
    #типы файлов для поиска
    type_file = ('jpg','JPG','NEF', 'nef', 'RAW', 'raw', 'PNG', 'png')
    # список полных путей до файла
    list_file=[]
    for i in os.walk(path_input):
        # вытаскивает название файла из полного пути
        for image in i[-1]:
            # если файл имеет расшиерне из указанных в type_file то обрабатывает
            if image.endswith(type_file):
                image = (i[0]+'\\'+image.strip())
                list_file.append(image)
    return list_file


def take_name_date(list_file:list):    
    for image in list_file:
        data = dt.fromtimestamp(getmtime(image)).strftime('%Y, %m')
        print(f'{image} создан: {data}')


def main():
    path_input = input("Введите путь для обрабатываемой папки: ")
    take_name_date(list_files(path_input))


if __name__ == "__main__":
    main()