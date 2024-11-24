from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base
from .crud import get_usuario, create_usuario
from pydantic import BaseModel

# Inicializar la aplicación
app = FastAPI()

# Middleware para CORS (si es necesario para frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar por los dominios del frontend si aplica
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Bienvenido a mi API!"}

# Sincronizar tablas con la base de datos al iniciar la app
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo Pydantic para crear usuarios
class UsuarioCreate(BaseModel):
    nombre: str
    correo: str
    contraseña: str
    direccion: str

    class Config:
        from_attributes = True  # Esto reemplaza 'orm_mode = True' de Pydantic v1

# Endpoint para crear un usuario
@app.post("/usuarios/")
def create_usuario_endpoint(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return create_usuario(db, **usuario.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para leer un usuario por ID
@app.get("/usuarios/{usuario_id}")
def read_usuario_endpoint(usuario_id: int, db: Session = Depends(get_db)):
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
