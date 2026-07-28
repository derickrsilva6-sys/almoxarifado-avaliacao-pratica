import enum
from sqlalchemy import Column, Integer, String, Enum
from database import Base

class TipoUsuario(str, enum.Enum):
    ADMINISTRADOR = "administrador"
    OPERADOR = "operador"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    tipo = Column(Enum(TipoUsuario), default=TipoUsuario.OPERADOR)
