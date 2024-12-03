# from datetime import datetime, timedelta, timezone
#
#
# import jwt
# from fastapi import Depends, FastAPI, HTTPException, Security, status
# from fastapi.security import (
#     OAuth2PasswordBearer,
#     OAuth2PasswordRequestForm,
#     SecurityScopes,
# )
# from jwt.exceptions import InvalidTokenError
# from passlib.context import CryptContext
# from pydantic import BaseModel, ValidationError
#
# from ..db import schemas
# from ..db.db import get_db
# from .hashing import verify_password
# from ..db.models.user import User
# from .token import KEY_TOKEN, create_access_token #, verify_token
#
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#
#
# # async def authenticate_user(user_credentials: OAuth2PasswordRequestForm, db_session: Session):
# #     result = await db_session.execute(select(User).filter_by(username=user_credentials.username))
# #     user = result.scalar_one()
# #     if not user:
# #         return False
# #     if verify_password(hashed_password=user.password,password= user_credentials.password):
# #         return user
# #     return False
#
# #
# # async def get_current_user(token: str = Depends(oauth2_scheme), db_session: Session = Depends(get_db)):
# #     credentials_exception = HTTPException(
# #         status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas o vencidas",
# #         headers={"WWW-Authenticate": "Bearer"},
# #     )
# #     valid_token = verify_token(token=token)
# #     """Return el user al que pertenece el token en otro caso retorna None."""
# #     if valid_token:
# #         user = User.get_instance(db_session, name=valid_token.username)
# #     if not valid_token or user is None:
# #         raise credentials_exception
# #     if not user.active:
# #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario inactivo")
# #     return user
# #
#
# # @router.post('/login')
# # async def login(form_user_credentials: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db)):
# #     try:
# #         user = await authenticate_user(form_user_credentials,db_session)  # Asegúrate de que authenticate_user sea asíncrona
# #         if not user:
# #             raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Usuario o contraseña incorrectos')
# #
# #         access_token = create_access_token(data={KEY_TOKEN: user.username})
# #         return {"access_token": access_token, "token_type": "bearer"}
# #
# #     except Exception as e:
# #         # Manejo genérico de excepciones
# #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
