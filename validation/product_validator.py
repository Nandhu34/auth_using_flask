from pydantic import Field ,BaseModel, field_validator,constr,Extra,ConfigDict


# class home_based_options/

class validate_home_product_requests(BaseModel):
    model_config=ConfigDict(extra='forbid')
    based_on:str=Field(max_length=8)
   


    

