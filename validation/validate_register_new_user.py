from pydantic import BaseModel,EmailStr , Field ,validator

from datetime import datetime
from typing import Optional 
from enum import Enum 

class UserRole(str,Enum):
     user='user'
     admin ='admin'

class regis_details_validating(BaseModel):
     username:str =Field(...,min_length =5)
     email: EmailStr 
     mobileNumber: str = Field(...,regex=r'^\d{10}$')
     password:str= Field(..., min_length=6)
     accessToken:str
     refreshToken:str
     dateOfRegister:Optional[str] = None
     dateOfLastLogin :Optional[str] = ""
     role :UserRole
     resetPasswordToken:Optional[str] = ""
     resetPasswordTokenExpire:Optional[str] = "" 

     @validator('date_of_register', pre=True, always=True)
     def set_date_of_register(cls, value):
        return value or datetime.now().isoformat()
     
     @validator ('username')
     def check_username(cls,value):
         if len(value)<5 : 
             raise ValueError(" user anme must be least 5 character long ")
         return value 
     
     @validator('password')
     def password_must_be_greater_than_5(cls, value):
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return value

     @validator('mobile_number')
     def mobile_number_must_be_10_digits(cls, value):
            if not value.isdigit() or len(value) != 10:
                raise ValueError('Mobile number must be exactly 10 digits')
            return value
     @validator('access_token', 'refresh_token', pre=True)
     def perform_token_operations(cls, value, field):
        # Add your custom token operations here
        return value