from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import Usuarios

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuarios).filter(Usuarios.usuarioID == usuario_id).first()

def create_usuario(db: Session, nombre: str, correo: str, contraseña: str, direccion: str):
    try:
        usuario = Usuarios(nombre=nombre, correo=correo, contraseña=contraseña, direccion=direccion)
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Error al crear usuario: {e.orig}")
