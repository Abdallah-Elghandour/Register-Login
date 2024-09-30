from datetime import datetime
import logging
from src.services.email import send_account_activation_confirmation_email, send_account_verification_email
from src.models.user import User
from config.security import get_password_hash, is_password_strong, verify_password
from fastapi import HTTPException

from src.utils.email_context import VERIFY_ACCOUNT

async def create_user_account(data, session, background_tasks):
    
    
    user_exist = session.query(User).filter(User.email == data.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Email is already exists.")
    
    if not is_password_strong(data.password):
        raise HTTPException(status_code=400, detail="Password is not strong enough")
    

    user = User()
    user.name = data.name
    user.surname = data.surname
    user.email = data.email
    user.password = get_password_hash(data.password)
    user.phone = data.phone
    user.address = data.address
    user.updated_at = datetime.now()
    user.is_active = False
    session.add(user)
    session.commit()
    session.refresh(user)

    await send_account_verification_email(user, background_tasks)
    
    return user


async def activate_user_account(data, session, background_tasks):
    user = session.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="This link is invalid.")
        
    user_token = user.get_context_string(context=VERIFY_ACCOUNT)

    try:
        token_valid = verify_password(user_token, data.token)
    except Exception as verify_exec:
        logging.exception(verify_exec)
        token_valid = False

    if not token_valid:
        raise HTTPException(status_code=400, detail="This link either expired or invalid.")

    user.is_active = True
    user.updated_at = datetime.now()
    user.verified_at = datetime.now()
    session.add(user)
    session.commit()
    session.refresh(user)
    await send_account_activation_confirmation_email(user, background_tasks)
    return user