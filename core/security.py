from fastapi import Depends, HTTPException, status, Request
from fastapi.requests import HTTPConnection
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import JWTError, jwt
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from core.config import Settings
from core.database import get_db
from users.models import UserModel

settings=Settings()
pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plan_password, hashed_password):
    return pwd_context.verify(plan_password, hashed_password)

async def create_access_token(data, expiery:timedelta):
    payload = data.copy()
    expire_in = datetime.now() + expiery
    payload.update({"exp":expire_in})
    return jwt.encode(payload,settings.JWT_SECRET,algorithm=settings.JWT_ALGORITHM)

async def create_refresh_token(data):
    return jwt.encode(data,settings.JWT_SECRET,algorithm=settings.JWT_ALGORITHM)

def get_token_payload(token):
    try:
        payload=jwt.decode(token,settings.JWT_SECRET,algorithms = settings.JWT_ALGORITHM)
    except JWTError:
        return None
    return payload

async def get_current_user(token: str = Depends(oauth2_scheme), db=None):
    payload = get_token_payload(token)
    if not payload or type(payload) is not dict:
        return None
    
    email_id = payload.get('id',None)
    if not email_id:
        return None
    
    if not db:
        db = next(get_db())

    user = db.query(UserModel).filter(UserModel.email == email_id).first()
    return user

# def require_user(request: Request):
#     # If you return UnauthenticatedUser, Starlette sets is_authenticated=False
#     if not getattr(request.user, "is_authenticated", False):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Authentication required",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return request.user
class JWTAuth:
    async def authenticate(self, conn:HTTPConnection):
        guest = AuthCredentials(['unauthenticated']), UnauthenticatedUser()
        if 'authorization' not in conn.headers:
            return guest
        
        # token = conn.headers.get('authorization').split(' ')[1] #Bearer token_hash
        # if not token:
        #     return guest
        auth = conn.headers.get("authorization")
        if not auth:
            return guest
        
        # Expect: "Bearer <token>"
        try:
            scheme, token = auth.split(" ", 1)
        except ValueError:
            return guest

        if scheme.lower() != "bearer" or not token:
            return guest
        
        user=await get_current_user(token=token)

        if not user:
            return guest
        
        return AuthCredentials(['Authenticated']),user
        
