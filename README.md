# AI Interview Coach

An AI-powered interview preparation platform that helps students and job seekers improve their interview skills through resume analysis, personalized mock interviews, voice-based interaction, and AI-generated performance feedback.

## Project Overview

AI Interview Coach uses Google's Gemini AI to analyze resumes, generate personalized interview questions, evaluate candidate answers, and create detailed interview performance reports.

The application is built using Python and Streamlit, with an interactive web interface.

## Features

### 1. Resume Analysis
- Upload a resume in PDF format.
- Extract resume text automatically.
- Analyze candidate information using Gemini AI.
- Identify technical skills, programming languages, education, projects, and work experience.
- Display strengths, weaknesses, missing skills, and improvement suggestions.

### 2. Interview Setup
- Select the desired job role.
- Choose the interview type:
  - Technical
  - Behavioral
  - Mixed
- Select the difficulty level:
  - Easy
  - Medium
  - Hard
- Generate personalized interview questions based on resume information.

### 3. Mock Interview
- Answer AI-generated interview questions.
- Listen to questions using browser text-to-speech.
- Speak answers using browser speech recognition.
- View and edit speech-to-text transcription.
- Submit answers for AI evaluation.
- Receive feedback and suggestions for improvement.

### 4. Interview Results
- View individual answer scores.
- Review strengths and areas for improvement.
- Receive an overall interview performance score.
- Generate a final AI-powered performance report.
- View performance charts.
- Download the interview report.

### 5. Session Management
- Maintain interview progress during the browser session.
- Recover supported session data after refreshing the browser.
- Clear interview data using the Clear All option.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application framework |
| Google Gemini API | AI-powered analysis and evaluation |
| PyMuPDF | PDF text extraction |
| Plotly | Interactive charts |
| HTML, CSS, JavaScript | Interface styling and browser components |
| Web Speech API | Speech recognition and text-to-speech |
| Pytest | Unit testing |

## Project Structure

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
│   ├── browser_storage.py
│   ├── browser_voice.py
│   ├── helpers.py
│   ├── resume_parser.py
│   └── voice_engine.py
│
├── browser_storage_component/
│   └── index.html
│
├── browser_voice_component/
│   └── index.html
│
├── documentation/
│   └── AI Interview Coach Documentation (1) (1).pdf
│
├── tests/
│   ├── test_helpers.py
│   └── test_resume_parser.py
│
├── .streamlit/
│   └── config.toml
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or later
- Google Gemini API key
- Internet connection
- Modern web browser (Google Chrome or Microsoft Edge recommended)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the Project Folder

```bash
cd YOUR_PROJECT_FOLDER
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API Key

Create a `.env` file in the project root directory.

Add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own Gemini API key.

**Important:** Never upload your `.env` file or expose your API key publicly.

### 5. Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## Google Gemini API

The project uses the Google Gemini API for:

- Resume analysis
- Personalized interview question generation
- Candidate answer evaluation
- Final interview performance reports

The configured model is:

`gemini-3.1-flash-lite`

A valid Gemini API key is required for AI-powered features.

## Running Tests

Run the unit tests using:

```bash
python -m pytest tests -v
```

## Deployment

The application can be deployed using **Streamlit Community Cloud**.

Deployment steps:

1. Push the project to a GitHub repository.
2. Log in to Streamlit Community Cloud.
3. Create a new application.
4. Select the GitHub repository and `app.py` as the main file.
5. Open the application's Advanced Settings and add the Gemini API key under Secrets.

Add this to the Streamlit Secrets configuration:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

6. Deploy the application.

Do not commit API keys or secret configuration files to GitHub.

## Privacy and Data Handling

- The application does not use a database or permanent user account storage.
- Interview information is maintained using Streamlit session state and browser session storage.
- Browser session storage is temporary and is not intended as permanent storage.
- Uploaded resume content and interview answers are sent to Google's Gemini API when AI features are used.
- Users should avoid uploading sensitive information they do not wish to share with the AI service.
- Users can use the Clear All option to clear application session data.

## Documentation

The detailed project documentation PDF is available in the repository:

`documentation/AI Interview Coach Documentation (1) (1).pdf`

## Future Enhancements

- Support for additional AI models.
- More interview categories and job roles.
- Advanced performance analytics.
- Additional resume formats.
- More detailed interview improvement recommendations.

## Author

**AI Interview Coach — College Project**

## License

This project is developed for educational and academic purposes.
