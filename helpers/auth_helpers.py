import jwt
import datetime 
from config import token_algorithm,secrete,access_token_exp_time,refresh_token_exp_time,hash_encoder,forget_password_exp_time
import bcrypt
from models.db_creation import new_user_collection


def generate_forget_password_token(data):
    try :
        print(" generating email token ")
        # print(data['email'])
        user_data = new_user_collection.find_one({"email":data['email']})
        print(user_data)

        data ={"email":user_data['email'],"role":user_data['role'], "password":user_data['password']}
        print(data)
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=forget_password_exp_time)
        data.update({"exp": expiration_time})
        encode_jwt = jwt.encode(data,secrete,algorithm=token_algorithm)
        print(encode_jwt)
        
        return encode_jwt
    
    except Exception as e:
         print(e)
         print(" exception ")
         return False 


def get_access_token(data):
    try :
        print(" access toekn function ")
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=access_token_exp_time)
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
    
def check_expired(token):
    try:
        # Decode the token (will raise an error if expired)
        jwt.decode(token, secrete, algorithms=[token_algorithm])
        return False  # Token is valid, not expired
    except jwt.ExpiredSignatureError:
        return True  # Token is expired
    except jwt.InvalidTokenError:
        return True  # Invalid token, treat as expired


def get_token_data(token):
    try:
        print(" get token dat ")
        # Decode the token (will raise an error if expired)
        print(token)
        data = jwt.decode(token, secrete, algorithms=[token_algorithm])
        print(data)
        return data
           # Token is valid, not expired
    except jwt.ExpiredSignatureError:
        print(" expirted ")
        return True  # Token is expired
    except jwt.InvalidTokenError:
        print(" invalid ")
        return True  # Invalid token, treat as expired

     
