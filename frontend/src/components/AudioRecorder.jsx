import { useState, useEffect, useRef } from 'react';

export default function AudioRecorder({ onTranscriptComplete, isEvaluating }) {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  
  // Use a ref to store the external browser API without triggering re-renders
  const recognitionRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const rec = new SpeechRecognition();
      rec.continuous = true;
      rec.interimResults = true;
      rec.lang = 'en-US';

      rec.onresult = (event) => {
        let currentTranscript = '';
        for (let i = 0; i < event.results.length; ++i) {
          currentTranscript += event.results[i][0].transcript;
        }
        setTranscript(currentTranscript);
      };

      rec.onerror = (event) => {
        console.error("Speech recognition error", event.error);
        setIsRecording(false);
      };

      rec.onend = () => {
        setIsRecording(false);
      };

      recognitionRef.current = rec;
    }
  }, []);

  const toggleRecording = () => {
    const recognition = recognitionRef.current;
    
    if (!recognition) {
      alert("Speech recognition is not supported in this browser. Please use Chrome or Edge, or type your answer manually below.");
      return;
    }

    if (isRecording) {
      recognition.stop();
      setIsRecording(false);
    } else {
      setTranscript(''); // Clear previous text when starting a new recording
      recognition.start();
      setIsRecording(true);
    }
  };

  const handleSubmit = () => {
    const recognition = recognitionRef.current;
    
    if (isRecording && recognition) {
      recognition.stop();
      setIsRecording(false);
    }
    onTranscriptComplete(transcript || "No transcript provided.");
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <button
          onClick={toggleRecording}
          disabled={isEvaluating}
          className={`px-5 py-2.5 rounded-xl text-sm font-bold shadow-sm transition-all flex items-center gap-2 ${
            isRecording 
              ? 'bg-rose-600 hover:bg-rose-700 text-white animate-pulse' 
              : 'bg-indigo-600 hover:bg-indigo-700 text-white'
          } disabled:opacity-50`}
        >
          <span className={`w-3 h-3 rounded-full ${isRecording ? 'bg-white' : 'bg-rose-400'}`}></span>
          {isRecording ? 'Stop Recording' : 'Record Answer'}
        </button>

        <button
          onClick={handleSubmit}
          disabled={isEvaluating || !transcript.trim()}
          className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold rounded-xl shadow-sm transition-all disabled:opacity-40"
        >
          {isEvaluating ? 'Evaluating Answer...' : 'Submit Answer →'}
        </button>
      </div>

      <div className="space-y-1.5">
        <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider">
          Live Transcription (Editable)
        </label>
        <textarea
          rows="4"
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          placeholder="Click 'Record Answer' to speak, or type directly here..."
          disabled={isEvaluating}
          className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl text-slate-800 text-sm font-medium focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600 outline-none transition-all shadow-inner"
        />
      </div>
    </div>
  );
}