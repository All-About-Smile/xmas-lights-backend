# schemas/common.py
from pydantic import BaseModel

class MessageResponse(BaseModel):
    detail: str