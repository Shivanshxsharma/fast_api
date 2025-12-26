from pydantic import BaseModel, Field,EmailStr,AnyUrl,field_validator,model_validator,computed_field
from typing import List,Optional,Annotated


## for nested model
class child_model(BaseModel):
   child_name:str


class patient(BaseModel):
   name:Annotated[str,Field(description="" , default="shiv",strict=True)]
   age:int=Field(gt=0)
   email:EmailStr
   allergies:List[str]
   married:Optional[bool]=None
   child:child_model
   @field_validator("email")
   @classmethod
   def email_validator(cls,value):

      valid_domains=["nsut.com"]
       
      domain=value.split('@')[-1]

      if domain not in valid_domains:
         raise ValueError("not from valid organisation")
      return value
   

   #for transformation eg LowerCase to UpperCase

   @field_validator("name")
   @classmethod
   def uppercase(cls,value):
      return value.upper()
   

   ## for model validation
   @model_validator(mode="after")
   def validate(cls,model):

      if model.age<18 and model.married==True:
         raise ValueError("patient is not the valid person")
      return model
      


   @computed_field
   @property
   def Threexage(self)->float:
     ans=3*self.age

     return ans
     


# computed field provides a way to compute a new key or field in the pydantic model  by using fields given by the user 
# field validayor is used for custom buisness more adavanced validation
#strict overrides the type coersion
#Anotated foe adding meta data and constraints
# email str and anyurl gives the inbuilt data validation for email
#whereas Field gives custom datavalidation
#mode in field validator allows it to work in two modes before  type coersion and after type coersion
p1=patient(name="shivansh" ,age=1,email="hi@nsut.com",allergies=["peanut allergy"],married=False)

print(p1)



# what if the validation needs the value of two parameters in that case we use model validator 
#MODEL VALIDATOR


# exportation from pydantic model to python dictionary and and json

temp=p1.model_dump()
temp2=p1.model_dump_json()

