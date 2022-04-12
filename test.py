import os
import hashlib
from PIL import Image
from os.path import getmtime
from datetime import datetime as dt
import shutil
from os import path







def list_files(path_input):

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

def take_size_file(list_file:list):
    for image in list_file:
        size = os.stat(image).st_size
        print(f'File Size in Bytes is {size} : {image}')
       
def take_MD5(list_file:list):
    for image in list_file:
        md5hash = hashlib.md5(Image.open(image).tobytes())
        print(md5hash.hexdigest(), image)

def remove_empty_dir(path_input:str ):
    all_dir = []
    for i in os.walk(path_input):
        all_dir.insert(0,i)
    for dir in all_dir:
        if dir[-1] == [] and dir[-2] == []:
            os.removedirs(dir[0])
        else:
            print(f'В папке {dir} имеются файлы отличные от изображений')
            continue
        



def main():
    path_input = input("Введите путь для обрабатываемой папки: ")
    #take_name_date(list_files(path_input))
    #take_MD5(list_files(path_input))
    remove_empty_dir(path_input)
    
    


if __name__ == "__main__":
    main()