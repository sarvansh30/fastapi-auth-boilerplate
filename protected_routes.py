from fastapi import APIRouter
from fastapi.responses import JSONResponse

protected_route = APIRouter()

@protected_route.get('/home')
def home():
    return JSONResponse(
        status_code=200,
        content={"message": "Welcome to the protected home route!"}
    )