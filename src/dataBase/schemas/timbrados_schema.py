from datetime import datetime
from pydantic import BaseModel


class TimbradoSchema(BaseModel):
    timbrado_number: str
    client_name: str
    numero_inicio: str
    numero_fin: str
    end_date: datetime
