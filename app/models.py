from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, DateTime, Enum, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

# Declaración de la base para la definición de las tablas.
Base = declarative_base()

# Tabla Usuarios: Representa los usuarios registrados en el sistema.
class Usuarios(Base):
    __tablename__ = "Usuarios"  # Nombre de la tabla en la base de datos.
    usuarioID = Column(Integer, primary_key=True, index=True)  # Identificador único del usuario.
    nombre = Column(String(100), nullable=False)  # Nombre del usuario, obligatorio.
    correo = Column(String(100), unique=True, nullable=False, index=True)  # Correo electrónico único y obligatorio.
    contraseña = Column(String(255), nullable=False)  # Contraseña cifrada del usuario.
    direccion = Column(String(255), nullable=False)  # Dirección del usuario.
    telefono = Column(String(15))  # Teléfono opcional del usuario.
    estado = Column(Enum('activo', 'inactivo'), default='activo')  # Estado del usuario (activo/inactivo).
    created_at = Column(TIMESTAMP, server_default=func.now())  # Fecha de creación del registro.
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # Última fecha de modificación.
    pedidos = relationship("Pedidos", back_populates="usuario")  # Relación con los pedidos realizados por el usuario.

# Tabla Categorías: Define las categorías de los productos.
class Categorias(Base):
    __tablename__ = "Categorias"  # Nombre de la tabla en la base de datos.
    categoriaID = Column(Integer, primary_key=True, index=True)  # Identificador único de la categoría.
    nombre = Column(String(100), nullable=False, unique=True)  # Nombre único y obligatorio de la categoría.
    descripcion = Column(Text)  # Descripción opcional de la categoría.
    estado = Column(Enum('activo', 'inactivo'), default='activo')  # Estado de la categoría.
    created_at = Column(TIMESTAMP, server_default=func.now())  # Fecha de creación del registro.
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # Última fecha de modificación.
    productos = relationship("Productos", back_populates="categoria")  # Relación con los productos asociados a la categoría.

# Tabla Productos: Representa los productos disponibles en el sistema.
class Productos(Base):
    __tablename__ = "Productos"  # Nombre de la tabla en la base de datos.
    productoID = Column(Integer, primary_key=True, index=True)  # Identificador único del producto.
    nombre = Column(String(100), nullable=False)  # Nombre del producto, obligatorio.
    descripcion = Column(Text)  # Descripción opcional del producto.
    precio = Column(DECIMAL(10, 2), nullable=False)  # Precio del producto, obligatorio.
    categoriaID = Column(Integer, ForeignKey("Categorias.categoriaID"), nullable=False)  # Relación con la categoría del producto.
    stock = Column(Integer, nullable=False, default=0)  # Cantidad disponible del producto.
    sku = Column(String(50), unique=True)  # Código único del producto.
    estado = Column(Enum('activo', 'inactivo', 'agotado'), default='activo')  # Estado del producto.
    created_at = Column(TIMESTAMP, server_default=func.now())  # Fecha de creación del registro.
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # Última fecha de modificación.
    categoria = relationship("Categorias", back_populates="productos")  # Relación con la categoría del producto.
    detalles_pedido = relationship("Detalles_Pedido", back_populates="producto")  # Relación con los detalles de pedido asociados al producto.

# Tabla Pedidos: Representa las órdenes realizadas por los usuarios.
class Pedidos(Base):
    __tablename__ = "Pedidos"  # Nombre de la tabla en la base de datos.
    pedidoID = Column(Integer, primary_key=True, index=True)  # Identificador único del pedido.
    usuarioID = Column(Integer, ForeignKey("Usuarios.usuarioID"), nullable=False)  # Relación con el usuario que realizó el pedido.
    fecha_pedido = Column(TIMESTAMP, server_default=func.now())  # Fecha en la que se realizó el pedido.
    estado_pedido = Column(Enum('pendiente', 'procesando', 'enviado', 'entregado', 'cancelado'), default='pendiente')  # Estado actual del pedido.
    total = Column(DECIMAL(10, 2), nullable=False)  # Total del pedido.
    metodo_pago = Column(String(50))  # Método de pago utilizado.
    created_at = Column(TIMESTAMP, server_default=func.now())  # Fecha de creación del registro.
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # Última fecha de modificación.
    usuario = relationship("Usuarios", back_populates="pedidos")  # Relación con el usuario que realizó el pedido.
    detalles = relationship("Detalles_Pedido", back_populates="pedido")  # Relación con los detalles asociados al pedido.

# Tabla Detalles_Pedido: Detalla los productos incluidos en un pedido específico.
class Detalles_Pedido(Base):
    __tablename__ = "Detalles_Pedido"  # Nombre de la tabla en la base de datos.
    detalleID = Column(Integer, primary_key=True, autoincrement=True)  # Identificador único del detalle.
    pedidoID = Column(Integer, ForeignKey("Pedidos.pedidoID"), nullable=False)  # Relación con el pedido al que pertenece el detalle.
    productoID = Column(Integer, ForeignKey("Productos.productoID"), nullable=False)  # Relación con el producto incluido en el detalle.
    cantidad = Column(Integer, nullable=False)  # Cantidad del producto en el detalle.
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)  # Precio unitario del producto.
    subtotal = Column(DECIMAL(10, 2), nullable=False)  # Subtotal del detalle (precio_unitario * cantidad).
    created_at = Column(TIMESTAMP, server_default=func.now())  # Fecha de creación del registro.
    pedido = relationship("Pedidos", back_populates="detalles")  # Relación con el pedido asociado.
    producto = relationship("Productos", back_populates="detalles_pedido")  # Relación con el producto incluido en el detalle.