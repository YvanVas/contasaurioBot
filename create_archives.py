import os


def create_directory(dir_name: str, month=None, start_month=None, end_month=None):

    dir = 'Z:/r90/'+dir_name

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


def main() -> None:

    dir_name = input('Nombre de la carpeta: ')

    create_directory(dir_name=dir_name, start_month=1, end_month=4)


if __name__ == '__main__':
    main()
