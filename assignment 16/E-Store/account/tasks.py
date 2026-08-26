from django.conf import settings
from account.utils import EmailThread

BASE_URL = settings.BASE_URL.rstrip("/") + "/"


def send_verification_email(email, token):
    web_based_endpoint = f"{BASE_URL}account/verify/email/"
    api_based_endpoint = f"{BASE_URL}api/account/verify/email/"
    

    subject = "Account Verification"

    message = f"""Hello,

        We received a request to verify your account.

        Your verification token:
        {token}

        Endpoint:
        {web_based_endpoint}
        if you want api based 
        {api_based_endpoint}

        Body:
        {{
            "token": "{token}"
        }}

        This token will expire in 24 hours.

        If you did not create this account, ignore this email.

        Thanks,
        Your Team
        """

    EmailThread(subject, message, email).start()


def send_password_reset_email(email, token):

    web_based_endpoint = f"{BASE_URL}account/password/reset/confirm/"
    api_based_endpoint = f"{BASE_URL}api/account/password/reset/confirm/"

    subject = "Reset Your Password"

    message = f"""Hello,
        We received a request to reset your password.

        Your reset token:
        {token}

        Endpoint:
        {web_based_endpoint}
        if you want api based 
        {api_based_endpoint}
        Body:
        {{
            "token": "{token}"
        }}

        This token will expire in 24 hours.

        If you did not request this, ignore this email.

        Thanks,
        Your Team
        """

    EmailThread(subject, message, email).start()  
    
