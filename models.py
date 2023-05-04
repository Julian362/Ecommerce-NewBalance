import db
from werkzeug.security import generate_password_hash, check_password_hash

hashed_password_code = "pbkdf2:sha256"


class User:
    nickname = ""
    document = ""
    email = ""
    password = ""
    rol = ""

    def __init__(self, p_nickname, p_document, p_email, p_password, p_rol):
        self.nickname = p_nickname
        self.document = p_document
        self.email = p_email
        self.password = p_password
        self.rol = p_rol

    @classmethod
    def load(cls, p_email):
        sql = "SELECT * FROM person WHERE email=?"
        obj = db.execute_select(sql, [p_email])
        if obj and len(obj) > 0:
            return cls(
                obj[0]["nickname"],
                obj[0]["document"],
                obj[0]["email"],
                obj[0]["password"],
                obj[0]["rol"],
            )
        return None

    def logging(self):
        sql = "SELECT * FROM person WHERE email=?"
        obj_user = db.execute_select(sql, [self.email])
        if obj_user and len(obj_user) > 0:
            if check_password_hash(obj_user[0]["password"], self.password):
                return True
        return False


class Person:
    document = ""
    nickname = ""
    name = ""
    last_name = ""
    email = ""
    phone = 0
    gender = ""
    address = ""
    country = ""
    department = ""
    city = ""
    password = ""
    rol = ""
    state = ""

    def __init__(
        self,
        p_document,
        p_nickname,
        p_name,
        p_last_name,
        p_email,
        p_phone,
        p_gender,
        p_address,
        p_country,
        p_department,
        p_city,
        p_password,
        p_rol,
        p_state,
    ) -> None:
        self.document = p_document
        self.nickname = p_nickname
        self.name = p_name
        self.last_name = p_last_name
        self.email = p_email
        self.phone = p_phone
        self.gender = p_gender
        self.address = p_address
        self.country = p_country
        self.department = p_department
        self.city = p_city
        self.password = p_password
        self.rol = p_rol
        self.state = p_state

    def create(self):
        sql = "INSERT INTO person (document, nickname,name,last_name,email,phone,gender,address,country,department,city,password,rol,state) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
        hashed_password = generate_password_hash(
            self.password, method=hashed_password_code, salt_length=40
        )
        obj = db.execute_sql(
            sql,
            [
                self.document,
                self.nickname,
                self.name,
                self.last_name,
                self.email,
                self.phone,
                self.gender,
                self.address,
                self.country,
                self.department,
                self.city,
                hashed_password,
                self.rol,
                self.state,
            ],
        )
        return obj > 0

    @classmethod
    def cargar(cls, p_rol, p_document):
        sql = "SELECT * FROM person WHERE rol = ? and document=?;"
        obj = db.execute_select(sql, [p_rol, p_document])
        if obj and len(obj) > 0:
            return cls(
                obj[0]["document"],
                obj[0]["nickname"],
                obj[0]["name"],
                obj[0]["last_name"],
                obj[0]["email"],
                obj[0]["phone"],
                obj[0]["gender"],
                obj[0]["address"],
                obj[0]["country"],
                obj[0]["department"],
                obj[0]["city"],
                obj[0]["password"],
                obj[0]["rol"],
                obj[0]["state"],
            )

        return None

    @classmethod
    def delete(cls, p_rol, p_document):
        sql = "DELETE FROM person WHERE rol = ? and document=?;"
        obj = db.execute_sql(sql, [p_rol, p_document])
        if obj and obj > 0:
            return "Borrado correctamente el user "

        return None

    @classmethod
    def block(cls, p_document, p_state):
        if p_state == "T":
            sql = 'UPDATE person set state = "F" Where document = ?;'
        elif p_state == "F":
            sql = 'UPDATE person set state = "T" Where document = ?;'
        obj = db.execute_sql(sql, [p_document])
        if obj and obj > 0:
            return True

        return False

    @classmethod
    def edit(
        cls,
        document,
        nickname,
        name,
        last_name,
        email,
        phone,
        gender,
        address,
        country,
        department,
        city,
        password,
        rol,
    ):
        sql = "UPDATE person set nickname=?,name=?,last_name=?,email=?,phone=?,gender=?,address=?,country=?,department=?,city=?,password=?,rol=? WHERE document=?"
        hashed_password = generate_password_hash(
            password, method=hashed_password_code, salt_length=40
        )
        obj = db.execute_sql(
            sql,
            [
                nickname,
                name,
                last_name,
                email,
                phone,
                gender,
                address,
                country,
                department,
                city,
                hashed_password,
                rol,
                document,
            ],
        )
        if obj and obj > 0:
            return True

    def create(self):
        sql = "INSERT INTO person (document,nickname,name,last_name,email,phone,gender,address,country,department,city,password,rol,state) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
        hashed_password = generate_password_hash(
            self.password, method=hashed_password_code, salt_length=40
        )
        obj = db.execute_sql(
            sql,
            [
                self.document,
                self.nickname,
                self.name,
                self.last_name,
                self.email,
                self.phone,
                self.gender,
                self.address,
                self.country,
                self.department,
                self.city,
                hashed_password,
                self.rol,
                self.state,
            ],
        )
        if obj and obj > 0:
            return True

        return False

    @staticmethod
    def list(rol):
        sql = "SELECT * FROM person WHERE rol = ? ORDER BY document;"

        return db.execute_select(sql, [rol])


class Calification:
    id = 0
    rating = 0
    comment = ""
    reference_product = ""
    nickname = ""
    document = ""

    def __init__(
        self,
        p_id,
        p_rating,
        p_comment,
        p_reference_product,
        p_nickname,
        p_document,
    ) -> None:
        self.id = p_id
        self.rating = p_rating
        self.comment = p_comment
        self.reference_product = p_reference_product
        self.nickname = p_nickname
        self.document = p_document

    @classmethod
    def cargar(cls, p_document, p_reference_product):
        sql = "SELECT person.document, person.nickname, calification.*  FROM calification inner join product on product.reference = calification.reference_product inner join inventory on inventory.reference_product = product.reference inner join cart_inventory on cart_inventory.id_inventory = inventory.id inner join cart on cart.id = cart_inventory.id_cart inner join person on person.document = cart.document_person where person.document = ? and product.reference=?;"
        obj = db.execute_select(sql, [p_document, p_reference_product])
        if obj and len(obj) > 0:
            return cls(
                obj[0]["id"],
                obj[0]["rating"],
                obj[0]["comment"],
                obj[0]["reference_product"],
                obj[0]["nickname"],
                obj[0]["document"],
            )

        return None

    def create(self):
        sql = (
            "INSERT INTO calification (rating,comment,reference_product)VALUES (?,?,?);"
        )
        obj = db.execute_sql(sql, [self.rating, self.comment, self.reference_product])
        if obj and obj > 0:
            return True

    @classmethod
    def edit(cls, rating, comment, reference, id):
        sql = "UPDATE calification SET rating = ?,  comment = ?, reference_product = ? WHERE id = ? ;"
        obj = db.execute_sql(sql, [rating, comment, reference, id])
        if obj and obj > 0:
            return True

    @classmethod
    def delete(cls, id):
        sql = "DELETE FROM calification WHERE id = ? ;"
        obj = db.execute_sql(sql, [id])
        if obj and obj > 0:
            return "Borrado correctamente el comment "

        return None

    @staticmethod
    def all_comments(reference):
        sql = " SELECT calification.nickname, calification.comment, calification.rating, calification.reference_product FROM calification WHERE reference_product = ? ORDER BY id desc;"
        return db.execute_select(sql, [reference])

    @staticmethod
    def limit_comments(reference):
        sql = " SELECT calification.nickname, calification.comment, calification.rating, calification.reference_product FROM calification WHERE reference_product = ? ORDER BY id desc LIMIT 3;"
        return db.execute_select(sql, [reference])

    @staticmethod
    def average_comments(reference):
        sql = "SELECT ROUND(AVG(rating),2) as average FROM calification where reference_product = ? ;"
        return db.execute_select(sql, [reference])


class Admin:
    name = ""
    last_name = ""
    document = ""
    nickname = ""
    phone = 0
    email = ""
    gender = ""
    country = ""
    department = ""
    city = ""
    address = ""
    password = ""
    rol = ""
    state = ""

    def __init__(
        self,
        p_name,
        p_last_name,
        p_document,
        p_gender,
        p_nickname,
        p_phone,
        p_email,
        p_country,
        p_department,
        p_city,
        p_address,
        p_password,
        p_rol,
        p_state,
    ):
        self.name = p_name
        self.last_name = p_last_name
        self.document = p_document
        self.nickname = p_nickname
        self.phone = p_phone
        self.email = p_email
        self.gender = p_gender
        self.country = p_country
        self.department = p_department
        self.city = p_city
        self.address = p_address
        self.password = p_password
        self.rol = p_rol
        self.state = p_state

    @classmethod
    def load(cls, p_document):
        sql = "SELECT document, nickname, name, last_name, email, phone, gender, address, country, department, city, password, rol, state FROM person WHERE rol='admin' and document=?;"
        obj = db.execute_select(sql, [p_document])
        if obj and len(obj) > 0:
            return cls(
                obj[0]["name"],
                obj[0]["last_name"],
                obj[0]["document"],
                obj[0]["gender"],
                obj[0]["nickname"],
                obj[0]["phone"],
                obj[0]["email"],
                obj[0]["country"],
                obj[0]["department"],
                obj[0]["city"],
                obj[0]["address"],
                obj[0]["password"],
                obj[0]["rol"],
                obj[0]["state"],
            )
        return None

    def edit(self):
        sql = "UPDATE person SET nickname = ?, name = ?, last_name = ?, email = ?, phone = ?, gender = ?, address = ?, country = ?, department = ?, city = ?, password = ?, rol = ?, state = ? WHERE document = ? AND rol = 'admin';"
        hashed_password = generate_password_hash(
            self.password, method=hashed_password_code, salt_length=40
        )
        obj = db.execute_sql(
            sql,
            [
                self.nickname,
                self.name,
                self.last_name,
                self.email,
                self.phone,
                self.gender,
                self.address,
                self.country,
                self.department,
                self.city,
                hashed_password,
                self.rol,
                self.state,
                self.document,
            ],
        )
        if obj and obj > 0:
            return True
        return False

    def create(self):
        sql = "INSERT INTO person (document, nickname, name, last_name, email, phone, gender, address, country, department, city, password, rol, state) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        hashed_password = generate_password_hash(
            self.password, method=hashed_password_code, salt_length=40
        )
        obj = db.execute_sql(
            sql,
            [
                self.document,
                self.nickname,
                self.name,
                self.last_name,
                self.email,
                self.phone,
                self.gender,
                self.address,
                self.country,
                self.department,
                self.city,
                hashed_password,
                self.rol,
                self.state,
            ],
        )
        if obj and obj > 0:
            return True
        return False

    def delete(self):
        sql = "DELETE FROM person WHERE document = ? AND rol = 'admin';"
        obj = db.execute_sql(sql, [self.document])
        if obj and obj > 0:
            return True
        return False

    def block(self):
        if self.state == "T":
            sql = "UPDATE person set state = 'F' Where document = ? AND rol = 'admin';"
        elif self.state == "F":
            sql = "UPDATE person set state = 'T' Where document = ? AND rol = 'admin';"
        obj = db.execute_sql(sql, [self.document])
        if obj and obj > 0:
            return True
        return False

    @staticmethod
    def list():
        sql = "SELECT state, document, name, last_name, email FROM person WHERE rol='admin';"
        return db.execute_select(sql, None)


class Product:
    id = 0
    name = ""
    reference = ""
    size = ""
    price = ""
    amount = ""
    discount = ""
    color = ""
    description = ""
    gender = ""

    def __init__(
        self,
        gp_id,
        gp_name,
        gp_reference,
        gp_size,
        gp_price,
        gp_amount,
        gp_discount,
        gp_color,
        gp_description,
        gp_gender,
    ):
        self.id = gp_id
        self.name = gp_name
        self.reference = gp_reference
        self.size = gp_size
        self.price = gp_price
        self.amount = gp_amount
        self.discount = gp_discount
        self.color = gp_color
        self.description = gp_description
        self.gender = gp_gender

    @classmethod
    def block(cls, gp_reference, gp_state):
        if gp_state == "T":
            sql = 'UPDATE product set state = "F" Where reference = ?;'
        elif gp_state == "F":
            sql = 'UPDATE product set state = "T" Where reference = ?;'
        obj = db.execute_sql(sql, [gp_reference])
        if obj and obj > 0:
            return True

        return False

    def create(self):
        sql = "INSERT INTO product (reference,name,price,description,state,discount) VALUES (?,?,?,?,?,?);"
        sql2 = "INSERT INTO inventory (size,reference_product,color,amount,gender) VALUES (?,?,?,?,?);"
        obj = db.execute_sql(
            sql,
            [
                self.reference,
                self.name,
                self.price,
                self.description,
                "T",
                self.discount,
            ],
        )
        obj2 = db.execute_sql(
            sql2, [self.size, self.reference, self.color, self.amount, self.gender]
        )
        if obj and obj2 and obj > 0 and obj2 > 0:
            return True
        return False

    @classmethod
    def load(cls, id):
        sql = "select product.name, product.reference, inventory.size, product.price, inventory.amount, product.discount, inventory.color, product.description, inventory.gender from product inner join inventory on inventory.reference_product=product.reference WHERE reference= ?;"
        obj = db.execute_select(sql, [id])
        if obj and len(obj) > 0:
            return cls(
                id,
                obj[0]["name"],
                obj[0]["reference"],
                obj[0]["size"],
                obj[0]["price"],
                obj[0]["amount"],
                obj[0]["discount"],
                obj[0]["color"],
                obj[0]["description"],
                obj[0]["gender"],
            )
        return None

    @classmethod
    def load_product(cls, id):
        sql = "select product.name, product.reference, inventory.size, product.price, inventory.amount, product.discount, inventory.color, product.description, inventory.gender from product inner join inventory on inventory.reference_product=product.reference where reference = ?;"
        obj = db.execute_select(sql, [id])
        if obj and len(obj) > 0:
            return cls(
                id,
                obj[0]["name"],
                obj[0]["reference"],
                obj[0]["size"],
                obj[0]["price"],
                obj[0]["amount"],
                obj[0]["discount"],
                obj[0]["color"],
                obj[0]["description"],
                obj[0]["gender"],
            )
        return None

    @classmethod
    def edit(
        cls,
        id,
        name,
        reference,
        size,
        price,
        amount,
        discount,
        color,
        description,
        gender,
    ):
        sql = "UPDATE product SET name = ?,price = ?,description = ?,state = ?,discount = ? WHERE reference=?"
        sql2 = "UPDATE inventory SET size = ?, reference_product = ?, color = ?, amount = ?, gender = ? WHERE id = ?"
        obj = db.execute_sql(sql, [name, price, description, "T", discount, reference])
        obj2 = db.execute_sql(sql2, [size, reference, color, amount, gender, id])
        if obj and obj2 and obj > 0 and obj2 > 0:
            return True

    @classmethod
    def create_cart(cls, reference, document, size, color):
        if not Product.load_cart(document):
            create_cart = "INSERT INTO cart (document_person) VALUES ( ? );"
            db.execute_sql(create_cart, [document])
        select_id = "SELECT person.name,cart.id FROM person INNER JOIN cart ON cart.document_person = person.document WHERE person.document = ?;"
        obj_select_id = db.execute_select(select_id, [document])
        select_product = "SELECT inventory.id,product.name FROM product INNER JOIN inventory ON inventory.reference_product = product.reference WHERE product.reference = ? AND inventory.color = ? AND inventory.size = ?;"
        obj_select_product = db.execute_select(select_product, [reference, color, size])
        if obj_select_product:
            insert_product = "INSERT INTO cart_inventory (id_cart, id_inventory, amount ) VALUES ( ?, ?, ? );"
            obj_select_product = db.execute_sql(
                insert_product,
                [obj_select_id[0]["id"], obj_select_product[0]["id"], 1],
            )
        if obj_select_product:
            return True
        else:
            return False

    @classmethod
    def delete(cls, id):
        sql = "DELETE FROM inventory WHERE id = ? ;"
        obj = db.execute_sql(sql, [id])
        if obj and obj > 0:
            return "Borrado correctamente el comentario "

        return None

    @staticmethod
    def load_individual(ref):
        sql = "select product.name, product.price, product.description, product.reference, inventory.size, inventory.color, inventory.amount from product inner join inventory on inventory.reference_product = product.reference where product.reference = ? ;"
        return db.execute_select(sql, [ref])

    @staticmethod
    def list():
        sql = "select inventory.id, product.state, product.name, product.price, inventory.reference_product as reference, inventory.amount, inventory.size,inventory.color   from product inner join inventory on inventory.reference_product=product.reference  order by name asc;"
        return db.execute_select(sql, None)

    @staticmethod
    def list_search():
        sql = "select product.reference from product order by name desc;"
        return db.execute_select(sql, None)

    @staticmethod
    def list_search_product(reference):
        sql = "select inventory.id, product.state, product.name, product.price, inventory.reference_product as reference, inventory.amount, inventory.size,inventory.color   from product inner join inventory on inventory.reference_product=product.reference where product.reference=? order by name asc;"
        print(db.execute_select(sql, [reference]))
        return db.execute_select(sql, [reference])

    @staticmethod
    def list_reference(gender):
        sql = "select product.state, product.name, product.price, inventory.reference_product as reference, inventory.amount, inventory.size  from product inner join inventory on inventory.reference_product=product.reference where inventory.gender = ? group by reference  order by name asc;"
        return db.execute_select(sql, gender)

    @staticmethod
    def filter(gender, orden, size, color):
        if orden == "asc":
            sql = 'SELECT inventory.id,product.state, product.name,  product.price, inventory.reference_product AS reference, inventory.amount, inventory.size, inventory.color FROM product INNER JOIN inventory ON inventory.reference_product = product.reference WHERE inventory.gender = ? AND CASE WHEN "0" = ? then 1=1 else inventory.color = ? END AND CASE  WHEN "0" = ? then 1=1 else inventory.size = ? END group by reference ORDER BY product.price asc;'
            return db.execute_select(sql, [gender, color, color, size, size])

        elif orden == "desc":
            sql = 'SELECT inventory.id,product.state, product.name,  product.price, inventory.reference_product AS reference, inventory.amount, inventory.size, inventory.color FROM product INNER JOIN inventory ON inventory.reference_product = product.reference WHERE inventory.gender = ? AND CASE WHEN "0" = ? then 1=1 else inventory.color = ? END AND CASE  WHEN "0" = ? then 1=1 else inventory.size = ? END group by reference ORDER BY product.price desc;'
            return db.execute_select(sql, [gender, color, color, size, size])

        else:
            sql = 'SELECT inventory.id,product.state, product.name,  product.price, inventory.reference_product AS reference, inventory.amount, inventory.size, inventory.color FROM product INNER JOIN inventory ON inventory.reference_product = product.reference WHERE inventory.gender = ? AND CASE WHEN "0" = ? then 1=1 else inventory.color = ? END AND CASE  WHEN "0" = ? then 1=1 else inventory.size = ? END group by reference ORDER BY product.name;'
            return db.execute_select(sql, [gender, color, color, size, size])

    @staticmethod
    def load_cart(id):
        sql = " SELECT inventory.id as idv ,cart.id,product.name, product.price, product.reference, inventory.size, inventory.color, inventory.amount from person inner join cart on cart.document_person = person.document inner join cart_inventory on cart_inventory.id_cart = cart.id inner join inventory on inventory.id = cart_inventory.id_inventory inner join product on inventory.reference_product = product.reference where person.document = ? ;"
        return db.execute_select(sql, [id])

    @staticmethod
    def delete_cart(id):
        sql = "delete from cart_inventory where id_inventory = ? ;"
        return db.execute_sql(sql, [id])


class Account:
    name = ""
    last_name = ""
    document = ""
    nickname = ""
    phone = 0
    email = ""
    gender = ""
    country = ""
    department = ""
    city = ""
    address = ""
    password = ""
    rol = ""
    state = ""

    def __init__(
        self,
        p_name,
        p_last_name,
        p_document,
        p_gender,
        p_nickname,
        p_phone,
        p_email,
        p_country,
        p_department,
        p_city,
        p_address,
        p_password,
        p_rol,
        p_state,
    ):
        self.name = p_name
        self.last_name = p_last_name
        self.document = p_document
        self.nickname = p_nickname
        self.phone = p_phone
        self.email = p_email
        self.gender = p_gender
        self.country = p_country
        self.department = p_department
        self.city = p_city
        self.address = p_address
        self.password = p_password
        self.rol = p_rol
        self.state = p_state

    @classmethod
    def load(cls, p_document):
        sql = "SELECT document, nickname, name, last_name, email, phone, gender, address, country, department, city, password, rol, state FROM person WHERE rol='user' and document=?;"
        obj = db.execute_select(sql, [p_document])
        if obj and len(obj) > 0:
            return cls(
                obj[0]["name"],
                obj[0]["last_name"],
                obj[0]["document"],
                obj[0]["gender"],
                obj[0]["nickname"],
                obj[0]["phone"],
                obj[0]["email"],
                obj[0]["country"],
                obj[0]["department"],
                obj[0]["city"],
                obj[0]["address"],
                obj[0]["password"],
                obj[0]["rol"],
                obj[0]["state"],
            )
        return None

    def edit(self):
        sql = "UPDATE person SET nickname = ?, name = ?, last_name = ?, email = ?, phone = ?, gender = ?, address = ?, country = ?, department = ?, city = ?, password = ?, rol = ?, state = ? WHERE document = ? AND rol = 'user';"
        hashed_password = generate_password_hash(
            self.password, method=hashed_password_code, salt_length=40
        )
        obj = db.execute_sql(
            sql,
            [
                self.nickname,
                self.name,
                self.last_name,
                self.email,
                self.phone,
                self.gender,
                self.address,
                self.country,
                self.department,
                self.city,
                hashed_password,
                self.rol,
                self.state,
                self.document,
            ],
        )
        if obj and obj > 0:
            return True
        return False
