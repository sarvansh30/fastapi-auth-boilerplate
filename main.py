from fastapi import FastAPI
from auth_route import auth_route
from middlewares import AuthMiddleware
from protected_routes import protected_route
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.add_middleware(AuthMiddleware)
app.include_router(auth_route,prefix="/auth")
app.include_router(protected_route,prefix="/protected")