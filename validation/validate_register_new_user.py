from pydantic import BaseModel, EmailStr, Field, root_validator,field_validator, constr ,model_validator, ValidationError
from datetime import datetime
from typing import Optional
from enum import Enum
import re 

class UserRole(str, Enum):
    user = 'user'
    admin = 'admin'

class RegisterDetailsValidating(BaseModel):
    username: constr(min_length=5)
    email: EmailStr
    mobile_number: constr(pattern=r'^\d{10}$')  # Ensure mobile number is 10 digits
    password: constr(min_length=6)
    access_token: str
    refresh_token: str
    date_of_register: Optional[str] = None
    date_of_last_login: Optional[str] = ""
    role: UserRole
    reset_password_token: Optional[str] = ""
    reset_password_token_expire: Optional[str] = ""
    pincode: constr(min_length=6, max_length=6)  
    address: constr(min_length=10, max_length=200)  

    @field_validator('date_of_register')
    def set_date_of_register(cls, value):
        return value or datetime.now().isoformat()
    
    @field_validator('address')
    def validate_address(cls, value):
        # Define a regex pattern for validating the address
        pattern = re.compile(r'^[\w\s,().-]+$')
        if not pattern.match(value):
            raise ValueError('Address contains invalid characters')
        return value
    
    # @validator('mobile_number')
    # def mobile_number_must_be_10_digits(cls, value):
    #     if not value.isdigit() or len(value) != 10:
    #         raise ValueError('Mobile number must be exactly 10 digits')
    #     return value

class login_validation (BaseModel):
    print(" validation ")
    email:EmailStr
    password:constr(min_length=6)

class forget_password_validation (BaseModel):
    print(" forget password validation ")
    email:EmailStr

