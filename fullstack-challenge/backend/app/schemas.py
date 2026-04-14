from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class ProviderBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    service_type: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=10)
    email: EmailStr
    phone: str | None = None
    city: str | None = None


class ProviderCreate(ProviderBase):
    pass


class ProviderUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    service_type: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, min_length=10)
    email: EmailStr | None = None
    phone: str | None = None
    city: str | None = None


class ProviderOut(ProviderBase):
    id: int
    ai_category: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
