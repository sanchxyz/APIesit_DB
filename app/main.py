# Importaciones necesarias para la creación de la API y manejo de datos
from fastapi import FastAPI, Depends, HTTPException  # FastAPI proporciona las herramientas para crear la API
from fastapi.middleware.cors import CORSMiddleware  # Middleware para habilitar CORS (Cross-Origin Resource Sharing)
from sqlalchemy.orm import Session  # Para manejar las sesiones de SQLAlchemy
from .database import SessionLocal, engine  # Se importan el motor de base de datos y la configuración de la sesión local
from .models import Base  # Importa la clase Base para manejar la creación de tablas en la base de datos
from .crud import get_usuario, create_usuario, delete_usuario, update_usuario, get_categoria, create_categoria, delete_categoria, update_categoria, get_producto, create_producto, delete_producto, update_producto, get_pedido, create_pedido, delete_pedido, update_pedido, get_detalle_pedido, create_detalle_pedido, delete_detalle_pedido, update_detalle_pedido  # Funciones CRUD para manejar usuarios, categorías, productos, pedidos, etc.
from pydantic import BaseModel  # Para la validación de datos con Pydantic

# Inicializar la aplicación FastAPI
app = FastAPI()

# Configuración del middleware CORS para permitir que el frontend acceda a la API
# Permite solicitudes desde cualquier origen (esto debe ajustarse a necesidades de seguridad específicas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes de todos los orígenes (reemplazar por dominios específicos en producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todas las cabeceras
)

# Ruta de prueba para la raíz de la API
@app.get("/")
def read_root():
    return {"message": "Bienvenido a mi API para la ESIT !"}

# Evento de inicio de la aplicación para crear las tablas de la base de datos
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# Dependencia para obtener una sesión de base de datos
# Esta función es utilizada por FastAPI para crear y gestionar la conexión a la base de datos
def get_db():
    db = SessionLocal()  # Crea una nueva sesión de base de datos
    try:
        yield db  # La sesión es devuelta al llamador
    finally:
        db.close()  # Asegura que la sesión sea cerrada después de su uso

# Modelos Pydantic para la creación y actualización de datos

class UsuarioCreate(BaseModel):
    nombre: str
    correo: str
    contraseña: str
    direccion: str
    telefono: str | None = None
    estado: str = 'activo'

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    correo: str | None = None
    contraseña: str | None = None
    direccion: str | None = None
    telefono: str | None = None
    estado: str | None = None

class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: str = ""
    estado: str = 'activo'

    class Config:
        from_attributes = True

class CategoriaUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    estado: str | None = None

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    categoriaID: int
    stock: int
    sku: str
    estado: str = 'activo'

    class Config:
        from_attributes = True

class ProductoUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    precio: float | None = None
    categoriaID: int | None = None
    stock: int | None = None
    sku: str | None = None
    estado: str | None = None

class PedidoCreate(BaseModel):
    usuarioID: int
    total: float
    metodo_pago: str | None = None
    estado_pedido: str = 'pendiente'

    class Config:
        from_attributes = True

class PedidoUpdate(BaseModel):
    total: float | None = None
    metodo_pago: str | None = None
    estado_pedido: str | None = None

class DetallePedidoCreate(BaseModel):
    pedidoID: int
    productoID: int
    cantidad: int
    precio_unitario: float
    subtotal: float

    class Config:
        from_attributes = True

class DetallePedidoUpdate(BaseModel):
    cantidad: int | None = None
    precio_unitario: float | None = None
    subtotal: float | None = None


# Endpoints para usuarios

@app.post("/usuarios/")
def create_usuario_endpoint(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        # Crear un usuario en la base de datos
        return create_usuario(db, **usuario.dict())
    except Exception as e:
        # En caso de error, lanzar una excepción HTTP con el detalle del error
        raise HTTPException(status_code=400, detail=str(e))

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