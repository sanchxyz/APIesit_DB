# Importación de las clases necesarias de SQLAlchemy
from sqlalchemy import create_engine  # Función para crear el motor de conexión con la base de datos
from sqlalchemy.orm import sessionmaker  # Función para configurar el manejador de sesiones
from sqlalchemy.exc import SQLAlchemyError  # Excepción que maneja los errores específicos de SQLAlchemy

# Configuración de la URL de conexión a la base de datos
# La URL incluye el tipo de base de datos (mysql), el nombre del usuario (root),
# la contraseña (simple123), la dirección del host (localhost), el puerto (3306) y el nombre de la base de datos (Ecommerce_Esit)
DATABASE_URL = "mysql+pymysql://root:simple123@localhost:3306/Ecommerce_Esit"

# Crear el motor de conexión a la base de datos
# El motor se configura con un tamaño de pool de 20 conexiones y un máximo de conexiones adicionales de 0 (sin sobrecarga).
# Esto asegura un manejo eficiente de conexiones sin exceder los recursos del servidor de base de datos.
try:
    engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)
except SQLAlchemyError as e:
    # Si ocurre un error al intentar establecer la conexión, se captura el error y se imprime un mensaje.
    # La excepción SQLAlchemyError proporciona detalles sobre el tipo específico de error en la conexión.
    print("Error al conectar a la base de datos:", e)

# Configuración de la sesión de la base de datos
# 'autocommit=False' evita que la sesión confirme automáticamente las transacciones sin explícitamente llamarlo.
# 'autoflush=False' evita que las consultas se envíen de manera automática antes de un commit.
# 'bind=engine' asocia la sesión con el motor de base de datos previamente creado.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
