from datetime import timedelta
from auth.responses import TokenResponse
from core.config import Settings
from core.security import create_access_token, create_refresh_token, get_token_payload, verify_password
from users.models import UserModel
from fastapi.exceptions import HTTPException

settings=Settings()
async def get_token(data,db):
    user = db.query(UserModel).filter(UserModel.email==data.username).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email is not registered with us",
            headers={"WWW-Authenticate":"Bearer"}
        ) 
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid Login Credential",
            headers={"WWW-Authenticate":"Bearer"}
        ) 
    _verify_user_access(user=user)

    return await _get_user_token(user=user) #return access token and refresh token

async def get_refresh_token(token, db):
    payload = get_token_payload(token=token)
    email_id = payload.get('id',None)
    if not email_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate":"Bearer"}
        )
    user = db.query(UserModel).filter(UserModel.email==email_id).first()
    return await _get_user_token(user=user,refresh_token=token)

def _verify_user_access(user: UserModel):
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Your account is inactive please contact support.",
            headers={"WWW-Authenticate":"Bearer"}
        )
    if not user.is_verified:
        #trigger user account verification email
        raise HTTPException(
            status_code=400,
            detail="Your account is unverified, we have send the account verification email.",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
async def _get_user_token(user: UserModel, refresh_token= None):
    payload = {"id": user.email}
    access_token_expiery = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MUNUTES)

    access_token = await create_access_token(payload, access_token_expiery)
    if not refresh_token:
        refresh_token =await create_refresh_token(payload)

    return TokenResponse(
        access_token = access_token,
        refresh_token = refresh_token,
        expire_in = access_token_expiery.seconds #in secounds
    )