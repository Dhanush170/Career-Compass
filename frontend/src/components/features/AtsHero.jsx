import GlassCard from "../ui/Glasscard";
import Badge from "../ui/Badge";
import { Shield, AlertCircle } from "lucide-react";

const AtsHero = ({ data }) => {
  // data = the full JSON object
  const score = Math.round(data.ats_score || 0);
  const band = data.ats_band || "N/A";
  const missing = data.missing_skills || [];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      {/* Score Card */}
      <GlassCard className="relative overflow-hidden group">
        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
          <Shield size={100} />
        </div>
        <div className="flex items-center justify-between relative z-10">
          <div>
            <div className="flex items-baseline gap-2">
              <span className="text-6xl font-bold text-white tracking-tighter">{score}</span>
              <span className="text-slate-400">/100</span>
            </div>
            <Badge color={score > 70 ? "green" : "red"} className="mt-2 text-sm">
              {band}
            </Badge>
          </div>
        </div>
      </GlassCard>

      {/* Missing Skills Summary */}
      <GlassCard className="md:col-span-2">
        <div className="flex justify-between items-start mb-3">
            <h3 className="text-slate-100 font-semibold flex items-center gap-2">
                <AlertCircle size={18} className="text-red-400"/> Critical Gaps
            </h3>
            <Badge color="red">{missing.length} Missing</Badge>
        </div>
        <div className="flex flex-wrap gap-2">
            {missing.slice(0, 6).map((skill, i) => (
                <span key={i} className="px-3 py-1 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-300 hover:text-white transition-colors">
                    {skill}
                </span>
            ))}
            {missing.length > 6 && (
                <span className="px-3 py-1 text-slate-500 text-sm">+{missing.length - 6} more</span>
            )}
        </div>
        <p className="text-xs text-slate-500 mt-3">{data.suggestion.substring(0, 120)}...</p>
      </GlassCard>
    </div>
  );
};
export default AtsHero;