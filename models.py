import db
from werkzeug.security import generate_password_hash, check_password_hash

#Clase usuario, para la respectiva pantalla.
class usuario():
    #Se crean las variables de la clase
    nickname=''
    documento=''
    correo=''
    contrasena=''
    tipo_rol=''

    #Se establece el método constructor
    def __init__(self,p_nickname,p_documento,p_correo, p_contrasena, p_tipo_rol):
        self.nickname=p_nickname
        self.documento=p_documento
        self.correo = p_correo
        self.contrasena =p_contrasena
        self.tipo_rol= p_tipo_rol

    @classmethod
    def cargar(cls,p_correo):
        sql="SELECT * FROM persona WHERE correo=?"
        obj=db.ejecutar_select(sql,[p_correo])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["nickname"], obj[0]["documento"], obj[0]["correo"], obj[0]["contrasena"], obj[0]["tipo_rol"]) 
        return None


    def logear(self):
        # sql="SELECT * FROM usuarios WHERE usuario='"+ self.usuario + "' and password='"+ self.password + "'"
        sql="SELECT * FROM persona WHERE correo=?"
        obj_usuario=db.ejecutar_select(sql,[self.correo])
        if obj_usuario:
            if len(obj_usuario) >0:
                if check_password_hash(obj_usuario[0]["contrasena"],self.contrasena):
                    return True
        return False

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

        sql='INSERT INTO persona (documento, nickname,nombre,apellidos,correo,telefono,sexo,direccion,pais,departamento,ciudad,contrasena,tipo_rol,estado) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);'
        hashed_contrena=generate_password_hash(self.contrasena, method='pbkdf2:sha256',salt_length=40)
        obj=db.ejecutar_insert(sql,[self.documento,self.nickname,self.nombre,self.apellidos,self.correo,self.telefono,self.sexo,self.direccion,self.pais,self.departamento,self.ciudad,hashed_contrena,self.tipo_rol,self.estado])
        return (obj>0)

    # def insertar_registro(self):
    #     #Se hace la consulta con la base de datos.
    #     sql='INSERT INTO persona (documento, nickname,nombre,apellidos,correo,telefono,sexo,direccion,pais,departamento,ciudad,contrasena,tipo_rol,estado) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);'
    #     #Ejecuta el SQL que está arriba (insert en este caso)
    #     obj=db.ejecutar_insert(sql,[self.documento,self.nickname,self.nombre,self.apellidos,self.correo,self.telefono,self.sexo,self.direccion,self.pais,self.departamento,self.ciudad,self.contrasena,self.tipo_rol,self.estado])
    #     #Validación de la existencia del objeto
    #     return (obj>0)

    @classmethod
    def cargar(cls, p_rol, p_documento):
        sql = 'SELECT * FROM persona WHERE tipo_rol = ? and documento=?;'
        obj = db.ejecutar_select(sql,[ p_rol, p_documento])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["documento"],obj[0]["nickname"],obj[0]["nombre"], obj[0]["apellidos"], obj[0]["correo"], obj[0]["telefono"], obj[0]["sexo"], obj[0]["direccion"], obj[0]["pais"], obj[0]["departamento"], obj[0]["ciudad"], obj[0]["contrasena"], obj[0]["tipo_rol"], obj[0]["estado"])

        return None

    # Función para eliminar
    @classmethod
    def delete(cls, p_rol, p_documento):
        sql = 'DELETE FROM persona WHERE tipo_rol = ? and documento=?;'
        obj = db.ejecutar_insert(sql,[ p_rol, p_documento ])
        if obj:
            if obj > 0:
                return "Borrado corectamente el usuario "

        return None

    # Función para el bloquear o desbloquear al usuario
    @classmethod
    def block(cls, p_documento, p_estado):
        if p_estado == "T":
            sql = 'UPDATE persona set estado = "F" Where documento = ?;'
        elif p_estado == "F":
            sql = 'UPDATE persona set estado = "T" Where documento = ?;'
        obj = db.ejecutar_insert(sql, [p_documento])
        if obj:
            if obj > 0:
                return True

        return False

    # Función para editar los datos de usuario
    @classmethod
    def editar(cls,documento,nickname,nombre,apellidos,correo,telefono,sexo,direccion,pais,departamento,ciudad,contrasena,rol):
        sql="UPDATE persona set nickname=?,nombre=?,apellidos=?,correo=?,telefono=?,sexo=?,direccion=?,pais=?,departamento=?,ciudad=?,contrasena=?,tipo_rol=? WHERE documento=?"
        hashed_contrena=generate_password_hash(contrasena, method='pbkdf2:sha256',salt_length=40)
        obj = db.ejecutar_insert(sql,[nickname,nombre,apellidos,correo,telefono,sexo,direccion,pais,departamento,ciudad,hashed_contrena,rol,documento])
        if obj:
            if obj > 0:
                return True

    #Función para crear al usuario
    def crear(self):
        sql="INSERT INTO persona (documento,nickname,nombre,apellidos,correo,telefono,sexo,direccion,pais,departamento,ciudad,contrasena,tipo_rol,estado) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
        hashed_contrena=generate_password_hash(self.contrasena, method='pbkdf2:sha256',salt_length=40)
        obj = db.ejecutar_insert(sql,[self.documento,self.nickname,self.nombre,self.apellidos,self.correo,self.telefono,self.sexo,self.direccion,self.pais,self.departamento,self.ciudad,hashed_contrena,self.tipo_rol,self.estado])
        if obj:
            if obj > 0:
                return True

        return False

    # Función para obtener el listado de los usuarios
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

    @staticmethod
    def todos_los_comentarios(referencia):
        sql=' SELECT calificacion.nickname, calificacion.comentario, calificacion.puntuacion, calificacion.referencia_producto FROM calificacion WHERE referencia_producto = ? ORDER BY id desc;'
        return db.ejecutar_select(sql,[referencia])

    @staticmethod
    def tres_comentarios(referencia):
        sql= ' SELECT calificacion.nickname, calificacion.comentario, calificacion.puntuacion, calificacion.referencia_producto FROM calificacion WHERE referencia_producto = ? ORDER BY id desc LIMIT 3;'
        return db.ejecutar_select(sql,[referencia])
    
    @staticmethod
    def promedio_comentarios(referencia):
        sql='SELECT ROUND(AVG(puntuacion),2) as promedio FROM calificacion where referencia_producto = ? ;'
        return db.ejecutar_select(sql,[referencia])
class gestionAdministrador():
    nombre = ''
    apellido = ''
    documento = ''
    nickname = ''
    telefono = 0
    correo = ''
    sexo = ''
    pais = ''
    departamento = ''
    ciudad = ''
    direccion = ''
    contrasena = ''
    tipo_rol = ''
    estado = ''

    def __init__(self, p_nombre, p_apellido, p_documento, p_sexo,  p_nickname, p_telefono, p_correo, p_pais, p_departamento, p_ciudad, p_direccion, p_contrasena, p_tipo_rol, p_estado):
        self.nombre = p_nombre
        self.apellido = p_apellido
        self.documento = p_documento
        self.nickname = p_nickname
        self.telefono = p_telefono
        self.correo = p_correo
        self.sexo = p_sexo
        self.pais = p_pais
        self.departamento = p_departamento
        self.ciudad = p_ciudad
        self.direccion = p_direccion
        self.contrasena = p_contrasena
        self.tipo_rol = p_tipo_rol
        self.estado = p_estado

    @classmethod
    def cargar_datos(cls, p_documento):
        sql = "SELECT documento, nickname, nombre, apellidos, correo, telefono, sexo, direccion, pais, departamento, ciudad, contrasena, tipo_rol, estado FROM persona WHERE tipo_rol='admin' and documento=?;"
        obj = db.ejecutar_select(sql, [p_documento])
        if obj:
            if len(obj) > 0:
                return cls(obj[0]["nombre"], obj[0]["apellidos"], obj[0]["documento"], obj[0]["sexo"], obj[0]["nickname"], obj[0]["telefono"], obj[0]["correo"], obj[0]["pais"], obj[0]["departamento"], obj[0]["ciudad"], obj[0]["direccion"], obj[0]["contrasena"], obj[0]["tipo_rol"], obj[0]["estado"])
        return None
    
    def editar_datos(self):
        sql = "UPDATE persona SET nickname = ?, nombre = ?, apellidos = ?, correo = ?, telefono = ?, sexo = ?, direccion = ?, pais = ?, departamento = ?, ciudad = ?, contrasena = ?, tipo_rol = ?, estado = ? WHERE documento = ? AND tipo_rol = 'admin';"
        hashed_contrena=generate_password_hash(self.contrasena, method='pbkdf2:sha256',salt_length=40)
        obj = db.ejecutar_insert(sql, [self.nickname, self.nombre, self.apellido, self.correo, self.telefono, self.sexo, self.direccion, self.pais, self.departamento, self.ciudad, hashed_contrena, self.tipo_rol, self.estado, self.documento])
        if obj:
            if obj > 0:
                return True
        return False

    def crear_admin(self):
        sql="INSERT INTO persona (documento, nickname, nombre, apellidos, correo, telefono, sexo, direccion, pais, departamento, ciudad, contrasena, tipo_rol, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        hashed_contrena=generate_password_hash(self.contrasena, method='pbkdf2:sha256',salt_length=40)
        obj = db.ejecutar_insert(sql, [self.documento, self.nickname, self.nombre, self.apellido, self.correo, self.telefono, self.sexo, self.direccion, self.pais, self.departamento, self.ciudad, hashed_contrena, self.tipo_rol, self.estado])
        if obj:
            if obj > 0:
                return True
        return False

    def eliminar_admin(self):
        sql="DELETE FROM persona WHERE documento = ? AND tipo_rol = 'admin';"
        obj = db.ejecutar_insert(sql, [self.documento])
        if obj:
            if obj > 0:
                return True
        return False

    def bloquear_admin(self):
        if self.estado=="T":
            sql="UPDATE persona set estado = 'F' Where documento = ? AND tipo_rol = 'admin';"
        elif self.estado=="F":
            sql="UPDATE persona set estado = 'T' Where documento = ? AND tipo_rol = 'admin';"
        obj=db.ejecutar_insert(sql, [self.documento])
        if obj:
            if obj > 0:
                return True
        return False

    @staticmethod
    def listado_administrador():
        sql = "SELECT estado, documento, nombre, apellidos, correo FROM persona WHERE tipo_rol='admin';"
        return db.ejecutar_select(sql, None)


class producto():
    id=0
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
    def __init__(self,gp_id,gp_nombre,gp_referencia, gp_talla, gp_precio, gp_cantidad, gp_descuento, gp_color, gp_descripcion, gp_sexo):
        self.id=gp_id
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


    # Metodo de insercion a la base de datos
    def crear(self):
        sql="INSERT INTO producto (referencia,nombre,precio,descripcion,estado,descuento) VALUES (?,?,?,?,?,?);"
        sql2="INSERT INTO inventario (talla,referencia_producto,color,cantidad,sexo) VALUES (?,?,?,?,?);"
        obj = db.ejecutar_insert(sql,[self.referencia,self.nombre,self.precio,self.descripcion,'T', self.descuento])
        obj2 = db.ejecutar_insert(sql2,[self.talla,self.referencia,self.color,self.cantidad,self.sexo])
        if obj and obj2:
            if obj > 0 and obj2>0:
                return True
        return False


    #  Metodo de cargar datos al formulario
    @classmethod
    def cargar(cls,id):
        sql = 'select producto.nombre, producto.referencia, inventario.talla, producto.precio, inventario.cantidad, producto.descuento, inventario.color, producto.descripcion, inventario.sexo from producto inner join inventario on inventario.referencia_producto=producto.referencia WHERE id= ?;'
        obj = db.ejecutar_select(sql,[id])
        if obj:
            if len(obj)>0:
                # orden del constructor
                return cls(id,obj[0]["nombre"],obj[0]["referencia"],obj[0]["talla"], obj[0]["precio"], obj[0]["cantidad"], obj[0]["descuento"], obj[0]["color"], obj[0]["descripcion"], obj[0]["sexo"])
        return None
    
    @classmethod
    def cargarProducto(cls,id):
        sql = 'select producto.nombre, producto.referencia, inventario.talla, producto.precio, inventario.cantidad, producto.descuento, inventario.color, producto.descripcion, inventario.sexo from producto inner join inventario on inventario.referencia_producto=producto.referencia where referencia = ?;'
        obj = db.ejecutar_select(sql,[id])
        if obj:
            if len(obj)>0:
                # orden del constructor
                return cls(id,obj[0]["nombre"],obj[0]["referencia"],obj[0]["talla"], obj[0]["precio"], obj[0]["cantidad"], obj[0]["descuento"], obj[0]["color"], obj[0]["descripcion"], obj[0]["sexo"])
        return None






    #Función para editar los datos de usuario
    @classmethod
    def editar(cls,id,nombre,referencia,talla,precio,cantidad,descuento,color,descripcion,sexo):
        sql="UPDATE producto SET nombre = ?,precio = ?,descripcion = ?,estado = ?,descuento = ? WHERE referencia=?"
        sql2="UPDATE inventario SET talla = ?, referencia_producto = ?, color = ?, cantidad = ?, sexo = ? WHERE id = ?"
        obj = db.ejecutar_insert(sql,[ nombre, precio, descripcion, 'T', descuento,referencia])
        obj2 = db.ejecutar_insert(sql2,[talla, referencia, color, cantidad,sexo,id])
        if obj and obj2:
            if obj > 0 and obj2>0:
                return True
    @classmethod
    def crear_carrito(cls,referencia,documento,talla,color):
        if not producto.cargar_carrito(documento):
            create_carrito="INSERT INTO carrito (documento_persona) VALUES ( ? );"
            obj_create_carrito = db.ejecutar_insert(create_carrito,[documento])
        select_id="SELECT persona.nombre,carrito.id FROM persona INNER JOIN carrito ON carrito.documento_persona = persona.documento WHERE persona.documento = ?;"
        obj_select_id= db.ejecutar_select(select_id,[documento])
        select_producto="SELECT inventario.id,producto.nombre FROM producto INNER JOIN inventario ON inventario.referencia_producto = producto.referencia WHERE producto.referencia = ? AND inventario.color = ? AND inventario.talla = ?;"
        obj_select_producto= db.ejecutar_select(select_producto,[referencia, color, talla])
        if obj_select_producto:
            insert_producto="INSERT INTO carrito_inventario (id_carrito, id_inventario, cantidad ) VALUES ( ?, ?, ? );"
            obj_select_producto= db.ejecutar_insert(insert_producto,[obj_select_id[0]["id"],obj_select_producto[0]["id"],1])
        if obj_select_producto:
            return True
        else:
            return False


    @classmethod
    def delete(cls,id):
        sql = 'DELETE FROM inventario WHERE id = ? ;'
        obj = db.ejecutar_insert(sql,[ id ])
        if obj:
            if obj>0:
                return "Borrado corectamente el comentario "

        return None

    # Metodo de estatico para llamar la lista de productos
    @staticmethod
    def productoindividual(ref):
        sql= 'select producto.nombre, producto.precio, producto.descripcion, producto.referencia, inventario.talla, inventario.color, inventario.cantidad from producto inner join inventario on inventario.referencia_producto = producto.referencia where producto.referencia = ? ;'
        return db.ejecutar_select(sql,[ref])

    @staticmethod
    def listado():
        sql = 'select inventario.id, producto.estado, producto.nombre, producto.precio, inventario.referencia_producto as referencia, inventario.cantidad, inventario.talla,inventario.color   from producto inner join inventario on inventario.referencia_producto=producto.referencia  order by nombre asc;'
        return db.ejecutar_select(sql, None)
           
    @staticmethod
    def listado_searchs():
        sql = 'select  producto.referencia from producto order by nombre desc;'
        return db.ejecutar_select(sql, None)
    
    @staticmethod
    def listado_buscarp(referencia):
        sql = 'select inventario.id, producto.estado, producto.nombre, producto.precio, inventario.referencia_producto as referencia, inventario.cantidad, inventario.talla,inventario.color   from producto inner join inventario on inventario.referencia_producto=producto.referencia where producto.referencia=? order by nombre asc;'
        return db.ejecutar_select(sql, [referencia])

    @staticmethod
    def listado_referencia(sexo):
        sql = 'select producto.estado, producto.nombre, producto.precio, inventario.referencia_producto as referencia, inventario.cantidad, inventario.talla  from producto inner join inventario on inventario.referencia_producto=producto.referencia where inventario.sexo = ? group by referencia  order by nombre asc;'
        return db.ejecutar_select(sql, sexo)

    

    @staticmethod
    def filtrar(sexo, orden, talla, color):

        if orden=="asc":
            sql = 'SELECT inventario.id,producto.estado, producto.nombre,  producto.precio, inventario.referencia_producto AS referencia, inventario.cantidad, inventario.talla, inventario.color FROM producto INNER JOIN inventario ON inventario.referencia_producto = producto.referencia WHERE inventario.sexo = ? AND CASE WHEN "0" = ? then 1=1 else inventario.color = ? END AND CASE  WHEN "0" = ? then 1=1 else inventario.talla = ? END group by referencia ORDER BY producto.precio asc;'
            return db.ejecutar_select(sql,[sexo, color,color, talla, talla])

                        
        elif orden=="desc":
            sql = 'SELECT inventario.id,producto.estado, producto.nombre,  producto.precio, inventario.referencia_producto AS referencia, inventario.cantidad, inventario.talla, inventario.color FROM producto INNER JOIN inventario ON inventario.referencia_producto = producto.referencia WHERE inventario.sexo = ? AND CASE WHEN "0" = ? then 1=1 else inventario.color = ? END AND CASE  WHEN "0" = ? then 1=1 else inventario.talla = ? END group by referencia ORDER BY producto.precio desc;'
            return db.ejecutar_select(sql,[sexo, color,color, talla, talla])
        

        else:
            sql = 'SELECT inventario.id,producto.estado, producto.nombre,  producto.precio, inventario.referencia_producto AS referencia, inventario.cantidad, inventario.talla, inventario.color FROM producto INNER JOIN inventario ON inventario.referencia_producto = producto.referencia WHERE inventario.sexo = ? AND CASE WHEN "0" = ? then 1=1 else inventario.color = ? END AND CASE  WHEN "0" = ? then 1=1 else inventario.talla = ? END group by referencia ORDER BY producto.nombre;'
            return db.ejecutar_select(sql,[sexo, color ,color,talla,talla])
    
    @staticmethod
    def cargar_carrito(id):
        sql = ' SELECT inventario.id as idv ,carrito.id,producto.nombre, producto.precio, producto.referencia, inventario.talla, inventario.color, inventario.cantidad from persona inner join carrito on carrito.documento_persona = persona.documento inner join carrito_inventario on carrito_inventario.id_carrito = carrito.id inner join inventario on inventario.id = carrito_inventario.id_inventario inner join producto on inventario.referencia_producto = producto.referencia where persona.documento = ? ;'
        return db.ejecutar_select(sql, [id])
    @staticmethod
    def borrar_carrito(id):
        sql = 'delete from carrito_inventario where id_inventario = ? ;'
        return db.ejecutar_insert(sql, [id])


class gestionMiCuenta():
    nombre = ''
    apellido = ''
    documento = ''
    nickname = ''
    telefono = 0
    correo = ''
    sexo = ''
    pais = ''
    departamento = ''
    ciudad = ''
    direccion = ''
    contrasena = ''
    tipo_rol = ''
    estado = ''

    def __init__(self, p_nombre, p_apellido, p_documento, p_sexo,  p_nickname, p_telefono, p_correo, p_pais, p_departamento, p_ciudad, p_direccion, p_contrasena, p_tipo_rol, p_estado):
        self.nombre = p_nombre
        self.apellido = p_apellido
        self.documento = p_documento
        self.nickname = p_nickname
        self.telefono = p_telefono
        self.correo = p_correo
        self.sexo = p_sexo
        self.pais = p_pais
        self.departamento = p_departamento
        self.ciudad = p_ciudad
        self.direccion = p_direccion
        self.contrasena = p_contrasena
        self.tipo_rol = p_tipo_rol
        self.estado = p_estado

    @classmethod
    def cargar_datos(cls, p_documento):
        sql = "SELECT documento, nickname, nombre, apellidos, correo, telefono, sexo, direccion, pais, departamento, ciudad, contrasena, tipo_rol, estado FROM persona WHERE tipo_rol='user' and documento=?;"
        obj = db.ejecutar_select(sql, [p_documento])
        if obj:
            if len(obj) > 0:
                return cls(obj[0]["nombre"], obj[0]["apellidos"], obj[0]["documento"], obj[0]["sexo"], obj[0]["nickname"], obj[0]["telefono"], obj[0]["correo"], obj[0]["pais"], obj[0]["departamento"], obj[0]["ciudad"], obj[0]["direccion"], obj[0]["contrasena"], obj[0]["tipo_rol"], obj[0]["estado"])
        return None
    
    def editar_datos(self):
        sql = "UPDATE persona SET nickname = ?, nombre = ?, apellidos = ?, correo = ?, telefono = ?, sexo = ?, direccion = ?, pais = ?, departamento = ?, ciudad = ?, contrasena = ?, tipo_rol = ?, estado = ? WHERE documento = ? AND tipo_rol = 'user';"
        hashed_contrena=generate_password_hash(self.contrasena, method='pbkdf2:sha256',salt_length=40)
        obj = db.ejecutar_insert(sql, [self.nickname, self.nombre, self.apellido, self.correo, self.telefono, self.sexo, self.direccion, self.pais, self.departamento, self.ciudad, hashed_contrena, self.tipo_rol, self.estado, self.documento])
        if obj:
            if obj > 0:
                return True
        return False
