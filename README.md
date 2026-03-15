# ⚡ Async PokeAPI & Auth System

## 🎯 O Problema
Sistemas síncronos tradicionais sofrem com gargalos de I/O (Input/Output). Ao solicitar dados de múltiplos recursos em APIs externas, o servidor frequentemente congela, aguardando a resposta de cada requisição sequencialmente. Em cenários de alto tráfego, isso resulta em tempo de resposta inaceitável e alto consumo de recursos.

## 🛠️ A Solução
Esta API foi arquitetada para resolver o gargalo de rede utilizando processamento assíncrono avançado. Desenvolvida com **FastAPI**, ela atua como um agregador de dados competitivo. O sistema recebe uma matriz de parâmetros (um time de Pokémon) e orquestra requisições HTTPX simultâneas contra a PokeAPI REST original. Utilizando `asyncio.gather`, a aplicação busca, higieniza e estrutura os dados de múltiplos nós ao mesmo tempo, reduzindo o tempo total de resposta ao tempo da requisição mais lenta, não à soma delas.

Além do motor de extração, a API conta com um sistema de controle de acesso robusto, protegendo as rotas de busca através de autenticação via **JWT (JSON Web Tokens)** e persistência em banco de dados relacional.

## 🚀 Tecnologias Utilizadas
* **Backend:** FastAPI, Python 3.x
* **Assincronismo & Concorrência:** `asyncio`, `httpx` (Async HTTP Client)
* **Segurança:** OAuth2, JWT (JSON Web Tokens), Hashing de Senhas (bcrypt)
* **Banco de Dados:** SQLite3
* **Validação de Dados:** Pydantic

## ⚙️ Arquitetura e Fluxo de Dados
1. **Segurança (Auth):** O usuário deve criar uma conta (`/register`) e autenticar credenciais (`/login`) para gerar um token de acesso Bearer JWT.
2. **Injeção de Dependência:** A rota principal (`/porta`) é blindada. Ela intercepta a requisição e valida a assinatura criptográfica do token antes de liberar o processamento.
3. **Concorrência (`httpx` + `asyncio`):** A API abre um único *connection pool*. Em vez de iterar sobre o time de forma síncrona, ela cria coroutines para cada membro da matriz e as dispara em paralelo.
4. **Data Sanitization:** A resposta massiva da PokeAPI é dissecada. O sistema navega pela árvore do JSON, filtrando escopos não essenciais e aplicando `List Comprehensions` e `Dictionary Comprehensions` para retornar apenas o vetor tático limpo (Status Base, Tipologias, Habilidades e URL de Sprite).

## 📌 Endpoints da API

### 1. Autenticação e Usuários
* `POST /register`: Criação de novo usuário com hash de senha seguro no SQLite.
* `POST /login`: Validação de credenciais (OAuth2PasswordRequestForm) e emissão do JWT.

### 2. Motor de Agregação (Rota Protegida)
* `POST /porta`
  * **Headers Exigidos:** `Authorization: Bearer <seu_token_jwt>`
  * **Body Payload (JSON):**
    ```json
    {
      "pokemons": ["gengar", "scizor", "tyranitar", "togekiss"]
    }
    ```
  * **Resposta Esperada (200 OK):** Uma matriz otimizada contendo a extração paralela dos dados de todos os alvos solicitados simultaneamente.

## 💻 Como Executar Localmente

1. Clone o repositório.
2. Crie e ative um ambiente virtual (`python -m venv venv` e `source venv/bin/activate` ou `venv\Scripts\activate`).
3. Instale as dependências:
   ```bash
   pip install fastapi[standart] uvicorn httpx passlib[bcrypt] python-jose pydantic
3. Rode no terminal:
   ```bash
   fastapi dev main.py
