from pydantic import BaseModel, EmailStr, Field, root_validator,field_validator, constr ,model_validator, ValidationError,StringConstraints
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



class UserProfileUpdate(BaseModel):
    username: Optional[str]  # Optional for flexibility
    email: Optional[EmailStr]
    mobile_number: Optional[str]  # Ensure mobile number is 10 digits
    password: str  # Password is mandatory
    pincode: Optional[str]  # Ensure pincode is 6 digits
    address: Optional[str]


    @field_validator('mobile_number')
    def validate_mobile_number(cls, v):
        if v and not v.isdigit() or len(v) != 10:
            raise ValueError('Mobile number must be a 10-digit number.')
        return v
    
    @field_validator('pincode')
    def validate_pincode(cls, v):
        if v and not v.isdigit() or len(v) != 6:
            raise ValueError('Pincode must be a 6-digit number.')
        return v


    @model_validator(mode='before')
    def check_at_least_one_field(cls, values):
        # Extract values
        username, email, mobile_number, pincode, address = values.get('username'), values.get('email'), values.get('mobile_number'), values.get('pincode'), values.get('address')
        
        if not any([username, email, mobile_number, pincode, address]):
            raise ValueError('At least one of username, email, mobile_number, pincode, or address must be present.')
        return values
