

from app import mail,Message
from config import mail_sender
from helpers.auth_helpers import generate_forget_password_token,new_user_collection
def send_mail(data):
        try :
            # print(data)
            # from auth_helpers import new_user_collection
            reset_token = generate_forget_password_token(data)
            print({"email":data['email']})
            print(reset_token)
            
            update_forget_password=new_user_collection.update_one({"email":data['email']},{"$set":{"reset_password_token":reset_token,"reset_password_token_expire":False}})
            if update_forget_password.modified_count == 1:
                  print("token has been updated in db ")
            print(reset_token)


            # reset_token.replace('.','_')
            # exit(0)

            
            reset_url = f"http://127.0.0.1:5000/api/auth/reset_password/token={reset_token}"
            msg = Message(
        "Password Reset",
        sender=mail_sender ,

        recipients=[data['email']]
    )
            print(mail_sender,"mail sender ")
    # Plain text version

            # msg.body = f"""
            # Hey {data['email']}, sending you this email from my app, lmk if it works.
            # You can reset your password using this link: {reset_url}
            # """
            
            # HTML version with the button
            msg.html = f"""
            <html>
                <body>
                    <p>Hey {data['email']}jijji,</p>
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
              print("exception")
              return ({"status":"error","data":f"{str(e)}"})