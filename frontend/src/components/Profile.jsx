import { useState, useEffect, useCallback } from 'react';

export default function Profile({ token }) {
  const [profile, setProfile] = useState(null);
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchProfile = useCallback(async () => {
    setLoading(true);

    try {
      const res = await fetch('https://gen-ai-project-3-5eim.onrender.com/profile', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) setProfile(await res.json());
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    let active = true;

    const loadProfile = async () => {
      setLoading(true);

      try {
        const res = await fetch('https://gen-ai-project-3-5eim.onrender.com/profile', {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (!active || !res.ok) return;
        setProfile(await res.json());
      } catch (error) {
        console.error(error);
      } finally {
        if (active) setLoading(false);
      }
    };

    void loadProfile();

    return () => {
      active = false;
    };
  }, [token]);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setUploadStatus('Uploading and analyzing PDF...');
    const formData = new FormData();
    formData.append('resume', file);

    try {
      const res = await fetch('https://gen-ai-project-3-5eim.onrender.com/profile/resume', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });

      const data = await res.json();
      if (res.ok) {
        setUploadStatus('✅ Resume parsed and saved successfully!');
        fetchProfile();
      } else {
        setUploadStatus(`❌ Error: ${data.detail}`);
      }
    } catch {
      setUploadStatus('❌ Upload failed.');
    }
  };

  if (loading) return <div className="text-center text-slate-500 mt-20">Loading profile...</div>;

  return (
    <div className="max-w-5xl mx-auto space-y-6 animate-fade-in">
      
      {/* Top Banner Card */}
      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-8 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <img src={`https://ui-avatars.com/api/?name=${encodeURIComponent(profile?.name || 'User')}&background=4f46e5&color=fff&size=128`} alt="Avatar" className="w-24 h-24 rounded-full shadow-md border-4 border-white" />
          <div>
            <h2 className="text-2xl font-bold text-slate-900">{profile?.name}</h2>
            <p className="text-slate-500 font-medium">{profile?.email}</p>
            <div className="mt-2 inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-50 text-indigo-700 text-xs font-semibold">
              <span className="w-2 h-2 rounded-full bg-indigo-500"></span> Premium Plan
            </div>
          </div>
        </div>
        <button className="px-4 py-2 border border-slate-200 text-slate-600 text-sm font-semibold rounded-lg hover:bg-slate-50 transition-colors shadow-sm">
          Edit Profile
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Basic Information */}
        <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-8">
          <h3 className="text-lg font-bold text-slate-800 border-b border-slate-100 pb-4 mb-6">Basic Information</h3>
          <div className="space-y-4">
            <div>
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Full Name</label>
              <p className="font-medium text-slate-900 mt-1">{profile?.name}</p>
            </div>
            <div>
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Email Address</label>
              <p className="font-medium text-slate-900 mt-1">{profile?.email}</p>
            </div>
            <div>
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Location</label>
              <p className="font-medium text-slate-900 mt-1">Remote / Any</p>
            </div>
          </div>
        </div>

        {/* Resume Vault */}
        <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-8 flex flex-col">
          <h3 className="text-lg font-bold text-slate-800 border-b border-slate-100 pb-4 mb-6">Resume Vault</h3>
          
          <div className="flex-1 flex flex-col justify-center">
            <div className="flex items-center gap-4 mb-6">
              <div className={`w-12 h-12 rounded-full flex items-center justify-center text-2xl ${profile?.has_resume ? 'bg-emerald-100 text-emerald-600' : 'bg-amber-100 text-amber-600'}`}>
                {profile?.has_resume ? '📄' : '⚠️'}
              </div>
              <div>
                <p className="font-bold text-slate-900">
                  {profile?.has_resume ? 'Resume is Active' : 'No Resume Found'}
                </p>
                <p className="text-sm text-slate-500">
                  {profile?.has_resume ? 'The AI is using your document to generate questions.' : 'Upload a PDF so the AI can tailor questions to your experience.'}
                </p>
              </div>
            </div>

            <form onSubmit={handleUpload} className="space-y-4 mt-auto">
              <div className="flex items-center gap-3">
                <input 
                  type="file" 
                  accept=".pdf" 
                  onChange={(e) => setFile(e.target.files[0])}
                  className="block w-full text-sm text-slate-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 transition-colors border border-slate-200 rounded-lg"
                />
                <button 
                  type="submit" 
                  disabled={!file}
                  className="px-5 py-2.5 bg-slate-900 hover:bg-slate-800 text-white text-sm font-semibold rounded-lg disabled:opacity-50 transition-colors shadow-sm"
                >
                  Upload
                </button>
              </div>
              {uploadStatus && (
                <p className={`text-sm font-medium ${uploadStatus.includes('✅') ? 'text-emerald-600' : 'text-indigo-600'}`}>
                  {uploadStatus}
                </p>
              )}
            </form>
          </div>
        </div>

      </div>
    </div>
  );
}