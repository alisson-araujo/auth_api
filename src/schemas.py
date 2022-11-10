from pydantic import BaseModel


class AuthDetail(BaseModel):
    cpf: str
    password: str