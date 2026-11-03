import { useState } from 'react';

export default function AuthScreen({ onAuthSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const endpoint = isLogin ? '/login' : '/signup';
    const payload = isLogin ? { email, password } : { email, password, name };

    try {
      const res = await fetch(`http://127.0.0.1:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      
      if (res.ok) {
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('userName', data.name);
        onAuthSuccess(data.access_token, data.name);
      } else {
        setError(data.detail || 'Authentication failed');
      }
    } catch {
      setError('Network error. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex text-slate-900 bg-white">
      
      {/* Left Side: Form */}
      <div className="w-full lg:w-1/2 flex flex-col justify-center px-12 sm:px-24 overflow-y-auto">
        <div className="max-w-md w-full mx-auto space-y-8">
          <div>
            <div className="flex items-center gap-2 mb-8">
              <div className="w-8 h-8 rounded bg-indigo-600 flex items-center justify-center font-bold text-white shadow-sm">AI</div>
              <span className="text-xl font-bold text-slate-800 tracking-tight">InterviewCoach</span>
            </div>
            <h2 className="text-3xl font-bold tracking-tight text-slate-900">
              {isLogin ? 'Welcome Back!' : 'Create Your Account'}
            </h2>
            <p className="mt-2 text-sm text-slate-500">
              {isLogin ? 'Sign in to continue your interview journey.' : 'Start your journey to a better interview experience.'}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            {!isLogin && (
              <div>
                <label className="block text-sm font-medium text-slate-700">Full Name</label>
                <input type="text" required value={name} onChange={e => setName(e.target.value)} className="mt-1 w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600 outline-none transition-all" placeholder="John Doe" />
              </div>
            )}
            <div>
              <label className="block text-sm font-medium text-slate-700">Email Address</label>
              <input type="email" required value={email} onChange={e => setEmail(e.target.value)} className="mt-1 w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600 outline-none transition-all" placeholder="you@example.com" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">Password</label>
              <input type="password" required value={password} onChange={e => setPassword(e.target.value)} className="mt-1 w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600 outline-none transition-all" placeholder="••••••••" />
            </div>

            {error && <div className="text-red-500 text-sm font-medium bg-red-50 p-3 rounded-lg border border-red-100">{error}</div>}

            <button disabled={loading} type="submit" className="w-full flex justify-center py-3 px-4 rounded-full shadow-md text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-600 transition-colors disabled:opacity-50">
              {loading ? 'Processing...' : isLogin ? 'Sign In' : 'Sign Up'}
            </button>
          </form>

          <div className="text-center">
            <button onClick={() => { setIsLogin(!isLogin); setError(''); }} className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
              {isLogin ? "Don't have an account? Sign Up" : "Already have an account? Sign In"}
            </button>
          </div>
        </div>
      </div>

      {/* Right Side: Branding */}
      <div className="hidden lg:flex w-1/2 bg-[#1e1b4b] text-white flex-col justify-center px-16 relative overflow-hidden">
        <div className="relative z-10 max-w-lg">
          <h2 className="text-4xl font-bold mb-6 leading-tight">
            {isLogin ? 'Better Practice.\nBigger Opportunities.' : 'Learn. Practice.\nSucceed.'}
          </h2>
          <p className="text-indigo-200 text-lg mb-8 leading-relaxed">
            Join thousands of job seekers who are building their confidence and landing their dream jobs with InterviewCoach.
          </p>
          
          <div className="space-y-6 bg-white/5 p-6 rounded-2xl border border-white/10 backdrop-blur-sm">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-indigo-500/30 flex items-center justify-center text-xl shadow-inner">🎯</div>
              <div>
                <h4 className="font-semibold text-white">AI-Powered Feedback</h4>
                <p className="text-sm text-indigo-200 mt-1">Get detailed insights on your performance in real-time.</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-indigo-500/30 flex items-center justify-center text-xl shadow-inner">📈</div>
              <div>
                <h4 className="font-semibold text-white">Track Your Progress</h4>
                <p className="text-sm text-indigo-200 mt-1">See your improvement and filler-word reduction over time.</p>
              </div>
            </div>
          </div>
        </div>
        
        <div className="absolute top-1/4 -right-20 w-96 h-96 bg-indigo-600 rounded-full mix-blend-multiply filter blur-3xl opacity-40 animate-pulse"></div>
        <div className="absolute bottom-0 -left-10 w-72 h-72 bg-purple-600 rounded-full mix-blend-multiply filter blur-3xl opacity-30"></div>
      </div>
    </div>
  );
}