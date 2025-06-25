from fastapi import APIRouter
from user_model import User, LoginReq
from fastapi import HTTPException, status
from passlib.context import CryptContext
from fastapi.responses import JSONResponse

auth_route = APIRouter()
userDB={}
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def create_token(payload:str,exp:int):

    return token

@auth_route.post("/login")
def login(userInfo:LoginReq):
    try:
        if userDB.get(userInfo.username)==None:
            raise HTTPException(status_code=404,detail="username not found")
        else:
            if pwd_context.verify(userInfo.password,userDB.get(userInfo.username).password):
                token  = create_token(userInfo.username,exp=10)
                return JSONResponse(
                    status_code=200,
                    content={"token": token}
                )
            else:
                raise HTTPException(status_code=401,detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=404,detail="Error logging")


def hash_password(password:str)->str:
    try:
        hash_pwd = pwd_context.hash(password)
        print(hash_pwd)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error handling data")
    return hash_pwd

@auth_route.post('/signup')
def signup(userInfo:User):

    if userDB.get(userInfo.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    try:
        userInfo.password = hash_password(userInfo.password)
        userDB[userInfo.username] = userInfo
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user")
    
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail="User created successfully")