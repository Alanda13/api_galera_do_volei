# main.py

from typing import Optional, List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from datetime import datetime

# --- Modelos de Dados ---
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

class AvaliacaoCriar(BaseModel):
    partida_id: UUID
    avaliador_id: UUID
    avaliado_id: Optional[UUID] = None
    nota: int
    comentario: Optional[str] = None

# --- Dados em Memória ---
jogadores_db = {}
partidas_db = {}
avaliacoes_db = {}

app = FastAPI()

# --- Endpoints ---

@app.post("/jogadores", response_model=JogadorResposta, status_code=status.HTTP_201_CREATED)
async def criar_jogador(jogador: JogadorCriar):
    # UUID4 cria um ID único e aleatório para cada jogador.
    # É bom pra não ter ID repetido e não expor o total de usuários.
    jogador_id = uuid4()
    jogadores_db[jogador_id] = {
        "id": jogador_id,
        "nome": jogador.nome,
        "email": jogador.email,
        "sexo": jogador.sexo,
        "categoria": jogador.categoria,
        "convidado_por": jogador.convidado_por,
    }
    return jogadores_db[jogador_id]

@app.get("/jogadores/{jogador_id}", response_model=JogadorResposta)
async def buscar_jogador(jogador_id: UUID):
    jogador = jogadores_db.get(jogador_id)
    if not jogador:
        # Quando o jogador nao eh encontrado, a gente "levanta" um erro;
        # HTTPException avisa que deu erro, e o 404 diz que o item naoo existe
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jogador não encontrado")
    return jogador

@app.get("/jogadores")
async def listar_jogadores():
    return list(jogadores_db.values())

@app.post("/partidas", response_model=PartidaResposta, status_code=status.HTTP_201_CREATED)
async def criar_partida(partida: PartidaCriar):
    if partida.criador_id not in jogadores_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Criador da partida não encontrado")
    
    partida_id = uuid4()
    nova_partida = {
        "id": partida_id,
        "local": partida.local,
        "data": partida.data,
        "categoria": partida.categoria,
        "tipo": partida.tipo,
        "status": "em-adesao",
        "criador_id": partida.criador_id,
        "jogadores_confirmados": [partida.criador_id],
        "pedidos_adesao": [],
        "jogadores_presentes": []
    }
    partidas_db[partida_id] = nova_partida
    return nova_partida

@app.get("/partidas", response_model=List[PartidaResposta])
async def listar_partidas():
    return list(partidas_db.values())

@app.get("/partidas/{partida_id}", response_model=PartidaResposta)
async def buscar_partida(partida_id: UUID):
    partida = partidas_db.get(partida_id)
    if not partida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partida não encontrada")
    return partida

@app.post("/partidas/{partida_id}/adesao", status_code=status.HTTP_200_OK)
async def solicitar_adesao(partida_id: UUID, pedido: PedidoAdesao):
    partida = partidas_db.get(partida_id)
    if not partida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partida não encontrada")
    
    if pedido.jogador_id not in jogadores_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jogador não encontrado")
        
    if pedido.jogador_id in partida["pedidos_adesao"] or pedido.jogador_id in partida["jogadores_confirmados"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Jogador já solicitou ou está na partida")
    
    partida["pedidos_adesao"].append(pedido.jogador_id)
    return {"mensagem": "Pedido de adesão enviado com sucesso."}

@app.put("/partidas/{partida_id}/adesao/{jogador_id}")
async def gerenciar_adesao(partida_id: UUID, jogador_id: UUID, acao: str):
    partida = partidas_db.get(partida_id)
    if not partida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partida não encontrada")
    
    if acao not in ["aceitar", "rejeitar"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ação inválida. Use 'aceitar' ou 'rejeitar'.")

    if jogador_id not in partida["pedidos_adesao"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido de adesão não encontrado para este jogador.")

    if acao == "aceitar":
        partida["pedidos_adesao"].remove(jogador_id)
        partida["jogadores_confirmados"].append(jogador_id)
        return {"mensagem": "Pedido de adesão aceito com sucesso."}
    
    elif acao == "rejeitar":
        partida["pedidos_adesao"].remove(jogador_id)
        return {"mensagem": "Pedido de adesão rejeitado com sucesso."}

@app.put("/partidas/{partida_id}/status")
async def atualizar_status_partida(partida_id: UUID, status_atualizacao: PartidaStatus):
    partida = partidas_db.get(partida_id)
    if not partida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partida não encontrada.")
    
    if status_atualizacao.status not in ["ativa", "encerrada"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status inválido. Use 'ativa' ou 'encerrada'.")
    
    partida["status"] = status_atualizacao.status
    return {"mensagem": f"Status da partida alterado para '{status_atualizacao.status}'."}

@app.put("/partidas/{partida_id}/presenca")
async def registrar_presenca(partida_id: UUID, jogadores_presentes: list[UUID]):
    partida = partidas_db.get(partida_id)
    if not partida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partida não encontrada.")

    for jogador_id in jogadores_presentes:
        if jogador_id not in partida["jogadores_confirmados"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"O jogador {jogador_id} não está confirmado nesta partida.")
    
    partida["jogadores_presentes"] = jogadores_presentes
    return {"mensagem": "Presença dos jogadores registrada com sucesso."}

@app.post("/avaliacoes", status_code=status.HTTP_201_CREATED)
async def criar_avaliacao(avaliacao: AvaliacaoCriar):
    if avaliacao.partida_id not in partidas_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partida não encontrada.")
    if avaliacao.avaliador_id not in jogadores_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avaliador não encontrado.")
    
    avaliacao_id = uuid4()
    avaliacoes_db[avaliacao_id] = avaliacao.dict()
    avaliacoes_db[avaliacao_id]["id"] = avaliacao_id
    
    return {"mensagem": "Avaliação registrada com sucesso.", "id": avaliacao_id}