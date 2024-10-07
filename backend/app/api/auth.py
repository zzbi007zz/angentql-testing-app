from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from backend.app.models.user import User
from backend.app.services.auth import AuthService
from backend.app.utils.auth.jwt_utils import create_access_token, create_refresh_token, verify_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await AuthService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/register")
async def register(user: User):
    await AuthService.register_user(user)
    return {"message": "User created successfully"}

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    username = verify_token(refresh_token, "refresh")
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token}