from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator
from datetime import datetime
from typing import List
from decimal import Decimal
class Message(BaseModel):

    count: int
    date: datetime
    size: int

    model_config = ConfigDict(from_attributes=True)

class MessageStatus(BaseModel):

    count: str
    size: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("size", mode='before')
    def format_size(cls, v):
        # Ensure the size is in integer format
        bytes_size = int(v)
        
        # Define units and their respective limits
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0

        # Convert bytes to the largest readable unit
        while bytes_size >= 1024 and unit_index < len(units) - 1:
            bytes_size /= 1024
            unit_index += 1

        # Format the size with two decimal places
        readable_size = f"{bytes_size:.2f} {units[unit_index]}"
        return readable_size

    @field_validator("count", mode='before')
    def format_count(cls, v):
        count_str = str(v)
        formatted_count = " ".join([count_str[max(i-3, 0):i] for i in range(len(count_str), 0, -3)][::-1])

        return formatted_count