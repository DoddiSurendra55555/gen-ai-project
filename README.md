# AI Interview Coach

An AI-powered interview preparation platform that helps students and job seekers improve their interview skills through resume analysis, personalized mock interviews, voice-based interaction, and AI-generated performance feedback.

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

Hybrid Retrieval-Augmented Generation (Hybrid RAG) combines information from multiple knowledge sources before providing relevant context to a Large Language Model (LLM).

In this project, two knowledge sources are used:

1. **Candidate Resume:** Contains information such as skills, education, projects, experience, and technical knowledge.
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
                  RESUME DOCUMENT
                        |
                        |
                        v
            GENERAL INTERVIEW KNOWLEDGE
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
              +---------+---------+
              |                   |
              v                   v
       RESUME RETRIEVAL     GENERAL RETRIEVAL
              |                   |
              +---------+---------+
                        |
                        v
                 RETRIEVED CONTEXT
                        |
              +---------+---------+
              |                   |
              v                   v
       QUESTION GENERATION   ANSWER EVALUATION
              |                   |
              v                   v
       PERSONALIZED           AI FEEDBACK
        QUESTIONS              AND SCORES
              |                   |
              +---------+---------+
                        |
                        v
                 INTERVIEW RESULTS
```

### How Hybrid RAG Works

**Step 1: Collect knowledge sources**

The system collects the candidate's extracted resume text and general interview knowledge documents.

The general knowledge base contains 15 interview-related topics:

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

These vectors represent the semantic meaning of the text and allow the system to compare the