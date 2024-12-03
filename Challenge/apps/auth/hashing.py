import hashlib


# class Hash():
def hash_password(password: str) -> str:
    """Genera un hash SHA-256 de la contraseña proporcionada."""
    # Codificar la contraseña en bytes y calcular el hash
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password( hashed_password: str, password: str) -> bool:
    """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
    return hashed_password == hash_password(password)
