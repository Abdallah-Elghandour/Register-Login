from fastapi import APIRouter, Depends, status, BackgroundTasks
from src.services.user import create_user_account, activate_user_account
from src.schemas.responses.user import UserResponse
from src.schemas.requests.user import RegisterUserRequest, VerifyUserRequest
from sqlalchemy.orm import Session
from config.database import get_session
from fastapi.responses import JSONResponse

register_router = APIRouter(
    prefix="/register",
    tags=["register"],
    responses={404: {"description": "Not found"}},
)


@register_router.post("/user", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(data: RegisterUserRequest, background_tasks: BackgroundTasks, session: Session=Depends(get_session)):
    return await create_user_account(data, session, background_tasks)



@register_router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_user_account(data: VerifyUserRequest, background_tasks: BackgroundTasks, session: Session=Depends(get_session)):
    await activate_user_account(data, session, background_tasks)
    return JSONResponse({"message": "User account has been verified."})
