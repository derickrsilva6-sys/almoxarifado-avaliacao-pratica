from pydantic import BaseModel
from models.usuario import TipoUsuario

class UsuarioBase(BaseModel):
    nome: str
    username: str
    tipo: TipoUsuario

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
