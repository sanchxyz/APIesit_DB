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
    

# Función para eliminar un usuario por ID
def delete_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuarios).filter(Usuarios.usuarioID == usuario_id).first()
    if not usuario:
        return None
    db.delete(usuario)
    db.commit()
    return usuario
    

# Función para actualizar un usuario por ID
def update_usuario(db: Session, usuario_id: int, nuevo_usuario: dict):
    usuario = db.query(Usuarios).filter(Usuarios.usuarioID == usuario_id).first()
    if not usuario:
        return None
    for key, value in nuevo_usuario.items():
        setattr(usuario, key, value)
    db.commit()
    db.refresh(usuario)
    return usuario




