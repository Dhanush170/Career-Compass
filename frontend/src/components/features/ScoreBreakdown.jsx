import React from 'react';
import GlassCard from "../ui/GlassCard";

const ScoreBreakdown = ({ scores }) => {
  // Helper to determine color based on score value
  const getColor = (val) => {
    if (val >= 75) return "bg-emerald-500";
    if (val >= 50) return "bg-blue-500";
    return "bg-amber-500";
  };

  const scoreItems = [
    { 
      label: "Keyword Match", 
      value: scores.keyword_score, 
      desc: "Presence of hard skills from the JD." 
    },
    { 
      label: "Semantic Match", 
      value: scores.semantic_score, 
      desc: "Contextual alignment with the role." 
    },
    { 
      label: "Experience Impact", 
      value: scores.experience_score, 
      desc: "Usage of action verbs and metrics." 
    },
    { 
      label: "Formatting", 
      value: scores.format_score, 
      desc: "ATS-readability and structure." 
    }
  ];

  return (
    <GlassCard title="Score Breakdown">
      <div className="space-y-5">
        {scoreItems.map((item, idx) => (
          <div key={idx}>
            <div className="flex justify-between items-end mb-1">
              <span className="text-sm font-medium text-slate-200">{item.label}</span>
              <span className="text-sm font-bold text-white">{Math.round(item.value)}/100</span>
            </div>
            
            {/* Progress Bar Container */}
            <div className="h-2 w-full bg-slate-700/50 rounded-full overflow-hidden mb-1">
              <div 
                className={`h-full ${getColor(item.value)} transition-all duration-1000 ease-out`} 
                style={{ width: `${item.value}%` }} 
              />
            </div>
            
            <p className="text-[10px] text-slate-400">{item.desc}</p>
          </div>
        ))}
      </div>
    </GlassCard>
  );
};

export default ScoreBreakdown;