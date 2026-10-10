from utils.pdf_loader import PDFLoader
from utils.text_splitter import split_resume
from utils.retriever import create_retriever

from rag import create_rag_chain

text = PDFLoader.extract_text("Sohail_CV.pdf")

chunks = split_resume(text)

retriever = create_retriever(chunks)

rag_chain = create_rag_chain(retriever)

job_description = """
We are looking for an AI Engineer.

Required Skills

Python
LangChain
FastAPI
Docker
SQL
Deep Learning
"""

response = rag_chain.invoke(
    {
        "job_description": job_description
    }
)

print("=" * 70)

print(response)

print("=" * 70)