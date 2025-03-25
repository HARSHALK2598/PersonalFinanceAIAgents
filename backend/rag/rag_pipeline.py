from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.schema import Document
import yaml

with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

embedding_model = OpenAIEmbeddings()
llm = OpenAI(temperature=0.3, openai_api_key=config["openai_api_key"])

documents = [
    Document(page_content="Investing in bonds is suitable for short-term low-risk goals."),
    Document(page_content="Tech sector has high growth but also high volatility."),
    Document(page_content="For retirement in 20 years, a mix of stocks and ETFs is recommended."),
]

vector_store = FAISS.from_documents(documents, embedding_model)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
rag_chain = RetrievalQA(combine_documents_chain=llm, retriever=retriever)
