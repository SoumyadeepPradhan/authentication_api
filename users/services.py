
from datetime import datetime
from fastapi import HTTPException
from users.models import UserModel
from core.security import get_password_hash


async def create_user_account(data, db):
    user=db.query(UserModel).filter(data.email == UserModel.email).first()
    if user:
        raise HTTPException(status_code=422, detail="Email is already registered with us.")
    new_user = UserModel(
        first_name = data.first_name,
        last_name = data.last_name,
        email = data.email,
        password = get_password_hash(data.password),
        is_active = False,
        is_verified = False,
        registered_at = datetime.now(),
        updated_at = datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
