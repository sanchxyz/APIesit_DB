from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Clave secreta y configuración del token
SECRET_KEY = "clave_secreta_super_segura"  # La contraseñas mas segurda del mundo 
ALGORITHM = "HS256"  # Algoritmo para firmar el JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tiempo de expiración del token en minutos
# Inicializar el esquema OAuth2 para extraer el token del encabezado Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/auth/")

# Función para crear un token JWT
def create_access_token(data: dict):
    """Genera un token JWT con un tiempo de expiración."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para verificar un token JWT
def verify_token(token: str):
    """Decodifica un token JWT y valida su firma."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Retorna los datos del token si es válido
    except JWTError:
        return None  # Retorna None si el token no es válido o expiró
    

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Valida el token JWT y extrae los datos del usuario."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        user_id = payload.get("id")
        if user_email is None or user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"id": user_id, "email": user_email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

