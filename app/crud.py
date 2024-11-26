# Importación de la clase Session de SQLAlchemy para manejar la sesión de la base de datos
from sqlalchemy.orm import Session
# Importación de IntegrityError para manejar errores de integridad en la base de datos
from sqlalchemy.exc import IntegrityError
# Importación del modelo 'Usuarios', que representa la tabla de usuarios en la base de datos
from .models import Usuarios

# Función para obtener un usuario de la base de datos por su ID
def get_usuario(db: Session, usuario_id: int):
    # Realiza una consulta a la base de datos para obtener el primer usuario cuyo ID coincida
    # con el proporcionado. Si no se encuentra, retorna None.
    return db.query(Usuarios).filter(Usuarios.usuarioID == usuario_id).first()

# Función para crear un nuevo usuario en la base de datos
def create_usuario(db: Session, nombre: str, correo: str, contraseña: str, direccion: str):
    try:
        # Crea una nueva instancia del modelo Usuarios utilizando los datos proporcionados
        usuario = Usuarios(nombre=nombre, correo=correo, contraseña=contraseña, direccion=direccion)
        # Añade la instancia del usuario a la sesión de la base de datos
        db.add(usuario)
        # Realiza un commit para guardar los cambios en la base de datos
        db.commit()
        # Refresca la instancia del usuario para obtener cualquier cambio de la base de datos
        db.refresh(usuario)
        # Retorna el objeto usuario que ha sido creado
        return usuario
    except IntegrityError as e:
        # Si ocurre un error de integridad (por ejemplo, violación de una restricción única),
        # realiza un rollback para revertir los cambios en la base de datos
        db.rollback()
        # Lanza una excepción personalizada con el mensaje de error
        raise Exception(f"Error al crear usuario: {e.orig}")
    

# Función para eliminar un usuario de la base de datos por su ID
def delete_usuario(db: Session, usuario_id: int):
    # Realiza una consulta para obtener el usuario con el ID proporcionado
    usuario = db.query(Usuarios).filter(Usuarios.usuarioID == usuario_id).first()
    # Si no se encuentra el usuario, retorna None
    if not usuario:
        return None
    # Elimina el usuario de la base de datos
    db.delete(usuario)
    # Realiza el commit para aplicar los cambios (eliminación)
    db.commit()
    # Retorna el objeto usuario que fue eliminado
    return usuario
    

# Función para actualizar los detalles de un usuario por su ID
def update_usuario(db: Session, usuario_id: int, nuevo_usuario: dict):
    # Realiza una consulta para obtener el usuario con el ID proporcionado
    usuario = db.query(Usuarios).filter(Usuarios.usuarioID == usuario_id).first()
    # Si el usuario no existe, retorna None
    if not usuario:
        return None
    # Itera sobre cada clave-valor en el diccionario 'nuevo_usuario' para actualizar los atributos del usuario
    for key, value in nuevo_usuario.items():
        setattr(usuario, key, value)
    # Realiza el commit para guardar los cambios en la base de datos
    db.commit()
    # Refresca el objeto usuario para obtener cualquier actualización desde la base de datos
    db.refresh(usuario)
    # Retorna el objeto usuario con los cambios aplicados
    return usuario
