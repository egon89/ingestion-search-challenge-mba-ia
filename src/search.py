import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Configuration from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL")
DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")

# Check for essential environment variables
if not all([GOOGLE_API_KEY, GOOGLE_EMBEDDING_MODEL, GOOGLE_MODEL, DATABASE_URL, PG_VECTOR_COLLECTION_NAME]):
    print("Error: One or more essential environment variables for search.py are not set. Please check your .env file.")
    exit(1)

# Initialize components (global for efficiency if multiple calls)
embeddings = GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL, google_api_key=GOOGLE_API_KEY)
db = PGVector(
    collection_name=PG_VECTOR_COLLECTION_NAME,
    connection=DATABASE_URL,
    embeddings=embeddings
)
retriever = db.as_retriever(search_kwargs={"k": 10})
llm = ChatGoogleGenerativeAI(model=GOOGLE_MODEL, google_api_key=GOOGLE_API_KEY)

# Define the prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", """
CONTEXT:
{context}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."
        """),
        ("user", """
PERGUNTA DO USUÁRIO:
{question}

RESPONDA A 'PERGUNTA DO USUÁRIO'
         """),
    ]
)

# Create a LangChain chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt_template
    | llm
    | StrOutputParser()
)

def get_answer(query: str) -> str:
    """
    Searches the vector database for relevant documents and generates an answer
    using the LLM based on the retrieved context.
    """
    print(f"Searching for relevant documents for query: '{query}'...")
    # The rag_chain handles retrieval, prompt construction, and LLM invocation
    response = rag_chain.invoke(query)
    return response

if __name__ == "__main__":
    # Example usage (for testing purposes)
    # This part will not be executed when imported by chat.py
    test_query = "Qual o faturamento da Empresa SuperTechIABrazil?"
    answer = get_answer(test_query)
    print(f"PERGUNTA: {test_query}")
    print(f"RESPOSTA: {answer}")
