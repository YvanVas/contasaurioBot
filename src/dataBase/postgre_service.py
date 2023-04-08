import os
import psycopg2
from psycopg2 import Error


def conection_db():
    """
        Crea la conexión a la base de datos con
        Postgresql.
        :return Connection object or None
    """

    # conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn = psycopg2.connect(
        host="localhost",
        database="contribuyentes_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

    return conn


def create_tables() -> None:
    """ Crea la tabla en la base de datos,
        si aún no existe. Indicando la base de datos
        especifica.
        :return None
    """
    try:
        conn = conection_db()
        cursor = conn.cursor()

        for end_ruc in range(10):

            cursor.execute(f"""CREATE TABLE IF NOT EXISTS contribuyentes{end_ruc} (
                    id	 INT PRIMARY KEY NOT NULL,
                    fullname	VARCHAR(255) UNIQUE NOT NULL,
                    dv VARCHAR(10) NOT NULL,
                    ruc VARCHAR(255) NOT NULL
                );""")

        conn.commit()
        conn.close()
    except Error as e:
        print(e)


def put_contribuyente0(data: dict) -> None:
    try:
        conn = conection_db()
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO contribuyentes0 (id, fullname, dv, ruc)\
                VALUES('{data['ci']}', '{data['fullname']}', '{data['dv']}', '{data['ruc']}')")

        conn.commit()
        conn.close()

        return True
    except Error as e:
        conn.close()
        print(e)


def put_contribuyente1(data: dict) -> None:
    try:
        conn = conection_db()
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO contribuyentes1 (id, fullname, dv, ruc)\
                VALUES('{data['ci']}', '{data['fullname']}', '{data['dv']}', '{data['ruc']}')")

        conn.commit()
        conn.close()

        return True
    except Error as e:
        conn.close()
        print(e)


def put_contribuyente2(data: dict) -> None:
    try:
        conn = conection_db()
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO contribuyentes2 (id, fullname, dv, ruc)\
                VALUES('{data['ci']}', '{data['fullname']}', '{data['dv']}', '{data['ruc']}')")

        conn.commit()
        conn.close()

        return True
    except Error as e:
        conn.close()
        print(e)


def put_contribuyente3(data: dict) -> None:
    try:
        conn = conection_db()
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO contribuyentes3 (id, fullname, dv, ruc)\
                VALUES('{data['ci']}', '{data['fullname']}', '{data['dv']}', '{data['ruc']}')")

        conn.commit()
        conn.close()

        return True
    except Error as e:
        conn.close()
        print(e)


def put_contribuyente4(data: dict) -> None:
    try:
        conn = conection_db()
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO contribuyentes4 (id, fullname, dv, ruc)\
                VALUES('{data['ci']}', '{data['fullname']}', '{data['dv']}', '{data['ruc']}')")

        conn.commit()
        conn.close()

        return True
    except Error as e:
        conn.close()
        print(e)


def put_contribuyente5(data: dict) -> None:
    try:
        conn = conection_db()
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO contribuyentes5 (id, fullname, dv, ruc)\
                VALUES('{data['ci']}', '{data['fullname']}', '{data['dv']}', '{data['ruc']}')")

        conn.commit()
        conn.close()

        return True
    except Error as e:
        conn.close()
        print(e)


def put_contribuyente6(data: dict) -> None:
    try:
        conn = conection_db()
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO contribuyentes6 (id, fullname, dv, ruc)\
                VALUES('{data['ci']}', '{data['fullname']}', '{data['dv']}', '{data['ruc']}')")

        conn.commit()
        conn.close()

        return True
    except Error as e:
        conn.close()
        print(e)


def put_contribuyente7(data: dict) -> None:
    try:
        conn = conection_db()
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO contribuyentes7 (id, fullname, dv, ruc)\
                VALUES('{data['ci']}', '{data['fullname']}', '{data['dv']}', '{data['ruc']}')")

        conn.commit()
        conn.close()

        return True
    except Error as e:
        conn.close()
        print(e)


def put_contribuyente8(data: dict) -> None:
    try:
        conn = conection_db()
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO contribuyentes8 (id, fullname, dv, ruc)\
                VALUES('{data['ci']}', '{data['fullname']}', '{data['dv']}', '{data['ruc']}')")

        conn.commit()
        conn.close()

        return True
    except Error as e:
        conn.close()
        print(e)


def put_contribuyente9(data: dict) -> None:
    try:
        conn = conection_db()
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO contribuyentes9 (id, fullname, dv, ruc)\
                VALUES('{data['ci']}', '{data['fullname']}', '{data['dv']}', '{data['ruc']}')")

        conn.commit()
        conn.close()

        return True
    except Error as e:
        conn.close()
        print(e)


def all_contribuyentes() -> tuple:
    try:
        conn = conection_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM contribuyentes")
        data = cursor.fetchall()

        conn.commit()
        conn.close()

        return data
    except Error as e:
        conn.close()
        print(e)


def delete_contribuyente(id_contribuyente) -> None:
    conn = conection_db()
    try:
        cursor = conn.cursor()

        cursor.execute(
            f"DELETE FROM contribuyentes WHERE id = {id_contribuyente}")

        conn.commit()
        conn.close()
    except Error as e:
        conn.close()
        print(e)
