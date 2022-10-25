import re
import os
from zipfile import ZipFile, ZIP_DEFLATED


def to_zip(path: str) -> zip:

    jungle_zip = ZipFile(path.replace('.txt', '.zip'), 'w')

    name = re.findall('\w+.txt', path)

    jungle_zip.write(filename=path, arcname=name[0],
                     compress_type=ZIP_DEFLATED)

    jungle_zip.close()


def scan_files(file_extension='.txt') -> list:
    raiz_dir = 'Z:/r90'

    with os.scandir(raiz_dir) as ficheros:

        subdirectorios = [
            f'{raiz_dir}/{fichero.name}/' for fichero in ficheros if fichero.is_dir()]

    files = []
    for file in subdirectorios:

        with os.scandir(file) as ficheros:

            for fichero in ficheros:

                if fichero.is_file():

                    files.append(file + fichero.name)
                else:
                    sub = file+fichero.name+'/'

                    with os.scandir(sub) as ficheros:

                        for fichero in ficheros:
                            if fichero.is_file() and fichero.name.endswith(file_extension):
                                files.append(sub + fichero.name)

    return files


def xls_to_txt():

    files = scan_files('.xls')

    if files:

        for file in files:

            old_name = file
            new_name = file.replace('.xls', '.txt')

            if os.path.isfile(new_name):
                print("El archivo ya se convirtió: ", new_name)
            else:
                # Rename the file
                os.rename(old_name, new_name)

        # print('Convirtiendo los archivos xls a txt...')
        # print('\n')
    else:
        print('No hay archivos para convertir')


def format_line_text(text: str) -> list:

    format_line = text.replace("\t", '*').replace("\n", '')

    document = format_line.split('*')

    ruc = document[2]

    if ruc.strip() != 'X':
        format_ruc = re.findall('0*([0-9]+)', ruc)

        document[2] = format_ruc[0]

        return document
    else:
        return document


def read_file(path: str) -> list:

    content = []

    if os.path.exists(path):

        with open(path, 'r', errors='ignore') as f:

            for line in f:

                if not line.strip():
                    continue
                
                document = format_line_text(line)

                details_document = ''

                for detail in document:

                    details_document += detail.strip()
                    details_document += '\t'

                content.append(details_document)

        return content
    else:
        print('El archivo no existe!')


def write_file(file_content: list, path='tratado.txt') -> None:

    with open(path, 'w', encoding='utf8') as f:
        for line in file_content:
            f.write(line)
            f.write('\n')


def delete_file(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)
    else:
        print("El archivo no existe!")
