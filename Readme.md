# Projeto Galera do Vôlei API

Este projeto consiste em um exercício de **design de API**. O objetivo foi criar uma API funcional com o framework FastAPI para gerenciar uma comunidade de praticantes de vôlei. 

---

### Funcionalidades e Regras de Negócio

Aqui estão as funcionalidades implementadas e as regras de negócio que a API segue:

* **Cadastro de Jogadores:**
    * Cada jogador é identificado por um **ID único e aleatório (UUID)**.
    * A API valida automaticamente o formato do e-mail e outros campos de entrada.

* **Criação de Partidas:**
    * Uma partida só pode ser criada por um **jogador já cadastrado**.
    * O criador de uma partida é automaticamente adicionado à lista de **jogadores confirmados**.
    * Toda nova partida tem o status inicial `em-adesao`.

* **Gestão de Adesão:**
    * Um jogador pode **solicitar adesão** a uma partida, o que adiciona seu ID à lista de `pedidos_adesao`.
    * O criador da partida tem o poder de **gerenciar esses pedidos**, podendo aceitar ou rejeitar.
    * Ao ser aceito, o ID do jogador é movido da lista de `pedidos_adesao` para a de `jogadores_confirmados`.

* **Ciclo de Vida da Partida:**
    * A API permite alterar o **status da partida** (para `ativa` ou `encerrada`), simulando o começo e o fim de um jogo.
    * O registro de **presença** só pode ser feito para jogadores que estejam na lista de `jogadores_confirmados`.

* **Avaliações:**
    * Após uma partida, os jogadores podem **avaliar outros jogadores ou a partida** em si.
    * As avaliações são armazenadas separadamente, permitindo futuramente a criação de um sistema de reputação.

---

### Endpoints da API

A API é estruturada em três recursos principais: `jogadores`, `partidas` e `avaliacoes`.

#### Jogadores
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/jogadores` | Cria um novo jogador. |
| `GET` | `/jogadores/{jogador_id}` | Busca um jogador pelo ID. |
| `GET` | `/jogadores` | Lista todos os jogadores. |

#### Partidas
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/partidas` | Cria uma nova partida. |
| `GET` | `/partidas` | Lista todas as partidas. |
| `GET` | `/partidas/{partida_id}` | Busca os detalhes de uma partida. |
| `POST` | `/partidas/{partida_id}/adesao` | Envia um pedido de adesão. |
| `PUT` | `/partidas/{partida_id}/adesao/{jogador_id}` | Gerencia (aceita ou rejeita) um pedido de adesão. |
| `PUT` | `/partidas/{partida_id}/status` | Altera o status da partida. |
| `PUT` | `/partidas/{partida_id}/presenca` | Registra a presença dos jogadores. |

#### Avaliações
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/avaliacoes` | Registra uma nova avaliação. |

---

### Como Rodar o Projeto

1.  **Clone o repositório:**
    `git clone https://github.com/Alanda13/Projeto_Galera_do_volei.git`
2.  **Navegue até a pasta do projeto:**
    `cd Projeto_Galera_do_volei`
3.  **Crie e ative um ambiente virtual:**
    -   `python -m venv venv`
    -   `venv\Scripts\activate` (Windows)
    -   `source venv/bin/activate` (macOS/Linux)
4.  **Instale as dependências:**
    `pip install fastapi "uvicorn[standard]" "pydantic[email]"`
5.  **Execute a API:**
    `uvicorn main:app --reload`

A API estará rodando em `http://127.0.0.1:8000`.

---

### Testes

Para comprovar o funcionamento da API, os resultados dos testes no Postman estão compilados em um arquivo PDF.

[**Ver Documentação de Testes (PDF)**](./docs/testes%20de%20edpoints.pdf)