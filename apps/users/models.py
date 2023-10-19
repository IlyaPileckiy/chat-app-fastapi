from typing import Optional
from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]

    @property
    def profile_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email
