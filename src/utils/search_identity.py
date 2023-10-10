# from msilib.schema import
import re
import requests

from download_ruc_files import scan_files
from download_ruc_files import read_file


def search_identity_number(identity_number: str) -> dict | None:
    """
        Recibe un numero de documento,
        realiza la consulta a la página del mec,
        retorna un diccionario con los datos.
        :param '12345'
        :return Dict
        >>> search_identity_number('12345')
        {
            'ci':'12345',
            'fullname':'Juan Perez',
        }
    """
    try:

        link = f"https://www.mec.gov.py/cms_v4/denuncias/buscar_persona?documento={identity_number.strip()}"

        response = requests.get(link).json()

        if response is not None:

            data = {
                'ci': response['id_persona'],
                'fullname': f"{response['nombre_persona']}, {response['apellido_persona']}",
            }

            return data
        else:
            return response
    except:
        print('error')


def search_contribuyente(ruc: str) -> dict | None:
    """
    Retorna un diccionario con los datos, si encuentra el ruc en los archivos
    sino retorna un None.
    Tambien puede discriminar guiones (-)
    :param '12345-1' or '12345'
    :return Dict
    >>> search_contribuyente('12345')
        {
            'ci':'12345',
            'fullname':'Juan Perez',
            'ruc': '12345-1',
        }
    >>> search_contribuyente('12345')
        None
    """

    ruc_reference = ruc

    if '-' in ruc_reference:

        # 12345-6 -> 5
        end_ruc = re.findall('\d*(\d)-', ruc_reference)[0]

        # 12345-6 -> 12345
        ruc_reference = re.findall('(\d*)-', ruc_reference)[0]
    else:
        # 12345 -> 5
        end_ruc = re.findall('\d*(\d)', ruc_reference)[0]

    path_data = scan_files(end_ruc=end_ruc)

    data_contribuyentes = read_file(path_data)

    filtered_data = list(filter(
        lambda contribuyente: contribuyente['ci'] == ruc_reference, data_contribuyentes))

    if filtered_data:
        contribuyente = dict(filtered_data[0])

        return contribuyente
    else:
        return None


def find_identity_data(identity_number: str) -> str:
    """
        Busca el numero de documento en el listado de RUC de la SET y
        en la pagina del MEC con dos funciones distinas.
        Compara entre los datos y devuelve un mensaje dependiendo de
        la información que obtuvo.

        :param identity number
        :return message

        >>> find_identity_data('123456')
        str -> 'Es contribuyente: (ruc) (fullname)'
        str -> 'No es contribuyente: (ci) (fullname)'
        str -> 'No encontré datos' 
    """

    not_contribuyente = search_identity_number(identity_number)

    contribuyente = search_contribuyente(identity_number)

    if contribuyente is not None:
        return f'*Es contribuyente*\nRUC: `{contribuyente["ruc"]}`\nNombre: `{contribuyente["fullname"]}`\nEstado: `{contribuyente["status"]}`'

    elif contribuyente is None and not_contribuyente is not None:
        return f'*No es contribuyente*\nCI: `{not_contribuyente["ci"]}`\nNombre: `{not_contribuyente["fullname"]}`'

    elif contribuyente is None and not_contribuyente is None:
        return 'No encontré datos...'
