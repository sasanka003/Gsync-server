from fastapi_mail import FastMail, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

MAIL_TO = os.getenv("MAIL_TO")

conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = 2525,
    MAIL_SERVER = "mail.smtp2go.com",
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=False,
    USE_CREDENTIALS = True,
    TEMPLATE_FOLDER="templates"
)

fm = FastMail(conf)
