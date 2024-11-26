# Proyecto de Base de Datos con Python 🚀

Este proyecto de Python tiene como objetivo aplicar los conceptos de **modelado de datos**, **conectividad** y **optimización de bases de datos en la nube** para crear una solución de gestión de datos web. La aplicación simula un entorno real, optimizando la estructura, las conexiones y el mantenimiento de datos en un entorno de alta concurrencia.

Utilizando **FastAPI** y **SQLAlchemy**, se desarrolla una API REST que interactúa con una base de datos **MySQL**. La estructura modular y escalable permite un desarrollo eficiente y mantenimiento a largo plazo.

---

## 🗂️ Estructura del Proyecto

```plaintext
APIesit_DB/
├── app/                # Contiene la lógica de la aplicación
│   ├── __init__.py     # Inicializa el paquete app
│   ├── main.py         # Punto de entrada de la aplicación
│   ├── models.py       # Define los modelos de datos
│   ├── database.py     # Interacción con la base de datos
│   └── crud.py         # Operaciones CRUD (Create, Read, Update, Delete)
├── venv/               # Entorno virtual
├── requirements.txt    # Lista de dependencias
├── .gitignore          # Archivos a ignorar en el control de versiones
└── README.md           # Este archivo



⚙️ Instalación
Sigue estos pasos para configurar y ejecutar el proyecto:

1. Clonar el repositorio

git@github.com:sanchxyz/APIesit_DB.git

cd APIesit_D


2. Crear un entorno virtual

python -m venv venv


Activar el entorno virtual:

venv\Scripts\activate


macOS/Linux:

source venv/bin/activate


3. Instalar dependencias

pip install -r requirements.txt



🚀 Uso
1. Iniciar la aplicación
Inicia el servidor con el siguiente comando:

uvicorn app.main:app --reload



2. Acceder a la documentación interactiva

FastAPI genera automáticamente una interfaz para interactuar con la API.

Documentación Swagger: http://127.0.0.1:8000/docs
Documentación alternativa (Redoc): http://127.0.0.1:8000/redoc


✨ Características
Modelado de datos eficiente: Utilizando SQLAlchemy para mapear entidades.
API REST: Rápida y moderna, implementada con FastAPI.
Soporte para concurrencia: Ideal para entornos de alta demanda.
Documentación automática: Generada por FastAPI para facilitar el desarrollo y pruebas.


📂 Requisitos del sistema
Python: 3.9 o superior
MySQL: Instalado y configurado
Dependencias: Ver requirements.txt


🛠️ Tecnologías utilizadas
Lenguaje: Python 🐍
Framework: FastAPI ⚡
ORM: SQLAlchemy
Base de datos: MySQL 🐬


🌟 Contribuciones
¡Las contribuciones son bienvenidas! Sigue estos pasos:

Haz un fork del repositorio.
Crea una rama para tu feature: git checkout -b feature/nueva-funcionalidad.
Realiza los cambios y haz un commit: git commit -m "Agrega nueva funcionalidad".
Envía un pull request.


📄 Licencia
Este proyecto está bajo la Licencia MIT. Para más detalles, consulta el archivo LICENSE.