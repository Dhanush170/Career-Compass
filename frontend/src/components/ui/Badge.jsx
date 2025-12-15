const Badge = ({ children, color = "blue", className }) => {
  const colors = {
    blue: "bg-blue-500/20 text-blue-300 border-blue-500/30",
    green: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
    red: "bg-red-500/20 text-red-300 border-red-500/30",
    amber: "bg-amber-500/20 text-amber-300 border-amber-500/30",
    purple: "bg-purple-500/20 text-purple-300 border-purple-500/30",
  };
  
  return (
    <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium border ${colors[color]} ${className}`}>
      {children}
    </span>
  );
};
export default Badge;