import os
import shlex  # Для получения параметров
import shutil

def f_name(file_name):
    '''Проверка на корректность имени файла'''
    pat = '@!№;%$:?*\'\",'
    for x in pat:
        if x in file_name:
            return False
    return True

def get_part(path, type_data=3):
    '''Получить из указанного пути
    0 - путь без имени файла
    1 - только имя файла
    2 - только расширение с точкой
    3 - имя + расширение'''
    if type_data == 0:
        return os.path.dirname(path)
    elif type_data == 1:
        return os.path.splitext(os.path.basename(path))[0]
    elif type_data == 2:
        return os.path.splitext(os.path.basename(path))[1]
    elif type_data == 3:
        return f'{os.path.splitext(os.path.basename(path))[0]}{os.path.splitext(os.path.basename(path))[1]}'


def f_help():
    print(f' Справка по командам ')
    print(f'* Внимание! Если в параметрах есть пробелы, то возьмите их в кавычки')
    print(f'* Внимание! Если в параметрах не указать полный путь, то действие будет применено в каталоге по умоланию\n')
    print('exit Выход из программы \n'
          'help Справка по командам \n'
          'dir - показать содержимое каталога по умолчанию; \n  '
          'dir c:\kat - показать содержимое указанного каталога \n'
          'cd  c:\kat           - сменить каталог по умолчанию; \n  '
          'cd "c:\Новая папка" - сменить каталог по умолчанию;\n'
          'cfile d:\data1.txt     - создать файл; \n  '
          'cfile data1.txt        - создать файл в каталоге по умолчанию; \n  '
          'cfile "d:\data 1.txt"  - создать файл с пробелом в имени;\n'
          'mkdir d:\Folder     - создать каталог; \n  '
          'mkdir Folder        - создать каталог в каталоге по умолчанию; \n  '
          'mkdir "d:\Folder 2" - создать каталог с пробелом в имени; \n'
          'copy D:\Test\Каталог1 D:\Test\Каталог2        - копировать каталог; \n  '
          'copy "D:\Test\Каталог 1" "D:\Test\Каталог 2"  - копировать каталог с пробелом в имени; \n  '
          'copy new.txt "D:\Test\Каталог 2"              - копировать файл из каталога по умолчанию; \n'
          'move D:\Test\Каталог1 D:\Test\Каталог2        - переместить каталог; \n  '
          'move "Каталог 1" "D:\Test\Каталог 2"          - переместить каталог с пробелом в имени; \n  '
          'move new.txt "D:\Test\Каталог 2"              - переместить файл из каталога по умолчанию;\n'
          'del c:\kat      - удалить каталог; \n  '
          'del c:\doc.txt  - удалить файл; \n  '
          'del doc.txt     - удалить файл в каталоге по умолчанию'
          )

def f_dir(path=None):
    '''Печать содержимого указанного каталога, по умолчанию текущего'''
    if not path:
        path = os.getcwd()
    path = f'{path}\\'  # Для корректного отображения: d: или d:\
    if not os.path.exists(path):
        er_tit = 'Не найден каталог'
        print(f'{er_tit}: {path}')
        return er_tit
    lst_dir = os.listdir(path)
    print(f'Содержимое каталога: {path}')
    for i, x in enumerate(lst_dir):
        print(f'{i + 1:>4}. {x}')
    return 'Каталог найден'

def cd(path):
    '''Изменить каталог по умолчанию'''
    if not os.path.exists(path):
        er_tit = 'Не найден каталог'
        print(f'{er_tit}: {path}')
        return er_tit
    os.chdir(path)
    er_tit = 'Был изменен каталог по умолчанию'
    print(f'{er_tit}')
    return er_tit

def f_create_file(path):
    '''Создать файл'''
    if not '\\' in path and not '/' in path:  # Если указан файл в текущем каталоге
        path = f'{defc()}\\{path}'
    if not os.path.exists(get_part(path, 0)):
        er_tit = 'Не найден путь'
        print(f'{er_tit}: {get_part(path, 0)}')
        return er_tit
    if not f_name(get_part(path)):
        er_tit = 'Не корректное имя'
        print(f'{er_tit}: {get_part(path)}')
        return er_tit
    # Создать файл
    try:
        with open(fr'{path}', 'w') as file:
            pass
    except Exception as e:
        print(f'Ошибка создания файла, {e.__class__} {e.__str__()}')
    er_tit = 'Файл был удачно создан'
    print(f'{er_tit}: {path}')
    return er_tit

def f_create_dir(path):
    '''Создать каталог'''
    if not '\\' in path and not '/' in path:  # Если указан каталог в текущем каталоге
        path = f'{os.getcwd()}\\{path}'
    if not os.path.exists(get_part(path, 0)):
        er_tit = 'Не найден путь'
        print(f'{er_tit}: {get_part(path, 0)}')
        return er_tit
    if not f_name(get_part(path)):
        er_tit = 'Не корректное имя'
        print(f'{er_tit}: {get_part(path)}')
        return er_tit
    # Создать файл
    try:
        os.mkdir(path)
    except Exception as e:
        print(f'Ошибка создания каталога, {e.__class__} {e.__str__()}')
    er_tit = 'Каталог был удачно создан'
    print(f'{er_tit}: {path}')
    return er_tit

def f_copy(a, b):
    '''Копировать файл или каталог'''
    # Проверка на существование
    if not os.path.exists(a):
        a = f'{os.getcwd()}\\{a}'  # Добавить каталог по умолчанию перед именем
    if not os.path.exists(a):
        er_tit = 'Не найден откуда копировать'
        print(f'{er_tit}: {a}')
        return er_tit
    if not os.path.exists(get_part(b, 0)):
        er_tit = 'Не найден каталог куда копировать'
        print(f'{er_tit}: {b}')
        return er_tit
    if not f_name(get_part(b)):
        er_tit = 'Не корректное имя куда копировать'
        print(f'{er_tit}: {get_part(b)}')
        return er_tit
    # Узнать файл или каталог
    if os.path.isfile(a):
        if os.path.isdir(b):  # Если куда копировать каталог
            b = f'{b}\\{get_part(a)}'  # Добавить имя файла
        if os.path.exists(b):
            er_tit = 'Куда копировать уже существует'
            print(f'{er_tit}: {b}')
            return er_tit
        shutil.copy2(a, b)
        er_tit = 'Файл был удачно скопирован'
        print(er_tit)
    else:
        if get_part(a) != get_part(b):
            b = f'{b}\\{get_part(a)}'
        if os.path.exists(b):
            er_tit = 'Куда копировать уже существует'
            print(f'{er_tit}: {b}')
            return er_tit
        shutil.copytree(a, b)
        er_tit = 'Каталог был удачно скопирован'
        print(er_tit)
    return er_tit

def f_move(a, b):
    '''Копировать файл или каталог'''
    # Проверка на существование
    if not os.path.exists(a):
        a = f'{os.getcwd()}\\{a}'  # Добавить каталог по умолчанию перед именем
    if not os.path.exists(a):
        er_tit = 'Не найден откуда переместить'
        print(f'{er_tit}: {a}')
        return er_tit
    if not os.path.exists(get_part(b, 0)):
        er_tit = 'Не найден каталог куда переместить'
        print(f'{er_tit}: {b}')
        return er_tit
    if not f_name(get_part(b)):
        er_tit = 'Не корректное имя куда копировать'
        print(f'{er_tit}: {get_part(b)}')
        return er_tit
    # Узнать файл или каталог
    if os.path.isfile(a):
        if os.path.isdir(b):  # Если куда копировать каталог
            b = f'{b}\\{get_part(a)}'  # Добавить имя файла
        if os.path.exists(b):
            er_tit = 'Куда переместить уже существует'
            print(f'{er_tit}: {b}')
            return er_tit
        shutil.move(a, b)
        er_tit = 'Файл был удачно перемещен'
        print(er_tit)
    else:
        if get_part(a) != get_part(b):
            b = f'{b}\\{get_part(a)}'
        if os.path.exists(b):
            er_tit = 'Куда переместить уже существует'
            print(f'{er_tit}: {b}')
            return er_tit
        shutil.copytree(a, b)
        shutil.rmtree(a)
        er_tit = 'Каталог был удачно перемещен'
        print(er_tit)
    return er_tit

def f_del(path):
    '''Удалить файл или каталог
    '''
    if os.path.exists(path):
        if os.path.isfile(path):
            try:
                os.remove(path)
            except Exception as e:
                print(f'Ошибка выполнения команды удаления, {e.__class__} {e.__str__()}')
        else:
            try:
                shutil.rmtree(path)
            except Exception as e:
                print(f'Ошибка выполнения команды удаления, {e.__class__} {e.__str__()}')
    er_tit = 'ОК'
    print(er_tit)
    return er_tit

def del_end_slash(line: str):
    '''Удалить концевой слэш '\' в строке, если он есть '''
    if not line:
        return line
    if line.strip()[-1] == '\\':
        return line[:-1]
    return line

def main():
    print('Введите help для справки по командам')
    while True:
        print(os.getcwd())
        s = del_end_slash(input(r' > ').strip()).replace('\\', '\\\\')
        try:
            lst = shlex.split(s)
        except:
            print('Неправильная команда')
            continue
        if not lst:  # Если ничего не введено
            continue
        coman = lst[0]
        coman1 = None
        if len(lst) > 1:
            coman1 = del_end_slash(lst[1]).replace('\\', '\\\\')
            if len(lst) == 3:
                coman2 = del_end_slash(lst[2]).replace('\\', '\\\\')
        try:
            match coman:
                case 'help':
                    f_help()
                case 'cd':
                    cd(coman1)
                case 'dir':
                    f_dir(coman1)
                case 'mkdir':
                    f_create_dir(coman1)
                case 'del':
                    f_del(coman1)
                case 'cfile':
                    f_create_file(coman1)
                case 'copy':
                    f_copy(coman1,coman2)
                case 'move':
                    f_move(coman1,coman2)
                case 'exit':
                    break
                case _:
                    print('Не верная команда')
        except Exception as e:
            print(f'Ошибка выполнения команды: {coman}')

        print()

main()