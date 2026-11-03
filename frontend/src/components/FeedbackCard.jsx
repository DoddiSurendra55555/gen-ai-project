export default function FeedbackCard({ feedback }) {
  if (!feedback) return null;

  const getScoreColor = (score) => {
    if (score >= 8) return 'text-emerald-400 border-emerald-500/40 bg-emerald-950/20';
    if (score >= 5) return 'text-amber-400 border-amber-500/40 bg-amber-950/20';
    return 'text-rose-400 border-rose-500/40 bg-rose-950/20';
  };

  return (
    <div className="p-6 bg-slate-900/90 border border-slate-800 rounded-xl space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <h3 className="text-xl font-bold text-slate-100">Interviewer Scorecard</h3>
        <div className={`px-4 py-2 rounded-xl border text-2xl font-extrabold ${getScoreColor(feedback.score)}`}>
          {feedback.score} <span className="text-xs font-semibold text-slate-400">/ 10</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 bg-emerald-950/20 border border-emerald-800/40 rounded-lg">
          <h4 className="font-semibold text-emerald-400 mb-2">Strengths Demonstrated</h4>
          <ul className="list-disc list-inside space-y-1 text-sm text-slate-300">
            {feedback.strengths.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>

        <div className="p-4 bg-rose-950/20 border border-rose-800/40 rounded-lg">
          <h4 className="font-semibold text-rose-400 mb-2">Areas for Improvement</h4>
          <ul className="list-disc list-inside space-y-1 text-sm text-slate-300">
            {feedback.areas_for_improvement.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="p-4 bg-slate-800/50 border border-slate-700/60 rounded-lg">
        <h4 className="font-semibold text-indigo-400 mb-2">Key Points for an Ideal Answer</h4>
        <ul className="list-disc list-inside space-y-1 text-sm text-slate-300">
          {feedback.ideal_answer_points.map((item, idx) => (
            <li key={idx}>{item}</li>
          ))}
        </ul>
      </div>

      <div className="text-xs text-slate-400 flex justify-between items-center pt-2">
        <span>Filler Word Count: <strong>{feedback.filler_words_count}</strong></span>
        <span>Evaluated by Gemini 2.5 Flash</span>
      </div>
    </div>
  );
}