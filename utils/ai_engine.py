
import json
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# GEMINI CONFIGURATION
# --------------------------------------------------

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
# SHARED GEMINI JSON GENERATION FUNCTION
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
# 1. RESUME ANALYSIS
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
# 2. INTERVIEW QUESTION GENERATION
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
# 3. ANSWER EVALUATION
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
# 4. FOLLOW-UP QUESTION GENERATION
# --------------------------------------------------

FOLLOW_UP_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "should_ask": {
            "type": "BOOLEAN",
        },
        "follow_up_question": {
            "type": "STRING",
        },
        "reason": {
            "type": "STRING",
        },
    },
    "required": [
        "should_ask",
        "follow_up_question",
        "reason",
    ],
}


def generate_follow_up_question(
    question,
    answer,
    evaluation,
    resume_analysis=None,
    job_role="",
    difficulty="Medium",
    previous_follow_ups=None,
):
    """
    Decide whether a useful follow-up is needed and generate it.

    The caller controls the maximum number of follow-ups.
    """

    if not isinstance(question, str) or not question.strip():
        raise ValueError("Original interview question cannot be empty.")

    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("Candidate answer cannot be empty.")

    if not isinstance(evaluation, dict):
        raise ValueError("Answer evaluation must be a dictionary.")

    if not isinstance(previous_follow_ups, list):
        previous_follow_ups = []

    prompt = f"""
You are an experienced human interviewer conducting a live interview.

Your task is to decide whether the candidate's answer deserves
one useful follow-up question.

Original interview question:
{question}

Candidate's answer:
{answer}

Evaluation of the answer:
{json.dumps(evaluation, ensure_ascii=False)}

Candidate resume context:
{json.dumps(resume_analysis or {}, ensure_ascii=False)}

Job role:
{job_role}

Interview difficulty:
{difficulty}

Previously asked follow-up questions:
{json.dumps(previous_follow_ups, ensure_ascii=False)}

Instructions:

1. Decide whether a follow-up question would genuinely improve
   the interview.
2. Ask a follow-up if the answer is incomplete, unclear,
   too general, lacks an example, or needs deeper explanation.
3. You may also ask a deeper question when the candidate gives
   a strong answer and further exploration is useful.
4. The follow-up must be directly related to the original question
   and the candidate's actual answer.
5. Do not repeat the original question.
6. Do not repeat any previously asked follow-up question.
7. Match the selected interview difficulty.
8. Keep the question clear, natural, and conversational.
9. Do not introduce unrelated topics.
10. Do not assume facts that the candidate has not provided.
11. If the answer is already sufficiently complete and no useful
    follow-up exists, set should_ask to false and return an empty
    follow_up_question.
12. Keep the reason short and explain why the follow-up is useful,
    or why another question is unnecessary.

Return only the requested structured response.
"""

    result = _generate_json(prompt, FOLLOW_UP_SCHEMA)

    should_ask = result.get("should_ask")
    follow_up_question = result.get("follow_up_question")
    reason = result.get("reason")

    if not isinstance(should_ask, bool):
        raise RuntimeError(
            "Gemini returned an invalid follow-up decision."
        )

    if not isinstance(follow_up_question, str):
        raise RuntimeError(
            "Gemini returned an invalid follow-up question."
        )

    if not isinstance(reason, str):
        raise RuntimeError(
            "Gemini returned an invalid follow-up reason."
        )

    if should_ask and not follow_up_question.strip():
        raise RuntimeError(
            "Gemini decided to ask a follow-up but returned no question."
        )

    if not should_ask:
        result["follow_up_question"] = ""

    return result


# --------------------------------------------------
# 5. FINAL INTERVIEW REPORT
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
