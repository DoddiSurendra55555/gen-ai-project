import os
import json
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from bson import ObjectId
import motor.motor_asyncio
from google import genai
from google.genai import types
from dotenv import load_dotenv
import fitz  
import jwt

from auth import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM

load_dotenv()

# ==========================================
# 1. SCHEMAS & DATA MODELS
# ==========================================

class AnswerFeedback(BaseModel):
    score: int = Field(..., ge=1, le=10, description="Overall score out of 10")
    strengths: List[str] = Field(..., description="What the candidate explained accurately")
    areas_for_improvement: List[str] = Field(..., description="Missing details or misconceptions")
    ideal_answer_points: List[str] = Field(..., description="Key points an ideal answer should include")
    filler_words_count: int = Field(default=0, description="Estimated count of filler words")
    follow_up_question: Optional[str] = Field(None, description="A probing follow-up question if the answer was incomplete. Leave null if perfect.")

class QuestionRound(BaseModel):
    question_id: str = Field(default_factory=lambda: str(ObjectId()))
    question_text: str
    category: str = "Technical"
    user_transcript: Optional[str] = None
    feedback: Optional[AnswerFeedback] = None

class InterviewSession(BaseModel):
    session_id: Optional[str] = None
    user_id: str
    role_applied_for: str
    mode: str = "Technical"
    experience: str = "Mid-Level"
    difficulty: str = "Medium"
    duration: int = 5 # NEW: Duration in minutes
    generated_questions: List[str] = []
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = "in-progress"
    questions: List[QuestionRound] = []

class CreateSessionRequest(BaseModel):
    role_applied_for: str
    mode: str
    experience: str
    difficulty: str
    duration: int # NEW
    generated_questions: List[str]

class GenerateQuestionsRequest(BaseModel):
    role: str
    mode: str
    experience: str
    difficulty: str

class EvaluateRequest(BaseModel):
    session_id: str
    question_text: str
    transcript: str
    role_applied_for: str
    mode: str
    experience: str
    difficulty: str

class GeneratedQuestions(BaseModel):
    questions: List[str] = Field(..., description="A list of 4 custom interview questions based on the resume")

class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    name: str

# ==========================================
# 2. SERVER INITIALIZATION
# ==========================================

app = FastAPI(title="AI Placement Interview Coach")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI = os.getenv("MONGODB_URI", "")
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = mongo_client["placement_coach_db"]
sessions_collection = db["sessions"]
users_collection = db["users"]
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", ""))

def get_best_available_model(client):
    try:
        available_models = client.models.list()
        flash_models = [m.name.replace("models/", "") for m in available_models if "flash" in m.name and "omni" not in m.name]
        if flash_models:
            flash_models.sort(reverse=True)
            return flash_models[0]
    except: pass
    return "gemini-1.5-flash"

ACTIVE_MODEL = get_best_available_model(gemini_client)

# ==========================================
# 4. AUTHENTICATION & PROFILE ENDPOINTS
# ==========================================

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id: raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except: raise HTTPException(status_code=401, detail="Could not validate credentials")

@app.post("/signup", response_model=Token)
async def signup(user: UserCreate):
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email registered")
    user_doc = {
        "email": user.email, "name": user.name, "hashed_password": get_password_hash(user.password),
        "created_at": datetime.now(timezone.utc).isoformat(), "resume_text": None
    }
    res = await users_collection.insert_one(user_doc)
    return {"access_token": create_access_token({"sub": user.email, "user_id": str(res.inserted_id)}), "name": user.name}

@app.post("/login", response_model=Token)
async def login(user: UserLogin):
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_access_token({"sub": db_user["email"], "user_id": str(db_user["_id"])}), "name": db_user["name"]}

@app.get("/profile")
async def get_profile(user_id: str = Depends(get_current_user)):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user: raise HTTPException(status_code=404, detail="User not found")
    return {"name": user.get("name"), "email": user.get("email"), "has_resume": bool(user.get("resume_text"))}

@app.post("/profile/resume")
async def upload_profile_resume(resume: UploadFile = File(...), user_id: str = Depends(get_current_user)):
    try:
        pdf_bytes = await resume.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        resume_text = "".join(page.get_text() for page in doc)
        doc.close()
    except Exception as e: raise HTTPException(status_code=500, detail="PDF error")
    await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"resume_text": resume_text}})
    return {"message": "Resume saved", "has_resume": True}

# ==========================================
# 5. INTERVIEW & SESSION ENDPOINTS
# ==========================================

@app.post("/generate-questions", response_model=GeneratedQuestions)
async def generate_dynamic_questions(payload: GenerateQuestionsRequest, user_id: str = Depends(get_current_user)):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user or not user.get("resume_text"): raise HTTPException(status_code=400, detail="No resume")
    
    sys_inst = (f"You are a Hiring Manager interviewing a candidate for a {payload.role} role. "
                f"Experience: {payload.experience}. Mode: {payload.mode}. Difficulty: {payload.difficulty}. "
                "Review the resume and generate 4 questions. Return JSON matching GeneratedQuestions schema.")
    
    try:
        res = gemini_client.models.generate_content(
            model=ACTIVE_MODEL, contents=f"Resume:\n{user['resume_text']}",
            config=types.GenerateContentConfig(system_instruction=sys_inst, response_mime_type="application/json", response_schema=GeneratedQuestions, temperature=0.7)
        )
        return GeneratedQuestions(**json.loads(res.text))
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/sessions", response_model=InterviewSession)
async def create_session(payload: CreateSessionRequest, user_id: str = Depends(get_current_user)):
    new_session = InterviewSession(
        user_id=user_id, role_applied_for=payload.role_applied_for, mode=payload.mode,
        experience=payload.experience, difficulty=payload.difficulty, duration=payload.duration, 
        generated_questions=payload.generated_questions, questions=[]
    )
    result = await sessions_collection.insert_one(new_session.model_dump())
    session_id_str = str(result.inserted_id)
    await sessions_collection.update_one({"_id": result.inserted_id}, {"$set": {"session_id": session_id_str}})
    new_session.session_id = session_id_str
    return new_session

@app.get("/sessions/history")
async def get_session_history(user_id: str = Depends(get_current_user)):
    cursor = sessions_collection.find({"user_id": user_id}).sort("created_at", -1)
    sessions = await cursor.to_list(length=100)
    for s in sessions: s["_id"] = str(s["_id"])
    return {"history": sessions}

@app.get("/sessions/{session_id}")
async def get_single_session(session_id: str, user_id: str = Depends(get_current_user)):
    session = await sessions_collection.find_one({"session_id": session_id, "user_id": user_id})
    if not session: raise HTTPException(status_code=404, detail="Session not found")
    session["_id"] = str(session["_id"])
    return session

# NEW: Endpoint to forcefully complete a session when the timer runs out
@app.post("/sessions/{session_id}/complete")
async def complete_session(session_id: str, user_id: str = Depends(get_current_user)):
    result = await sessions_collection.update_one(
        {"session_id": session_id, "user_id": user_id},
        {"$set": {"status": "completed"}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session completed successfully"}

@app.post("/sessions/evaluate", response_model=AnswerFeedback)
async def evaluate_answer(payload: EvaluateRequest):
    sys_inst = (f"You are a Hiring Manager evaluating a {payload.experience} candidate for {payload.role_applied_for}. "
                f"Mode: {payload.mode}. Difficulty: {payload.difficulty}. "
                "CRITICAL: If the answer is weak or difficulty is Hard, provide a `follow_up_question` to probe deeper. "
                "Return JSON matching AnswerFeedback schema.")
    try:
        res = gemini_client.models.generate_content(
            model=ACTIVE_MODEL, contents=f'Question: "{payload.question_text}"\nResponse: "{payload.transcript}"',
            config=types.GenerateContentConfig(system_instruction=sys_inst, response_mime_type="application/json", response_schema=AnswerFeedback, temperature=0.2)
        )
        feedback = AnswerFeedback(**json.loads(res.text))
        round_entry = QuestionRound(question_text=payload.question_text, user_transcript=payload.transcript, feedback=feedback)

        update_query = {"$push": {"questions": round_entry.model_dump()}}
        if feedback.follow_up_question:
            update_query["$push"]["generated_questions"] = f"Follow-up: {feedback.follow_up_question}"

        await sessions_collection.update_one({"session_id": payload.session_id}, update_query)
        
        session = await sessions_collection.find_one({"session_id": payload.session_id})
        if len(session.get("questions", [])) >= len(session.get("generated_questions", [])):
            await sessions_collection.update_one({"session_id": payload.session_id}, {"$set": {"status": "completed"}})
            
        return feedback
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))