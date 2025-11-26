

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To
from app.core.config import Settings

def send_verification_email(recipient_email: str, verification_link: str):

    
    
    html_content = f"""
    <html>
        <body>
            <h3>Account Verification Required</h3>
            <p>Welcome to Neo stores! Please click the link below to verify your email address:</p>
            <p style="padding: 10px; background-color: #f0f8ff; border-radius: 5px;">
                <a href="{verification_link}">CLICK HERE TO VERIFY YOUR ACCOUNT</a>
            </p>
            <p>If you did not request this, please ignore this email.</p>
        </body>
    </html>
    """

    message = Mail(
        from_email=Settings.SENDER_EMAIL,
        to_emails=To(recipient_email),
        subject='[NEO] Account Verification',
        html_content=html_content
    )

    try:
        
        sg = SendGridAPIClient(Settings.SENDGRID_API_KEY)
        response = sg.send(message)
        
        
        if 200 <= response.status_code < 300:
            print(f"SendGrid Success: Mail submitted to {recipient_email} ---")
            return True
        else:
            print(f"!!! SendGrid Error: Status {response.status_code}, Body: {response.body} !!!")
            return False
            
    except Exception as e:
        print(f"!!! SendGrid API Connection Error: {e} !!!")
        return False
    

def send_reset_password_email(recipient_email: str, verification_link: str):

    
    
    html_content = f"""
    <html>
        <body>
            <h3>Forget password notification</h3>
            <p>Welcome to Neo stores! Please click the link below to reset your password:</p>
            <p style="padding: 10px; background-color: #f0f8ff; border-radius: 5px;">
                <a href="{verification_link}">CLICK HERE TO RESET YOUR PASSWORD</a>
            </p>
            <p>If you did not request this, please ignore this email.</p>
        </body>
    </html>
    """

    message = Mail(
        from_email=Settings.SENDER_EMAIL,
        to_emails=To(recipient_email),
        subject='[NEO] PASSWORD RESET',
        html_content=html_content
    )

    try:
        
        sg = SendGridAPIClient(Settings.SENDGRID_API_KEY)
        response = sg.send(message)
        
        
        if 200 <= response.status_code < 300:
            print(f"SendGrid Success: Mail submitted to {recipient_email} ---")
            return True
        else:
            print(f"!!! SendGrid Error: Status {response.status_code}, Body: {response.body} !!!")
            return False
            
    except Exception as e:
        print(f"!!! SendGrid API Connection Error: {e} !!!")
        return False