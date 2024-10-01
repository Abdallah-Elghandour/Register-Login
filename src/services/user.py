from datetime import datetime, timedelta
import logging
from src.services.email import send_account_activation_confirmation_email, send_account_verification_email
from src.models.user import User, UserToken
from config import security
from fastapi import HTTPException
from config.settings import get_settings
from src.utils.string import unique_string
from src.utils.email_context import VERIFY_ACCOUNT


settings = get_settings()


async def create_user_account(data, session, background_tasks):
    
    
    user_exist = session.query(User).filter(User.email == data.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Email is already exists.")
    
    if not security.is_password_strong(data.password):
        raise HTTPException(status_code=400, detail="Password is not strong enough")
    

    user = User()
    user.name = data.name
    user.surname = data.surname
    user.email = data.email
    user.password = security.get_password_hash(data.password)
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
        token_valid = security.verify_password(user_token, data.token)
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

async def get_login_token(data, session):
    user = await security.load_user(data.username, session)
    if not user:
        raise HTTPException(status_code=400, detail="Email is not registered.")
    
    if not security.verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password.")
    
    if not user.verified_at:
        raise HTTPException(status_code=400, detail="User account is not verified.")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User account has been deactivated.")
    

    return _generate_tokens(user, session)
def _generate_tokens(user, session):
    refresh_key = unique_string(100)
    access_key = unique_string(50)
    rt_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    user_token = UserToken()
    user_token.user_id = user.id
    user_token.refresh_key = refresh_key
    user_token.access_key = access_key
    user_token.expires_at = datetime.now() + rt_expires
    session.add(user_token)
    session.commit()
    session.refresh(user_token)

    at_payload = {
        'sub': security.str_encode(str(user.id)),
        'a': access_key,
        'r': security.str_encode(str(user_token.id)),
        'n': security.str_encode(f"{user.name} {user.surname}")
    }

    at_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.generate_token(at_payload, settings.JWT_SECRET, settings.JWT_ALGORITHM, at_expires)

    rt_payload = {
        'sub': security.str_encode(str(user.id)), 
        't': refresh_key, 
        'a': access_key}
    refresh_token = security.generate_token(rt_payload, settings.SECRET_KEY, settings.JWT_ALGORITHM, rt_expires)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": at_expires.seconds
    }