from pydantic import BaseModel, EmailStr, Field, root_validator,field_validator, constr ,model_validator, ValidationError
from datetime import datetime
from typing import Optional
from enum import Enum
from helpers.auth_helpers import get_access_token,get_refresh_token,hash_password

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

    @field_validator('date_of_register')
    def set_date_of_register(cls, value):
        return value or datetime.now().isoformat()

    # @validator('mobile_number')
    # def mobile_number_must_be_10_digits(cls, value):
    #     if not value.isdigit() or len(value) != 10:
    #         raise ValueError('Mobile number must be exactly 10 digits')
    #     return value
    
    # @field_validator('access_token', 'refresh_token',mode='before')
    # def perform_token_operations(cls, value, values,field):
    #     username = values.get('username')
    #     email=values.get('email')
    #     mobile_number = values.get('mobile_number')
    #     role= values.get('role')
    #     raw_data = {"username":username,"email":email,"mobile_number":mobile_number,'role':role}
    #     token = get_access_token(raw_data)
    #     print(raw_data)
    #     return value

    @model_validator(mode='after')
    def perform_token_operations(self):
        username = self.username
        email=self.email
        mobile_number = self.mobile_number
        role= self.role
        raw_data = {"username":username,"email":email,"mobile_number":mobile_number,'role':role}
        token = get_access_token(raw_data)
        if token: 
            self.access_token = token
        else:
            self.access_token=""
            raise ValueError ('access toekn not generated')
        
        refresh_toekn = get_refresh_token(raw_data)
        if refresh_toekn:
            self.refresh_token = refresh_toekn
        else :
            self.refresh_token =""
            raise ValueError ('refresh  toekn not generated')
      
        hashed_password = hash_password(self.password)
        if hashed_password:
            self.password = hashed_password
        else:
            raise ValueError('encoded password error ')

