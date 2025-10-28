# vai definir os DTOS para o request e response

from typing import Optional, List
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

# dtos do jogador
class JogadorCriar(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    sexo: Optional[str] = None
    categoria: Optional[str] = None
    convidado_por: Optional[UUID] = None

class JogadorResposta(BaseModel):
    id: UUID
    nome: str
    email: EmailStr
    sexo: Optional[str]
    categoria: Optional[str]
    convidado_por: Optional[UUID]

# dtos da partida
class PartidaCriar(BaseModel):
    local: str
    data: datetime
    categoria: str
    tipo: str
    criador_id: UUID

class PartidaResposta(BaseModel):
    id: UUID
    local: str
    data: datetime
    categoria: str
    tipo: str
    status: str
    criador_id: UUID
    jogadores_confirmados: List[UUID]
    pedidos_adesao: List[UUID]
    jogadores_presentes: List[UUID] = []

class PedidoAdesao(BaseModel):
    jogador_id: UUID

class PartidaStatus(BaseModel):
    status: str

# dtos de avaliação
class AvaliacaoCriar(BaseModel):
    partida_id: UUID
    avaliador_id: UUID
    avaliado_id: Optional[UUID] = None
    nota: int
    comentario: Optional[str] = None