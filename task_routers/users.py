from fastapi import APIRouter, HTTPException,Depends
from task_schemas import UserCreate
from database import get_db
from task_models import Users
from task_security import auth
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
def create_user(user : UserCreate, db = Depends(get_db)):
    user_exist = db.query(Users).filter(Users.username == user.username).first()
    if user_exist:
        raise HTTPException(status_code =400, detail ="User already exist")
    # new_user = Users(**user.model_dump()) #{"username"="", "password"=""}
    new_user = Users(username=user.username, password=auth.hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id":new_user.id, "username":new_user.username} 

@router.post("/login")
def user_login(user:UserCreate,db=Depends(get_db)):
    # user_exist = db.query(Users).filter(Users.username== user.username, Users.password == user.password).first()
    user_exist = db.query(Users).filter(Users.username== user.username).first()
    if not user_exist:
        raise HTTPException(status_code =401, detail ="Invalid Credentials")
    if not auth.verify_password(user.password,user_exist.password):
        raise HTTPException(status_code =401, detail ="Invalid Credentials")
    access_token = auth.create_access_token({'sub':user_exist.username})
    return {"token":access_token, "token_type":"bearer"}
    
@router.post("/token")
def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user_exist = db.query(Users).filter(Users.username== form_data.username).first()
    if not user_exist:
        raise HTTPException(status_code =401, detail ="Invalid Credentials")
    if not auth.verify_password(form_data.password,user_exist.password):
        raise HTTPException(status_code =401, detail ="Invalid Credentials")
    access_token = auth.create_access_token({'sub':user_exist.username})
    return {"access_token":access_token, "token_type":"bearer"}
