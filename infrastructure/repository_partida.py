
from typing import Dict, Any, List, Optional
from uuid import UUID

#simulação de banco dedados em memoria
PARTIDAS_DB: Dict[UUID, Dict[str, Any]] = {}

class PartidaRepository:
    """Responsabilidade Única: Acesso aos dados de Partidas."""
    
    def get_by_id(self, partida_id: UUID) -> Optional[Dict[str, Any]]:
        return PARTIDAS_DB.get(partida_id)
        
    def add(self, partida_data: Dict[str, Any]):
        PARTIDAS_DB[partida_data["id"]] = partida_data
        
    def get_all(self) -> List[Dict[str, Any]]:
        return list(PARTIDAS_DB.values())

    def update(self, partida_id: UUID, partida_data: Dict[str, Any]):
        if partida_id in PARTIDAS_DB:
            PARTIDAS_DB[partida_id].update(partida_data)
            return True
        return False