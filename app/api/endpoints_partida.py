from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from domain.models import PartidaCriar, PartidaResposta, PedidoAdesao
from app.services.service_partida import PartidaService

router_partida = APIRouter(prefix="/partidas", tags=["Partidas"])
partida_service = PartidaService()

@router_partida.post("", response_model=PartidaResposta, status_code=status.HTTP_201_CREATED)
async def criar_partida_endpoint(partida: PartidaCriar):
    try:
        nova_partida = partida_service.criar_partida(partida)
        return nova_partida
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router_partida.post("/{partida_id}/adesao", status_code=status.HTTP_200_OK)
async def solicitar_adesao_endpoint(partida_id: UUID, pedido: PedidoAdesao):
    try:
        partida_service.solicitar_adesao(partida_id, pedido)
        return {"mensagem": "Pedido de adesão enviado com sucesso."}
    except ValueError as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))