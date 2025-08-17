from fastapi import FastAPI
from fastapi.responses import JSONResponse
from core.database import Base
from users.routes import router as guest_router, user_router
from auth.route import router as auth_router
from core.database import engine
from core.security import JWTAuth
from starlette.middleware.authentication import AuthenticationMiddleware

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app=FastAPI()
app.include_router(guest_router)
app.include_router(auth_router)
app.include_router(user_router)

#middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

@app.get('/')
def health_check():
    return JSONResponse(content={"status":"Running"})

# if __name__=="__main__":
#     import uvicorn
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=8090,
#         reload=True
#     )