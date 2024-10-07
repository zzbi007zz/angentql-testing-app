from typing import Optional
from backend.app.models.user import User
from backend.app.utils.auth.jwt_utils import verify_token

class AuthService:
    @classmethod
    async def authenticate_user(cls, username: str, password: str) -> Optional[User]:
        user = await cls.get_user_by_username(username)
        if user and user.verify_password(password):
            return user
        return None

    @classmethod
    async def register_user(cls, user: User):
        user.hashed_password = User.hash_password(user.password)
        # Save user to database
        pass

    @classmethod
    async def get_user_by_username(cls, username: str) -> Optional[User]:
        # Fetch user from database
        return None

    @classmethod
    async def get_current_user(cls, token: str) -> Optional[User]:
        username = verify_token(token, "access")
        if username:
            return await cls.get_user_by_username(username)
        return None