from sqlalchemy import Column, DateTime, Integer, String, Text, func

from .database import Base


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    service_type = Column(String(120), nullable=False, index=True)
    description = Column(Text, nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    phone = Column(String(30), nullable=True)
    city = Column(String(120), nullable=True, index=True)
    ai_category = Column(String(120), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
