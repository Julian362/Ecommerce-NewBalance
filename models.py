import db

#Clase usuario, para la respectiva pantalla.
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

    @classmethod
    def cargar(cls, p_rol, p_documento):
        sql = 'SELECT * FROM persona WHERE tipo_rol = ? and documento=?;'
        obj = db.ejecutar_select(sql,[ p_rol, p_documento])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["documento"],obj[0]["nickname"],obj[0]["nombre"], obj[0]["apellidos"], obj[0]["correo"], obj[0]["telefono"], obj[0]["sexo"], obj[0]["direccion"], obj[0]["pais"], obj[0]["departamento"], obj[0]["ciudad"], obj[0]["contrasena"], obj[0]["tipo_rol"], obj[0]["estado"])

        return None

    #Función para eliminar
    @classmethod
    def delete(cls, p_rol, p_documento):
        sql = 'DELETE FROM persona WHERE tipo_rol = ? and documento=?;'
        obj = db.ejecutar_insert(sql,[ p_rol, p_documento ])
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
    def editar(cls,documento,nickname,nombre,apellidos,correo,telefono,sexo,direccion,pais,departamento,ciudad,contrasena,rol):
        sql="UPDATE persona set nickname=?,nombre=?,apellidos=?,correo=?,telefono=?,sexo=?,direccion=?,pais=?,departamento=?,ciudad=?,contrasena=?,tipo_rol=? WHERE documento=?"
        obj = db.ejecutar_insert(sql,[nickname,nombre,apellidos,correo,telefono,sexo,direccion,pais,departamento,ciudad,contrasena,rol,documento])
        if obj:
            if obj > 0:
                return True

    #Función para crear al usuario
    def crear(self):
        sql="INSERT INTO persona (documento,nickname,nombre,apellidos,correo,telefono,sexo,direccion,pais,departamento,ciudad,contrasena,tipo_rol,estado) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
        obj = db.ejecutar_insert(sql,[self.documento,self.nickname,self.nombre,self.apellidos,self.correo,self.telefono,self.sexo,self.direccion,self.pais,self.departamento,self.ciudad,self.contrasena,self.estado])
        if obj:
            if obj > 0:
                return True

        return False

    #Función para obtener el listado de los usuarios
    @staticmethod
    def listado(rol):
        sql = 'SELECT * FROM persona WHERE tipo_rol = ? ORDER BY documento;'

        return db.ejecutar_select(sql, [rol])

class calificacion:
    id = 0
    puntuacion = 0
    comentario = ''
    referencia_producto = ''
    nickname = ''
    documento = ''

    def __init__(self,p_id, p_puntuacion, p_comentario,p_referencia_producto, p_nickname, p_documento) -> None:
        self.id = p_id
        self.puntuacion = p_puntuacion
        self.comentario = p_comentario
        self.referencia_producto = p_referencia_producto
        self.nickname = p_nickname
        self.documento = p_documento

    @classmethod
    def cargar(cls, p_documento,p_referencia_producto):
        sql = 'SELECT persona.documento, persona.nickname, calificacion.*  FROM calificacion inner join producto on producto.referencia = calificacion.referencia_producto inner join inventario on inventario.referencia_producto = producto.referencia inner join carrito_inventario on carrito_inventario.id_inventario = inventario.id inner join carrito on carrito.id = carrito_inventario.id_carrito inner join persona on persona.documento = carrito.documento_persona where persona.documento = ? and producto.referencia=?;'
        obj = db.ejecutar_select(sql,[ p_documento, p_referencia_producto ])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["id"],obj[0]["puntuacion"],obj[0]["comentario"],obj[0]["referencia_producto"],obj[0]["nickname"],obj[0]["documento"])

        return None

    def crear(self):
        sql="INSERT INTO calificacion (puntuacion,comentario,referencia_producto)VALUES (?,?,?);"
        obj = db.ejecutar_insert(sql,[self.puntuacion,self.comentario,self.referencia_producto])
        if obj:
            if obj > 0:
                return True

    @classmethod
    def editar(cls,puntuacion,comentario,referencia,id):
        sql="UPDATE calificacion SET puntuacion = ?,  comentario = ?, referencia_producto = ? WHERE id = ? ;"
        obj = db.ejecutar_insert(sql,[puntuacion,comentario,referencia,id])
        if obj:
            if obj > 0:
                return True

    @classmethod
    def delete(cls,id):
        sql = 'DELETE FROM calificacion WHERE id = ? ;'
        obj = db.ejecutar_insert(sql,[ id ])
        if obj:
            if obj>0:
                return "Borrado corectamente el comentario "

        return None

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
        sql = 'select producto.estado, producto.nombre, producto.precio, inventario.referencia_producto as referencia, inventario.cantidad, inventario.talla  from producto inner join inventario on inventario.referencia_producto=producto.referencia  order by nombre asc;'
        return db.ejecutar_select(sql, None)

    def listado_referencia():
        sql = 'select producto.estado, producto.nombre, producto.precio, inventario.referencia_producto as referencia, inventario.cantidad, inventario.talla  from producto inner join inventario on inventario.referencia_producto=producto.referencia  group by referencia  order by nombre asc;'
        return db.ejecutar_select(sql, None)

