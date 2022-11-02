from datetime import datetime
import os

FILE_PATH = os.environ['FILE_PATH']
CHAT_PATH = os.environ['CHAT_PATH']
GROUP_PATH = os.environ['GROUP_PATH']


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
    
    return items


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
    


def delete_items() -> None:
    with open(FILE_PATH, 'w', encoding='utf-8') as file:
        file.write('')
    


# Save information
def verify_group(group_id: str) -> bool:
    with open(GROUP_PATH, 'r', encoding='utf-8') as file:
        for line in file:
            if group_id in line:
                return True
    
    return False


def verify_user(user_id: str) -> bool:
    with open(CHAT_PATH, 'r', encoding='utf-8') as file:
        for line in file:
            if user_id in line:
                return True
    
    return False


def add_user(user_id: str, user_first_name: str) -> None:
    verify = verify_user(str(user_id))
    if verify == False:
        with open(CHAT_PATH, 'a', encoding='utf-8') as file:
            file.write(f'{user_id},{user_first_name}\n')
    


def add_chat_info(message: dict, user: dict):
    chat_id = message['chat']['id']
    chat_name = message['chat']['title']
    chat_type = message['chat']['type']

    if chat_type == 'group':
        verify = verify_group(str(chat_id))
        if verify == False:
            with open(GROUP_PATH, 'a', encoding='utf-8') as file:
                file.write(f'{chat_id},{chat_name}\n')
            

        # Add user
        add_user(user['id'], user['first_name'])
    else:
        # Add user
        add_user(user['id'], user['first_name'])
