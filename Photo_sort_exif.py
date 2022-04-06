import os
from exif import Image
from os.path import getmtime
from datetime import datetime as dt
import shutil
from os import path

def create_move(path, image):
    os.makedirs(path,exist_ok=True)
    shutil.move(image, path)


def create_path_exif(img_date, path_out, mode=1):
    path_year = path_out + '\\' + ((str(img_date.get('datetime'))).split()[0]).split(':')[0]
    path_month = path_year + '\\' + ((str(img_date.get('datetime'))).split()[0]).split(':')[1]
    path_day = path_month + '\\' + ((str(img_date.get('datetime'))).split()[0]).split(':')[2]
    try:
        if mode ==1:
            return path_out
        elif mode ==2:
            return path_year
        elif mode ==3:
            return path_month
        elif mode ==4:
            return path_day
    except:
        print(f"Введty неверный режим работы, {mode} - недопустимое значение")


def create_path_win(image, path_out, mode = 1):
    path_year = path_out + '\\' + (dt.fromtimestamp(getmtime(image)).strftime('%Y'))
    path_month = path_year + '\\' + (dt.fromtimestamp(getmtime(image)).strftime('%m'))
    path_day = path_month + '\\' + (dt.fromtimestamp(getmtime(image)).strftime('%d'))
    try:
        if mode ==1:
            return path_out
        elif mode ==2:
            return path_year
        elif mode ==3:
            return path_month
        elif mode ==4:
            return path_day
    except:
        print(f"Введty неверный режим работы, {mode} - недопустимое значение")


def sort_photo(path_input, path_out, mode_parse): #
    # указываем расширения файлов для поиска и обработки
    type_file = ('jpg','JPG','NEF', 'nef', 'RAW', 'raw', 'PNG', 'png')
    # в цикле собираем все файлы и дириктории
    for i in os.walk(path_input):
        # вытаскивает название файла из полного пути
        for image in i[-1]:
            # если файл имеет расшиерне из указанных в type_file то обрабатывает
            if image.endswith(type_file):
                image = (i[0]+'\\'+image)
                # открываем файл для считывания EXIF
                try:
                    with open(image, 'rb') as image_file:
                        img_date = Image(image_file)
                    if img_date.has_exif:
                # # Если информация о дате съемке присутсвует то обрабатываем
                        if img_date.get('datetime')!= None:
                            create_move(create_path_exif(img_date, path_out, mode_parse), image)
                except Exception as e:
                    print(f'{e} хз что не так {image}')  
                    
                finally:
                    create_move(create_path_win(image, path_out, mode_parse), image) 
                
                    

def main():
    mode_parse = int(input(f'выбор режима раскладывания по каталогам \n'
                f'1- все в кучу (в папку path_out)\n'
                f'2- создает папку с годами и раскладывает на основе полученной информации\n'
                f'3- в папке с годами создает папку с месяцем\n'
                f'4- в папке с годами создает папку с месяцем и в ней разбивка по дням\n'
                f'Введите режим обработки: '))
    
    # указываем папку для поиска и обработки фото
    path_input = input("Введите путь для обрабатываемой папки: ")      

    # указываем папку для сохранения результат
    path_out = input("Введите путь для сохранения фото: ") 
    sort_photo(path_input, path_out, mode_parse) #


if __name__ == "__main__":
    main()


