from utils.pdf_loader import PDFLoader
from utils.text_splitter import split_resume
from utils.retriever import create_retriever

from rag import create_rag_chain


def ats_agent(state):
    """
    Generate ATS report using RAG.
    """

    resume_text = PDFLoader.extract_text(
        state["resume_path"]
    )

    chunks = split_resume(resume_text)

    retriever = create_retriever(chunks)

    rag_chain = create_rag_chain(retriever)

    report = rag_chain.invoke(
        {
            "job_description": state["job_description"]
        }
    )

    state["resume_text"] = resume_text
    state["retrieved_context"] = ""
    state["ats_report"] = report

    return state