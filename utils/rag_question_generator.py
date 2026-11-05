
"""
RAG-powered interview question generation.

Connects the Hybrid RAG knowledge system to the existing
Gemini interview question generator.
"""

from utils.hybrid_rag import (
    build_hybrid_knowledge_store,
    retrieve_hybrid_context,
    get_knowledge_store_summary,
)

from utils.ai_engine import generate_questions


# ---------------------------------------------------------
# 1. BUILD A SEARCH QUERY
# ---------------------------------------------------------

def build_interview_search_query(
    resume_analysis,
    job_role,
    interview_type,
    difficulty,
):
    """
    Build a semantic search query using the candidate profile
    and selected interview configuration.
    """

    if not isinstance(resume_analysis, dict):
        raise ValueError("Resume analysis must be a dictionary.")

    skills = resume_analysis.get("technical_skills", [])
    languages = resume_analysis.get("programming_languages", [])
    projects = resume_analysis.get("projects", [])
    experience = resume_analysis.get("work_experience", [])

    def format_items(items):
        if not isinstance(items, list):
            return ""

        return ", ".join(
            str(item)
            for item in items
            if item
        )

    search_query = f"""
    Prepare interview questions for the job role: {job_role}.

    Interview type: {interview_type}.
    Difficulty: {difficulty}.

    Candidate technical skills:
    {format_items(skills)}

    Candidate programming languages:
    {format_items(languages)}

    Candidate projects:
    {format_items(projects)}

    Candidate work experience:
    {format_items(experience)}

    Find relevant candidate skills, project concepts,
    technical subjects, and interview knowledge.

    For behavioral interviews, prioritize communication,
    teamwork, problem-solving, and real-world experiences.

    For technical interviews, prioritize relevant
    programming, databases, algorithms, and other
    job-related technical concepts.

    For mixed interviews, include both technical and
    behavioral knowledge.
    """

    return search_query.strip()


# ---------------------------------------------------------
# 2. GENERATE QUESTIONS USING HYBRID RAG
# ---------------------------------------------------------

def generate_rag_questions(
    resume_text,
    resume_analysis,
    job_role,
    interview_type,
    difficulty,
    num_questions=5,
    knowledge_store=None,
    client=None,
):
    """
    Generate personalized questions using resume-based
    and general interview knowledge.

    If a knowledge store is supplied, it is reused.
    Otherwise, a new store is built.

    Returns:
        questions:
            Generated interview questions.

        knowledge_store:
            Temporary hybrid knowledge store.

        knowledge_summary:
            Counts of retrieved knowledge chunks.

        retrieved_context:
            Context supplied to Gemini.
    """

    # Validate inputs.
    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not isinstance(resume_analysis, dict):
        raise ValueError("Resume analysis must be a dictionary.")

    if not isinstance(job_role, str) or not job_role.strip():
        raise ValueError("Job role cannot be empty.")

    if interview_type not in ["Technical", "Behavioral", "Mixed"]:
        raise ValueError("Invalid interview type.")

    if difficulty not in ["Easy", "Medium", "Hard"]:
        raise ValueError("Invalid difficulty level.")

    if not isinstance(num_questions, int) or not 1 <= num_questions <= 15:
        raise ValueError(
            "Number of questions must be between 1 and 15."
        )

    # Build the knowledge store if it has not been supplied.
    if knowledge_store is None:

        knowledge_store = build_hybrid_knowledge_store(
            resume_text=resume_text,
            client=client,
        )

    if not isinstance(knowledge_store, list) or not knowledge_store:
        raise ValueError("Hybrid knowledge store is empty.")

    # Build a search query from the candidate profile.
    search_query = build_interview_search_query(
        resume_analysis=resume_analysis,
        job_role=job_role,
        interview_type=interview_type,
        difficulty=difficulty,
    )

    # Retrieve relevant information from both sources.
    retrieved = retrieve_hybrid_context(
        query=search_query,
        knowledge_store=knowledge_store,
        resume_top_k=3,
        general_top_k=4,
        client=client,
    )

    if not retrieved["resume_chunks"]:
        raise RuntimeError(
            "Unable to retrieve relevant candidate resume information."
        )

    if not retrieved["general_chunks"]:
        raise RuntimeError(
            "Unable to retrieve relevant general interview knowledge."
        )

    # Create a separate copy so the original resume analysis
    # stored in Streamlit Session State remains unchanged.
    enhanced_analysis = dict(resume_analysis)

    enhanced_analysis["retrieved_interview_knowledge"] = {
        "instructions": (
            "Use this retrieved information to create relevant "
            "interview questions. Candidate experience and skills "
            "must only be taken from the actual resume analysis. "
            "General knowledge must not be presented as candidate "
            "experience."
        ),
        "context": retrieved["context"],
    }

    # Generate questions using the existing Gemini engine.
    questions = generate_questions(
        resume_analysis=enhanced_analysis,
        job_role=job_role.strip(),
        interview_type=interview_type,
        difficulty=difficulty,
        num_questions=num_questions,
    )

    return {
        "questions": questions,
        "knowledge_store": knowledge_store,
        "knowledge_summary": get_knowledge_store_summary(
            knowledge_store
        ),
        "retrieved_context": retrieved,
    }
