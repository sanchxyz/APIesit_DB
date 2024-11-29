from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# URL de conexión a la base de datos en Clever Cloud
DATABASE_URL = "mysql+pymysql://uq0mfjrhjiodyetg:b4X7Uar2RmXzqEX642sN@bvs4gf3xerihsn5ovmva-mysql.services.clever-cloud.com:3306/bvs4gf3xerihsn5ovmva"

#Para coneccion local
#DATABASE_URL = "mysql+pymysql://root:simple123@localhost:3306/Ecommerce_DB"

try:
    # Crear el motor de la base de datos
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,  # Ajuste de tamaño del pool según sea necesario
        max_overflow=0,  # Evita que se creen conexiones adicionales más allá del pool_size
        pool_timeout=30,  # Tiempo de espera para obtener una conexión del pool
        pool_pre_ping=True,  # Verifica la conexión antes de usarla
        echo=False  # Desactiva la salida SQL (útil para producción)
    )
except SQLAlchemyError as e:
    # Manejador de errores en caso de fallo de conexión
    print("Error al conectar a la base de datos:", e)
    raise

# Crear la sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()  # Establece una sesión para acceder a la DB
    try:
        yield db  # Retorna la sesión para ser usada por otras funciones
    finally:
        db.close()  # Cierra la sesión cuando termine de usarse
