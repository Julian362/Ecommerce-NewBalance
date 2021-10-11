import db

class usuario():

    estado = 'F'
    nickname = ''
    nombre = ''
    apellidos = ''
    documento = ''
    celular = ''
    sexo = ''
    correo = ''

    def __init__(self, p_nickname, p_estado, p_nombre, p_apellidos, p_documento, p_celular, p_sexo, p_correo) -> None:
        self.estado = p_estado
        self.nickname = p_nickname
        self.nombre = p_nombre
        self.apellidos = p_apellidos
        self.documento = p_documento
        self.sexo = p_sexo
        self.correo = p_correo
        self.celular = p_celular

    @classmethod
    def cargar(cls, p_nickname):
        sql = 'SELECT * FROM usuario Where nickname = ?;'
        obj = db.ejecutar_select(sql,[ p_nickname ])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["nickname"],obj[0]["estado"],obj[0]["nombre"],obj[0]["apellidos"],obj[0]["documento"],obj[0]["celular"],obj[0]["sexo"],obj[0]["correo"])

        return None

    @classmethod
    def delete(cls, p_nickname):
        sql = 'DELETE FROM usuario Where nickname = ?;'
        obj = db.ejecutar_insert(sql,[ p_nickname ])
        if obj:
            if obj>0:
                return "Borrado corectamente el usuario "

        return "No se pudo borrar el usuario "

    @classmethod
    def block(cls, p_nickname, p_estado):
        if p_estado == "T":
            sql = 'UPDATE usuario set estado = "F" Where nickname = ?;'
        elif p_estado == "F":
            sql = 'UPDATE usuario set estado = "T" Where nickname = ?;'
        obj = db.ejecutar_insert(sql,[ p_nickname ])
        if obj:
            if obj > 0:
                return True

        return False

    @classmethod
    def editar(cls,nombre, apellidos, correo, documento, celular, nickname):
        sql="UPDATE usuario set nombre = ?,apellidos = ?, correo= ? ,documento= ? ,celular= ? where nickname= ?"
        obj = db.ejecutar_insert(sql,[nombre, apellidos, correo, documento, celular, nickname])
        if obj:
            if obj > 0:
                return True

        return False

    @staticmethod
    def listado():
        sql = "SELECT * FROM usuario ORDER BY nickname;"
        return db.ejecutar_select(sql, None)
