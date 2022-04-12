from itertools import count
import os
import shutil
from sre_parse import State
from exif import Image
from os.path import getmtime
from datetime import datetime as dt
from progress.bar import Bar





def create_move(path, image):
    os.makedirs(path,exist_ok=True)
    try:
        shutil.move(image, path)
    except Exception as e:
        print(f'{image} по пути {path} существует')
        if os.stat(image).st_size == os.stat(path + "\\" + image.split("\\")[-1]).st_size:
            new_path = path + "\\" + (image.split("\\")[-1]).split('.')[-2] + '_copy_.' + (image.split("\\")[-1]).split('.')[-1]
            shutil.move(image, new_path )
            print(f'{image} сохранен как {new_path}')
        elif os.stat(image).st_size != os.stat(path + "\\" + image.split("\\")[-1]).st_size:
            new_path = path + "\\" + (image.split("\\")[-1]).split('.')[-2] + '_offsize_.' + (image.split("\\")[-1]).split('.')[-1]
            shutil.move(image, new_path )
            print(f'{image} сохранен как {new_path}')            
            
            
def remove_empty_dir(path_input:str, del_mode:int ):
    if del_mode == 1:
        all_dir = []
        for i in os.walk(path_input):
            all_dir.insert(0,i)
        for dir in all_dir:
            if dir[-1] == [] and dir[-2] == []:
                os.removedirs(dir[0])
            else:
                #print(f'В папке {dir} имеются файлы отличные от изображений')
                continue
    elif del_mode != 0:
        print(f'Выбран неверный режим удаления {del_mode}, '
              f'Пакпи небыли удалены')
    elif del_mode == 0:
        print(f'Выбран режим без удаления ')
          

def create_path_exif(img_date, path_out, mode):
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
        print(f"Введён неверный режим работы, {mode} - недопустимое значение")


def create_path_win(image, path_out, mode):
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
        print(f"Введён неверный режим работы, {mode} - недопустимое значение")


def sort_photo(path_input, path_out, mode_parse, del_mode):
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
                    else:
                        create_move(create_path_win(image, path_out, mode_parse), image)
                        
                except Exception as e:
                    print(f'{e} хз что не так {image}')
                    create_move(create_path_win(image, path_out, mode_parse), image)       

    remove_empty_dir(path_input, del_mode)
 
   
def main():
    mode_parse = int(input(f'выбор режима раскладывания по каталогам \n'
                f'1- все в кучу (в папку path_out)\n'
                f'2- создает папку с годами и раскладывает на основе полученной информации\n'
                f'3- в папке с годами создает папку с месяцем\n'
                f'4- в папке с годами создает папку с месяцем и в ней разбивка по дням\n'
                f'Введите режим обработки: '))
    del_mode = int(input(f"Режим удаления пустых папок после перемещния фото \n"
                        f'0- папки не удаляются\n'
                        f'1- удаляет все пустые папки\n'
                        f'Введите режим удаления: '))
    # указываем папку для поиска и обработки фото
    path_input = input("Введите путь для обрабатываемой папки: ")      

    # указываем папку для сохранения результат
    path_out = input("Введите путь для сохранения фото: ")

    while sort_photo(path_input, path_out, mode_parse, del_mode):
        with Bar('Processing') as bar:
            for i in range(20):
        # Do some work
                bar.next()

    
    print('Все готово!')
    


if __name__ == "__main__":
    main()


