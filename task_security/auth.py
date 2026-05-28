from passlib.context import CryptContext
from jose import jwt, JWTError 
from .config import settings
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from task_models import Users

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode, settings.secret_key, settings.algorithm)

def verify_token(token:str):
    try:
        payload = jwt.decode(token,settings.secret_key, settings.algorithm)
        username = payload.get("sub")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid Token")
    
def get_current_user(token = Depends(oauth2_scheme), db = Depends(get_db)):
    username = verify_token(token)
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(status_code = 404, details = "User not found")
    return user 





