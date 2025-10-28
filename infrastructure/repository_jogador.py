
from typing import Dict, Any, List, Optional
from uuid import UUID

# simulacao de um banco de dados só que em memoria
JOGADORES_DB: Dict[UUID, Dict[str, Any]] = {}

class JogadorRepository:
    """Responsabilidade Única: Acesso aos dados de Jogadores."""
    
    def get_by_id(self, jogador_id: UUID) -> Optional[Dict[str, Any]]:
        return JOGADORES_DB.get(jogador_id)
        
    def add(self, jogador_data: Dict[str, Any]):
        JOGADORES_DB[jogador_data["id"]] = jogador_data
        
    def get_all(self) -> List[Dict[str, Any]]:
        return list(JOGADORES_DB.values())
# sem implementação de um banco de dados real ainda!!!