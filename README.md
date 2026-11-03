# AI-Powered Interview Coach 🎙️🤖

An intelligent, full-stack web application designed to simulate high-pressure, real-world technical and behavioral interviews. By ingesting a candidate's resume and leveraging the Google Gemini API, the system generates highly personalized questions, listens to spoken answers in real-time, and provides immediate, actionable feedback.

## ✨ Features
* **Resume-Tailored Questions:** Upload a PDF resume to generate custom interview questions based on your actual experience.
* **Voice-First Interaction:** Real-time Speech-to-Text (Web Speech API) transcription of your answers.
* **Adaptive Follow-Ups:** AI dynamically generates probing follow-up questions if your initial answer lacks technical depth.
* **Instant Scorecards:** Get evaluated out of 10, with identified strengths, areas for improvement, and filler-word detection.
* **Downloadable Reports:** Export your interview performance as a PDF.

## 🛠️ Tech Stack
* **Frontend:** React.js, Tailwind CSS, Vite
* **Backend:** Python, FastAPI, PyMuPDF (fitz), JWT Authentication
* **Database:** MongoDB Atlas (Motor Async Driver)
* **AI Engine:** Google Gemini 1.5 API (Structured Outputs)

## 🚀 Getting Started (Local Development)

### Prerequisites
* Node.js (v18+)
* Python (3.10+)
* MongoDB Atlas Cluster (Free Tier)

### 1. Clone the Repository
```bash
git clone [https://github.com/DoddiSurendra55555/gen-ai-project.git](https://github.com/DoddiSurendra55555/gen-ai-project.git)
cd gen-ai-project
