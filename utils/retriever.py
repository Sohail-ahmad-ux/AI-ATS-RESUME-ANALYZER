from utils.vector_store import create_vector_store


def create_retriever(chunks):
    """
    Create a retriever from resume chunks.
    """

    vector_db = create_vector_store(chunks)

    retriever = vector_db.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever