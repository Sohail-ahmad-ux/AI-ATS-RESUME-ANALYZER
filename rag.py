from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from config import llm
from prompts.rag_prompt import RAG_PROMPT


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def create_rag_chain(retriever):
    """
    Create a RAG chain for ATS evaluation.
    """

    context_chain = (
        RunnableLambda(lambda x: x["job_description"])
        | retriever
        | RunnableLambda(format_docs)
    )

    chain = (
        {
            "context": context_chain,
            "job_description": RunnableLambda(
                lambda x: x["job_description"]
            ),
        }
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain