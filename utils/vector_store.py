from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Local embedding model (free)
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


def create_vector_store(documents: list[str]) -> Chroma:
    """
    Create an in-memory Chroma vector database
    from a list of text documents.
    """

    vector_db = Chroma.from_texts(
        texts=documents,
        embedding=embedding_model,
    )

    return vector_db