from fastapi import APIRouter, Depends, status, BackgroundTasks
from src.services import user
from src.schemas.responses.user import UserResponse, LoginResponse
from src.schemas.requests.user import RegisterUserRequest, VerifyUserRequest
from sqlalchemy.orm import Session
from config.database import get_session
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

guest_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(data: RegisterUserRequest, background_tasks: BackgroundTasks, session: Session=Depends(get_session)):
    return await user.create_user_account(data, session, background_tasks)



@user_router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_user_account(data: VerifyUserRequest, background_tasks: BackgroundTasks, session: Session=Depends(get_session)):
    await user.activate_user_account(data, session, background_tasks)
    return JSONResponse({"message": "User account has been verified."})

@guest_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def user_login(data: OAuth2PasswordRequestForm = Depends(), session: Session=Depends(get_session)):
    return  await user.get_login_token(data, session)
