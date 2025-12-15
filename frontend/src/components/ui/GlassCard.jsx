import { cn } from "../../lib/utils";

const GlassCard = ({ children, className, title, action }) => {
  return (
    <div className={cn(
      "bg-slate-900/60 backdrop-blur-md border border-white/10 rounded-2xl p-5 shadow-xl transition-all hover:border-white/20",
      className
    )}>
      {(title || action) && (
        <div className="flex justify-between items-center mb-4 border-b border-white/5 pb-3">
          {title && <h3 className="text-slate-100 font-semibold text-lg">{title}</h3>}
          {action}
        </div>
      )}
      {children}
    </div>
  );
};

export default GlassCard;