export default function LandingPage({ onGetStarted }) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 selection:bg-indigo-100 scroll-smooth">
      
      {/* Navigation */}
      <nav className="fixed w-full bg-white/80 backdrop-blur-md z-50 border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => window.scrollTo(0, 0)}>
            <div className="w-8 h-8 rounded bg-indigo-600 flex items-center justify-center font-bold text-white shadow-sm">AI</div>
            <span className="text-xl font-bold text-slate-800 tracking-tight">InterviewCoach</span>
          </div>
          <div className="hidden md:flex gap-8 text-sm font-medium text-slate-600">
            <a href="#home" className="hover:text-indigo-600 transition-colors">Home</a>
            <a href="#features" className="hover:text-indigo-600 transition-colors">Features</a>
            <a href="#testimonials" className="hover:text-indigo-600 transition-colors">Testimonials</a>
          </div>
          <div className="flex gap-4">
            <button onClick={onGetStarted} className="px-5 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors">Sign In</button>
            <button onClick={onGetStarted} className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-full shadow-md transition-colors">Sign Up</button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="home" className="pt-32 pb-16 md:pt-40 md:pb-24 px-6">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <h1 className="text-5xl md:text-6xl font-extrabold text-slate-900 leading-[1.1] tracking-tight">
              Your AI-Powered <br/><span className="text-indigo-600">Interview Coach</span>
            </h1>
            <p className="text-lg text-slate-600 leading-relaxed max-w-lg">
              Practice real interview questions, get instant feedback, sharpen your skills, and build the confidence you need to land your dream job.
            </p>
            <div className="pt-4">
              <button onClick={onGetStarted} className="px-8 py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-full shadow-lg shadow-indigo-200 transition-transform hover:-translate-y-0.5 flex items-center gap-2">
                Get Started Free 
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
              </button>
            </div>
          </div>

          <div className="relative">
            <div className="absolute inset-0 bg-indigo-100 rounded-3xl transform rotate-3 scale-105 -z-10"></div>
            <img 
              src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" 
              alt="Professional interview preparation" 
              className="rounded-3xl shadow-2xl object-cover h-[500px] w-full border border-slate-200"
            />
            <div className="absolute -bottom-6 -left-6 bg-white p-4 rounded-xl shadow-xl border border-slate-100 flex items-center gap-4">
              <div className="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center font-bold text-lg">90%</div>
              <div>
                <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Overall Score</p>
                <p className="text-sm font-bold text-slate-800">Excellent performance!</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 bg-white border-y border-slate-200">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">Everything you need to succeed</h2>
            <p className="text-slate-600">Our platform uses advanced AI to simulate real interview environments tailored specifically to your resume.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-8 rounded-2xl bg-slate-50 border border-slate-100">
              <div className="w-12 h-12 bg-indigo-100 text-indigo-600 rounded-xl flex items-center justify-center mb-6">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path></svg>
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Voice-Based Practice</h3>
              <p className="text-slate-600 text-sm leading-relaxed">Speak your answers out loud. Our AI transcription engine evaluates your actual delivery, not just your typing speed.</p>
            </div>
            
            <div className="p-8 rounded-2xl bg-slate-50 border border-slate-100">
              <div className="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-xl flex items-center justify-center mb-6">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Instant Feedback</h3>
              <p className="text-slate-600 text-sm leading-relaxed">Get scored out of 10 instantly. We highlight your strengths, pinpoint areas for improvement, and catch your filler words.</p>
            </div>

            <div className="p-8 rounded-2xl bg-slate-50 border border-slate-100">
              <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center mb-6">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Resume Integration</h3>
              <p className="text-slate-600 text-sm leading-relaxed">Upload your PDF resume once. The AI analyzes your past experience and creates hyper-specific questions just for you.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-24 bg-slate-50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">Loved by job seekers</h2>
            <p className="text-slate-600">See how our AI Coach is helping professionals land their dream roles.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
              <div className="flex text-amber-400 mb-4">★★★★★</div>
              <p className="text-slate-700 mb-6 font-medium">"The dynamic follow-up questions caught me off guard in the best way possible. It felt exactly like a real technical interview."</p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-slate-200 flex items-center justify-center font-bold text-slate-600">SJ</div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900">Sarah Jenkins</h4>
                  <p className="text-xs text-slate-500">Software Engineer</p>
                </div>
              </div>
            </div>

            <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
              <div className="flex text-amber-400 mb-4">★★★★★</div>
              <p className="text-slate-700 mb-6 font-medium">"Being able to see exactly how many times I say 'um' and 'like' was a game changer for my confidence."</p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-slate-200 flex items-center justify-center font-bold text-slate-600">MD</div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900">Marcus Davis</h4>
                  <p className="text-xs text-slate-500">Product Manager</p>
                </div>
              </div>
            </div>

            <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm hidden md:block">
              <div className="flex text-amber-400 mb-4">★★★★★</div>
              <p className="text-slate-700 mb-6 font-medium">"I uploaded my resume and it asked me about a highly specific MongoDB project I did years ago. Unbelievable accuracy."</p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-slate-200 flex items-center justify-center font-bold text-slate-600">AL</div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900">Anna Lee</h4>
                  <p className="text-xs text-slate-500">Data Analyst</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-12 text-center">
        <p className="text-slate-500 text-sm">© 2026 InterviewCoach AI. All rights reserved.</p>
      </footer>
    </div>
  );
}