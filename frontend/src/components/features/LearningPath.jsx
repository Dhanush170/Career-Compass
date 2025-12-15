import GlassCard from "../ui/Glasscard";
import Badge from "../ui/Badge";

const LearningPath = ({ steps }) => {
  return (
    <GlassCard title="Learning Path">
      <div className="relative pl-4 space-y-8 before:absolute before:left-[11px] before:top-2 before:h-[95%] before:w-[2px] before:bg-slate-800">
        {steps.map((step, i) => (
          <div key={i} className="relative group">
            {/* Dot */}
            <div className="absolute -left-[21px] top-1 w-4 h-4 rounded-full bg-slate-900 border-2 border-blue-500 z-10 group-hover:scale-110 transition-transform" />
            
            <div>
              <span className="text-[10px] uppercase tracking-wider text-blue-400 font-bold mb-1 block">
                Step {step.step} • {step.duration_weeks} Weeks
              </span>
              <h5 className="text-sm font-medium text-white mb-1">{step.title}</h5>
              <div className="flex gap-2 mb-2">
                <Badge color="purple">{step.type}</Badge>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed bg-slate-800/50 p-2 rounded border border-white/5">
                {step.notes}
              </p>
            </div>
          </div>
        ))}
      </div>
    </GlassCard>
  );
};
export default LearningPath;