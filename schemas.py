from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    email: str
    password: str
    name: str
    active: Optional[bool] = True
    admin: Optional[bool] = False

    class config:
        from_attributes = True


class OrderSchema(BaseModel):
    user_id: int

    class config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class config:
        from_attributes = True


class OrderItemSchema(BaseModel):
    quantity: int
    topping: str
    size: str
    price_item: float

    class config:
        from_attributes = True