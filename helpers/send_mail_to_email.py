

from app import mail,Message
from helpers.auth_helpers import generate_forget_password_token
def send_mail(data):
        try :
            # print(data)
            reset_token = generate_forget_password_token(data)
            print(reset_token)
            # reset_token.replace('.','_')
            # exit(0)

            
            reset_url = f"http://127.0.0.1:5000/api/auth/reset_password/token={reset_token}"
            msg = Message(
        "Password Reset",
        sender="nandhakumarsmail,com",
        recipients=[data['email']]
    )
    # Plain text version
            msg.body = f"""
            Hey {data['email']}, sending you this email from my app, lmk if it works.
            You can reset your password using this link: {reset_url}
            """
            
            # HTML version with the button
            msg.html = f"""
            <html>
                <body>
                    <p>Hey {data['email']},</p>
                    <p>Sending you this email from my app, lmk if it works.</p>
                    <p>
                        <a href="{reset_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">
                            Reset Your Password
                        </a>
                    </p>
                </body>
            </html>
            """
            mail.send(msg)

            return ({"status":"success","data":"link has been generated kindly reset password in 5 min"})
        except Exception as e:
              return ({"status":"error","data":f"{str(e)}"})