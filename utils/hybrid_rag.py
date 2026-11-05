
"""
Hybrid RAG system.

Combines:
1. Candidate-specific resume knowledge.
2. General interview knowledge.

Candidate data is passed into the functions and is not
saved to a permanent database.
"""

from utils.rag_engine import (
    build_knowledge_store,
    retrieve_relevant_chunks,
)

from knowledge_base.interview_knowledge import (
    get_general_knowledge_documents,
)


# ---------------------------------------------------------
# 1. PREPARE BOTH KNOWLEDGE SOURCES
# ---------------------------------------------------------

def prepare_hybrid_documents(resume_text):
    """
    Combine the candidate's resume with general interview
    knowledge.

    The resume remains a separate document source.
    """

    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError(
            "A valid resume text is required to build hybrid knowledge."
        )

    documents = [
        {
            "text": resume_text.strip(),
            "source": "resume",
        }
    ]

    general_documents = get_general_knowledge_documents()

    documents.extend(general_documents)

    return documents


# ---------------------------------------------------------
# 2. BUILD THE HYBRID KNOWLEDGE STORE
# ---------------------------------------------------------

def build_hybrid_knowledge_store(resume_text, client=None):
    """
    Build an embedding-based knowledge store containing
    the candidate's resume and general interview knowledge.

    The returned store should be kept in Streamlit session
    state for the current candidate.
    """

    documents = prepare_hybrid_documents(resume_text)

    knowledge_store = build_knowledge_store(
        documents,
        client=client,
    )

    return knowledge_store


# ---------------------------------------------------------
# 3. RETRIEVE RESUME AND GENERAL KNOWLEDGE SEPARATELY
# ---------------------------------------------------------

def retrieve_hybrid_context(
    query,
    knowledge_store,
    resume_top_k=3,
    general_top_k=3,
    client=None,
):
    """
    Retrieve relevant information from both sources.

    Separate retrieval prevents one knowledge source
    from completely dominating the results.
    """

    if not isinstance(query, str) or not query.strip():
        raise ValueError("A valid search query is required.")

    if not isinstance(knowledge_store, list):
        raise ValueError("A valid knowledge store is required.")

    if not knowledge_store:
        raise ValueError("The hybrid knowledge store is empty.")

    # Retrieve candidate-specific information.
    resume_chunks = retrieve_relevant_chunks(
        query=query,
        knowledge_store=knowledge_store,
        top_k=resume_top_k,
        source_filter="resume",
        client=client,
    )

    # Retrieve general interview knowledge.
    general_chunks = retrieve_relevant_chunks(
        query=query,
        knowledge_store=knowledge_store,
        top_k=general_top_k,
        source_filter="general",
        client=client,
    )

    # Build readable context for Gemini.
    context_parts = []

    if resume_chunks:

        context_parts.append(
            "CANDIDATE RESUME INFORMATION:"
        )

        for index, chunk in enumerate(resume_chunks, start=1):

            context_parts.append(
                f"\nResume section {index}:\n"
                f"{chunk['text']}"
            )

    if general_chunks:

        context_parts.append(
            "\nGENERAL INTERVIEW KNOWLEDGE:"
        )

        for index, chunk in enumerate(general_chunks, start=1):

            context_parts.append(
                f"\nKnowledge section {index}:\n"
                f"{chunk['text']}"
            )

    combined_context = "\n".join(context_parts)

    return {
        "resume_chunks": resume_chunks,
        "general_chunks": general_chunks,
        "context": combined_context,
    }


# ---------------------------------------------------------
# 4. GET A SIMPLE KNOWLEDGE STORE SUMMARY
# ---------------------------------------------------------

def get_knowledge_store_summary(knowledge_store):
    """
    Return counts of resume and general knowledge chunks.
    """

    if not isinstance(knowledge_store, list):
        raise ValueError("Knowledge store must be a list.")

    resume_count = sum(
        1 for chunk in knowledge_store
        if chunk.get("source") == "resume"
    )

    general_count = sum(
        1 for chunk in knowledge_store
        if chunk.get("source") == "general"
    )

    return {
        "total_chunks": len(knowledge_store),
        "resume_chunks": resume_count,
        "general_chunks": general_count,
    }
