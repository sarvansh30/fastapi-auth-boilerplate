from fastapi import FastAPI
from auth_route import auth_route
from middlewares import AuthMiddleware
from protected_routes import protected_route
from contextlib import asynccontextmanager
from redis_manager import redis_manager
# import redis.asyncio as redis
import os
from typing import Optional

# Below is an approach for quick small application
# redis_client = Optional[redis.Redis] = None

# @asynccontextmanager
# async def lifespan(app:FastAPI):
#     global redis_client
#     redis_client = redis.from_url(os.getenv("REDIS_URL"),decode_responses = True)

#     try:
#         await redis_client.ping()
#         print("Redis server intisalised")
#     except Exception as e:
#         print(e)
    
#     yield

#     if redis_client:
#         redis_client.close()
    

@asynccontextmanager
async def lifespan(app:FastAPI):
    await redis_manager.redis_init()

    yield

    await redis_manager.close_redis()


app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.add_middleware(AuthMiddleware)
app.include_router(auth_route,prefix="/auth")
app.include_router(protected_route,prefix="/protected")