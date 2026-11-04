
import json
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


# Load API key from local .env or Streamlit Cloud secrets.
load_dotenv()

MODEL_NAME = "gemini-3.1-flash-lite"


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


API_KEY = _get_api_key()
client = genai.Client(api_key=API_KEY)


# --------------------------------------------------
# Shared Gemini JSON generation function
# --------------------------------------------------

def _generate_json(prompt, response_schema):
    """Generate and validate a JSON response from Gemini."""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": response_schema,
                "temperature": 0.3,
            },
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        result = json.loads(response.text)

        if not isinstance(result, dict):
            raise RuntimeError(
                "Gemini returned an unexpected response format."
            )

        return result

    except json.JSONDecodeError as error:
        raise RuntimeError(
            "Gemini returned invalid JSON. Please try again."
        ) from error

    except Exception as error:
        error_message = str(error)

        if "503" in error_message or "UNAVAILABLE" in error_message:
            message = (
                "Gemini is temporarily busy. "
                "Please wait and try again."
            )
        elif "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            message = (
                "Gemini API usage limit reached. "
                "Please try again later."
            )
        elif "401" in error_message or "403" in error_message:
            message = (
                "Gemini API authentication failed. "
                "Please check your API key."
            )
        elif isinstance(error, RuntimeError):
            raise
        else:
            message = (
                "An error occurred while communicating with Gemini. "
                "Please try again."
            )

        raise RuntimeError(message) from error


# --------------------------------------------------
# 1. Resume Analysis
# --------------------------------------------------

RESUME_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "name": {"type": "STRING"},
        "summary": {"type": "STRING"},
        "education": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
        "technical_skills": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
        "programming_languages": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
        "projects": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
        "work_experience": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
        "certifications": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
        "strengths": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
        "weaknesses": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
        "missing_skills": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
        "improvement_suggestions": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
    },
    "required": [
        "name",
        "summary",
        "education",
        "technical_skills",
        "programming_languages",
        "projects",
        "work_experience",
        "certifications",
        "strengths",
        "weaknesses",
        "missing_skills",
        "improvement_suggestions",
    ],
}


def analyze_resume(resume_text):
    """Analyze resume content using Gemini."""

    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    prompt = f"""
You are an experienced technical recruiter and resume reviewer.

Analyze the following resume carefully.

Instructions:
1. Extract only information supported by the resume.
2. Never invent qualifications, skills, projects, or experience.
3. Use an empty string if the candidate's name is unavailable.
4. Use empty arrays if a section is not present.
5. Identify strengths using evidence from the resume.
6. Identify weaknesses as areas where the resume could improve.
7. Suggest relevant skills the candidate could develop.
8. Separate programming languages from other technical skills.
9. Do not assume projects or leadership roles are paid employment.
10. Keep the summary concise and professional.
11. Do not include unnecessary personal contact information.

Resume content:

{resume_text}
"""

    return _generate_json(prompt, RESUME_SCHEMA)


# --------------------------------------------------
# 2. Interview Question Generation
# --------------------------------------------------

QUESTIONS_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "questions": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "question": {"type": "STRING"},
                    "category": {"type": "STRING"},
                    "expected_topics": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"},
                    },
                },
                "required": [
                    "question",
                    "category",
                    "expected_topics",
                ],
            },
        },
    },
    "required": ["questions"],
}


def generate_questions(
    resume_analysis,
    job_role,
    interview_type,
    difficulty,
    num_questions=5,
):
    """Generate personalized interview questions."""

    if not isinstance(resume_analysis, dict):
        raise ValueError("Resume analysis must be a dictionary.")

    if not isinstance(job_role, str) or not job_role.strip():
        raise ValueError("Job role cannot be empty.")

    if interview_type not in ["Technical", "Behavioral", "Mixed"]:
        raise ValueError("Invalid interview type.")

    if difficulty not in ["Easy", "Medium", "Hard"]:
        raise ValueError("Invalid difficulty level.")

    if not isinstance(num_questions, int) or not 1 <= num_questions <= 15:
        raise ValueError("Number of questions must be between 1 and 15.")

    prompt = f"""
You are an experienced interviewer.

Generate exactly {num_questions} interview questions.

Candidate resume analysis:
{json.dumps(resume_analysis, ensure_ascii=False)}

Job role: {job_role}
Interview type: {interview_type}
Difficulty: {difficulty}

Instructions:
- Personalize questions using the candidate's actual skills and projects.
- Match the requested difficulty.
- Technical interviews must test relevant technical knowledge.
- Behavioral interviews must test communication, teamwork,
  leadership, and problem-solving.
- Mixed interviews must include both types.
- Avoid duplicate questions.
- Include useful expected topics for evaluating each answer.
- Do not invent experience for the candidate.
"""

    result = _generate_json(prompt, QUESTIONS_SCHEMA)

    questions = result.get("questions")

    if not isinstance(questions, list) or len(questions) != num_questions:
        raise RuntimeError(
            "Gemini did not generate the requested number of questions."
        )

    return questions


# --------------------------------------------------
# 3. Answer Evaluation
# --------------------------------------------------

EVALUATION_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "score": {"type": "INTEGER"},
        "feedback": {"type": "STRING"},
        "strengths": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
        "improvements": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
        "ideal_answer": {"type": "STRING"},
    },
    "required": [
        "score",
        "feedback",
        "strengths",
        "improvements",
        "ideal_answer",
    ],
}


def evaluate_answer(question, answer, resume_analysis=None):
    """Evaluate a candidate's interview answer."""

    if not isinstance(question, str) or not question.strip():
        raise ValueError("Interview question cannot be empty.")

    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("Answer cannot be empty.")

    prompt = f"""
You are a fair and constructive interview evaluator.

Evaluate the candidate's answer.

Interview question:
{question}

Candidate answer:
{answer}

Candidate resume context:
{json.dumps(resume_analysis or {}, ensure_ascii=False)}

Instructions:
- Give a score from 0 to 100.
- Evaluate relevance, accuracy, clarity, and completeness.
- Do not reward unsupported claims.
- Be constructive and specific.
- Identify what the candidate did well.
- Explain how the answer can improve.
- Provide an example of a stronger answer.
- Do not penalize information that the question did not require.
"""

    result = _generate_json(prompt, EVALUATION_SCHEMA)

    score = result.get("score")

    if not isinstance(score, int) or not 0 <= score <= 100:
        raise RuntimeError("Gemini returned an invalid evaluation score.")

    return result


# --------------------------------------------------
# 4. Final Interview Report
# --------------------------------------------------

REPORT_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "overall_summary": {"type": "STRING"},
        "overall_score": {"type": "INTEGER"},
        "performance_level": {"type": "STRING"},
        "strengths": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
        "areas_for_improvement": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
        "recommendations": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
    },
    "required": [
        "overall_summary",
        "overall_score",
        "performance_level",
        "strengths",
        "areas_for_improvement",
        "recommendations",
    ],
}


def generate_final_report(
    evaluations,
    job_role,
    interview_type,
    difficulty,
):
    """Generate a final interview performance report."""

    if not isinstance(evaluations, list) or not evaluations:
        raise ValueError("At least one evaluation is required.")

    prompt = f"""
You are an experienced interview performance coach.

Create a final interview performance report.

Job role: {job_role}
Interview type: {interview_type}
Difficulty: {difficulty}

Interview evaluations:
{json.dumps(evaluations, ensure_ascii=False)}

Instructions:
- Calculate the overall score from the evaluation scores.
- Keep the overall score between 0 and 100.
- Summarize the candidate's performance.
- Identify recurring strengths.
- Identify important areas for improvement.
- Provide practical recommendations.
- Do not invent performance details.
- Keep feedback encouraging and professional.
"""

    result = _generate_json(prompt, REPORT_SCHEMA)

    score = result.get("overall_score")

    if not isinstance(score, int) or not 0 <= score <= 100:
        raise RuntimeError(
            "Gemini returned an invalid overall score."
        )

    return result
