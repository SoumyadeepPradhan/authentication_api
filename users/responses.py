from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    