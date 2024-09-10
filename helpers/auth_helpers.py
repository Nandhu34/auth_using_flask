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
        print("Hashed Password:", hashed_password.decode(hash_encoder))
        return hashed_password.decode(hash_encoder)
    except Exception as e:
        # Handle the error
        print(f"An error occurred while hashing the password: {e}")
        return False

def decrypt_password(original_password,hashed_password):
    try:
        print("Decrypting password (verifying)...")
        # Compare the plain text password with the hashed password
        return bcrypt.checkpw(original_password.encode(hash_encoder), hashed_password.encode(hash_encoder))
    except Exception as e:
        print(f"An error occurred while verifying the password: {e}")
        return False