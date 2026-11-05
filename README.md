# AI Interview Coach

An AI-powered mock interview platform that helps candidates prepare for technical, HR, and behavioral interviews using personalized questions, voice-based interaction, and intelligent feedback.

The application uses **Google Gemini and Hybrid Retrieval-Augmented Generation (Hybrid RAG)** to generate resume-based interview questions and evaluate candidate answers using relevant information from both the candidate's resume and a general interview knowledge base.

## Features

### 1. Resume Analysis
- Upload a PDF resume.
- Extract resume text using PyMuPDF.
- Analyze skills, education, projects, experience, and other relevant details using Google Gemini.
- Use resume information to personalize interview preparation.

### 2. Personalized Interview Setup
- Select a job role.
- Choose the interview type.
- Select the difficulty level.
- Generate interview questions using Hybrid RAG.
- Receive questions based on the candidate's resume and relevant interview knowledge.

### 3. Voice-Based Mock Interview
- Listen to interview questions using browser text-to-speech.
- Answer using the browser microphone.
- Convert spoken responses into editable text using browser speech recognition.
- Submit typed or spoken answers for evaluation.

### 4. Hybrid RAG-Based Question Generation
- Retrieve relevant information from the candidate's resume.
- Retrieve relevant information from the general interview knowledge base.
- Combine the retrieved information into context for Gemini.
- Generate personalized and relevant interview questions.

### 5. Hybrid RAG-Based Answer Evaluation
- Evaluate answers using relevant resume information and general interview knowledge.
- Assess relevance, technical accuracy, clarity, and completeness.
- Generate scores, feedback, strengths, improvements, and example stronger answers.
- Apply the same RAG-based evaluation to follow-up answers.

### 6. Adaptive Follow-Up Questions
- Generate follow-up questions based on previous answers and evaluations.
- Explore the candidate's understanding in greater depth.
- Support up to two follow-up questions per main interview question.

### 7. Interview Results
- Display individual answer scores.
- Show strengths and areas for improvement.
- Display example stronger answers.
- Include follow-up discussion evaluations.
- Generate a final interview performance report.
- Visualize performance using Plotly.
- Download interview results as JSON.

---

## Hybrid RAG Architecture

### What is Hybrid RAG?

Hybrid Retrieval-Augmented Generation (Hybrid RAG) is an approach that combines information from multiple knowledge sources before sending relevant context to a Large Language Model (LLM).

In this project, two knowledge sources are used:

1. **Candidate Resume:** Contains personal information such as skills, education, projects, experience, and technical knowledge.
2. **General Interview Knowledge Base:** Contains general technical, programming, software engineering, behavioral, and HR interview knowledge.

The system retrieves relevant information from both sources and combines it to provide Gemini with context for generating personalized questions and evaluating answers.

### Architecture Overview

```text
                 CANDIDATE RESUME
                        |
                        v
                 PDF TEXT EXTRACTION
                        |
                        v
                 RESUME DOCUMENTS
                        |
                        |
                        v
GENERAL INTERVIEW KNOWLEDGE BASE
                        |
                        v
                GENERAL DOCUMENTS
                        |
                        |
                        v
              DOCUMENT PREPARATION
                        |
                        v
                 TEXT CHUNKING
                        |
                        v
              GEMINI EMBEDDINGS
                        |
                        v
             HYBRID KNOWLEDGE STORE
                        |
             +----------+----------+
             |                     |
             v                     v
       RESUME RETRIEVAL      GENERAL RETRIEVAL
             |                     |
             +----------+----------+
                        |
                        v
                RETRIEVED CONTEXT
                        |
             +----------+----------+
             |                     |
             v                     v
      QUESTION GENERATION    ANSWER EVALUATION
             |                     |
             v                     v
       PERSONALIZED           AI FEEDBACK
       QUESTIONS              AND SCORES
             |                     |
             +----------+----------+
                        |
                        v
                INTERVIEW RESULTS
```

### How Hybrid RAG Works

**Step 1: Collect knowledge sources**

The system collects the candidate's extracted resume text and general interview knowledge documents.

The general knowledge base contains 15 interview-related topics, including:

- Programming Fundamentals
- Data Structures and Algorithms
- Python Programming
- Databases and SQL
- Machine Learning and Artificial Intelligence
- Deep Learning and Generative AI
- Web Development
- Cloud Computing and Deployment
- Software Engineering
- Software Testing and Debugging
- Cybersecurity Fundamentals
- Project Explanation
- Behavioral Interview and STAR Method
- HR Interview and Communication
- Problem Solving and Communication

**Step 2: Document preparation and chunking**

The collected documents are prepared and divided into smaller text chunks.

Chunking allows the retrieval system to identify relevant sections instead of processing entire documents for every query.

Each chunk retains its source information, such as whether it comes from the candidate's resume or the general knowledge base.

**Step 3: Generate embeddings**

The project uses Google's `gemini-embedding-001` embedding model.

Text chunks are converted into numerical vector representations with a configured embedding dimension of 768.

These vectors represent the semantic meaning of the text and allow the system to compare the relevance of different chunks.

**Step 4: Build the hybrid knowledge store**

The generated embeddings and their associated text and metadata are organized into a knowledge store.

The store contains both:

- Resume-specific knowledge.
- General interview knowledge.

The knowledge store is maintained in the Streamlit session rather than permanently saving candidate-specific vector data.

**Step 5: Retrieve relevant information**

When a question needs to be generated or an answer needs to be evaluated, the system creates a retrieval query.

It retrieves relevant chunks separately from:

- The candidate's resume.
- The general interview knowledge base.

Cosine similarity is used to measure the semantic similarity between the query embedding and stored document embeddings.

The most relevant chunks from both sources are selected and combined into a single context.

**Step 6: Generate personalized questions**

The retrieved context is provided to Google Gemini along with the candidate's resume analysis and interview settings.

Gemini uses this information to generate interview questions relevant to the candidate's background and selected job role.

**Step 7: Evaluate candidate answers**

When the candidate submits an answer, the system retrieves relevant resume and general knowledge chunks again.

Gemini receives the interview question, candidate answer, resume analysis, expected topics, and retrieved Hybrid RAG context.

It generates an evaluation containing:

- Score (0–100).
- Feedback.
- Strengths.
- Areas for improvement.
- Example of a stronger answer.

The same Hybrid RAG evaluation process is used for main interview answers and follow-up answers.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application framework |
| Google Gemini API | AI question generation and answer evaluation |
| `gemini-embedding-001` | Text embedding generation |
| PyMuPDF | PDF resume text extraction |
| NumPy / Python vector operations | Numerical similarity calculations |
| Cosine Similarity | Semantic retrieval |
| Plotly | Interview performance visualization |
| Browser Web Speech API | Speech recognition and text-to-speech |
| JSON | Interview result export and data handling |
| Pytest | Application testing |

## Project Structure

```text
AI Interview Coach/
│
├── app.py
│
├── pages/
│   ├── 1_Resume_Analysis.py
│   ├── 2_Interview_Setup.py
│   ├── 3_Mock_Interview.py
│   └── 4_Interview_Results.py
│
├── utils/
│   ├── ai_engine.py
│   ├── resume_parser.py
│   ├── helpers.py
│   ├── browser_storage.py
│   ├── browser_voice.py
│   ├── voice_engine.py
│   ├── rag_engine.py
│   ├── hybrid_rag.py
│   ├── rag_question_generator.py
│   └── rag_evaluator.py
│
├── knowledge_base/
│   └── interview_knowledge.py
│
├── tests/
│   ├── test_resume_parser.py
│   └── test_helpers.py
│
├── browser_storage_component/
│   └── index.html
│
├── browser_voice_component/
│   └── index.html
│
├── .streamlit/
│   └── config.toml
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.10 or later.
- Google Gemini API key.
- Git.
- A modern web browser with microphone support.

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project directory:

```bash
cd "AI Interview Coach"
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure the Gemini API key

Create a `.env` file in the project's root directory using `.env.example` as a reference.

Add your Google Gemini API key using the variable name expected by the application.

**Important:** Never upload `.env` or expose your API key on GitHub.

### 4. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

---

## Application Workflow

1. Upload a candidate resume.
2. Extract and analyze the resume.
3. Select the desired job role, interview type, and difficulty.
4. Generate personalized questions using Hybrid RAG.
5. Start the mock interview.
6. Answer questions using voice or text.
7. Retrieve relevant resume and general knowledge for answer evaluation.
8. Receive AI-generated scores and feedback.
9. Answer adaptive follow-up questions.
10. View and download the final interview report.

## Testing

Run the automated tests using:

```bash
python -m pytest tests -v
```

Check Python syntax for the RAG modules:

```bash
python -m py_compile utils/rag_engine.py utils/hybrid_rag.py utils/rag_question_generator.py utils/rag_evaluator.py
```

## Privacy and Data Handling

- Candidate resumes are processed for interview personalization.
- Resume-specific knowledge stores are maintained in Streamlit session state.
- The Hybrid RAG implementation does not use a permanent database for candidate-specific embeddings.
- Resume content and submitted answers are sent to Google Gemini for AI processing.
- The application does not provide permanent resume storage or user authentication by default.
- API keys should be stored in local environment variables or deployment secrets, never committed to source control.

## Current RAG Scope

Hybrid RAG is integrated into:

- Personalized interview question generation.
- Main interview answer evaluation.
- Follow-up answer evaluation.

Adaptive follow-up question generation and final report generation continue to use the existing Gemini-based AI functions.

## Future Enhancements

- Expand the general interview knowledge base.
- Add support for additional document formats.
- Improve retrieval ranking and evaluation.
- Add more interview domains and specialized question collections.
- Introduce persistent user accounts and interview history.
- Add advanced analytics for interview performance.

## Conclusion

The AI Interview Coach combines conversational AI, voice-based interaction, resume analysis, and Hybrid Retrieval-Augmented Generation to provide a personalized interview preparation experience.

By combining candidate-specific resume information with general interview knowledge, the system provides more relevant interview questions and context-aware answer evaluations than a basic prompt-only interview system.
