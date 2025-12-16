import React, { useState, useRef } from 'react';
import { 
  Layout, Shield, AlertCircle, TrendingUp, Copy, 
  Upload, Search 
} from "lucide-react";
import GlassCard from './components/ui/GlassCard';
import Badge from './components/ui/Badge';
import ScoreBreakdown from './components/features/ScoreBreakdown'; // Import the breakdown component

export default function App() {
  // --- STATE ---
  const [jdText, setJdText] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null); // Add error state for UI banner
  
  const resultsRef = useRef(null);

  // --- HANDLERS ---
  const handleAnalyze = async () => {
    if (!jdText || !resumeFile) {
        alert("Please provide both Job Description and a Resume PDF.");
        return;
    }

    setLoading(true);
    setAnalysisData(null);
    setError(null);

    const formData = new FormData();
    formData.append("resume_file", resumeFile);
    formData.append("jd_text", jdText);

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            body: formData, 
        });

        if (response.ok) {
            const result = await response.json();
            setAnalysisData(result);
            setTimeout(() => {
                resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
            }, 100);
        } else {
            const err = await response.json();
            setError("Analysis failed: " + (err.detail || "Server Error"));
        }
    } catch (error) {
        console.error("Connection error:", error);
        setError("Failed to connect to backend. Please check if the server is running.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-300 font-sans pb-12">
      
      {/* --- HEADER --- */}
      <header className="fixed top-0 w-full h-[80px] z-50 bg-[#0f172a]/80 backdrop-blur-lg border-b border-white/5 flex items-center justify-center px-6">
        <div className="w-full max-w-[1280px] flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
              <Layout className="text-white w-6 h-6" />
            </div>
            <div>
              <h1 className="text-white font-bold text-xl tracking-tight">Career Compass</h1>
              <p className="text-xs text-slate-400">AI Resume Intelligence</p>
            </div>
          </div>
          {/* Show target role only if analysis exists */}
          {analysisData && (
             <div className="hidden md:block text-sm text-slate-400">
               Target: <span className="text-white font-medium">
                 {analysisData.roles?.[0]?.role || analysisData.primary_role || "General Role"}
               </span>
             </div>
          )}
        </div>
      </header>

      <main className="pt-[110px] px-6">
        <div className="max-w-[1280px] mx-auto space-y-8">

          {/* --- 1. INPUT SECTION (Always Visible) --- */}
          <section className="space-y-6">
            <div className="text-center space-y-2 mb-8">
              <h2 className="text-3xl font-bold text-white">Optimize Your Resume for Any Role</h2>
              <p className="text-slate-400">Paste your job description and upload your resume to get an AI-powered gap analysis.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Job Description Input */}
              <GlassCard title="1. Job Description" className="h-full flex flex-col">
                <textarea
                  className="w-full h-64 bg-slate-800/50 border border-white/10 rounded-xl p-4 text-sm text-slate-300 focus:ring-2 focus:ring-blue-500/50 focus:outline-none resize-none transition-all placeholder:text-slate-600"
                  placeholder="Paste the full Job Description here..."
                  value={jdText}
                  onChange={(e) => setJdText(e.target.value)}
                />
              </GlassCard>

              {/* Resume Input */}
              <GlassCard title="2. Your Resume (PDF)" className="h-full flex flex-col justify-center items-center">
                  <div className="border-2 border-dashed border-slate-600 rounded-xl p-8 w-full text-center hover:border-blue-500 transition-colors cursor-pointer relative h-64 flex flex-col justify-center">
                      <input 
                          type="file" 
                          accept=".pdf"
                          onChange={(e) => setResumeFile(e.target.files[0])}
                          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      />
                      <div className="flex flex-col items-center gap-3">
                          <Upload size={40} className="text-blue-400" />
                          {resumeFile ? (
                              <span className="text-emerald-400 font-medium">{resumeFile.name}</span>
                          ) : (
                              <span className="text-slate-400">Click to Upload PDF Resume</span>
                          )}
                      </div>
                  </div>
              </GlassCard>
            </div>

            {/* Analyze Button */}
            <div className="flex justify-center pt-4">
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className={`
                  relative group px-8 py-4 rounded-xl font-bold text-lg text-white shadow-2xl transition-all
                  ${loading ? 'bg-slate-700 cursor-not-allowed' : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:scale-105 hover:shadow-blue-500/30'}
                `}
              >
                {loading ? (
                  <span className="flex items-center gap-2">
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Analyzing...
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    <Search size={20} /> Analyze My Fit
                  </span>
                )}
              </button>
            </div>
          </section>

          {/* Error Banner */}
          {error && (
            <div className="bg-red-500/10 border border-red-500/50 text-red-200 p-4 rounded-xl flex items-center gap-3">
              <AlertCircle className="shrink-0" />
              <p>{error}</p>
              <button onClick={() => setError(null)} className="ml-auto text-sm hover:text-white">Dismiss</button>
            </div>
          )}

          {/* --- 2. ANALYSIS RESULTS (Conditional) --- */}
          {analysisData && (
            <div ref={resultsRef} className="space-y-8 pt-12 border-t border-white/5 animate-in fade-in slide-in-from-bottom-10 duration-700">
              
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                  <TrendingUp className="text-emerald-400" /> Analysis Report
                </h2>
                <button 
                  onClick={() => setAnalysisData(null)}
                  className="text-sm text-slate-400 hover:text-white"
                >
                  Clear Results
                </button>
              </div>

              {/* ROW 1: ATS Score & Missing Skills */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* ATS Score Card */}
                <GlassCard className="relative overflow-hidden group">
                  <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                    <Shield size={100} />
                  </div>
                  <div className="relative z-10">
                    <div className="flex items-baseline gap-2">
                      <span className="text-6xl font-bold text-white tracking-tighter">{Math.round(analysisData.ats_score)}</span>
                      <span className="text-slate-400 text-xl">/100</span>
                    </div>
                    <div className={`mt-3 inline-flex px-3 py-1 rounded-full text-sm font-bold border ${
                       analysisData.ats_score < 50 ? "bg-red-500/10 text-red-400 border-red-500/20" : "bg-green-500/10 text-green-400 border-green-500/20"
                    }`}>
                      {analysisData.ats_band}
                    </div>
                    <p className="text-xs text-slate-400 mt-4">Target: {analysisData.roles?.[0]?.role}</p>
                  </div>
                </GlassCard>

                {/* Missing Skills Card */}
                <GlassCard className="md:col-span-2">
                  <div className="flex justify-between items-start mb-4">
                      <h3 className="text-slate-100 font-semibold flex items-center gap-2">
                         <AlertCircle size={18} className="text-red-400"/> Critical Missing Skills
                      </h3>
                      <Badge color="red">{analysisData.missing_skills?.length || 0} Missing</Badge>
                  </div>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {(analysisData.missing_skills || []).map((skill, i) => (
                      <span key={i} className="px-3 py-1.5 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-300">
                        {skill}
                      </span>
                    ))}
                  </div>
                  <p className="text-xs text-slate-500 leading-relaxed border-t border-white/5 pt-3">
                    {analysisData.suggestion}
                  </p>
                </GlassCard>
              </div>

              {/* ROW 2: Detailed Breakdown (Full Width) */}
              {analysisData.scores && (
                 <ScoreBreakdown scores={analysisData.scores} />
              )}

              {/* ROW 3: Two Column Layout */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
                
                {/* LEFT COLUMN: Role Fit & Learning Path */}
                <div className="space-y-6">
                  
                  {/* Role Fit Analysis */}
                  <GlassCard title="Career Potential Analysis">
                    <div className="space-y-4">
                      {(analysisData.roles || []).map((role, idx) => (
                        <div key={idx} className={`p-4 rounded-xl border transition-all ${idx === 0 ? 'bg-blue-500/10 border-blue-500/30' : 'bg-slate-800/50 border-white/5'}`}>
                          <div className="flex justify-between items-center mb-2">
                            <h4 className={`font-semibold ${idx === 0 ? 'text-white' : 'text-slate-300'}`}>{role.role}</h4>
                            <span className="font-bold text-slate-200">{Math.round(role.score * 100)}%</span>
                          </div>
                          <div className="h-2 w-full bg-slate-700 rounded-full overflow-hidden mb-3">
                            <div className={`h-full ${idx === 0 ? 'bg-blue-500' : 'bg-slate-500'}`} style={{ width: `${role.score * 100}%` }} />
                          </div>
                          <p className="text-xs text-slate-400">{role.reason?.substring(0, 140)}...</p>
                        </div>
                      ))}
                    </div>
                  </GlassCard>

                  {/* Learning Path */}
                  <GlassCard title="Recommended Learning Path">
                    <div className="relative pl-4 space-y-6 before:absolute before:left-[11px] before:top-2 before:h-[95%] before:w-[2px] before:bg-slate-800">
                      {(analysisData.learning_path || []).map((step, i) => (
                        <div key={i} className="relative">
                          <div className="absolute -left-[21px] top-1 w-4 h-4 rounded-full bg-slate-900 border-2 border-blue-500 z-10" />
                          <div>
                            <span className="text-[10px] uppercase tracking-wider text-blue-400 font-bold mb-1 block">
                               Step {step.step} • {step.duration_weeks} Weeks
                            </span>
                            <h5 className="text-sm font-medium text-white mb-1">{step.title}</h5>
                            <span className="text-[10px] px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30">
                              {step.type}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </GlassCard>

                </div>

                {/* RIGHT COLUMN: Boosters & Trends */}
                <div className="space-y-6">
                  
                  {/* Keyword Boosters */}
                  <GlassCard title="Resume Keyword Boosters">
                    <div className="space-y-4">
                      {(analysisData.booster_suggestions || []).map((boost, i) => (
                        <div key={i} className="bg-slate-800/40 p-4 rounded-lg border border-white/5 hover:border-blue-500/30 transition-colors group">
                          <div className="flex justify-between items-start mb-2">
                             <span className="text-red-300 bg-red-500/10 px-2 py-0.5 rounded text-xs border border-red-500/20 font-mono">Missing: {boost.skill}</span>
                             <Copy size={14} className="text-slate-500 hover:text-white cursor-pointer" />
                          </div>
                          <p className="text-sm text-slate-300 font-mono bg-black/20 p-3 rounded border border-white/5 leading-relaxed select-all">
                            {boost.snippet}
                          </p>
                        </div>
                      ))}
                    </div>
                  </GlassCard>

                  {/* Future Trends */}
                  <GlassCard title="Future Industry Trends">
                      <div className="space-y-3">
                        {(analysisData.future_trends || []).map((trend, i) => (
                          <div key={i} className="p-3 bg-slate-800/50 rounded-lg border border-white/5 flex items-start gap-3">
                            <TrendingUp size={16} className="text-emerald-400 mt-1 shrink-0" />
                            <div>
                              <h5 className="text-sm font-medium text-emerald-100">{trend.name || trend.skill}</h5>
                              <p className="text-xs text-slate-400 mt-0.5">{trend.why}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                  </GlassCard>

                </div>

              </div>
            </div>
          )}

        </div>
      </main>
    </div>
  );
}