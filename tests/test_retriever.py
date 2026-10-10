from utils.pdf_loader import PDFLoader
from utils.text_splitter import split_resume
from utils.retriever import create_retriever

text = PDFLoader.extract_text("Sohail_CV.pdf")

chunks = split_resume(text)

retriever = create_retriever(chunks)

query = "Does this candidate know LangChain?"

docs = retriever.invoke(query)

print("=" * 60)
print("Query:", query)
print("=" * 60)

for i, doc in enumerate(docs, start=1):
    print(f"\nResult {i}")
    print("-" * 30)
    print(doc.page_content)