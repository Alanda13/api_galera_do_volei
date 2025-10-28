from fastapi import FastAPI
from app.api.endpoints_jogador import router_jogador
from app.api.endpoints_partida import router_partida

app = FastAPI(
    title="Projeto Galera do Vôlei API",
    description="API implementada com Separação de Responsabilidades (Arquitetura em Camadas)",
    version="1.0.0"
)
app.include_router(router_jogador)
app.include_router(router_partida)
