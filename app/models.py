# Importación de clases y funciones necesarias de SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import declarative_base, relationship

# Declarando la base para los modelos de SQLAlchemy
Base = declarative_base()

# Clase para la tabla 'Usuarios'
class Usuarios(Base):
    __tablename__ = "Usuarios"
    
    # Definición de las columnas de la tabla
    usuarioID = Column(Integer, primary_key=True, index=True)  # ID único para cada usuario
    nombre = Column(String(100), nullable=False)  # Nombre del usuario
    correo = Column(String(100), unique=True, nullable=False, index=True)  # Correo único para el usuario
    contraseña = Column(String(100), nullable=False)  # Contraseña del usuario
    direccion = Column(String(255), nullable=False)  # Dirección del usuario

# Clase para la tabla 'Categorias'
class Categorias(Base):
    __tablename__ = "Categorias"
    
    # Definición de las columnas de la tabla
    categoriaID = Column(Integer, primary_key=True, index=True)  # ID único para cada categoría
    nombre = Column(String(100), nullable=False)  # Nombre de la categoría
    descripcion = Column(Text, nullable=False)  # Descripción de la categoría

# Clase para la tabla 'Productos'
class Productos(Base):
    __tablename__ = "Productos"
    
    # Definición de las columnas de la tabla
    productoID = Column(Integer, primary_key=True, index=True)  # ID único para cada producto
    nombre = Column(String(100), nullable=False)  # Nombre del producto
    descripcion = Column(Text, nullable=False)  # Descripción del producto
    precio = Column(DECIMAL(10, 2), nullable=False)  # Precio del producto (decimal con 2 decimales)
    categoriaID = Column(Integer, ForeignKey("Categorias.categoriaID"), nullable=False)  # Relación con la categoría
    stock = Column(Integer, nullable=False)  # Stock disponible para el producto

# Clase para la tabla 'Pedidos'
class Pedidos(Base):
    __tablename__ = "Pedidos"
    
    # Definición de las columnas de la tabla
    pedidoID = Column(Integer, primary_key=True, index=True)  # ID único para cada pedido
    usuarioID = Column(Integer, ForeignKey("Usuarios.usuarioID"), nullable=False)  # Relación con el usuario que hizo el pedido
    fecha = Column(DateTime, nullable=False)  # Fecha en que se realizó el pedido
    total = Column(DECIMAL(10, 2), nullable=False)  # Total del pedido

# Clase para la tabla 'Pedido_Productos'
class Pedido_Productos(Base):
    __tablename__ = "Pedido_Productos"
    
    # Definición de las columnas de la tabla
    pedidoID = Column(Integer, ForeignKey("Pedidos.pedidoID"), primary_key=True)  # Relación con el pedido
    productoID = Column(Integer, ForeignKey("Productos.productoID"), primary_key=True)  # Relación con el producto
    cantidad = Column(Integer, nullable=False)  # Cantidad del producto en el pedido
    subtotal = Column(DECIMAL(10, 2), nullable=False)  # Subtotal de ese producto en el pedido
