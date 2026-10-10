from utils.vector_store import create_vector_store

documents = [
    "Python",
    "LangChain",
    "FastAPI",
    "Docker",
    "SQL"
]

db = create_vector_store(documents)

results = db.similarity_search(
    "REST API Development",
    k=3
)

print("=" * 50)

for doc in results:
    print(doc.page_content)

print("=" * 50)