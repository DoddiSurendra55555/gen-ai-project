# 🎯 AI Interview Coach

**Practice Better. Perform Confidently.**

AI Interview Coach is an AI-powered interview preparation platform that helps students and job seekers prepare for interviews using their own resumes. It analyzes uploaded resumes, generates personalized interview questions, evaluates answers, and provides a final performance report using Google's Gemini API.

## 📌 Project Information

| Detail | Information |
|---|---|
| Project Name | AI Interview Coach |
| Institution | Kalasalingam Academy of Research and Education |
| Project ID | PRJ011 |
| Team ID | T011 |
| Project Guide | Mr. SHIRWIN PRINCE I |
| Main Framework | Streamlit |
| Programming Language | Python |
| AI Model Provider | Google Gemini |

## ✨ Features

### 1. Resume Analysis
- Upload a resume in PDF format.
- Extract resume text using PyMuPDF.
- Validate PDF files and enforce a 5 MB upload limit.
- Analyze skills, education, experience, strengths, and improvement areas using Gemini.

### 2. Personalized Interview Setup
- Select your target job role.
- Choose an interview type:
  - Technical
  - Behavioral
  - Mixed
- Select difficulty:
  - Easy
  - Medium
  - Hard
- Generate between 1 and 15 personalized interview questions.

### 3. Mock Interview
- Answer generated questions one at a time.
- Submit answers for AI-powered evaluation.
- Receive a score out of 100.
- Get feedback, strengths, areas for improvement, and an example of a stronger answer.

### 4. Interview Results
- View individual answer scores.
- Check overall interview performance.
- Visualize results using Plotly charts.
- Receive AI-generated final feedback and recommendations.
- Download the interview report in JSON format.

### 5. Session Management
- Store interview information temporarily using Streamlit Session State.
- Clear application data using the Clear All option.
- No project database is required.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application framework and user interface |
| Google Gemini API | Resume analysis, question generation, and answer evaluation |
| google-genai | Gemini API integration |
| PyMuPDF | PDF text extraction |
| Plotly | Performance charts and visualizations |
| python-dotenv | Local environment variable management |
| pytest | Automated testing |

## 📁 Project Structure

```text
AI-Interview-Coach/
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
│   └── helpers.py
│
├── tests/
│   ├── test_resume_parser.py
│   └── test_helpers.py
│
├── .streamlit/
│   └── config.toml
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

Install the following before running the application:

- Python 3.10 or later
- pip (Python package installer)
- Google Gemini API key
- Visual Studio Code (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-interview-coach.git
```

Navigate into the project directory:

```bash
cd ai-interview-coach
```

### Step 2: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 3: Configure the Gemini API Key

Create a `.env` file in the project root directory.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get an API key from:

https://aistudio.google.com/apikey

**Important:** Never upload your actual `.env` file or API key to GitHub.

### Step 4: Run the Application

Execute:

```bash
python -m streamlit run app.py
```

Open the local application in your browser:

http://localhost:8501

## 🚀 Application Workflow

1. Open the AI Interview Coach homepage.
2. Navigate to Resume Analysis.
3. Upload your PDF resume.
4. Click Analyze My Resume.
5. Review the AI-generated resume analysis.
6. Open Interview Setup.
7. Select your job role, interview type, difficulty, and number of questions.
8. Generate personalized interview questions.
9. Start the Mock Interview.
10. Submit answers to each question.
11. Receive AI-generated evaluation and feedback.
12. Open Interview Results to view your performance report.
13. Download your report as a JSON file.

## 🧪 Testing

The project uses pytest for automated testing.

Run all tests:

```bash
python -m pytest tests -v
```

Check Python syntax:

```bash
python -m compileall -q app.py pages utils tests
```

Check installed dependencies:

```bash
python -m pip check
```

The resume parser tests cover:

- Valid PDF text extraction.
- Empty PDF upload.
- Invalid PDF file.
- PDF files exceeding the 5 MB limit.
- PDF files without readable selectable text.

## 🔒 Privacy and Data Handling

- Resume and interview data are maintained temporarily using Streamlit Session State.
- The project does not use a database for permanent storage.
- Users can clear temporary application data using Clear All.
- Resume content and interview answers may be sent to Google's Gemini API when AI features are used.
- The Gemini API key must be kept private and must not be committed to a public repository.

**Note:** Scanned PDFs containing only images are not currently supported because OCR functionality has not been implemented.

## ☁️ Deployment

The application can be deployed using Streamlit Community Cloud.

1. Push the project source code to a GitHub repository.
2. Visit https://share.streamlit.io/
3. Sign in using GitHub.
4. Select Create app.
5. Choose the project repository and `main` branch.
6. Set the main file path to `app.py`.
7. Add the Gemini API key under the application's Secrets settings.
8. Deploy the application.

For hosted deployment, configure the application to read the Gemini API key from Streamlit secrets as well as the local environment.

Example Streamlit secret:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

Do not commit real API credentials to GitHub.

## 🔮 Future Enhancements

- Integrate browser-based speech recognition and speech synthesis into the main mock interview workflow.
- Add OCR support for scanned PDF resumes.
- Add PDF export for final interview reports.
- Improve answer evaluation with more detailed communication and technical scoring.
- Add optional interview history and user accounts.
- Support additional languages for interview practice.

## 👨‍💻 Contributors

Project team members:

- G. Naga Mithra Reddy
- Vinukonda Reshma
- C. Lahari
- D. Surendra
- P. Kavitha

## 📄 License

This project was developed for academic purposes at Kalasalingam Academy of Research and Education.

---

**AI Interview Coach — Practice Better. Perform Confidently.**