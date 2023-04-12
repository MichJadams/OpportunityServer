from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class ApplicationStatus(str, Enum):
    applied = 'applied'
    interviewing = 'interviewing'
    rejected = 'rejected'
    partial_application = 'partial_application'
    going_to_apply = 'going_to_apply'

class OpportunityBase(BaseModel):
    url: str
    role_description: str
    notes: str
    title: str 
    date_applied: datetime
    application_status: ApplicationStatus

# There is nothing that is included in the version created originally that 
# isn't also returned when reading back the opportunity from the database 
class OpportunityCreate(OpportunityBase):
    pass 

class Opportunity(OpportunityBase):
    id: int 
    user_name: str
    created_at: datetime
    updated_at: datetime 
    
    class Config:
        org_mode = True

class UserBase(BaseModel):
    name: str 

# when inititally creating a user, we need a password, but not 
# when reading it from the database 
class UserCreate(UserBase):
    password: str 

class User(UserBase):
    id: int 
    opportunities: list[Opportunity] = []

# this tells pydantic to read the model even if it is not a dictionary 
# in other words, it will now accept from a database 
    class Config:
        org_mode = True

