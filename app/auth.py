from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from . import models, schemas, crud
from sqlalchemy.orm import Session
import os

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2PasswordBearer è una dependency che permette di estrarre il token dal header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Passlib CryptContext per gestire la sicurezza delle password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Funzione per creare un hash della password
def hash_password(password: str):
    return pwd_context.hash(password)


# Funzione per verificare la password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# Funzione per creare un access token (JWT)
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Funzione per decodificare il token JWT e ottenere l'utente
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")


# Funzione per ottenere l'utente da database dato un token
def get_user_from_token(db: Session, token: str):
    username = decode_access_token(token)
    user = crud.get_user(db=db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


# Funzione per ottenere l'utente autenticato tramite dependency
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return get_user_from_token(db=db, token=token)


# Funzione per ottenere un token di accesso con username e password
def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user(db=db, username=username)
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user


# Funzione per creare un token di accesso quando l'utente si logga
from fastapi import APIRouter

router = APIRouter()


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

