import React from "react";

interface Props {
  title: string;
  value: string | number;
  hintIcon?: React.ReactNode;
}

const StatsCard: React.FC<Props> = ({ title, value, hintIcon }) => {
  return (
    <div className="card p-5">
      <div className="flex items-center justify-between">
        <p className="text-xs tracking-widest text-gray-400 uppercase">{title}</p>
        <div className="w-8 h-8 rounded-xl bubble flex items-center justify-center">
          {hintIcon ?? <span className="text-indigo-300">⤴</span>}
        </div>
      </div>
      <div className="mt-4 text-4xl font-bold text-indigo-300">{value}</div>
    </div>
  );
};

export default StatsCard;
