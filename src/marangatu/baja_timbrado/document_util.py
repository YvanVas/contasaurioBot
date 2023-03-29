import re
import os
from utils import export_files

RUC_ANULADO = 'XXX'
ANULADOS_PATH = 'Z:/anulados'


def clean_line_data(line_data: str) -> list:
    # Clean spaces
    data = line_data.strip()
    # To list with coma
    document_data = data.split(',')
    # Remove '"' to data
    document_data = [data.replace('"', '').strip() for data in document_data]
    return document_data


def remove_start_ceros(number: str) -> str:
    """
    Elimina los ceros iniciales de un número dado o de un numero que podria contener una cadena.

    Args:
    - number (str): El número que se va a procesar.

    Returns:
    - str: El número/cadena resultante sin ceros iniciales.
    """
    non_zero_digits = re.findall('0*([0-9]+|[a-zA-Z]+)', number)
    if len(non_zero_digits) > 0:
        return non_zero_digits[0]
    return number


def document_number_format(number: str) -> dict:
    """
    Formatea un número de documento en tres partes: establecimiento, punto de expedición y número de documento.

    Args:
    - number (str): El número de documento a formatear.

    Returns:
    - dict: Un diccionario con las siguientes claves:
        - 'establecimiento': El código de establecimiento del documento (3 dígitos).
        - 'punto_expedicion': El código de punto de expedición del documento (3 dígitos).
        - 'number': El número de documento sin ceros iniciales (7 dígitos).
        - 'total_number': El número de documento original (13 dígitos).
    """
    formatted_document_number = re.split(
        '([0-9]{3})([0-9]{3})([0-9]{7})', number)[1:-1]

    document_number = {
        'establecimiento': formatted_document_number[0],
        'punto_expedicion': formatted_document_number[1],
        'number': remove_start_ceros(formatted_document_number[2]),
        'total_number': number
    }

    return document_number


def separate_anulados(path: str = ANULADOS_PATH) -> list:
    """
    Lee un archivo de texto y extrae los datos de los documentos anulados.

    Args:
    - path (str): La ruta del archivo a procesar.

    Returns:
    - list: Una lista de diccionarios con los datos de los documentos anulados. Cada
      diccionario contiene los siguientes campos:
      - timbrado: El número de timbrado del documento.
      - date: La fecha de emisión del documento.
      - document_number: Un diccionario con los campos 'establecimiento', 'punto_expedicion',
        'number' y 'total_number' que representan el número de documento separados en sus partes.
      - client_ruc: El número de RUC del cliente del documento.
      - client_name: El nombre del cliente al que se emitió el documento.
    """
    # Get all anulados file path
    anulados_files_path = export_files.scan_files(
        file_extension='.TXT', raiz_dir=ANULADOS_PATH)

    if len(anulados_files_path) > 0:
        # Init anulados list
        anulados = []
        # Init anulados path
        separated_anulados_path = []
        # Init cont
        cont = 0

        # Recorrer los path de los anulados
        for anulado_file_path in anulados_files_path:
            # Open txt file in read mode
            with open(file=anulado_file_path, mode='r', errors='ignore') as file:

                for line in file:
                    # Ignore the first line (head)
                    if cont == 0:
                        cont += 1
                        continue

                    # Clean line data
                    document_data = clean_line_data(line_data=line)

                    # Extract timbrado, date, document_number, ruc, client value with position
                    document_data = {
                        'timbrado':  remove_start_ceros(document_data[1]),
                        'date': document_data[4],
                        'document_number': document_number_format(document_data[5]),
                        'client_ruc': remove_start_ceros(document_data[6]),
                        'client_name': document_data[7],
                    }

                    # Filter ANULADOS
                    if document_data['client_ruc'] == RUC_ANULADO:
                        # Add data to anulados list
                        anulados.append(document_data)
                        separated_anulados_path.append(
                            anulado_file_path.replace('.TXT', '.txt'))

                    cont += 1

            if len(anulados) > 0:
                write_file(anulados=anulados, path=anulado_file_path)
                rename_file(file_path=anulado_file_path)
            else:
                export_files.delete_file(path=anulado_file_path)
        return separated_anulados_path
    return anulados_files_path


def write_file(anulados: list, path='tratado.txt') -> None:

    with open(file=path, mode='w', errors='ignore') as file:
        for anulado_dict in anulados:
            anulado_text = f"{anulado_dict['timbrado']},{anulado_dict['date']},{anulado_dict['document_number']['total_number']},{anulado_dict['client_ruc']},{anulado_dict['client_name']}"
            file.write(anulado_text)
            file.write('\n')


def rename_file(file_path: str):
    if os.path.exists(file_path):
        old_name = file_path
        new_name = old_name.replace('.TXT', '.txt')
        os.rename(old_name, new_name)
    else:
        print("El archivo no existe!")


def get_anulados_data(path: str) -> list:
    anulados_data = []
    contribuyente_name = re.findall('/([a-z]+)/', path)[0]
    with open(file=path, mode='r', errors='ignore') as file:
        for line in file:

            # timbrado, date, document_number, ruc, client value with position
            anulado_data = line.split(',')

            data = {
                'contribuyente': contribuyente_name,
                'timbrado':  anulado_data[0],
                'date': anulado_data[1],
                'document_number': document_number_format(anulado_data[2]),
                'client_ruc': anulado_data[3],
                'client_name': anulado_data[4].replace('\n', ''),
            }
            anulados_data.append(data)

    return anulados_data
