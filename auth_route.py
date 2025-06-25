from fastapi import APIRouter, Body
from user_model import User, LoginReq, createUser
from fastapi import HTTPException, status
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta,timezone
load_dotenv()
import os



algorithm = os.getenv("ALGORITHM")
secret_key = os.getenv("SECRET_KEY")

auth_route = APIRouter()
userDB={}
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


def create_token(username:str,exp:int):

    try:
        expire = datetime.now(timezone.utc) + timedelta(minutes=exp)
    
        payload = {
        "user":username,
        "exp":expire
        }
        token = jwt.encode(payload,secret_key,algorithm=algorithm)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error creating token")
    
    return token

@auth_route.post("/login")
def login(userInfo:LoginReq):
    try:
        if userDB.get(userInfo.username) is None:
            raise HTTPException(status_code=404, detail="username not found")
        if userDB.get(userInfo.username).active_session:
            raise HTTPException(status_code=401, detail="This account already in use")
        if pwd_context.verify(userInfo.password, userDB.get(userInfo.username).password):
            token = create_token(userInfo.username, exp=10)
            userDB.get(userInfo.username).active_session = True
            return JSONResponse(status_code=200, content={"token": token})
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except HTTPException:
        raise  # re-raise HTTPExceptions so FastAPI handles them
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error logging")


def hash_password(password:str)->str:
    try:
        hash_pwd = pwd_context.hash(password)
        print(hash_pwd)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error handling data")
    return hash_pwd

@auth_route.post('/signup')
def signup(userInfo:createUser):

    if userDB.get(userInfo.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    try:
        userInfo.password = hash_password(userInfo.password)
        userInfo = User(**userInfo.model_dump())
        userDB[userInfo.username] = userInfo
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user")
    
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail="User created successfully")


@auth_route.post('/logout')
def logout_user(token:str = Body(...)):
    
    try:
        payload = jwt.decode(token,secret_key,algorithms=algorithm)
        username = payload.get("user")
        if username in userDB:
            userDB.get(username).active_session = False
            return JSONResponse(
                status_code=200,
                content={"message": "Logout successful"}
            )
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
