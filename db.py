import sqlite3

from sqlite3 import Error


def conectar():
    try:
        connection = sqlite3.connect("database/data.db")
        return connection
    except Error as err:
        print(err)
        return None


def execute_select(_sql, list_parameters):
    try:
        connection = conectar()
        if connection:
            connection.row_factory = fabricar_diccionario
            objeto_cursor = connection.cursor()

            if list_parameters:
                objeto_cursor.execute(_sql, list_parameters)
            else:
                objeto_cursor.execute(_sql)

            filas = objeto_cursor.fetchall()
            objeto_cursor.close
            connection.close
            return filas
        else:
            print(
                "No se pudo establecer la conexión a la base de datos. ver errores previos"
            )
            return None
    except Error as err:
        print("Error al ejecutar Sentencia SELECT SQL:" + str(err))
        return None


def fabricar_diccionario(cursor, row):
    diccionario = {}
    for idx, col in enumerate(cursor.description):
        diccionario[col[0]] = row[idx]

    return diccionario


def execute_sql(_sql, list_parameters):
    try:
        connection = conectar()
        if connection:
            objeto_cursor = connection.cursor()
            filas = objeto_cursor.execute(_sql, list_parameters).rowcount
            objeto_cursor.close()
            connection.commit()
            connection.close
            return filas
        else:
            print(
                "No se pudo establecer la conexión a la base de datos. ver errores previos"
            )
            return -1
    except Error as err:
        print("Error al ejecutar Sentencia SQL:" + str(err))
        return -1
