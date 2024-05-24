from pydantic import BaseModel


#class MessageCreate(BaseModel):
    
class MessageCreate(BaseModel):
    topic: str
    size: int

