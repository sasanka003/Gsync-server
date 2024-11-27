import os
from dotenv import load_dotenv
from phi.agent import Agent
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.supabase import SupabaseVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from phi.knowledge.langchain import LangChainKnowledgeBase
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from supabase.client import Client, create_client

# ----- SETUP -----

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# ----- RAG: Agent -----

supabase: Client = create_client(supabase_url, supabase_key)
embeddings = OpenAIEmbeddings()
directory = "../documents"
loader = DirectoryLoader(path=directory, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
text_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.MARKDOWN, chunk_size=1000, chunk_overlap=100
)

def prepare_database():
    docs = loader.load()
    documents = text_splitter.split_documents(docs)
    SupabaseVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        client=supabase,
        table_name="documents",
        chunk_size=500
    )

vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="documents",
    query_name="match_documents",
)


rag_agent = Agent() 