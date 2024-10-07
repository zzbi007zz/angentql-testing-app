from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt

class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

    @classmethod
    def hash_password(cls, password: str):
        return bcrypt.hash(password)

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)