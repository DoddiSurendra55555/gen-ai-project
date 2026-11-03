import { useState } from 'react';
import LandingPage from './components/LandingPage';
import AuthScreen from './components/AuthScreen';
import InterviewDashboard from './components/InterviewDashboard';
import Profile from './components/Profile';
import HistoryDashboard from './components/HistoryDashboard';

export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem('token'));
  const [userName, setUserName] = useState(() => localStorage.getItem('userName'));
  const [showAuth, setShowAuth] = useState(false);
  const [currentTab, setCurrentTab] = useState('dashboard');
  const [activeSessionId, setActiveSessionId] = useState(null);

  const handleAuthSuccess = (newToken, newName) => {
    setToken(newToken);
    setUserName(newName);
    setShowAuth(false);
    setCurrentTab('dashboard');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userName');
    setToken(null);
    setUserName('');
    setShowAuth(false);
  };

  const handleStartPractice = () => {
    setActiveSessionId(null);
    setCurrentTab('practice');
  };

  if (!token) {
    return showAuth ? (
      <AuthScreen onAuthSuccess={handleAuthSuccess} />
    ) : (
      <LandingPage onGetStarted={() => setShowAuth(true)} />
    );
  }

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-900">
      {/* Dark Sidebar */}
      <aside className="w-64 bg-[#1e1b4b] text-white flex flex-col transition-all duration-300 shadow-xl z-20">
        <div className="h-16 flex items-center px-6 border-b border-indigo-900/50">
          <div className="w-8 h-8 rounded bg-indigo-500 flex items-center justify-center font-bold mr-3 shadow-sm">
            AI
          </div>
          <span className="text-lg font-bold tracking-wide">InterviewCoach</span>
        </div>

        <nav className="flex-1 py-8 px-4 space-y-2">
          <button onClick={() => setCurrentTab('dashboard')} className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${currentTab === 'dashboard' ? 'bg-indigo-600 text-white shadow-md' : 'text-indigo-200 hover:bg-indigo-900/50 hover:text-white'}`}>
            <svg className="w-5 h-5 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
            Dashboard
          </button>
          
          <button onClick={() => setCurrentTab('practice')} className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${currentTab === 'practice' ? 'bg-indigo-600 text-white shadow-md' : 'text-indigo-200 hover:bg-indigo-900/50 hover:text-white'}`}>
            <svg className="w-5 h-5 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path></svg>
            Practice
          </button>
          
          <button onClick={() => setCurrentTab('profile')} className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${currentTab === 'profile' ? 'bg-indigo-600 text-white shadow-md' : 'text-indigo-200 hover:bg-indigo-900/50 hover:text-white'}`}>
            <svg className="w-5 h-5 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
            Profile
          </button>
        </nav>

        <div className="p-4 border-t border-indigo-900/50">
          <button onClick={handleLogout} className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium text-indigo-300 hover:bg-indigo-900/50 hover:text-white transition-colors">
            <svg className="w-5 h-5 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
            Log Out
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col overflow-hidden relative">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 shadow-sm z-10">
          <div className="text-lg font-semibold text-slate-800">
            {currentTab === 'dashboard' && 'Dashboard'}
            {currentTab === 'practice' && 'Interview Practice Area'}
            {currentTab === 'profile' && 'Manage Your Profile'}
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3">
              <span className="text-sm font-medium text-slate-600">{userName}</span>
              <img src={`https://ui-avatars.com/api/?name=${encodeURIComponent(userName)}&background=4f46e5&color=fff`} alt="Avatar" className="w-9 h-9 rounded-full shadow-sm border border-slate-200" />
            </div>
          </div>
        </header>

        <div className="flex-1 overflow-auto p-8 bg-slate-50">
          {currentTab === 'profile' ? (
            <Profile token={token} />
          ) : currentTab === 'dashboard' ? (
             <HistoryDashboard token={token} onStartNew={handleStartPractice} onResume={(id) => { setActiveSessionId(id); setCurrentTab('practice'); }} />
          ) : (
            <InterviewDashboard token={token} resumeSessionId={activeSessionId} onComplete={() => setCurrentTab('dashboard')} />
          )}
        </div>
      </main>
    </div>
  );
}