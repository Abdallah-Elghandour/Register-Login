from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func

from config.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    # character limits?

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String, index=True)
    address = Column(String)
    is_active = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=True, server_default=func.now())
    
    def get_context_string(self, context: str):
        return f"{context}{self.password[-6:]}{self.updated_at.strftime('%m%d%Y%H%M%S')}".strip()