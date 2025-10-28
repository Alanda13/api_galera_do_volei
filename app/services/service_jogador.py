
from uuid import uuid4, UUID
from typing import List, Optional
from domain.models import JogadorCriar, JogadorResposta
from infrastructure.repository_jogador import JogadorRepository

class JogadorService:
    """Responsabilidade Única: Regras de negócio relacionadas a Jogadores."""
    
    def __init__(self):
        # usa o repositório p/persistencia.
        self.repo = JogadorRepository() 
        
    def criar_jogador(self, jogador: JogadorCriar) -> JogadorResposta:
    
        jogador_id = uuid4()
        

        #aqui converte o dto p/ formato interno de repositorio
        dados_finais = jogador.model_dump()
        dados_finais["id"] = jogador_id
        dados_finais["email"] = dados_finais["email"].lower() 
        dados_finais.pop("senha") # Não salva a senha pura
        
        self.repo.add(dados_finais)
        
        # Retorna o DTO de Resposta
        return JogadorResposta(**dados_finais)
        
    def buscar_jogador(self, jogador_id: UUID) -> Optional[JogadorResposta]:
        jogador_data = self.repo.get_by_id(jogador_id)
        
        if jogador_data:
            return JogadorResposta(**jogador_data)
        return None

    def listar_jogadores(self) -> List[JogadorResposta]:
        jogadores_data = self.repo.get_all()
        return [JogadorResposta(**j) for j in jogadores_data]