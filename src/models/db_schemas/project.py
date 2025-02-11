from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import  ObjectId

class Project(BaseModel):
    _id : Optional[ObjectId] = None
    project_id :str = Field(..., min_length=1)

    class Config :
        arbitrary_types_allowed=True

