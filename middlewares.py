from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM= os.getenv("ALGORITHM")

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path.startswith("/protected"):
            auth = request.headers.get("Authorization")
            # print(auth)

            if not auth or not auth.startswith("Bearer "):
                return JSONResponse(
                    status_code=401,
                    content={"detail": "No authorisation token"}
                )
            token = auth[len("Bearer "):]

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            except JWTError:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid token"}
                )

        response = await call_next(request)
        return response