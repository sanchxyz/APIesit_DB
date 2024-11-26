# Importaciones necesarias para la creación de la API y manejo de datos
from fastapi import FastAPI, Depends, HTTPException  # FastAPI proporciona las herramientas para crear la API
from fastapi.middleware.cors import CORSMiddleware  # Middleware para habilitar CORS (Cross-Origin Resource Sharing)
from sqlalchemy.orm import Session  # Para manejar las sesiones de SQLAlchemy
from .database import SessionLocal, engine  # Se importan el motor de base de datos y la configuración de la sesión local
from .models import Base  # Importa la clase Base para manejar la creación de tablas en la base de datos
from .crud import get_usuario, create_usuario  # Funciones CRUD para manejar usuarios
from pydantic import BaseModel  # Para la validación de datos con Pydantic
from .crud import delete_usuario, update_usuario  # Funciones CRUD para eliminar y actualizar usuarios

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
    # Crea todas las tablas que estén definidas en los modelos de SQLAlchemy (como la tabla de 'Usuarios')
    Base.metadata.create_all(bind=engine)

# Dependencia para obtener una sesión de base de datos
# Esta función es utilizada por FastAPI para crear y gestionar la conexión a la base de datos
def get_db():
    db = SessionLocal()  # Crea una nueva sesión de base de datos
    try:
        yield db  # La sesión es devuelta al llamador
    finally:
        db.close()  # Asegura que la sesión sea cerrada después de su uso

# Modelo Pydantic para crear un nuevo usuario
# Pydantic se utiliza para validar los datos entrantes en la API
class UsuarioCreate(BaseModel):
    nombre: str
    correo: str
    contraseña: str
    direccion: str

    class Config:
        # Configura la compatibilidad con los modelos de SQLAlchemy
        # 'from_attributes' es una alternativa a 'orm_mode = True' en versiones anteriores de Pydantic
        from_attributes = True

# Endpoint para crear un nuevo usuario
# El decorador @app.post indica que este endpoint maneja solicitudes POST
@app.post("/usuarios/")
def create_usuario_endpoint(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        # Llama a la función de la capa CRUD para crear un usuario en la base de datos
        return create_usuario(db, **usuario.dict())
    except Exception as e:
        # Si ocurre un error, devuelve una respuesta HTTP con un código de error 400 (Bad Request)
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para leer un usuario por su ID
@app.get("/usuarios/{usuario_id}")
def read_usuario_endpoint(usuario_id: int, db: Session = Depends(get_db)):
    # Llama a la función de la capa CRUD para obtener el usuario por ID
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        # Si no se encuentra el usuario, se lanza una excepción HTTP 404 (No encontrado)
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Endpoint para eliminar un usuario por su ID
@app.delete("/usuarios/{usuario_id}")
def delete_usuario_endpoint(usuario_id: int, db: Session = Depends(get_db)):
    # Llama a la función de la capa CRUD para eliminar el usuario por ID
    usuario = delete_usuario(db, usuario_id)
    if not usuario:
        # Si no se encuentra el usuario, se lanza una excepción HTTP 404 (No encontrado)
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente", "usuario": usuario}

# Modelo Pydantic para actualizar un usuario
# Los campos son opcionales, ya que no es necesario enviar todos los campos al actualizar
class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    correo: str | None = None
    contraseña: str | None = None
    direccion: str | None = None

# Endpoint para actualizar un usuario por su ID
@app.put("/usuarios/{usuario_id}")
def update_usuario_endpoint(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    # Se crea un diccionario con los campos proporcionados por el usuario, excluyendo los valores no establecidos
    nuevo_usuario = usuario.dict(exclude_unset=True)
    # Llama a la función de la capa CRUD para actualizar el usuario
    usuario_actualizado = update_usuario(db, usuario_id, nuevo_usuario)
    if not usuario_actualizado:
        # Si no se encuentra el usuario, se lanza una excepción HTTP 404 (No encontrado)
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_actualizado
