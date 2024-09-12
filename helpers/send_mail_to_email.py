

from app import mail,Message
def send_mail():
        try :
            
            msg = Message(subject='Hello from the other side!', sender='nandhakumarselva2000@gmail.com', recipients=['nandhakumars@saptanglabs.com'])
            msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works."
            mail.send(msg)
            print(" mail send !")
            return ({"status":"success","data":"link has been generated kindly reset password in 5 min"})
        except Exception as e:
              return ({"status":"error","data":f"{str(e)}"})