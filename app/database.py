# Importar las librerías necesarias para interactuar con la base de datos usando SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# URL de conexión a la base de datos, que contiene el usuario, la contraseña, y la dirección del servidor
#DATABASE_URL = "mysql+pymysql://root:simple123@localhost:3306/Ecommerce_DB"
DATABASE_URL = "mysql+pymysql://uq0mfjrhjiodyetg:b4X7Uar2RmXzqEX642sN@bvs4gf3xerihsn5ovmva-mysql.services.clever-cloud.com:3306/bvs4gf3xerihsn5ovmva" 
# Descomentar la línea de arriba para usar una base de datos remota

try:
    # Crear el motor de la base de datos, configurando las opciones de conexión
    engine = create_engine(
        DATABASE_URL,  # URL de conexión a la base de datos
        pool_size=20,  # Número de conexiones activas en el pool
        max_overflow=0,  # Número máximo de conexiones adicionales cuando el pool está lleno
        pool_timeout=30,  # Tiempo de espera para obtener una conexión del pool
        pool_pre_ping=True,  # Verificar si una conexión está activa antes de usarla
        echo=False  # Cambiar a True para habilitar los logs de depuración de SQL
    )
except SQLAlchemyError as e:
    # Si ocurre un error al conectar con la base de datos, se captura la excepción y se muestra un mensaje
    print("Error al conectar a la base de datos:", e)
    raise  # Relanzar la excepción para que el error no pase desapercibido

# Crear la sesión local para interactuar con la base de datos (sin auto-commit ni auto-flush)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener una sesión de la base de datos y manejar el ciclo de vida de la conexión
def get_db():
    db = SessionLocal()  # Crear una nueva sesión
    try:
        yield db  # Devolver la sesión para ser utilizada en las operaciones de base de datos
    finally:
        db.close()  # Cerrar la sesión cuando se haya terminado de usarla
