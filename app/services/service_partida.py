
from uuid import uuid4, UUID
from typing import List, Optional, Dict, Any
from domain.models import PartidaCriar, PartidaResposta, PedidoAdesao, PartidaStatus
from infrastructure.repository_partida import PartidaRepository
from infrastructure.repository_jogador import JogadorRepository # para verificações

class PartidaService:
    """Responsabilidade Única: Regras de negócio relacionadas a Partidas."""
    
    def __init__(self):
        self.partida_repo = PartidaRepository()
        self.jogador_repo = JogadorRepository() 
        
    def criar_partida(self, partida: PartidaCriar) -> PartidaResposta:
        
        # verificando a lógica de negócio!!!!1
        if not self.jogador_repo.get_by_id(partida.criador_id):
            raise ValueError("Criador da partida não encontrado.") 
        
        partida_id = uuid4()
        nova_partida = partida.model_dump()
        
        # lóogica de negocio
        nova_partida.update({
            "id": partida_id,
            "status": "em-adesao",
            "jogadores_confirmados": [partida.criador_id],
            "pedidos_adesao": [],
            "jogadores_presentes": []
        })
        
        self.partida_repo.add(nova_partida)
        return PartidaResposta(**nova_partida)

    def solicitar_adesao(self, partida_id: UUID, pedido: PedidoAdesao):
        
        partida: Dict[str, Any] = self.partida_repo.get_by_id(partida_id)
        if not partida:
            raise ValueError("Partida não encontrada.")
            
        jogador_id = pedido.jogador_id
        
        if not self.jogador_repo.get_by_id(jogador_id):
            raise ValueError("Jogador não encontrado.")
            
        if jogador_id in partida["pedidos_adesao"] or jogador_id in partida["jogadores_confirmados"]:
             raise ValueError("Jogador já solicitou ou está na partida.")

        partida["pedidos_adesao"].append(jogador_id)
        self.partida_repo.update(partida_id, partida)
        return True # Indica sucesso
