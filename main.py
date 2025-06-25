from fastapi import FastAPI
from auth_route import auth_route
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(auth_route,prefix="/auth")