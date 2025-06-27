from fastapi import APIRouter
from fastapi.responses import JSONResponse
from redis_manager import redis_manager
import json

protected_route = APIRouter()

db = {
    "Sarvnash": { 
        "email": "sarvansh.pachori45@gmail.com",
        "full_name": "Sarvansh Pachori"
    }
}

@protected_route.get('/home')
async def home():
    try:

        userData = await redis_manager.client.get("Sarvansh")

        if not userData:
            userData = db["Sarvnash"]

            await redis_manager.client.setex("Sarvansh",300,json.dumps(userData))
            userData["source"] = "database"
        else:
            userData = json.loads(userData)
            userData["source"] = "redis-cache"
    except Exception as e:
        print(e)

    return JSONResponse(
        status_code=200,
        content={"message": "Welcome to the protected home route!",
                 "data":userData}
    )