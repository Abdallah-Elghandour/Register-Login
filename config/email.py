import os
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from fastapi.background import BackgroundTasks
from config.settings import get_settings

settings = get_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
    MAIL_PORT=int(os.environ.get("MAIL_PORT")),
    MAIL_SERVER=os.environ.get("MAIL_SERVER"),
    MAIL_STARTTLS=os.environ.get("MAIL_STARTTLS"),
    # MAIL_SSL_TLS=os.environ.get("MAIL_SSL_TLS"),
    # MAIL_DEBUG=True,
    MAIL_FROM=os.environ.get("MAIL_FROM"),
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "src/templates",
    MAIL_FROM_NAME=os.environ.get("MAIL_FROM_NAME"),
    USE_CREDENTIALS=bool(os.environ.get("USE_CREDENTIALS"))
)


fm = FastMail(conf)


async def send_email(recipients: list, subject: str, context: dict, template_name: str,
                     background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=context,
        subtype=MessageType.html
    )

    background_tasks.add_task(fm.send_message, message, template_name=template_name)