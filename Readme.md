# 🏐 Projeto Galera do Vôlei 

Este projeto implementa a API do "Galera do Vôlei" em **Python/FastAPI**, focando na aplicação de **Arquitetura em Camadas** e no princípio **SOLID (SRP)**, conforme solicitado pela disciplina de Separação de Responsabilidades.


---

## 🏗️ 1. Estrutura Arquitetural (Separação de Responsabilidades)

A API está organizada em 4 camadas para garantir o desacoplamento do código:

* **`domain`**: Contém os Modelos e DTOs (a definição dos dados).
* **`infrastructure`**: Responsável pela Persistência (simulação em memória).
* **`app/services`**: Contém a Lógica de Negócio e regras da aplicação.
* **`app/api`**: Lida exclusivamente com as rotas HTTP e respostas (Controllers).

---

## 👉 Documentação da API: http://127.0.0.1:8000/docs
