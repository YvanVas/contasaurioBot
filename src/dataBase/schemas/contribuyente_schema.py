from pydantic import BaseModel


class ContribuyenteSchema(BaseModel):
    ruc: str
    dv: str
    fullname: str
    status: str