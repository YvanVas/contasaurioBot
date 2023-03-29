import os

PATH_DIR = 'Z:/r90/'


def create_directory(dir_name: str, month=None, start_month=None, end_month=None):

    dir = PATH_DIR+dir_name

    if os.path.exists(dir):
        print('La carpeta ya existe!')
    else:
        os.mkdir(dir)
        print('Carpeta creada')

        if month is not None:
            subdir = dir + '/' + month
            os.mkdir(subdir)
            print('Subcarpeta creada en: ', subdir)

        if start_month and end_month is not None:

            for i in range(start_month, end_month+1):
                dir_month = dir + '/' + '0'+str(i)
                os.mkdir(dir_month)

                print('Subcarpetas creada: ', dir_month)


def create_subdir(dir_name, start_month=None, end_month=None):

    dir = PATH_DIR+dir_name

    subs_dir = ''
    if start_month and end_month is not None:

        for i in range(start_month, end_month+1):

            if i > 9:
                dir_month = dir + '/' + str(i)
            else:
                dir_month = dir + '/' + '0'+str(i)

            if os.path.exists(dir_month):
                subs_dir += f'Ya existe: {dir_month}\n'
            else:
                os.mkdir(dir_month)
                subs_dir += f'Subcarpetas creada: {dir_month} \n'

    return subs_dir


def main() -> None:

    dir_name = input('Nombre de la carpeta: ')

    # create_directory(dir_name=dir_name, start_month=5, end_month=12)

    print(create_subdir(dir_name=dir_name, start_month=1, end_month=12))


if __name__ == '__main__':
    main()
