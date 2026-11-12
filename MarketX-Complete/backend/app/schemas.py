from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(default="", max_length=30)
    password: str = Field(min_length=8, max_length=128)
class LoginIn(BaseModel):
    email: EmailStr
    password: str
class UserOut(BaseModel):
    id: int; name: str; email: EmailStr; phone: str
    model_config=ConfigDict(from_attributes=True)
class TokenOut(BaseModel):
    access_token: str
    token_type: str="bearer"
    user: UserOut
class ListingIn(BaseModel):
    title: str = Field(min_length=4, max_length=140)
    description: str = Field(min_length=10, max_length=5000)
    price: float = Field(gt=0, le=100000000)
    category: str
    condition: str = "Used"
    city: str
    state: str = "Telangana"
    image_url: str = ""
class ListingUpdate(BaseModel):
    title: Optional[str]=None; description: Optional[str]=None; price: Optional[float]=None
    category: Optional[str]=None; condition: Optional[str]=None; city: Optional[str]=None
    state: Optional[str]=None; image_url: Optional[str]=None
class ListingOut(BaseModel):
    id: int; title: str; description: str; price: float; category: str
    condition: str; city: str; state: str; image_url: str; seller_id: int
    seller: UserOut; created_at: object
    model_config=ConfigDict(from_attributes=True)
