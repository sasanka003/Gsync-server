import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.openai import OpenAIChat
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

# def prepare_database():
#     directory = "../documents"
#     loader = DirectoryLoader(path=directory, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
#     text_splitter = RecursiveCharacterTextSplitter.from_language(
#         language=Language.MARKDOWN, chunk_size=1000, chunk_overlap=100
#     )
#     docs = loader.load()
#     documents = text_splitter.split_documents(docs)
#     SupabaseVectorStore.from_documents(
#         documents=documents,
#         embedding=embeddings,
#         client=supabase,
#         table_name="documents",
#         chunk_size=500
#     )

vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="documents",
    query_name="match_documents",
)

retriever = vector_store.as_retriever(search_kwargs={"k": 8})
knowledge_base = LangChainKnowledgeBase(retriever=retriever)

# ----- PROMPT: agent -----

introduction = """
You are a Srilankan agriculture reasearch assistant who is well versed in researching about the economic imapacts of various crops,
insights on right crops for the right place and some one who has deep expertise in prviding valuable insights related to agriculture.
"""
guidelines = [
    "You will search through the vector database and try to find all possible details relavant to the query",
    "If you cannot answer using existing say that your knowledge base has insufficient data.",
    "Stay truthful, while giving an answer is necessary, maintaining your reliability is essential in this field of study"
]

instructions =[
    "Analyze the retrieved documents from the database and identify the necessary data relavant to the user query.",
    "Reflect on all possible answers and determine the most appropriate answer that you will provide to the user.", 
    "You ,must make the answer as exhaustive as possible."
]


rag_agent = Agent(
    provider=OpenAIChat(temperature=0.1),
    name="Document search agent",
    introduction=introduction,
    knowledge_base=knowledge_base,
    add_context=True,
    instructions=instructions,
    guidelines=guidelines,
    expected_output="An exhaustive answer that can explain or clarify the user query, as long as it can be answered by using existing data"
) 

# result = rag_agent.run(message="Tell me about the best plants to grown in Colombo Srilanka")
# print(result)