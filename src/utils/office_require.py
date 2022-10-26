from datetime import datetime

FILE_PATH = 'src/archives/lists/list.txt'
CHAT_PATH = 'src/archives/chats/chat.txt'
GROUP_PATH = 'src/archives/chats/group.txt'


def today() -> datetime:
    return datetime.now().date().strftime('%d-%m-%Y')


def items_format(items: str):
    items_list = items.split(',')
    return items_list


def read_items() -> list:
    items = []
    with open(FILE_PATH, 'r', encoding='utf-8') as file:

        for line in file:
            line = line.strip()
            items_content = items_format(line)
            items.append(
                {
                    'date': items_content[0],
                    'items': items_content[1:]
                }
            )
    file.close()
    return items


def verify_group(group_id: str) -> bool:
    with open(GROUP_PATH, 'r', encoding='utf-8') as file:
        for line in file:
            if group_id in line:
                file.close()
                return True
    file.close()
    return False


def verify_user(user_id: str) -> bool:
    with open(CHAT_PATH, 'r', encoding='utf-8') as file:
        for line in file:
            if user_id in line:
                file.close()
                return True
    file.close()
    return False


def message_format(message: str) -> str:
    date = today()
    items = message.replace("falta", "")
    # Add date and items
    return f'{date},{items}'


def add_items(message: str) -> None:

    items = message_format(message)
    with open(FILE_PATH, 'a', encoding='utf-8') as file:
        file.write(items)
        file.write('\n')
    file.close()


def delete_items() -> None:
    with open(FILE_PATH, 'w', encoding='utf-8') as file:
        file.write('')
    file.close()


def add_chat_info(message: dict, user: dict):
    chat_id = message['chat']['id']
    chat_name = message['chat']['title']
    chat_type = message['chat']['type']

    if chat_type == 'group':
        verify = verify_group(str(chat_id))
        if verify == False:
            with open(GROUP_PATH, 'a', encoding='utf-8') as file:
                file.write(f'{chat_id},{chat_name}\n')
            file.close()

        # Add user
        user_id = user['id']
        user_first_name = user['first_name']

        verify = verify_user(str(user_id))
        if verify == False:
            with open(CHAT_PATH, 'a', encoding='utf-8') as file:
                file.write(f'{user_id},{user_first_name}\n')
            file.close()
    else:
        user_id = user['id']
        user_first_name = user['first_name']
        verify = verify_user(str(user_id))
        if verify == False:
            with open(CHAT_PATH, 'a', encoding='utf-8') as file:
                file.write(f'{user_id},{user_first_name}\n')
            file.close()