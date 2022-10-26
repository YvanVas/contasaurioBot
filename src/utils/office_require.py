from datetime import datetime


FILE_PATH = 'src/archives/lists/list.txt'


def today() -> datetime:
    return datetime.now().date().strftime('%d-%m-%Y')


def items_format(items: str):
    items_list = items.split(',')
    return items_list


def read_list_file() -> list:
    items = []
    with open(FILE_PATH, 'r', encoding='utf-8') as file:

        for line in file:
            line = line.strip()
            items_content = items_format(line)
            items.append(
                {
                    'date':items_content[0],
                    'items':items_content[1:]
                }
            )
    file.close()
    return items


def message_format(message: str) -> str:
    date = today()
    items = message.replace("falta", "").strip()
    # Add date and items
    return f'{date},{items}'


def add_items(message: str) -> None:

    items = message_format(message)
    with open(FILE_PATH, 'a', encoding='utf-8') as file:
        file.write(items)
        file.write('\n')
    file.close()


items = read_list_file()
print(items)

# message = 'falta boligrafo, 6 carpetas, rotulos'

# add_items(message)

# read_list_file()
