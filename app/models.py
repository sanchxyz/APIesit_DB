from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, Enum, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

# Declaración del modelo base para la definición de las tablas de la base de datos.
Base = declarative_base()

# Tabla Usuarios: Almacena información sobre los usuarios registrados en el sistema.
class Usuarios(Base):
    __tablename__ = "Usuarios"  # Nombre de la tabla en la base de datos.
    usuarioID = Column(Integer, primary_key=True, index=True)  # Identificador único del usuario.
    nombre = Column(String(100), nullable=False)  # Nombre del usuario, obligatorio.
    correo = Column(String(100), unique=True, nullable=False, index=True)  # Correo electrónico único, obligatorio y utilizado como índice.
    hashed_password = Column(String, nullable=False)  # Contraseña hasheada, obligatorio por seguridad.
    direccion = Column(String(255), nullable=False)  # Dirección del usuario, obligatorio.
    telefono = Column(String(15))  # Teléfono del usuario, opcional.
    estado = Column(Enum('activo', 'inactivo'), default='activo')  # Estado del usuario, por defecto 'activo'.
    created_at = Column(TIMESTAMP, server_default=func.now())  # Fecha y hora de creación del registro.
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # Fecha y hora de la última modificación.

    # Relación con la tabla Pedidos, permite acceder a los pedidos realizados por el usuario.
    pedidos = relationship("Pedidos", back_populates="usuario")

# Tabla Categorías: Contiene las categorías a las que pueden pertenecer los productos.
class Categorias(Base):
    __tablename__ = "Categorias"
    categoriaID = Column(Integer, primary_key=True, index=True)  # Identificador único de la categoría.
    nombre = Column(String(100), nullable=False, unique=True)  # Nombre único y obligatorio de la categoría.
    descripcion = Column(Text)  # Descripción opcional de la categoría.
    estado = Column(Enum('activo', 'inactivo'), default='activo')  # Estado de la categoría, por defecto 'activo'.
    created_at = Column(TIMESTAMP, server_default=func.now())  # Fecha de creación del registro.
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # Fecha de la última modificación.

    # Relación con la tabla Productos, permite acceder a los productos asociados a la categoría.
    productos = relationship("Productos", back_populates="categoria")

# Tabla Productos: Almacena los productos disponibles para los usuarios.
class Productos(Base):
    __tablename__ = "Productos"
    productoID = Column(Integer, primary_key=True, index=True)  # Identificador único del producto.
    nombre = Column(String(100), nullable=False)  # Nombre del producto, obligatorio.
    descripcion = Column(Text)  # Descripción opcional del producto.
    precio = Column(DECIMAL(10, 2), nullable=False)  # Precio del producto, obligatorio.
    categoriaID = Column(Integer, ForeignKey("Categorias.categoriaID"), nullable=False)  # Relación con la categoría del producto.
    stock = Column(Integer, nullable=False, default=0)  # Cantidad disponible del producto, por defecto 0.
    sku = Column(String(50), unique=True)  # Código único del producto.
    estado = Column(Enum('activo', 'inactivo', 'agotado'), default='activo')  # Estado del producto, por defecto 'activo'.
    created_at = Column(TIMESTAMP, server_default=func.now())  # Fecha de creación del registro.
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # Fecha de la última modificación.

    # Relaciones con otras tablas: Categorías y Detalles_Pedido.
    categoria = relationship("Categorias", back_populates="productos")
    detalles_pedido = relationship("Detalles_Pedido", back_populates="producto")

# Tabla Pedidos: Representa las órdenes realizadas por los usuarios.
class Pedidos(Base):
    __tablename__ = "Pedidos"
    pedidoID = Column(Integer, primary_key=True, index=True)  # Identificador único del pedido.
    usuarioID = Column(Integer, ForeignKey("Usuarios.usuarioID"), nullable=False)  # Relación con el usuario que realizó el pedido.
    fecha_pedido = Column(TIMESTAMP, server_default=func.now())  # Fecha y hora en la que se realizó el pedido.
    estado_pedido = Column(Enum('pendiente', 'procesando', 'enviado', 'entregado', 'cancelado'), default='pendiente')  # Estado actual del pedido.
    total = Column(DECIMAL(10, 2), nullable=False)  # Total del pedido.
    metodo_pago = Column(String(50))  # Método de pago utilizado en el pedido.
    created_at = Column(TIMESTAMP, server_default=func.now())  # Fecha de creación del registro.
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # Fecha de la última modificación.

    # Relaciones con otras tablas: Usuarios y Detalles_Pedido.
    usuario = relationship("Usuarios", back_populates="pedidos")
    detalles = relationship("Detalles_Pedido", back_populates="pedido")

# Tabla Detalles_Pedido: Representa los productos incluidos en un pedido.
class Detalles_Pedido(Base):
    __tablename__ = "Detalles_Pedido"
    detalleID = Column(Integer, primary_key=True, autoincrement=True)  # Identificador único del detalle.
    pedidoID = Column(Integer, ForeignKey("Pedidos.pedidoID"), nullable=False)  # Relación con el pedido al que pertenece el detalle.
    productoID = Column(Integer, ForeignKey("Productos.productoID"), nullable=False)  # Relación con el producto incluido en el detalle.
    cantidad = Column(Integer, nullable=False)  # Cantidad del producto incluida en el detalle.
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)  # Precio unitario del producto.
    subtotal = Column(DECIMAL(10, 2), nullable=False)  # Subtotal del detalle (precio_unitario * cantidad).
    created_at = Column(TIMESTAMP, server_default=func.now())  # Fecha de creación del registro.

    # Relaciones con otras tablas: Pedidos y Productos.
    pedido = relationship("Pedidos", back_populates="detalles")
    producto = relationship("Productos", back_populates="detalles_pedido")
