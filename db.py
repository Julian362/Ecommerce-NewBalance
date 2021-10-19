import sqlite3

from sqlite3 import Error

#Se establece la conexión con la base de datos
def conectar():
    try:
        conexion =sqlite3.connect('database/dataOficial.db')
        return conexion
    except Error as err:
        print(err)
        return None

#Para seleccionar datos de la base de datos (solo select)
def ejecutar_select(_sql,lista_parametros):
    try:
        conexion = conectar()
        if conexion:
            conexion.row_factory = fabricar_diccionario
            objeto_cursor = conexion.cursor()

            if lista_parametros:
                objeto_cursor.execute(_sql, lista_parametros)
            else:
                objeto_cursor.execute(_sql)

            filas = objeto_cursor.fetchall()
            objeto_cursor.close
            conexion.close
            return filas
        else:
            print("No se pudo establecer la conexión a la base de datos. ver errores previos")
            return None
    except Error as err:
        print("Error al ejecutar Sentenica SELECT SQL:"+str(err))
        return None

#Fabrica de diccionario
def fabricar_diccionario(cursor, row):
    diccionario={}
    for idx, col in enumerate(cursor.description):
        diccionario[col[0]]=row[idx]

    return diccionario

#Función para seleccionar, editar y eliminar --> No confundir en el nombre
def ejecutar_insert(_sql,lista_parametros):
    try:
        conexion = conectar()
        if conexion:
            objeto_cursor = conexion.cursor()
            filas = objeto_cursor.execute(_sql,lista_parametros).rowcount
            objeto_cursor.close()
            conexion.commit()
            conexion.close
            return filas
        else:
            print("No se pudo establecer la conexión a la base de datos. ver errores previos")
            return -1
    except Error as err:
        print("Error al ejecutar Sentenica SQL:"+str(err))
        return -1