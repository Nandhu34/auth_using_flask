import jwt
import datetime 
from config import token_algorithm,secrete,access_token_exp_time,refresh_token_exp_time,hash_encoder
import bcrypt

def get_access_token(data):
    try :
        print(" access toekn function ")
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=access_token_exp_time)
        data.update({"exp": expiration_time})
        encode_jwt = jwt.encode(data,secrete,algorithm=token_algorithm)
        print(encode_jwt)
        raise ValueError("summa ")
        return encode_jwt
    
    except Exception as e:
         return False 


def get_refresh_token(data):
    try :
        print(" refresh  toekn function ")
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=refresh_token_exp_time)
        data.update({"exp": expiration_time})
        encode_jwt = jwt.encode(data,secrete,algorithm=token_algorithm)
        print(encode_jwt)
        return encode_jwt
    except Exception as e:
         return False 
    
def hash_password(data):
    try:
        # Generate a salt
        salt = bcrypt.gensalt()
        # Hash the password
        hashed_password = bcrypt.hashpw(data.encode(hash_encoder), salt)
        # Return the hashed password as a string
        return hashed_password.decode(hash_encoder)
    except Exception as e:
        # Return False or raise an error if something goes wrong
        print(f"An error occurred while hashing the password: {e}")
        return False