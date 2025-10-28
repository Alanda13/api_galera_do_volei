from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from typing import List
from domain.models import JogadorCriar, JogadorResposta
from app.services.service_jogador import JogadorService

router_jogador = APIRouter(prefix="/jogadores", tags=["Jogadores"])

# Instancia o service
jogador_service = JogadorService() 

@router_jogador.post("", response_model=JogadorResposta, status_code=status.HTTP_201_CREATED)
async def criar_jogador_endpoint(jogador: JogadorCriar):
    novo_jogador = jogador_service.criar_jogador(jogador)
    return novo_jogador

@router_jogador.get("", response_model=List[JogadorResposta])
async def listar_jogadores_endpoint():
    return jogador_service.listar_jogadores()

@router_jogador.get("/{jogador_id}", response_model=JogadorResposta)
async def buscar_jogador_endpoint(jogador_id: UUID):
    jogador = jogador_service.buscar_jogador(jogador_id)
    
    if not jogador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jogador não encontrado")
        
    return jogador