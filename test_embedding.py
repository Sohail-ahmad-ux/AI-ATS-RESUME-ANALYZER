from utils.vector_store import create_vector_store

docs = [
    "Python is a programming language.",
    "LangChain helps build AI applications.",
    "Groq provides fast inference."
]

db = create_vector_store(docs)

results = db.similarity_search("What is LangChain?")

print(results[0].page_content)