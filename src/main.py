import logging
import os
from random import randint
import re
from time import sleep
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ContextTypes, ConversationHandler, filters, CallbackContext
from download_ruc_files import download_zips, unzipping_files, scan_files
from utils.export_files import xls_to_txt, scan_files, read_file, write_file, to_zip, delete_file
from utils.search_identity import find_identity_data
from utils import office_require
from utils import nissei_scrapy
from utils.messages_list import *
from marangatu import marangatu

# Iniciar Loggin
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# funcion para enviar el primer mensaje luego del /start


TOKEN = os.environ['TOKEN']
IDENTITY = 1


def start(update, context):
    """Mensaje de Inicio"""
    update.message.reply_text(
        'Que tengo que hacer? vea /ayuda para ver la lsita de mis funciones.')


# funcion para explicar los comandos, lista de opciones
def help_command(update, context):
    """Lista de Funciones"""
    update.message.reply_text(
        """
        Funciones para el control de los Clientes.
    /nuevocliente - agregar cliente
    /listaclientes - ver todos los clientes

    Configuración de Clientes
    /agregartimbrado - agregar un nuevo timbrado
    /recepciondocumentos - resive los documentos
    /retirodocumentos - nose
    /colorcarpeta - agregar el color
    /export - exportar archivos de la R-90
    /buscarci - Busca el n° de documente en el RUC
    /

    Falta más funciones, pero aprendo rápido."""
    )


def msjAleatorio(listMsj: list) -> int:
    endMsj = len(listMsj) - 1
    positionMsj = randint(0, endMsj)
    return positionMsj


def echo(update: Update, context):
    # Busca una palabra clave, y responde con un mensaje
    chat_id = update.message.chat_id
    message = update.message.text.lower()

    user = update.message.from_user
    chat_id = update.message.chat_id

    # Save information
    office_require.add_chat_info(message=update.message, user=user)

    items = re.findall('^falta.+', message)

    if len(items) > 0:
        office_require.add_items(items[0])
        update.message.reply_text('Ok, agregados a la lista')

    if message == 'qué falta?' or message == 'que falta?':
        update.message.reply_text('Voy a buscar')
        sleep(1)
        items = office_require.read_items()
        items_message = ''
        if len(items) > 0:
            update.message.reply_text('Encontré que falta')
            for item in items:
                items_message += f'El {item["date"]}\n'
                for i in item["items"]:
                    items_message += f'{i.strip()}\n'
                items_message += '\n'
            update.message.reply_text(items_message)
        else:
            update.message.reply_text('No hay nada en falta 👍')

    if message == 'comprado':
        update.message.reply_text('Ok, borro datos de la lista 👌')
        office_require.delete_items()

    if message in agradecimientos:
        message = reply_agradecimientos[msjAleatorio(reply_agradecimientos)]
        update.message.reply_text(message)

    elif message in cumplidos:
        message = 'Claro'
        update.message.reply_text(message)

    elif message in regaños:
        message = reply_regaños[msjAleatorio(reply_regaños)]
        update.message.reply_text(message)

    elif message in saludos:
        message = reply_saludos[msjAleatorio(reply_saludos)]
        update.message.reply_text(message)

    elif message in nombres:
        update.message.reply_text('Si?')

    elif message == 'benitooo':
        update.message.reply_text('QUEE!!!')

    elif message in preguntas_quehacer:
        message = reply_quehacer[msjAleatorio(reply_quehacer)]
        update.message.reply_text(message)

    elif message in afirmaciones:
        reply = 'Sii'
        context.bot.send_message(
            chat_id=chat_id, text=reply)

    elif message in despedidas:
        message = reply_despedidas[msjAleatorio(reply_despedidas)]
        update.message.reply_text(message)

    if 'jaja' in message:
        context.bot.send_message(chat_id=chat_id, text=message.capitalize())

    if 'chaa' in message:
        reply = message.capitalize()
        context.bot.send_message(
            chat_id=chat_id, text=reply)


def search_identity(update: Update, context) -> int:

    update.message.reply_text(
        'Mandame el número de documento: \n\n envia "Listo" cuando termines las consultas.')

    return IDENTITY


def identity(update: Update, context):
    user = update.message.from_user
    # Responde con el mensaje anterior
    # update.message.reply_text(update.message.text)

    identity_number = update.message.text

    message_person_data = find_identity_data(identity_number)

    update.message.reply_text(message_person_data)


def done(update: Update, context) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    update.message.reply_text('Oc')
    user_data.clear()
    return ConversationHandler.END


def export_files_r90(update: Update, context):

    chat_id = update.message.chat_id

    context.bot.send_message(chat_id=chat_id, text='Buscando archivos... 🔍')

    xls_to_txt()

    files = scan_files()

    month_names = {
        '01': 'Enero',
        '02': 'Febrero',
        '03': 'Marzo',
        '04': 'Abril',
        '05': 'Mayo',
        '06': 'Junio',
        '07': 'Julio',
        '08': 'Agosto',
        '09': 'Septiembre',
        '10': 'Octubre',
        '11': 'Noviembre',
        '12': 'Diciembre',
    }

    if files:

        files_name = ''
        for file in files:
            client_name = re.findall('/([a-z]+)/', file)[0]
            month = month_names[re.findall('/([0-9]{2})/', file)[0]]
            search_year = re.findall('/([0-9]{4})/', file)

            if len(search_year) >= 1:
                year = search_year[0]
            else:
                year = 'Sin año'

            file_name = re.findall('\w+.txt', file)
            name = file_name[0]

            month_and_year = f'{month} - {year}'

            if client_name.capitalize() in files_name:
                if month_and_year in files_name:
                    files_name += f'{name}\n'
                else:
                    files_name += f'{month_and_year}\n{name}\n'
            else:
                files_name += f'{client_name.capitalize()}:\n{month_and_year}\n{name}\n'

        context.bot.send_message(
            chat_id=chat_id, text=f'{files_name} \n  Encontré estos archivos')

        for file in files:

            file_content = read_file(file)

            write_file(file_content, path=file)

            to_zip(file)

            delete_file(file)

        context.bot.send_message(
            chat_id=chat_id, text='Exportados a zip, listos para enviar 🦖')

    else:
        context.bot.send_message(
            chat_id=chat_id, text='No hay archivos nuevos :(')


def run_download_ruc(update, context):
    chat_id = update.message.chat_id

    update.message.reply_text("Descargando archivos...")
    download_zips()

    files = scan_files('.zip')
    if files is not None:
        unzipping_files()

    update.message.reply_text("Ruc descargados")


# Anulados
def export_anulados(update: Update, context):
    chat_id = update.message.chat_id

    context.bot.send_message(
        chat_id=chat_id, text='Buscando facturas anuladas... 🔍')

    # Separate anulados data and write to new txt file
    files_path = marangatu.document_util.separate_anulados()

    # Init anulados data list
    anulados_data = []

    # Get all anulados data in a list
    for file_path in files_path:
        anulados_data = marangatu.document_util.get_anulados_data(
            path=file_path)
        anulados_data.append(anulados_data)

    # Init total messagge response
    messagge_anulados = ''

    for data in anulados_data:
        contribuyente_name = data['contribuyente'].capitalize()
        anulado_data = f"{data['timbrado']} | {data['date']} | {data['document_number']['total_number']}"

        if contribuyente_name in messagge_anulados:
            messagge_anulados += f'{anulados_data}\n'
        else:
            messagge_anulados += f'{contribuyente_name}:\n{anulado_data}\n'

    # Send all anulados to chat
    context.bot.send_message(
        chat_id=chat_id, text=f'{messagge_anulados} \n  Encontré estos anulados')

# Iniciar al Menú Principal


def menu(bot, update):
    bot.message.reply_text(mainMenuMessage(),
                           reply_markup=mainMenuKeyboard())


# Menus del bot
def mainMenu(bot, update):
    bot.callback_query.message.edit_text(mainMenuMessage(),
                                         reply_markup=mainMenuKeyboard())


def clientConfigMenu(bot, update):
    bot.callback_query.message.edit_text(clientConfigMessage(),
                                         reply_markup=clientConfigKeyboard())


def second_menu(bot, update):
    bot.callback_query.message.edit_text(second_menu_message(),
                                         reply_markup=second_menu_keyboard())


def clientConfigSubmenu(bot, update):
    pass


def second_submenu(bot, update):
    pass


def error(update, context):
    print(f'Update {update} caused error {context.error}')


# Keyboardas - Menu de menues
def mainMenuKeyboard():
    keyboard = [[InlineKeyboardButton('Configuración de Clientes', callback_data='clientConfigMenu')],
                [InlineKeyboardButton('Eliminar Cliente', callback_data='m2')]]
    return InlineKeyboardMarkup(keyboard)


def clientConfigKeyboard():
    keyboard = [[InlineKeyboardButton('Nombre', callback_data='clientName')],
                [InlineKeyboardButton(
                    'Timbrado', callback_data='clientTimbrado')],
                [InlineKeyboardButton(
                    'Color de la Carpeta', callback_data='clientColorFolder')],
                [InlineKeyboardButton('Atras', callback_data='main')]]
    # escuchando la eleccion
    return InlineKeyboardMarkup(keyboard)


def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
                [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


# Mensajes de los menus
def mainMenuMessage():
    return 'Opciones:'


def clientConfigMessage():
    return 'Editar Clientes:'


def second_menu_message():
    return 'Choose the submenu in second menu:'

# TODO: hacer que direccione a su duncion correspondiente /cambiarNombre, y espere una respuesta y luego ejecute el cambio


def responseOption(update, context):
    query = update.callback_query
    # CallbackQueries necesita una respuesta para seguir
    query.answer()
    if query.data == 'clientName':
        query.edit_message_text(
            text="Ok. Enviame el nuevo nombre:")


# def saludo(context:CallbackContext):
#     context.bot.send_message(
#             chat_id=, text='Buen día gente ya amaneció')


def main():
    """Inicia el bot con un TOKEN"""
    updater = Updater(
        TOKEN, use_context=True)

    # job = updater.job_queue

    # job.run_daily(saludo, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=10, minute=33).replace(tzinfo=))

    dp = updater.dispatcher

    # Conversacion
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("buscarci", search_identity)],
        states={
            IDENTITY: [
                MessageHandler(Filters.regex("^[\d,-]*$"), identity)
            ],
        },
        fallbacks=[MessageHandler(Filters.regex("^Listo$"), done)],
    )

    dp.add_handler(conv_handler)

    # los diferentes comandos para bot
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('ayuda', help_command))

    dp.add_handler(CommandHandler('menu', menu))
    dp.add_handler(CommandHandler('export', export_files_r90))
    dp.add_handler(CommandHandler('anulados', export_anulados))
    dp.add_handler(CommandHandler('downloadruc', run_download_ruc))

    dp.add_handler(MessageHandler(Filters.text, echo))

    # Handlers del Menu
    updater.dispatcher.add_handler(
        CallbackQueryHandler(mainMenu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(
        clientConfigMenu, pattern='clientConfigMenu'))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(second_menu, pattern='m2'))
    # updater.dispatcher.add_handler(CallbackQueryHandler(clientConfigSubmenu, pattern='clientName'))
    # updater.dispatcher.add_handler(CallbackQueryHandler(clientConfigSubmenu, pattern='clientTimbrado'))
    # updater.dispatcher.add_handler(CallbackQueryHandler(clientConfigSubmenu, pattern='clientColorFolder'))

    updater.dispatcher.add_handler(CallbackQueryHandler(responseOption))

    updater.dispatcher.add_handler(
        CallbackQueryHandler(second_submenu, pattern='m2_1'))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(second_submenu, pattern='m2_2'))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling(drop_pending_updates=True)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
