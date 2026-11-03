import { useState, useEffect } from 'react';

export default function HistoryDashboard({ token, onStartNew, onResume }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/sessions/history', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setHistory(data.history);
        }
      } catch (err) {
        console.error("Failed to fetch history", err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, [token]);

  if (loading) return <div className="text-center text-slate-500 mt-20 font-medium">Loading your analytics...</div>;

  const totalInterviews = history.length;
  const completedQuestions = history.flatMap(s => s.questions).filter(q => q.feedback);
  const avgScore = completedQuestions.length 
    ? (completedQuestions.reduce((acc, q) => acc + q.feedback.score, 0) / completedQuestions.length).toFixed(1) : 0;
  const totalFillerWords = completedQuestions.reduce((acc, q) => acc + (q.feedback.filler_words_count || 0), 0);

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-fade-in">
      
      {/* Top Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white border border-slate-200 rounded-2xl shadow-sm flex items-center justify-between">
          <div>
            <div className="text-sm font-semibold text-slate-500 mb-1">Total Practice Sessions</div>
            <div className="text-3xl font-extrabold text-slate-800">{totalInterviews}</div>
          </div>
          <div className="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          </div>
        </div>
        <div className="p-6 bg-white border border-slate-200 rounded-2xl shadow-sm flex items-center justify-between">
          <div>
            <div className="text-sm font-semibold text-slate-500 mb-1">Avg. Interview Score</div>
            <div className="text-3xl font-extrabold text-slate-800">{avgScore}<span className="text-lg text-slate-400 font-semibold">/10</span></div>
          </div>
          <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path></svg>
          </div>
        </div>
        <div className="p-6 bg-white border border-slate-200 rounded-2xl shadow-sm flex items-center justify-between">
          <div>
            <div className="text-sm font-semibold text-slate-500 mb-1">Filler Words Detected</div>
            <div className="text-3xl font-extrabold text-slate-800">{totalFillerWords}</div>
          </div>
          <div className="w-12 h-12 bg-rose-50 text-rose-600 rounded-xl flex items-center justify-center">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Recommended Actions */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-bold text-slate-800">Recommended for You</h3>
            <button onClick={onStartNew} className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg shadow-sm transition-colors">
              + Start Custom Practice
            </button>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="p-6 bg-white border border-slate-200 rounded-2xl shadow-sm hover:shadow-md hover:border-indigo-300 transition-all cursor-pointer group" onClick={onStartNew}>
              <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center mb-5 group-hover:bg-blue-100 transition-colors">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
              </div>
              <h4 className="font-bold text-slate-800 text-lg">Behavioral Interview</h4>
              <p className="text-sm text-slate-500 mt-2 mb-6 line-clamp-2">Master common behavioral and cultural fit questions using the STAR method format.</p>
              <span className="text-sm font-semibold text-indigo-600 group-hover:text-indigo-700">Start Practice →</span>
            </div>
            
            <div className="p-6 bg-white border border-slate-200 rounded-2xl shadow-sm hover:shadow-md hover:border-indigo-300 transition-all cursor-pointer group" onClick={onStartNew}>
              <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center mb-5 group-hover:bg-emerald-100 transition-colors">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path></svg>
              </div>
              <h4 className="font-bold text-slate-800 text-lg">Technical Deep-Dive</h4>
              <p className="text-sm text-slate-500 mt-2 mb-6 line-clamp-2">Get ready for technical rounds with AI generated follow-up questions to test your depth.</p>
              <span className="text-sm font-semibold text-indigo-600 group-hover:text-indigo-700">Start Practice →</span>
            </div>
          </div>
        </div>

        {/* Recent Activity List */}
        <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6">
          <h3 className="text-lg font-bold text-slate-800 mb-6">Recent Activity</h3>
          <div className="space-y-6">
            {history.length === 0 ? (
              <p className="text-sm text-slate-500 text-center py-4">No recent activity. Start practicing!</p>
            ) : (
              history.slice(0, 5).map((session) => (
                <div key={session._id} className="flex gap-4">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 shadow-sm border ${session.status === 'completed' ? 'bg-emerald-50 text-emerald-600 border-emerald-100' : 'bg-amber-50 text-amber-600 border-amber-100'}`}>
                    {session.status === 'completed' ? (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                    ) : (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    )}
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-slate-800">
                      {session.status === 'completed' ? 'Completed: ' : 'Started: '}{session.role_applied_for}
                    </h4>
                    <p className="text-xs text-slate-500 mt-1">
                      {new Date(session.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })} • {session.mode}
                    </p>
                    {session.status === 'in-progress' && (
                      <button onClick={() => onResume(session.session_id)} className="mt-2 text-xs font-semibold text-indigo-600 hover:text-indigo-800">
                        Resume Session →
                      </button>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

      </div>
    </div>
  );
}