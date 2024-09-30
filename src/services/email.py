from fastapi import BackgroundTasks
from config.settings import get_settings

from config.email import send_email
from src.utils.email_context import VERIFY_ACCOUNT
from config.security import get_password_hash
settings = get_settings()


async def send_account_verification_email(account, background_tasks: BackgroundTasks):
    
    string_context = account.get_context_string(context=VERIFY_ACCOUNT)
    token = get_password_hash(string_context)
    activate_url = f"{settings.FRONTEND_HOST}/auth/account-verify?token={token}&email={account.email}"
    data = {
        'app_name': settings.APP_NAME,
        "name": account.name,
        'activate_url': activate_url
    }
    subject = f"Account Verification - {settings.APP_NAME}"
    await send_email(
        recipients=[account.email],
        subject=subject,
        template_name="user/account_verification.html",
        context=data,
        background_tasks=background_tasks
    )

async def send_account_activation_confirmation_email(account, background_tasks: BackgroundTasks):
    data = {
        'app_name': settings.APP_NAME,
        "name": account.name,
        'login_url': f'{settings.FRONTEND_HOST}'
    }
    subject = f"Welcome - {settings.APP_NAME}"
    await send_email(
        recipients=[account.email],
        subject=subject,
        template_name="user/account_verification_confirmation.html",
        context=data,
        background_tasks=background_tasks
    )