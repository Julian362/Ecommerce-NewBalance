import db

#Clase usuario, para la respectiva pantalla.
class producto():

    estado = 'F'
    nickname = ''
    nombre = ''
    apellidos = ''
    documento = ''
    telefono = ''
    sexo = ''
    correo = ''

    #Se establece el método constructor
    def __init__(self, p_nickname, p_estado, p_nombre, p_apellidos, p_documento, p_telefono, p_sexo, p_correo) -> None:
        self.estado = p_estado
        self.nickname = p_nickname
        self.nombre = p_nombre
        self.apellidos = p_apellidos
        self.documento = p_documento
        self.sexo = p_sexo
        self.correo = p_correo
        self.telefono = p_telefono

    #Función para cargar los datos
    @classmethod
    def cargar(cls, p_documento):
        sql = 'SELECT DISTINCT persona.* FROM persona inner join rol on persona.tipo_rol = "user" and persona.documento="?";'
        obj = db.ejecutar_select(sql,[ p_documento ])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["nickname"],obj[0]["estado"],obj[0]["nombre"],obj[0]["apellidos"],obj[0]["documento"],obj[0]["telefono"],obj[0]["sexo"],obj[0]["correo"])

        return None

    #Función para eliminar
    @classmethod
    def delete(cls, p_documento):
        sql = 'DELETE FROM persona inner join rol on persona.tipo_rol = "user" and persona.documento="?";'
        obj = db.ejecutar_insert(sql,[ p_documento ])
        if obj:
            if obj>0:
                return "Borrado corectamente el usuario "

        return None

    #Función para el bloquear o desbloquear al usuario
    @classmethod
    def block(cls, p_documento, p_estado):
        if p_estado == "T":
            sql = 'UPDATE persona set estado = "F" Where documento = ?;'
        elif p_estado == "F":
            sql = 'UPDATE persona set estado = "T" Where documento = ?;'
        obj = db.ejecutar_insert(sql,[ p_documento ])
        if obj:
            if obj > 0:
                return True

        return False

    #Función para editar los datos de usuario
    @classmethod
    def editar(cls,nombre, apellidos, correo, documento, telefono, nickname, sexo):
        sql="UPDATE persona set nombre = ?,apellidos = ?, correo= ? ,documento= ? , telefono= ?, sexo= ? where documento= ?"
        obj = db.ejecutar_insert(sql,[nombre, apellidos, correo, documento, telefono,  sexo, nickname])
        if obj:
            if obj > 0:
                return True

    #Función para crear al usuario
    def crear(cls,nombre, apellidos, correo, documento, telefono, nickname, sexo):
        sql="INSERT INTO persona (estado,nickname,nombre,apellidos,documento,sexo,correo,telefono) VALUES (?,?,?,?,?,?,?,?);"
        obj = db.ejecutar_insert(sql,["T",nickname,nombre, apellidos, documento,sexo, correo, telefono])
        if obj:
            if obj > 0:
                return True

        return False

    #Función para obtener el listado de los usuarios
    @staticmethod
    def listado():
        sql = 'SELECT DISTINCT persona.* FROM persona inner join rol on persona.tipo_rol = "user" ORDER BY documento;'
        return db.ejecutar_select(sql, None)

class calificacion:
    id = 0
    puntuacion = 0
    comentario = ''
    nickname = ''

    def __init__(self, p_puntuacion, p_comentario) -> None:
        self.puntuacion = p_puntuacion
        self.comentario = p_comentario

    @classmethod
    def cargar(cls, p_documento):
        sql = 'SELECT DISTINCT calificacion.* persona.nickname FROM calificacion inner join producto on producto.referencia = calificacion.referencia_producto inner join carrito  on  carrito.referencia_producto = producto.referencia inner join persona on persona.documento = carrito.documento_persona where persona.documento = ?;'
        obj = db.ejecutar_select(sql,[ p_documento ])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["puntuacion"],obj[0]["comentario"],obj[0]["nickname"])

        return None

class persona():

    #Se crean las variables de la clase
    documento=''
    nickname=''
    nombre =''
    apellidos=''
    correo=''
    telefono =0
    sexo=''
    direccion=''
    pais=''
    departamento=''
    ciudad=''
    contrasena=''
    tipo_rol=''
    estado=''

    #Se establece el método constructor
    def __init__(self,p_documento, p_nickname,p_nombre, p_apellidos, p_correo, p_telefono, p_sexo, p_direccion, p_pais, p_departamento, p_ciudad, p_contrasena, p_tipo_rol, p_estado) -> None:

        self.documento = p_documento
        self.nickname = p_nickname
        self.nombre = p_nombre
        self.apellidos = p_apellidos
        self.correo = p_correo
        self.telefono = p_telefono
        self.sexo = p_sexo
        self.direccion = p_direccion
        self.pais =p_pais
        self.departamento =p_departamento
        self.ciudad =p_ciudad
        self.contrasena =p_contrasena
        self.tipo_rol =p_tipo_rol
        self.estado =p_estado

    #Se crea la función para insertar los datos del registro
    def insertar_registro(self):
        #Se hace la consulta con la base de datos.
        sql='INSERT INTO persona (documento, nickname,nombre,apellidos,correo,telefono,sexo,direccion,pais,departamento,ciudad,contrasena,tipo_rol,estado) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);'
        #Ejecuta el SQL que está arriba (insert en este caso)
        obj=db.ejecutar_insert(sql,[self.documento,self.nickname,self.nombre,self.apellidos,self.correo,self.telefono,self.sexo,self.direccion,self.pais,self.departamento,self.ciudad,self.contrasena,self.tipo_rol,self.estado])
        #Validación de la existencia del objeto
        return (obj>0)

class producto():
    nombre = ""
    referencia = ""
    talla = ""
    precio= ""
    cantidad = ""
    descuento = ""
    color = ""
    descripcion = ""
    sexo = ""

    # cosntructor
    def __init__(self,gp_nombre,gp_referencia, gp_talla, gp_precio, gp_cantidad, gp_descuento, gp_color, gp_descripcion, gp_sexo):
        self.nombre = gp_nombre
        self.referencia = gp_referencia
        self.talla = gp_talla
        self.precio= gp_precio
        self.cantidad = gp_cantidad
        self.descuento = gp_descuento
        self.color = gp_color
        self.descripcion = gp_descripcion
        self.sexo = gp_sexo
 
    @classmethod
    def block(cls, gp_referencia, gp_estado):
        if gp_estado == "T":
            sql = 'UPDATE producto set estado = "F" Where referencia = ?;'
        elif gp_estado == "F":
            sql = 'UPDATE producto set estado = "T" Where referencia = ?;'
        obj = db.ejecutar_insert(sql,[ gp_referencia ])
        if obj:
            if obj > 0:
                return True

        return False

    def crear(self):
        sql="INSERT INTO producto (referencia,nombre,precio,descripcion,estado) VALUES (?,?,?,?,?);"
        sql2="INSERT INTO inventario (talla,referencia_producto,color,cantidad,sexo) VALUES (?,?,?,?,?);"
        obj = db.ejecutar_insert(sql,[self.referencia,self.nombre,self.precio,self.descripcion,'T'])
        obj2 = db.ejecutar_insert(sql2,[self.talla,self.referencia,self.color,self.cantidad,self.sexo])
        if obj and obj2:
            if obj > 0 and obj2>0:
                return True
        return False


    @staticmethod
    def listado():
        sql = 'select producto.estado, producto.nombre, producto.precio, inventario.referencia_producto as referencia, inventario.cantidad, inventario.talla from producto inner join inventario on inventario.referencia_producto=producto.referencia order by nombre asc;'
        return db.ejecutar_select(sql, None)

