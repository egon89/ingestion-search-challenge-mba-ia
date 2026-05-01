import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

# Configuration from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")
DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    if not all([GOOGLE_API_KEY, GOOGLE_EMBEDDING_MODEL, DATABASE_URL, PG_VECTOR_COLLECTION_NAME, PDF_PATH]):
        print("Error: One or more environment variables are not set. Please check your .env file.")
        exit(1)

    if not os.path.exists(PDF_PATH):
        print(f"Error: PDF file not found at {PDF_PATH}")
        exit(1)

    print(f"Loading PDF from {PDF_PATH}...")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from PDF.")

    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    print("Creating embeddings and ingesting into PGVector...")
    embeddings = GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL, google_api_key=GOOGLE_API_KEY)

    # Initialize PGVector, this will create the table if it doesn't exist
    # and ingest the documents.
    # pre_delete_collection=True ensures a fresh ingestion each time
    db = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        pre_delete_collection=True
    )
    print("Ingestion complete!")

if __name__ == "__main__":
    ingest_pdf()
