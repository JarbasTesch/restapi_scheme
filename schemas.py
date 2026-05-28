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