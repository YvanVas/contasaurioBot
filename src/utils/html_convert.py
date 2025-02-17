import pandas as pd
import re
from unicodedata import normalize
from pandas import notna
import datetime
from utils.html_build import build_html
from utils.search_identity import search_contribuyente, search_identity_number
from marangatu.consultar_ci import ConsultarCi

MONTH_NAMES = {
    '1': 'Enero',
    '2': 'Febrero',
    '3': 'Marzo',
    '4': 'Abril',
    '5': 'Mayo',
    '6': 'Junio',
    '7': 'Julio',
    '8': 'Agosto',
    '9': 'Septiembre',
    '10': 'Octubre',
    '11': 'Noviembre',
    '12': 'Diciembre',
}


def get_file_name(data_file: dict) -> str:
    ruc = str(data_file['RUC del Informante'][0])
    doc_register_type = str(data_file['Tipo de Registro'][0])
    date: datetime.date = data_file['Fecha de Emision'][0].date()
    month = MONTH_NAMES[str(date.month)]
    year = str(date.year)
    contribuyente_data = search_contribuyente(ruc)

    if contribuyente_data['names'] != '':
        file_name = f'{doc_register_type.title()} - {contribuyente_data["names"].title()} {contribuyente_data["surnames"].title()} - {month} - {year}'
    else:
        file_name = f'{doc_register_type.title()} - {contribuyente_data["fullname"].title()} - {month} - {year}'

    return file_name


def normalizate_chars(sting: str) -> str:

    # -> NFD y eliminar diacríticos
    sting = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
                   normalize("NFD", sting), 0, re.I
                   )
    # -> NFC
    sting = normalize('NFC', sting)

    return sting


def total_data_sum(column_data: dict) -> float:
    end_row = len(column_data)
    total_sum = 0

    for row in column_data:
        monto = column_data[row]
        if notna(monto):
            total_sum += column_data[row]
            monto_con_separador = '{:,.0f}'.format(monto)
            monto_con_separador = str(
                monto_con_separador).replace(',', '.')
            column_data[row] = monto_con_separador

    suma_con_separador = '{:,.0f}'.format(total_sum)
    suma_con_separador = str(suma_con_separador).replace(',', '.')

    column_data[end_row] = suma_con_separador

    return column_data


def to_html(path_xlsx: str) -> dict:
    """
     response = {
        'path_html': f'{file_name}.html',
        'total_grav_10': total_grav_10,
        'total_grav_5': total_grav_5,
        'total_exenta': total_grav_exenta,

    }
    """
    # Format file
    df = pd.read_excel(path_xlsx)
    
    # Reemplaza acentos en todos los nombres de columnas
    df.columns = df.columns.str.normalize('NFKD').str.encode(
        'ascii', errors='ignore').str.decode('utf-8')

    df['Fecha de Emision'] = pd.to_datetime(
        df['Fecha de Emision'], dayfirst=True)

    # Order by date
    df = df.sort_values(by='Fecha de Emision')

    # To dict
    file_content_dict = df.to_dict()

    # Get file name
    file_name = get_file_name(data_file=file_content_dict)

    if 'Compras' in file_name:
        delete_columns = [
            'RUC del Informante', 'Nombre o Razon Social del Informante', 'Condicion de la Operacion',
            'No Imputar', 'Numero de Comprobante Asociado', 'Timbrado del Comprobante Asociado'
        ]
    else:
        # Order by doc number
        df = df.sort_values(by='Numero de Comprobante')
        # To dict
        file_content_dict = df.to_dict()
        delete_columns = [
            'RUC del Informante', 'Nombre o Razon Social del Informante', 'Condicion de la Operacion', 'Numero de Comprobante Asociado', 'Timbrado del Comprobante Asociado'
        ]

    # delete innecessary data
    for column in delete_columns:
        file_content_dict.pop(column)

    # Add complete ruc and fullname
    # rucs_column: dict = file_content_dict['RUC / N? de Identificacion del Informado']
    # rucs_column: dict = file_content_dict['RUC / No de Identificacion del Informado']

    # Declarate New dict reference to contribuyente name
    # contribuyentes_fullname = {}
    # for ruc in rucs_column:
    #     # Ruc number
    #     ruc_reference = str(rucs_column[ruc])
    #     if ruc_reference == 'X':
    #         contribuyentes_fullname[ruc] = 'SIN NOMBRE'
    #     else:
    #         #contribuyente_data = search_contribuyente(ruc=ruc_reference)

    #         if contribuyente_data == None:

    #             contribuyente_data = search_identity_number(
    #                 identity_number=ruc_reference)

    #             if contribuyente_data == None:
    #                 print(ruc_reference)
    #                 # Search Marangatu
    #                 contribuyente_data = ConsultarCi().search_ci(ci=ruc_reference)
    #                 rucs_column[ruc] = contribuyente_data['ci']
    #                 contribuyentes_fullname[ruc] = normalizate_chars(
    #                     contribuyente_data['fullname'])
    #             else:
    #                 rucs_column[ruc] = contribuyente_data['ci']
    #                 contribuyentes_fullname[ruc] = normalizate_chars(
    #                     contribuyente_data['fullname'])
    #         else:
    #             rucs_column[ruc] = contribuyente_data['ruc']
    #             contribuyentes_fullname[ruc] = normalizate_chars(
    #                 contribuyente_data['fullname'])

    # # Add new column with fullname
    # file_content_dict['Razon Social'] = contribuyentes_fullname

    # Add montos gravados 10
    column_montos_10 = file_content_dict['Monto Gravado 10%']
    montos_gravados_10 = {}
    for monto in column_montos_10:
        value = column_montos_10[monto]
        monto_gravado = value/1.1
        montos_gravados_10[monto] = monto_gravado

    # Add montos gravados 5
    column_montos_5 = file_content_dict['Monto Gravado 5%']
    montos_gravados_5 = {}
    for monto in column_montos_5:
        value = column_montos_5[monto]
        monto_gravado = value/1.05
        montos_gravados_5[monto] = monto_gravado

    # Add new column montos gravados
    file_content_dict['Gravado 10%'] = montos_gravados_10
    file_content_dict['Gravado 5%'] = montos_gravados_5

    # Total sums
    total_data_sum(file_content_dict['Monto Gravado 10%'])
    total_data_sum(file_content_dict['Gravado 10%'])
    total_data_sum(file_content_dict['IVA 10%'])
    total_data_sum(file_content_dict['Monto Gravado 5%'])
    total_data_sum(file_content_dict['Gravado 5%'])
    total_data_sum(file_content_dict['IVA 5%'])
    total_data_sum(file_content_dict['Monto No Gravado / Exento '])
    total_data_sum(file_content_dict['Total Comprobante'])

    # Format timbrado number to str
    timbrados: dict = file_content_dict['Timbrado del Comprobante']

    for column in timbrados:
        timbrado = int(timbrados[column])
        timbrados[column] = str(timbrado)

    # Correct format date d/m/y
    fechas = dict = file_content_dict['Fecha de Emision']
    for column in fechas:
        fecha: datetime = fechas[column]
        fecha = fecha.date().strftime("%d/%m/%Y")
        fechas[column] = fecha

    # New columns order
   
    new_order = [
        "Fecha de Emision", "RUC / No de Identificacion del Informado", "Nombre o Razon Social del Informado", "Tipo de Comprobante",
        "Timbrado del Comprobante", "Numero de Comprobante", "Monto Gravado 10%", "Gravado 10%", "IVA 10%", "Monto Gravado 5%", "Gravado 5%", "IVA 5%", "Monto No Gravado / Exento ", "Total Comprobante",
        "Imputa IVA", "Imputa IRE",	"Imputa IRP"
    ]

    new_columns_name = [
        "Fecha", "RUC", "Razon Social", "Tipo Fact.", "Timbrado", "N. Fact.", "Total 10%", "Gravado 10%", "IVA 10%", "Total 5%", "Gravado 5%", "IVA 5%", "Exenta", "Total", "IVA", "IRE", "IRP"
    ]

    correct_data_dict = {}
    position = 0
    for head in new_order:
        correct_data_dict[head] = file_content_dict.pop(head)
        correct_data_dict[new_columns_name[position]
                          ] = correct_data_dict.pop(head)
        position += 1

    df = pd.DataFrame.from_dict(correct_data_dict)

    # last element of the column -> suma total 10
    last_key_grav_10 = list(correct_data_dict["Gravado 10%"])[-1]
    total_grav_10 = correct_data_dict['Gravado 10%'][last_key_grav_10]
    # last element of the column -> suma total 5
    last_key_grav_5 = list(correct_data_dict["Gravado 5%"])[-1]
    total_grav_5 = correct_data_dict['Gravado 5%'][last_key_grav_5]

    # last element of the column -> suma total exenta
    last_key_grav_exenta = list(correct_data_dict["Exenta"])[-1]
    total_exenta = correct_data_dict['Exenta'][last_key_grav_exenta]

    html = df.to_html(index=False, justify=None)

    table = html.replace('\n', '').replace('NaN', '').replace('NaT', '')

    html_content = build_html(title=file_name, table=table)

    with open(f'{file_name}.html', 'w') as f:
        f.write(html_content)

    response = {
        'total_grav_10': total_grav_10,
        'total_grav_5': total_grav_5,
        'total_exenta': total_exenta,
        'file_name': file_name,
        'path_html': f'{file_name}.html',
    }

    return response
