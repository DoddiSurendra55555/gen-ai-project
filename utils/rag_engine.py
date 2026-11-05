
import math
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

load_dotenv()

EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSIONS = 768

DEFAULT_CHUNK_SIZE = 900
DEFAULT_CHUNK_OVERLAP = 150

EMBEDDING_BATCH_SIZE = 50


# ---------------------------------------------------------
# GEMINI CLIENT
# ---------------------------------------------------------

def _get_api_key():
    """Get the Gemini API key from local environment or Streamlit secrets."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            api_key = None

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY was not found. "
            "Configure it in your .env file or Streamlit Cloud secrets."
        )

    return api_key


def _get_client():
    """Create a Gemini client when needed."""

    return genai.Client(api_key=_get_api_key())


# ---------------------------------------------------------
# 1. TEXT CHUNKING
# ---------------------------------------------------------

def chunk_text(
    text,
    chunk_size=DEFAULT_CHUNK_SIZE,
    overlap=DEFAULT_CHUNK_OVERLAP,
):
    """
    Divide text into smaller overlapping chunks.

    Overlapping chunks help preserve context between sections.

    Args:
        text: Source text.
        chunk_size: Maximum approximate chunk length in characters.
        overlap: Number of overlapping characters.

    Returns:
        A list of text chunks.
    """

    if not isinstance(text, str) or not text.strip():
        return []

    if not isinstance(chunk_size, int) or chunk_size < 100:
        raise ValueError("Chunk size must be at least 100 characters.")

    if not isinstance(overlap, int) or overlap < 0:
        raise ValueError("Overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size.")

    cleaned_text = " ".join(text.split())

    if len(cleaned_text) <= chunk_size:
        return [cleaned_text]

    chunks = []
    start = 0
    text_length = len(cleaned_text)

    while start < text_length:

        end = min(start + chunk_size, text_length)

        if end < text_length:
            boundary = cleaned_text.rfind(" ", start, end)

            if boundary > start + (chunk_size // 2):
                end = boundary

        chunk = cleaned_text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        next_start = end - overlap

        if next_start <= start:
            next_start = end

        start = next_start

    return chunks


# ---------------------------------------------------------
# 2. DOCUMENT PROCESSING
# ---------------------------------------------------------

def prepare_documents(documents):
    """
    Convert source documents into RAG chunks.

    Each document should contain:
        {
            "text": "...",
            "source": "resume" or "general"
        }

    Returns:
        A list of chunk dictionaries.
    """

    if not isinstance(documents, list):
        raise ValueError("Documents must be provided as a list.")

    prepared_chunks = []

    for document_index, document in enumerate(documents):

        if not isinstance(document, dict):
            continue

        document_text = document.get("text", "")
        source = document.get("source", "general")

        if not isinstance(document_text, str):
            continue

        if not document_text.strip():
            continue

        text_chunks = chunk_text(document_text)

        for chunk_index, chunk in enumerate(text_chunks):

            prepared_chunks.append({
                "text": chunk,
                "source": str(source),
                "document_index": document_index,
                "chunk_index": chunk_index,
            })

    return prepared_chunks


# ---------------------------------------------------------
# 3. GENERATE EMBEDDINGS
# ---------------------------------------------------------

def generate_embeddings(
    texts,
    task_type="RETRIEVAL_DOCUMENT",
    client=None,
):
    """
    Generate Gemini embeddings for a list of text strings.

    Embeddings are returned as ordinary Python lists so they
    can be stored in Streamlit session state.
    """

    if not isinstance(texts, list):
        raise ValueError("Texts must be provided as a list.")

    if not texts:
        return []

    if task_type not in [
        "RETRIEVAL_DOCUMENT",
        "RETRIEVAL_QUERY",
    ]:
        raise ValueError("Unsupported embedding task type.")

    if any(
        not isinstance(text, str) or not text.strip()
        for text in texts
    ):
        raise ValueError("Every embedding input must contain text.")

    if client is None:
        client = _get_client()

    all_embeddings = []

    try:

        for start in range(0, len(texts), EMBEDDING_BATCH_SIZE):

            batch = texts[
                start:start + EMBEDDING_BATCH_SIZE
            ]

            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=batch,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=EMBEDDING_DIMENSIONS,
                ),
            )

            if not response.embeddings:
                raise RuntimeError(
                    "Gemini returned empty embeddings."
                )

            if len(response.embeddings) != len(batch):
                raise RuntimeError(
                    "Gemini returned an unexpected number of embeddings."
                )

            for embedding in response.embeddings:

                values = list(embedding.values)

                if not values:
                    raise RuntimeError(
                        "Gemini returned an empty embedding vector."
                    )

                all_embeddings.append(values)

        return all_embeddings

    except Exception as error:

        if isinstance(error, RuntimeError):
            raise

        error_message = str(error)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            message = (
                "Gemini embedding API usage limit reached. "
                "Please try again later."
            )

        elif "401" in error_message or "403" in error_message:
            message = (
                "Gemini embedding authentication failed. "
                "Please check your API key."
            )

        else:
            message = (
                "Unable to generate text embeddings. "
                "Please check your Gemini API connection."
            )

        raise RuntimeError(message) from error


# ---------------------------------------------------------
# 4. BUILD KNOWLEDGE STORE
# ---------------------------------------------------------

def build_knowledge_store(documents, client=None):
    """
    Prepare documents and create their embeddings.

    The returned store is an ordinary Python list. It can be
    kept in Streamlit session state instead of being saved
    permanently to a database.
    """

    chunks = prepare_documents(documents)

    if not chunks:
        raise ValueError(
            "No readable text was found in the supplied documents."
        )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(
        texts,
        task_type="RETRIEVAL_DOCUMENT",
        client=client,
    )

    knowledge_store = []

    for chunk, embedding in zip(chunks, embeddings):

        knowledge_store.append({
            **chunk,
            "embedding": embedding,
        })

    return knowledge_store


# ---------------------------------------------------------
# 5. COSINE SIMILARITY
# ---------------------------------------------------------

def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two vectors.

    A higher score indicates greater semantic similarity.
    """

    if not vector_a or not vector_b:
        return 0.0

    if len(vector_a) != len(vector_b):
        raise ValueError(
            "Embedding vectors must have matching dimensions."
        )

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(value * value for value in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(value * value for value in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


# ---------------------------------------------------------
# 6. RETRIEVE RELEVANT CHUNKS
# ---------------------------------------------------------

def retrieve_relevant_chunks(
    query,
    knowledge_store,
    top_k=5,
    source_filter=None,
    client=None,
):
    """
    Find the most relevant knowledge chunks for a query.

    Args:
        query: User question or search text.
        knowledge_store: Store returned by build_knowledge_store.
        top_k: Maximum number of chunks to return.
        source_filter: Optional source name such as "resume".
        client: Optional Gemini client for testing.

    Returns:
        Relevant chunks sorted by similarity score.
    """

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if not isinstance(knowledge_store, list):
        raise ValueError("Knowledge store must be a list.")

    if not isinstance(top_k, int) or top_k < 1:
        raise ValueError("top_k must be a positive integer.")

    if not knowledge_store:
        return []

    matching_chunks = []

    for chunk in knowledge_store:

        if not isinstance(chunk, dict):
            continue

        if source_filter is not None:
            if chunk.get("source") != source_filter:
                continue

        if (
            isinstance(chunk.get("embedding"), list)
            and chunk.get("text")
        ):
            matching_chunks.append(chunk)

    if not matching_chunks:
        return []

    query_embeddings = generate_embeddings(
        [query],
        task_type="RETRIEVAL_QUERY",
        client=client,
    )

    query_embedding = query_embeddings[0]

    scored_chunks = []

    for chunk in matching_chunks:

        score = cosine_similarity(
            query_embedding,
            chunk["embedding"],
        )

        scored_chunk = {
            **chunk,
            "similarity": score,
        }

        scored_chunks.append(scored_chunk)

    scored_chunks.sort(
        key=lambda item: item["similarity"],
        reverse=True,
    )

    return scored_chunks[:top_k]
