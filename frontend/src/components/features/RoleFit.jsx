import GlassCard from "../ui/Glasscard";

const RoleFit = ({ roles }) => {
  return (
    <GlassCard title="Role Fit Analysis">
      <div className="space-y-4">
        {roles.map((role, idx) => (
          <div key={idx} className={`p-4 rounded-xl border transition-all ${idx === 0 ? 'bg-blue-500/10 border-blue-500/30' : 'bg-slate-800/50 border-white/5'}`}>
            <div className="flex justify-between items-center mb-2">
              <h4 className={`font-semibold ${idx === 0 ? 'text-white' : 'text-slate-300'}`}>
                {role.role}
              </h4>
              <span className="text-sm font-bold text-slate-200">
                {Math.round(role.score * 100)}%
              </span>
            </div>
            {/* Progress Bar */}
            <div className="h-2 w-full bg-slate-700 rounded-full overflow-hidden">
              <div 
                className={`h-full ${idx === 0 ? 'bg-blue-500' : 'bg-slate-500'} transition-all duration-500`} 
                style={{ width: `${role.score * 100}%` }} 
              />
            </div>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              {role.reason}
            </p>
          </div>
        ))}
      </div>
    </GlassCard>
  );
};
export default RoleFit;