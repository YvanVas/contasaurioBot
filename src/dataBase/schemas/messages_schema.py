import datetime
from pydantic import BaseModel


class MessageSchema(BaseModel):
    message_id: str
    chat_id: str
    from_user_id: int
    text: str
    date: datetime.datetime
