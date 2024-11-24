from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Configuración de conexión
DATABASE_URL = "mysql+pymysql://root:simple123@localhost:3306/Ecommerce_Esit"

# Crear el motor de conexión
try:
    engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)
except SQLAlchemyError as e:
    print("Error al conectar a la base de datos:", e)

# Configurar la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
