from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from decimal import Decimal
class Message(BaseModel):

    count: int
    date: datetime
    size: int

    model_config = ConfigDict(from_attributes=True)

class MessageStatus(BaseModel):

    count: int
    size: int

    model_config = ConfigDict(from_attributes=True)

    