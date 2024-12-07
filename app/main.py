# Importación de módulos necesarios de FastAPI
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Importación de módulos para manejar la base de datos con SQLAlchemy
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base

# Importación de las funciones CRUD desde el módulo correspondiente
from .crud import (
    get_usuario, create_usuario, delete_usuario, update_usuario,
    get_categoria, create_categoria, delete_categoria, update_categoria,
    get_producto, create_producto, delete_producto, update_producto,
    get_pedido, create_pedido, delete_pedido, update_pedido,
    get_detalle_pedido, create_detalle_pedido, delete_detalle_pedido, update_detalle_pedido,
    authenticate_usuario
)

# Importación de Pydantic para definir modelos de datos
from pydantic import BaseModel

# Inicialización de la aplicación FastAPI
app = FastAPI()

# Configuración del middleware CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,  # Permitir el envío de cookies y credenciales
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Ruta de prueba para verificar que la API está funcionando
@app.get("/", response_class=HTMLResponse)
def read_root():
    # Mensaje HTML que describe la API
    message = """Bienvenido a este proyecto que tiene como finalidad<br>
    crear una API que conecte con una base de datos para usar las funciones CRUD<br>
    Puedes usar swagger para ver los endpoints solo agrega a la URL ( /docs )<br>
    la API no tienen ningun factor de seguridad como JWT asi que puedes testear cada endpoint a discrecion<br><br>
    Creadores:<br>
    Gustavo Alejandro Sanchez<br>
    Griselda Marroquin<br>
    Guillermo Montenegro."""
    return message

# Evento de inicio para inicializar la base de datos
@app.on_event("startup")
def startup():
    # Crear todas las tablas definidas en los modelos si no existen
    Base.metadata.create_all(bind=engine)

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()  # Crear una nueva sesión de base de datos
    try:
        yield db  # Hacer que la sesión esté disponible como dependencia
    finally:
        db.close()  # Cerrar la sesión después de usarla

# Definición de modelos Pydantic para validación y serialización

# Modelo para crear un nuevo usuario
class UsuarioCreate(BaseModel):
    nombre: str  # Nombre del usuario
    correo: str  # Correo electrónico del usuario
    contraseña: str  # Contraseña del usuario
    direccion: str  # Dirección del usuario
    telefono: str | None = None  # Teléfono (opcional)
    estado: str = "activo"  # Estado del usuario, por defecto "activo"

# Modelo para autenticación de usuario
class UsuarioAuth(BaseModel):
    correo: str  # Correo del usuario
    contraseña: str  # Contraseña para autenticación

# Modelo para actualizar los datos de un usuario
class UsuarioUpdate(BaseModel):
    # Campos opcionales para actualizar los datos del usuario
    nombre: str | None = None
    correo: str | None = None
    contraseña: str | None = None
    direccion: str | None = None
    telefono: str | None = None
    estado: str | None = None

# Modelo para crear una categoría
class CategoriaCreate(BaseModel):
    nombre: str  # Nombre de la categoría
    descripcion: str = ""  # Descripción (por defecto, vacía)
    estado: str = 'activo'  # Estado de la categoría, por defecto "activo"

    class Config:
        from_attributes = True  # Configuración para permitir atributos adicionales

# Modelo para actualizar una categoría
class CategoriaUpdate(BaseModel):
    # Campos opcionales para actualizar una categoría
    nombre: str | None = None
    descripcion: str | None = None
    estado: str | None = None

# Modelo para crear un producto
class ProductoCreate(BaseModel):
    nombre: str  # Nombre del producto
    descripcion: str  # Descripción del producto
    precio: float  # Precio del producto
    categoriaID: int  # ID de la categoría asociada
    stock: int  # Cantidad en stock
    sku: str  # Código único del producto
    estado: str = 'activo'  # Estado del producto, por defecto "activo"

    class Config:
        from_attributes = True  # Configuración para atributos adicionales

# Modelo para actualizar un producto
class ProductoUpdate(BaseModel):
    # Campos opcionales para actualizar un producto
    nombre: str | None = None
    descripcion: str | None = None
    precio: float | None = None
    categoriaID: int | None = None
    stock: int | None = None
    sku: str | None = None
    estado: str | None = None

# Modelo para crear un pedido
class PedidoCreate(BaseModel):
    usuarioID: int  # ID del usuario que realiza el pedido
    total: float  # Monto total del pedido
    metodo_pago: str | None = None  # Método de pago (opcional)
    estado_pedido: str = 'pendiente'  # Estado del pedido, por defecto "pendiente"

    class Config:
        from_attributes = True  # Configuración para atributos adicionales

# Modelo para actualizar un pedido
class PedidoUpdate(BaseModel):
    # Campos opcionales para actualizar un pedido
    total: float | None = None
    metodo_pago: str | None = None
    estado_pedido: str | None = None

# Modelo para crear un detalle de pedido
class DetallePedidoCreate(BaseModel):
    pedidoID: int  # ID del pedido asociado
    productoID: int  # ID del producto asociado
    cantidad: int  # Cantidad de productos
    precio_unitario: float  # Precio unitario del producto
    subtotal: float  # Subtotal del detalle

    class Config:
        from_attributes = True  # Configuración para atributos adicionales

# Modelo para actualizar un detalle de pedido
class DetallePedidoUpdate(BaseModel):
    # Campos opcionales para actualizar un detalle de pedido
    cantidad: int | None = None
    precio_unitario: float | None = None
    subtotal: float | None = None


# Endpoints para usuarios
@app.post("/usuarios/")
def create_usuario_endpoint(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return create_usuario(db, **usuario.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/usuarios/auth/")
def authenticate_usuario_endpoint(usuario: UsuarioAuth, db: Session = Depends(get_db)):
    usuario_db = authenticate_usuario(db, usuario.correo, usuario.contraseña)
    if not usuario_db:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"message": "Autenticación exitosa", "usuario": usuario_db.nombre}


@app.get("/usuarios/{usuario_id}")
def read_usuario_endpoint(usuario_id: int, db: Session = Depends(get_db)):
    # Obtener un usuario por su ID
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        # Si no se encuentra el usuario, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.delete("/usuarios/{usuario_id}")
def delete_usuario_endpoint(usuario_id: int, db: Session = Depends(get_db)):
    # Eliminar un usuario por su ID
    usuario = delete_usuario(db, usuario_id)
    if not usuario:
        # Si no se encuentra el usuario, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente", "usuario": usuario}

@app.put("/usuarios/{usuario_id}")
def update_usuario_endpoint(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    # Actualizar un usuario con los nuevos datos proporcionados
    nuevo_usuario = usuario.dict(exclude_unset=True)
    usuario_actualizado = update_usuario(db, usuario_id, nuevo_usuario)
    if not usuario_actualizado:
        # Si no se encuentra el usuario, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_actualizado

# Endpoints para categorías

@app.post("/categorias/")
def create_categoria_endpoint(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    try:
        # Crear una categoría en la base de datos
        return create_categoria(db, **categoria.dict())
    except Exception as e:
        # En caso de error, lanzar una excepción HTTP con el detalle del error
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/categorias/{categoria_id}")
def read_categoria_endpoint(categoria_id: int, db: Session = Depends(get_db)):
    # Obtener una categoría por su ID
    categoria = get_categoria(db, categoria_id)
    if not categoria:
        # Si no se encuentra la categoría, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@app.delete("/categorias/{categoria_id}")
def delete_categoria_endpoint(categoria_id: int, db: Session = Depends(get_db)):
    # Eliminar una categoría por su ID
    categoria = delete_categoria(db, categoria_id)
    if not categoria:
        # Si no se encuentra la categoría, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"message": "Categoría eliminada exitosamente", "categoria": categoria}

@app.put("/categorias/{categoria_id}")
def update_categoria_endpoint(categoria_id: int, categoria: CategoriaUpdate, db: Session = Depends(get_db)):
    # Actualizar una categoría con los nuevos datos proporcionados
    nueva_categoria = categoria.dict(exclude_unset=True)
    categoria_actualizada = update_categoria(db, categoria_id, nueva_categoria)
    if not categoria_actualizada:
        # Si no se encuentra la categoría, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria_actualizada

# Endpoints para productos

@app.post("/productos/")
def create_producto_endpoint(producto: ProductoCreate, db: Session = Depends(get_db)):
    try:
        # Crear un producto en la base de datos
        return create_producto(db, **producto.dict())
    except Exception as e:
        # En caso de error, lanzar una excepción HTTP con el detalle del error
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/productos/{producto_id}")
def read_producto_endpoint(producto_id: int, db: Session = Depends(get_db)):
    # Obtener un producto por su ID
    producto = get_producto(db, producto_id)
    if not producto:
        # Si no se encuentra el producto, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.delete("/productos/{producto_id}")
def delete_producto_endpoint(producto_id: int, db: Session = Depends(get_db)):
    # Eliminar un producto por su ID
    producto = delete_producto(db, producto_id)
    if not producto:
        # Si no se encuentra el producto, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado exitosamente", "producto": producto}

@app.put("/productos/{producto_id}")
def update_producto_endpoint(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    # Actualizar un producto con los nuevos datos proporcionados
    nuevos_datos = producto.dict(exclude_unset=True)
    producto_actualizado = update_producto(db, producto_id, nuevos_datos)
    if not producto_actualizado:
        # Si no se encuentra el producto, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto_actualizado

# Endpoints para pedidos

@app.post("/pedidos/")
def create_pedido_endpoint(pedido: PedidoCreate, db: Session = Depends(get_db)):
    try:
        # Crear un pedido en la base de datos
        return create_pedido(db, **pedido.dict())
    except Exception as e:
        # En caso de error, lanzar una excepción HTTP con el detalle del error
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/pedidos/{pedido_id}")
def read_pedido_endpoint(pedido_id: int, db: Session = Depends(get_db)):
    # Obtener un pedido por su ID
    pedido = get_pedido(db, pedido_id)
    if not pedido:
        # Si no se encuentra el pedido, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@app.delete("/pedidos/{pedido_id}")
def delete_pedido_endpoint(pedido_id: int, db: Session = Depends(get_db)):
    # Eliminar un pedido por su ID
    pedido = delete_pedido(db, pedido_id)
    if not pedido:
        # Si no se encuentra el pedido, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"message": "Pedido eliminado exitosamente", "pedido": pedido}

@app.put("/pedidos/{pedido_id}")
def update_pedido_endpoint(pedido_id: int, pedido: PedidoUpdate, db: Session = Depends(get_db)):
    # Actualizar un pedido con los nuevos datos proporcionados
    nuevos_datos = pedido.dict(exclude_unset=True)
    pedido_actualizado = update_pedido(db, pedido_id, nuevos_datos)
    if not pedido_actualizado:
        # Si no se encuentra el pedido, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido_actualizado

# Endpoints para detalles de pedido

@app.post("/detalles_pedido/")
def create_detalle_pedido_endpoint(detalle: DetallePedidoCreate, db: Session = Depends(get_db)):
    try:
        # Crear un detalle de pedido en la base de datos
        return create_detalle_pedido(db, **detalle.dict())
    except Exception as e:
        # En caso de error, lanzar una excepción HTTP con el detalle del error
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/detalles_pedido/{detalle_id}")
def read_detalle_pedido_endpoint(detalle_id: int, db: Session = Depends(get_db)):
    # Obtener un detalle de pedido por su ID
    detalle = get_detalle_pedido(db, detalle_id)
    if not detalle:
        # Si no se encuentra el detalle de pedido, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    return detalle

@app.delete("/detalles_pedido/{detalle_id}")
def delete_detalle_pedido_endpoint(detalle_id: int, db: Session = Depends(get_db)):
    # Eliminar un detalle de pedido por su ID
    detalle = delete_detalle_pedido(db, detalle_id)
    if not detalle:
        # Si no se encuentra el detalle de pedido, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    return {"message": "Detalle de pedido eliminado exitosamente", "detalle": detalle}

@app.put("/detalles_pedido/{detalle_id}")
def update_detalle_pedido_endpoint(detalle_id: int, detalle: DetallePedidoUpdate, db: Session = Depends(get_db)):
    # Actualizar un detalle de pedido con los nuevos datos proporcionados
    nuevos_datos = detalle.dict(exclude_unset=True)
    detalle_actualizado = update_detalle_pedido(db, detalle_id, nuevos_datos)
    if not detalle_actualizado:
        # Si no se encuentra el detalle de pedido, lanzar excepción 404
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    return detalle_actualizado