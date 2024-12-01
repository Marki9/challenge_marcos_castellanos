import jwt
import datetime
from typing import Dict, Any

KEY_TOKEN = "__CHALLENGE__"  # Cambia esto por una clave secreta más segura

def create_access_token(data: Dict[str, Any], expires_delta: datetime.timedelta = None) -> str:
    """Crea un token de acceso JWT con la información proporcionada."""
    to_encode = data.copy()
    if expires_delta:
        expiration = datetime.datetime.utcnow() + expires_delta
    else:
        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expira en 1 hora
    to_encode.update({"exp": expiration})  # Añadir la fecha de expiración al payload
    return jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')

def verify_token(token: str) -> dict:
    """Verifica el token JWT y devuelve el payload si es válido."""
    try:
        return jwt.decode(token, KEY_TOKEN, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired."}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}
