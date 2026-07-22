#from sendgrid import SendGridAPIClient
#from sendgrid.helpers.mail import Mail, To
from fastapi_mail import FastMail, MessageSchema, MessageType
#from app.core.config import Settings
from app.utils.helpers import conf



async def send_verification_email(recipient_email: str, verification_link: str):

   try: 
        print("1. Entered send_verification_email")
    
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
        print("2. HTML created")
        message = MessageSchema(
            subject="WElcome to NEG store!!!!!",
            recipients=[recipient_email],
            body=html_content,
            subtype=MessageType.html,
        )
        print("3. Message created")
        fm = FastMail(conf)
        print("4. FastMail created")
        await fm.send_message(message)
        print("5. Email sent!")
   except Exception as e:
       print(repr(e))
    
async def send_reset_password_email(recipient_email: str, verification_link: str):

    
    
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

    message = MessageSchema(
        subject="WElcome to NEG store!!!!!",
        recipients=[recipient_email],
        body=html_content,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)