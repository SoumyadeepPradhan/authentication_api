from sqlalchemy import Boolean, DateTime, Integer, String, Column, func
from core.database import Base
# from core.database import engine

# Base.metadata.create_all(bind=engine)
class UserModel(Base):
    __tablename__= "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(100))
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    registered_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())