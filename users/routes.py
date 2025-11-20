from fastapi import APIRouter, Depends, HTTPException, Request,status
from fastapi.responses import JSONResponse, PlainTextResponse
from core.database import get_db
from users.models import UserModel
from users.responses import UserResponse
from users.schemas import CreateUserRequest
from sqlalchemy.orm import Session
from users.services import create_user_account
from core.security import get_current_user, oauth2_scheme

router=APIRouter(
    prefix="/users",
    tags=["user"],
    responses={
        404:{"description":"Not found"},
        401: {"description": "Unauthorized"}
    })
user_router=APIRouter(
    prefix="/users",
    tags=["user"],
    responses={
        404:{"description":"Not found"},
        401: {"description": "Unauthorized"}
    },
    dependencies=[Depends(oauth2_scheme)]
    )
@router.post('',status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        await create_user_account(data,db)
        payload={"message":"User account has been successfully created."}
        return JSONResponse(content=payload)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@user_router.post('/me', status_code=status.HTTP_200_OK)
def get_user_details(request: Request):
    return {"msg": f"Hello {request.user.first_name}, you are logged in!"}

@user_router.get("/protected",response_model=UserResponse)
def protected(email_id , db: Session = Depends(get_db) ):
    user = db.query(UserModel).filter(UserModel.email==email_id).first()
    return user
