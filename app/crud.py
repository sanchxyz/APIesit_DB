# Importación de la clase Session de SQLAlchemy para manejar la sesión de la base de datos
from sqlalchemy.orm import Session
# Importación de IntegrityError para manejar errores de integridad en la base de datos
from sqlalchemy.exc import IntegrityError
# Importación de los modelos de la base de datos
from .models import Usuarios, Categorias, Productos, Pedidos, Detalles_Pedido

# Función para obtener un usuario de la base de datos por su ID
def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuarios).filter(Usuarios.usuarioID == usuario_id).first()

# Función para crear un nuevo usuario en la base de datos
def create_usuario(db: Session, nombre: str, correo: str, contraseña: str, direccion: str, telefono: str = None, estado: str = 'activo'):
    try:
        usuario = Usuarios(
            nombre=nombre, 
            correo=correo, 
            contraseña=contraseña, 
            direccion=direccion,
            telefono=telefono,
            estado=estado
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Error al crear usuario: {e.orig}")

# Función para eliminar un usuario de la base de datos por su ID
def delete_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuarios).filter(Usuarios.usuarioID == usuario_id).first()
    if not usuario:
        return None
    db.delete(usuario)
    db.commit()
    return usuario

# Función para actualizar los detalles de un usuario por su ID
def update_usuario(db: Session, usuario_id: int, nuevo_usuario: dict):
    usuario = db.query(Usuarios).filter(Usuarios.usuarioID == usuario_id).first()
    if not usuario:
        return None
    for key, value in nuevo_usuario.items():
        setattr(usuario, key, value)
    db.commit()
    db.refresh(usuario)
    return usuario

# Función para obtener una categoría por su ID
def get_categoria(db: Session, categoria_id: int):
    return db.query(Categorias).filter(Categorias.categoriaID == categoria_id).first()

# Función para crear una nueva categoría
def create_categoria(db: Session, nombre: str, descripcion: str = "", estado: str = 'activo'):
    categoria = Categorias(
        nombre=nombre,
        descripcion=descripcion,
        estado=estado
    )
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

# Función para eliminar una categoría por su ID
def delete_categoria(db: Session, categoria_id: int):
    categoria = db.query(Categorias).filter(Categorias.categoriaID == categoria_id).first()
    if not categoria:
        return None
    db.delete(categoria)
    db.commit()
    return categoria

# Función para actualizar una categoría por su ID
def update_categoria(db: Session, categoria_id: int, nueva_categoria: dict):
    categoria = db.query(Categorias).filter(Categorias.categoriaID == categoria_id).first()
    if not categoria:
        return None
    for key, value in nueva_categoria.items():
        setattr(categoria, key, value)
    db.commit()
    db.refresh(categoria)
    return categoria

# Función para obtener un producto por su ID
def get_producto(db: Session, producto_id: int):
    return db.query(Productos).filter(Productos.productoID == producto_id).first()

# Función para crear un nuevo producto
def create_producto(db: Session, nombre: str, descripcion: str, precio: float, categoriaID: int, stock: int, sku: str, estado: str = 'activo'):
    producto = Productos(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        categoriaID=categoriaID,
        stock=stock,
        sku=sku,
        estado=estado
    )
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

# Función para eliminar un producto por su ID
def delete_producto(db: Session, producto_id: int):
    producto = db.query(Productos).filter(Productos.productoID == producto_id).first()
    if not producto:
        return None
    db.delete(producto)
    db.commit()
    return producto

# Función para actualizar un producto por su ID
def update_producto(db: Session, producto_id: int, nuevos_datos: dict):
    producto = db.query(Productos).filter(Productos.productoID == producto_id).first()
    if not producto:
        return None
    for key, value in nuevos_datos.items():
        setattr(producto, key, value)
    db.commit()
    db.refresh(producto)
    return producto

# Función para obtener un pedido por su ID
def get_pedido(db: Session, pedido_id: int):
    return db.query(Pedidos).filter(Pedidos.pedidoID == pedido_id).first()

# Función para crear un nuevo pedido
def create_pedido(db: Session, usuarioID: int, total: float, metodo_pago: str = None, estado_pedido: str = 'pendiente'):
    pedido = Pedidos(
        usuarioID=usuarioID,
        total=total,
        metodo_pago=metodo_pago,
        estado_pedido=estado_pedido
    )
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido

# Función para eliminar un pedido por su ID
def delete_pedido(db: Session, pedido_id: int):
    pedido = db.query(Pedidos).filter(Pedidos.pedidoID == pedido_id).first()
    if not pedido:
        return None
    db.delete(pedido)
    db.commit()
    return pedido

# Función para actualizar un pedido por su ID
def update_pedido(db: Session, pedido_id: int, nuevos_datos: dict):
    pedido = db.query(Pedidos).filter(Pedidos.pedidoID == pedido_id).first()
    if not pedido:
        return None
    for key, value in nuevos_datos.items():
        setattr(pedido, key, value)
    db.commit()
    db.refresh(pedido)
    return pedido

# Función para obtener los detalles de un pedido por su ID
def get_detalle_pedido(db: Session, detalle_id: int):
    return db.query(Detalles_Pedido).filter(Detalles_Pedido.detalleID == detalle_id).first()

# Función para crear un nuevo detalle de pedido
def create_detalle_pedido(db: Session, pedidoID: int, productoID: int, cantidad: int, precio_unitario: float, subtotal: float):
    detalle = Detalles_Pedido(
        pedidoID=pedidoID,
        productoID=productoID,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        subtotal=subtotal
    )
    db.add(detalle)
    db.commit()
    db.refresh(detalle)
    return detalle

# Función para eliminar un detalle de pedido por su ID
def delete_detalle_pedido(db: Session, detalle_id: int):
    detalle = db.query(Detalles_Pedido).filter(Detalles_Pedido.detalleID == detalle_id).first()
    if not detalle:
        return None
    db.delete(detalle)
    db.commit()
    return detalle

# Función para actualizar un detalle de pedido
def update_detalle_pedido(db: Session, detalle_id: int, nuevos_datos: dict):
    detalle = db.query(Detalles_Pedido).filter(Detalles_Pedido.detalleID == detalle_id).first()
    if not detalle:
        return None
    for key, value in nuevos_datos.items():
        setattr(detalle, key, value)
    db.commit()
    db.refresh(detalle)
    return detalle