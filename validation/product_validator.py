from pydantic import Field ,BaseModel, field_validator,constr,Extra,ConfigDict
from enum import Enum

# class home_based_options/
class option_for_home_product(Enum):
    discount ='discount'
    actual_price ="actual_price"
    discount_price="discount_price"



class validate_home_product_requests(BaseModel):
    model_config=ConfigDict(extra='forbid')
    based_on:option_for_home_product

    # based_on:str=Field(max_length=8)
    
   


    

