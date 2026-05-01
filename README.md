# Desafio MBA Engenharia de Software com IA - Full Cycle

Este projeto implementa um sistema de Ingestão e Busca Semântica de documentos PDF utilizando Python, LangChain, PostgreSQL com pgVector e Google Generative AI (Gemini).

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Execução](#execução)
  - [1. Iniciar o Banco de Dados](#1-iniciar-o-banco-de-dados)
  - [2. Ingestão do PDF](#2-ingestão-do-pdf)
  - [3. Interação via CLI](#3-interação-via-cli)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Modelos Utilizados](#modelos-utilizados)

---

## Pré-requisitos

Certifique-se de ter o seguinte software instalado em sua máquina:

*   **Docker** e **Docker Compose**: Para subir o banco de dados PostgreSQL com pgVector.
*   **Python 3.9+**: Para executar os scripts da aplicação.
*   **pip**: Gerenciador de pacotes do Python.

## Configuração do Ambiente
### VirtualEnv para Python
Recomenda-se criar um ambiente virtual para isolar as dependências do projeto. Você pode usar `venv` ou `virtualenv`:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

### Chaves de API
*   Obtenha uma `GOOGLE_API_KEY` do Google AI Studio.
*   (Opcional) Obtenha uma `OPENAI_API_KEY` da OpenAI, caso prefira utilizar os modelos da OpenAI.

### Variáveis de Ambiente
*   Copie o arquivo `.env.example` para `.env`:
    ```bash
    cp .env.example .env
    ```
*   Edite o arquivo `.env` e preencha as variáveis de ambiente com suas chaves de API e configurações desejadas.
    *   `GOOGLE_API_KEY`: Sua chave de API do Google.
    *   `GOOGLE_EMBEDDING_MODEL`: Modelo de embedding do Google (padrão: `models/embedding-001`).
    *   `GOOGLE_MODEL`: Modelo de LLM do Google (padrão: `gemini-pro`).
    *   `DATABASE_URL`: URL de conexão com o PostgreSQL (padrão para Docker: `postgresql+psycopg://postgres:postgres@localhost:5432/rag`).
    *   `PG_VECTOR_COLLECTION_NAME`: Nome da coleção no pgVector (padrão: `pdf_documents`).
    *   `PDF_PATH`: Caminho para o arquivo PDF a ser ingerido (padrão: `./document.pdf`).

### Instalar Dependências Python
*   Navegue até o diretório raiz do projeto e instale as dependências Python:
    ```bash
    pip install -r requirements.txt
    ```

---

## Execução

Siga os passos abaixo para executar a aplicação:

### 1. Iniciar o Banco de Dados

Suba o container Docker do PostgreSQL com a extensão pgVector habilitada:

```bash
docker compose up -d
```

Aguarde alguns segundos para que o banco de dados esteja totalmente inicializado e a extensão `vector` seja criada. Você pode verificar o status dos contêineres com `docker ps`.

### 2. Ingestão do PDF
Informe o arquivo PDF que deseja ingerir editando a variável `PDF_PATH` no arquivo `.env`. O arquivo `document.pdf` é uma versão reduzida do PDF original para facilitar os testes, mas você pode substituir por qualquer outro PDF de sua escolha.

Execute o script de ingestão para ler o documento PDF, dividir em chunks, criar embeddings e armazená-los no PostgreSQL:

```bash
python src/ingest.py
```

Você verá mensagens de progresso no terminal.

### 3. Interação via CLI

Após a ingestão, inicie a interface de linha de comando para fazer perguntas sobre o conteúdo do PDF:

```bash
python src/chat.py

# Ou, se preferir, execute diretamente o módulo:
python -m src.chat
```

O CLI irá solicitar suas perguntas. Digite `sair` ou `exit` para encerrar.

Exemplo de interação:

```
Bem-vindo ao Chat de Busca Semântica!
Digite 'sair' ou 'exit' para encerrar.

Faça sua pergunta: Qual o faturamento da Empresa SuperTechIABrazil?
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

Faça sua pergunta: Quantos clientes temos em 2024?
PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

Faça sua pergunta: sair
Encerrando o chat. Até logo!
```

---

## Estrutura do Projeto

```
├── docker-compose.yml      # Configuração do Docker Compose para PostgreSQL
├── requirements.txt        # Dependências Python
├── .env.example            # Template para variáveis de ambiente
├── src/
│   ├── ingest.py           # Script para ingestão de PDF no banco de dados
│   ├── search.py           # Lógica principal para busca semântica e interação com LLM
│   └── chat.py             # Interface de linha de comando para interação com o usuário
├── document.pdf            # Arquivo PDF de exemplo para ingestão
└── README.md               # Este arquivo
```
