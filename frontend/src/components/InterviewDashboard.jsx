import { useState, useEffect, useRef, useCallback } from 'react';
import AudioRecorder from './AudioRecorder';
import FeedbackCard from './FeedbackCard';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

export default function InterviewDashboard({ token, resumeSessionId, onComplete }) {
  const [role, setRole] = useState('Full Stack Software Engineer');
  const [experience, setExperience] = useState('Mid-Level (1-3 years)');
  const [mode, setMode] = useState('Technical Deep-Dive');
  const [difficulty, setDifficulty] = useState('Medium (Standard)');
  const [duration, setDuration] = useState(5); 
  
  const [interviewQuestions, setInterviewQuestions] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [sessionFeedback, setSessionFeedback] = useState([]); 
  const [isComplete, setIsComplete] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isDownloading, setIsDownloading] = useState(false);
  const [endReason, setEndReason] = useState('completed');

  const [timeLeft, setTimeLeft] = useState(null);
  const reportRef = useRef(null);

  // Robust Text-to-Speech Handler
  const speakQuestion = (text) => {
    if (!text || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel(); // Clear any stuck audio in the browser
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
  };

  // Auto-trigger attempt when question changes
  useEffect(() => {
    if (sessionId && !isComplete && interviewQuestions[currentQuestionIndex]) {
      const timer = setTimeout(() => {
        speakQuestion(interviewQuestions[currentQuestionIndex]);
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [currentQuestionIndex, interviewQuestions, sessionId, isComplete]);

  useEffect(() => {
    if (resumeSessionId) {
      const loadSession = async () => {
        setLoading(true);
        try {
          const res = await fetch(`https://gen-ai-project-1-ldr9.onrender.com/sessions/${resumeSessionId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          if (!res.ok) throw new Error('Failed to load session');
          const data = await res.json();
          
          setRole(data.role_applied_for);
          setMode(data.mode);
          setExperience(data.experience);
          setDifficulty(data.difficulty);
          setDuration(data.duration || 5);
          setInterviewQuestions(data.generated_questions);
          setSessionId(data.session_id);
          
          const pastFeedback = data.questions.map(q => ({
            question: q.question_text,
            transcript: q.user_transcript,
            evaluation: q.feedback
          }));
          setSessionFeedback(pastFeedback);
          setCurrentQuestionIndex(data.questions.length);
          setIsComplete(data.status === 'completed');
          
          if (data.status !== 'completed') {
            setTimeLeft((data.duration || 5) * 60);
          }
        } catch (err) {
          console.error("Session resume error:", err);
          setError("Could not resume session. Please start a new one.");
        } finally {
          setLoading(false);
        }
      };
      loadSession();
    }
  }, [resumeSessionId, token]);

  const handleTimeUp = useCallback(async () => {
    setIsComplete(true);
    setEndReason('time_up');
    window.speechSynthesis.cancel(); 
    try {
      await fetch(`https://gen-ai-project-1-ldr9.onrender.com/sessions/${sessionId}/complete`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
    } catch (err) {
      console.error("Failed to mark session as complete", err);
    }
  }, [sessionId, token]);

  const handleEndInterviewEarly = async () => {
    if (!window.confirm("Are you sure you want to end the interview early?")) return;
    
    setIsComplete(true);
    setEndReason('manual');
    window.speechSynthesis.cancel(); 
    try {
      await fetch(`https://gen-ai-project-1-ldr9.onrender.com/sessions/${sessionId}/complete`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
    } catch (err) {
      console.error("Failed to mark session as complete", err);
    }
  };

  useEffect(() => {
    if (!sessionId || isComplete || timeLeft === null) return;

    if (timeLeft > 0) {
      const timerId = setInterval(() => setTimeLeft(prev => prev - 1), 1000);
      return () => clearInterval(timerId);
    }

    if (timeLeft === 0) {
      const timeoutId = setTimeout(() => {
        handleTimeUp();
      }, 0);
      return () => clearTimeout(timeoutId);
    }
  }, [sessionId, isComplete, timeLeft, handleTimeUp]);

  const formatTime = (seconds) => {
    if (seconds === null) return "00:00";
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  const startSession = async () => {
    setLoading(true);
    setError(null);
    try {
      const questionRes = await fetch('https://gen-ai-project-1-ldr9.onrender.com/generate-questions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ role, mode, experience, difficulty }) 
      });
      if (!questionRes.ok) throw new Error('Failed to generate questions. Did you upload a resume in your profile?');
      const questionData = await questionRes.json();
      
      const sessionRes = await fetch('https://gen-ai-project-1-ldr9.onrender.com/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ 
          role_applied_for: role, mode, experience, difficulty, 
          duration: parseInt(duration), generated_questions: questionData.questions 
        })
      });
      if (!sessionRes.ok) throw new Error('Failed to create session');
      const sessionData = await sessionRes.json();
      
      setInterviewQuestions(questionData.questions);
      setSessionId(sessionData.session_id);
      setCurrentQuestionIndex(0);
      setSessionFeedback([]);
      setIsComplete(false);
      setEndReason('completed');
      setTimeLeft(parseInt(duration) * 60); 
    } catch (err) { setError(err.message); } 
    finally { setLoading(false); }
  };

  const handleAnswerSubmit = async (transcript) => {
    if (!sessionId || timeLeft === 0) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('https://gen-ai-project-1-ldr9.onrender.com/sessions/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId, question_text: interviewQuestions[currentQuestionIndex],
          transcript, role_applied_for: role, mode, experience, difficulty
        })
      });
      if (!res.ok) throw new Error('Evaluation request failed');
      const feedbackData = await res.json();

      setSessionFeedback(prev => [...prev, { question: interviewQuestions[currentQuestionIndex], transcript, evaluation: feedbackData }]);

      if (feedbackData.follow_up_question) {
        setInterviewQuestions(prev => {
          const newQ = [...prev];
          newQ.splice(currentQuestionIndex + 1, 0, `Follow-up: ${feedbackData.follow_up_question}`);
          return newQ;
        });
        setCurrentQuestionIndex(prev => prev + 1);
      } else if (currentQuestionIndex < interviewQuestions.length - 1) {
        setCurrentQuestionIndex(prev => prev + 1);
      } else {
        setIsComplete(true);
        setEndReason('completed');
      }
    } catch (err) { setError(err.message); } 
    finally { setLoading(false); }
  };

  const generatePDF = async () => {
    setIsDownloading(true);
    try {
      const element = reportRef.current;
      const canvas = await html2canvas(element, { scale: 2, backgroundColor: '#ffffff', useCORS: true });
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`Interview_Scorecard_${role.replace(/\s+/g, '_')}.pdf`);
    } catch (err) {
      console.error("Failed to generate PDF", err);
    } finally {
      setIsDownloading(false);
    }
  };

  const answeredQuestions = sessionFeedback.length;
  const overallScore = answeredQuestions > 0 
    ? (sessionFeedback.reduce((acc, curr) => acc + curr.evaluation.score, 0) / answeredQuestions).toFixed(1)
    : 0;
  
  const aggregatedImprovements = [...new Set(sessionFeedback.flatMap(f => f.evaluation.areas_for_improvement))].slice(0, 5);
  const aggregatedTips = [...new Set(sessionFeedback.flatMap(f => f.evaluation.ideal_answer_points))].slice(0, 5);

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-fade-in">
      {!sessionId ? (
        <div className="p-8 md:p-10 bg-white border border-slate-200 rounded-3xl shadow-sm">
          <div className="border-b border-slate-100 pb-6 mb-8">
            <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">Interview Configurator</h2>
            <p className="text-slate-500 text-sm mt-2">Set your parameters. The AI will tailor the simulation based on your profile's resume.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="space-y-2 lg:col-span-2">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider">Target Role</label>
              <input type="text" value={role} onChange={(e) => setRole(e.target.value)} className="w-full px-4 py-3 bg-white border border-slate-300 rounded-xl text-slate-900 font-medium focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600 outline-none transition-shadow shadow-sm"/>
            </div>
            
            <div className="space-y-2">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider">Time Limit</label>
              <select value={duration} onChange={(e) => setDuration(Number(e.target.value))} className="w-full px-4 py-3 bg-indigo-50 border border-indigo-100 rounded-xl text-indigo-700 font-bold focus:ring-2 focus:ring-indigo-600 outline-none transition-shadow cursor-pointer">
                <option value={2}>2 Minutes (Quick)</option>
                <option value={5}>5 Minutes (Standard)</option>
                <option value={10}>10 Minutes (Deep Dive)</option>
                <option value={15}>15 Minutes (Extensive)</option>
              </select>
            </div>

            <div className="space-y-2">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider">Interview Mode</label>
              <select value={mode} onChange={(e) => setMode(e.target.value)} className="w-full px-4 py-3 bg-white border border-slate-300 rounded-xl text-slate-700 font-medium focus:ring-2 focus:ring-indigo-600 outline-none transition-shadow shadow-sm cursor-pointer">
                <option>Technical Deep-Dive</option>
                <option>HR & Behavioral (STAR)</option>
                <option>Mixed (Technical + HR)</option>
              </select>
            </div>

            <div className="space-y-2">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider">Experience Level</label>
              <select value={experience} onChange={(e) => setExperience(e.target.value)} className="w-full px-4 py-3 bg-white border border-slate-300 rounded-xl text-slate-700 font-medium focus:ring-2 focus:ring-indigo-600 outline-none transition-shadow shadow-sm cursor-pointer">
                <option>Fresher (0 years)</option>
                <option>Mid-Level (1-3 years)</option>
                <option>Senior (4+ years)</option>
              </select>
            </div>

            <div className="space-y-2">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider">AI Rigor (Difficulty)</label>
              <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)} className="w-full px-4 py-3 bg-white border border-slate-300 rounded-xl text-slate-700 font-medium focus:ring-2 focus:ring-indigo-600 outline-none transition-shadow shadow-sm cursor-pointer">
                <option>Easy (Encouraging)</option>
                <option>Medium (Standard)</option>
                <option>Hard (Stress Interview)</option>
              </select>
            </div>
          </div>

          {error && <div className="mt-6 p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-sm font-medium">{error}</div>}
          
          <div className="mt-10 pt-6 border-t border-slate-100 flex justify-end">
            <button onClick={startSession} disabled={loading} className="w-full md:w-auto px-8 py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-md shadow-indigo-200 disabled:opacity-50 transition-all flex items-center justify-center gap-2">
              {loading ? (
                <><span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span> Preparing Environment...</>
              ) : 'Start Interview Session →'}
            </button>
          </div>
        </div>
      ) : !isComplete ? (
        <div className="space-y-6">
          <div className="p-8 bg-white border border-slate-200 rounded-3xl shadow-sm">
            
            {/* Header / Timer */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-6 mb-6 gap-4">
              <div className="flex items-center gap-3">
                <span className="flex items-center gap-2 px-3 py-1 bg-slate-100 rounded-lg text-xs font-bold text-slate-600 uppercase tracking-wider">
                  <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
                  {mode} • {difficulty}
                </span>
              </div>
              
              <div className="flex items-center gap-3">
                <div className={`px-5 py-2 rounded-xl border ${timeLeft < 60 ? 'bg-rose-50 border-rose-200 text-rose-600 animate-pulse' : 'bg-white border-slate-200 text-slate-700'} font-mono font-bold tracking-widest flex items-center gap-2 shadow-sm`}>
                  ⏱ {formatTime(timeLeft)}
                </div>
                <button 
                  onClick={handleEndInterviewEarly}
                  className="px-4 py-2 text-xs font-bold text-rose-600 bg-white hover:bg-rose-50 border border-rose-200 rounded-xl transition-colors shadow-sm"
                >
                  End Early
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between mb-3">
              <div className="text-xs font-bold text-indigo-600 uppercase tracking-wider">
                Question {currentQuestionIndex + 1} of {interviewQuestions.length}
              </div>
              
              {/* Manual Read Aloud Button */}
              <button
                onClick={() => speakQuestion(interviewQuestions[currentQuestionIndex])}
                className="flex items-center gap-2 px-3 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-600 rounded-lg text-xs font-bold transition-colors border border-indigo-100"
                title="Read question aloud"
              >
                <span>🔊</span> Read Aloud
              </button>
            </div>

            <h3 className="text-2xl font-extrabold text-slate-900 leading-relaxed py-2 mb-8">
              {interviewQuestions[currentQuestionIndex]}
            </h3>
            
            <AudioRecorder key={currentQuestionIndex} onTranscriptComplete={handleAnswerSubmit} isEvaluating={loading} />
          </div>

          {error && <div className="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-sm font-medium">{error}</div>}
          
          {sessionFeedback.length > 0 && (
            <div className="mt-8 pt-8">
              <h4 className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-4 px-2">Previous Answers</h4>
              <div className="space-y-4">
                {sessionFeedback.map((f, i) => (
                  <div key={i} className="p-5 bg-white border border-slate-200 shadow-sm rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                      <p className="text-sm font-bold text-slate-800 mb-1">Q: {f.question}</p>
                      <p className="text-xs text-slate-500 italic line-clamp-1">"{f.transcript}"</p>
                    </div>
                    <div className="shrink-0 px-4 py-2 bg-slate-50 border border-slate-100 rounded-lg text-sm font-bold text-slate-700">
                      Score: {f.evaluation.score}/10
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-8 pb-12">
          
          <div className="flex justify-between items-center py-4">
            <button onClick={onComplete} className="px-6 py-2.5 bg-white hover:bg-slate-50 text-slate-700 font-bold rounded-xl border border-slate-200 shadow-sm transition-colors flex items-center gap-2">
              ← Back to Dashboard
            </button>
            <button 
              onClick={generatePDF} 
              disabled={isDownloading}
              className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-md shadow-indigo-200 transition-colors flex items-center gap-2 disabled:opacity-50"
            >
              {isDownloading ? (
                <><span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span> Processing...</>
              ) : '📄 Download PDF'}
            </button>
          </div>

          <div ref={reportRef} className="space-y-8 bg-slate-50 p-6 md:p-10 rounded-3xl border border-slate-200 shadow-sm">
            
            <div className="p-8 bg-white border border-slate-200 rounded-2xl text-center space-y-4 shadow-sm">
              <h2 className="text-4xl font-extrabold text-slate-900 tracking-tight">
                {endReason === 'time_up' ? 'Time Limit Reached' : endReason === 'manual' ? 'Interview Ended Early' : 'Interview Complete'}
              </h2>
              <p className="text-slate-500 font-medium">Evaluation scorecard for the <strong>{role}</strong> position.</p>
              
              <div className="flex justify-center gap-4 mt-6 text-xs font-bold uppercase tracking-wider text-slate-400">
                <span>{mode}</span>
                <span>•</span>
                <span>{experience}</span>
              </div>
            </div>

            {answeredQuestions > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
                <div className="flex flex-col items-center justify-center p-6 bg-white rounded-2xl border border-slate-200 shadow-sm">
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">Final Score</span>
                  <div className="text-6xl font-extrabold text-indigo-600">{overallScore}<span className="text-2xl text-slate-400">/10</span></div>
                  <span className="text-xs font-medium text-slate-500 mt-3 bg-slate-50 px-3 py-1 rounded-full">Based on {answeredQuestions} answers</span>
                </div>

                <div className="p-6 bg-white rounded-2xl border border-slate-200 shadow-sm">
                  <span className="text-xs font-bold text-rose-500 uppercase tracking-widest mb-4 flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                    Areas to Improve
                  </span>
                  <ul className="list-disc pl-5 space-y-2 text-sm text-slate-600 font-medium">
                    {aggregatedImprovements.length > 0 
                      ? aggregatedImprovements.map((imp, idx) => <li key={idx}>{imp}</li>)
                      : <li>No major improvement areas detected.</li>}
                  </ul>
                </div>

                <div className="p-6 bg-white rounded-2xl border border-slate-200 shadow-sm">
                  <span className="text-xs font-bold text-emerald-500 uppercase tracking-widest mb-4 flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                    Actionable Tips
                  </span>
                  <ul className="list-disc pl-5 space-y-2 text-sm text-slate-600 font-medium">
                    {aggregatedTips.length > 0 
                      ? aggregatedTips.map((tip, idx) => <li key={idx}>{tip}</li>)
                      : <li>Great job hitting the key points!</li>}
                  </ul>
                </div>
              </div>
            ) : (
              <div className="text-slate-500 text-center mt-4 italic font-medium p-8 bg-white rounded-2xl border border-slate-200">No questions were answered during this session.</div>
            )}

            {answeredQuestions > 0 && (
              <div className="space-y-8 mt-12 pt-8 border-t border-slate-200">
                <h3 className="text-2xl font-bold text-slate-900 px-2">Detailed Breakdown</h3>
                {sessionFeedback.map((item, idx) => (
                  <div key={idx} className="space-y-4">
                    <div className="p-6 bg-white border border-slate-200 shadow-sm rounded-2xl">
                      <div className="text-xs font-bold text-indigo-500 tracking-wider mb-2 uppercase">Question {idx + 1}</div>
                      <h3 className="text-xl font-bold text-slate-900 mb-6">{item.question}</h3>
                      <div className="p-5 bg-slate-50 rounded-xl border border-slate-100">
                        <span className="text-xs font-bold text-slate-400 uppercase tracking-widest block mb-2">Your Transcript</span>
                        <p className="text-sm text-slate-700 leading-relaxed italic">"{item.transcript}"</p>
                      </div>
                    </div>
                    <FeedbackCard feedback={item.evaluation} />
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>
      )}
    </div>
  );
}