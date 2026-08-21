from celery import shared_task
from django.conf import settings
from account.utils import send_email



BASE_URL = settings.BASE_URL.rstrip("/") + "/"


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3}
)
def send_verification_email(email, otp):
    web_based_endpoint = f"{BASE_URL}account/verify/email/"
    api_based_endpoint = f"{BASE_URL}api/account/verify/email/"
    

    subject = "Account Verification"

    message = f"""Hello,

        We received a request to verify your account.

        Your verification OTP:
        {otp}

        Endpoint:
        {web_based_endpoint}
        if you want api based 
        {api_based_endpoint}

        Body:
        {{
            "otp": "{otp}"
        }}

        This otp will expire in 5 minute.

        If you did not create this account, ignore this email.

        Thanks,
        Your Team
        """

    send_email(subject, message, email)


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3}
)
def send_password_reset_email(email, otp):

    web_based_endpoint = f"{BASE_URL}account/password/reset/confirm/"
    api_based_endpoint = f"{BASE_URL}api/account/password/reset/confirm/"

    subject = "Reset Your Password"

    message = f"""Hello,
        We received a request to reset your password.

        Your reset OTP:
        {otp}

        Endpoint:
        {web_based_endpoint}
        if you want api based 
        {api_based_endpoint}
        Body:
        {{
            "otp": "{otp}"
        }}

        This otp will expire in 5 minute.

        If you did not request this, ignore this email.

        Thanks,
        Your Team
        """

    send_email(subject, message, email)  
    