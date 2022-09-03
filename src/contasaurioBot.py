import logging
import os
from random import randint
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ContextTypes, ConversationHandler, filters
from download_ruc_files import download_zips, unzipping_files, scan_files
from export_files import xls_to_txt, scan_files, read_file, write_file, to_zip, delete_file
from search_identity import find_identity_data, search_identity_number


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

    saludos = ['hola', 'holaa', 'hola benito', 'buendia benito', 'buen dia benito', 'buen día benito', 'buen dia', 'buen día',
               'buenos días benito', 'buenos dias benito']

    despedidas = ['bye', 'chau', 'chauu']

    agradecimientos = ['gracias', 'gracias benito', 'graciaas']

    nombres = ['benito', 'benitp', 'benitoo']

    cumplidos = ['que crack', 'que grande', 'que pro']

    regaños = ['benito asi no', 'benito así no',
               'asi no benito', 'así no benito', 'benito vos no', 'vos no benito', 'benito malo', 'que malo benito']

    preguntas_quehacer = ['que haces', 'qué haces', 'qué haces benito', 'que haces benito',
                          'qué haces benito?', 'que haces benito?', 'qué haces?', 'que haces?']

    consultas = []

    afirmaciones = ['vd benito', 'verdad benito', 'vdd benito']

    reply_saludos = ['Holaa 👋', 'Hola', 'Buenass', 'Buenos días Lic.',
                     'Tengo sueño', 'Ola', 'Bien y vos']

    reply_despedidas = ['Chauu 👋', 'Adios', 'Hasta luego', '👋', '👍']

    reply_agradecimientos = ['👍', 'De nada', '👌']

    reply_quehacer = ['Acá contando facturas',
                      'Estoy contando bytes', 'Estoy contando números', 'Estoy aprendiendo a contar', 'Estoy estudiando sobre como responder']

    reply_sentimientos = ['Muy bien!', 'Normal', 'Y practicamente existo']

    reply_regaños = [':(', 'tristin', '😔', '😞', '😨', '🥲']

    user = update.message.from_user
    chat_id = update.message.chat_id

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


def export_files_r90(update, context):

    chat_id = update.message.chat_id

    context.bot.send_message(chat_id=chat_id, text='Buscando archivos... 🔍')

    xls_to_txt()

    files = scan_files()

    if files:

        files_name = ''
        for file in files:
            file_name = re.findall('\w+.txt', file)
            name = file_name[0]

            files_name += name.replace('.txt', '.xls') + '\n'

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


def main():
    """Inicia el bot con un TOKEN"""
    updater = Updater(
        TOKEN, use_context=True)

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
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
