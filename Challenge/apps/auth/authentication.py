from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..db import schemas
from ..db.db import get_db
from .hashing import Hash
from ..db.models.user import User
from .token import KEY_TOKEN, create_access_token, verify_token

router = APIRouter(tags=['Authentication'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def authenticate_user(user_credentials: OAuth2PasswordRequestForm, db_session: Session):
    user =  User.get_instance(db_session, name = user_credentials.username)
    if not user:
        return False
    if not Hash.verify_password(plain_password=user_credentials.password, hashed_password=user.password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme),  db_session: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas o vencidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    valid_token = verify_token(token=token)
    """Return el user al que pertenece el token en otro caso retorna None."""
    if valid_token:
        user =  User.get_instance(db_session, name = valid_token.username)
    if not valid_token or user is None:
        raise credentials_exception
    if not user.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario inactivo")
    return user

@router.post('/login', response_model=schemas.token.Token)
def login(form_user_credentials: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db)):
    user =  authenticate_user(form_user_credentials, db_session)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Usuario o contraseña incorrectos')

    access_token = create_access_token(data={KEY_TOKEN: user.name})
    return {"access_token": access_token, "token_type": "bearer"}

# async def get_current_user():
#     return None