import React from "react";

interface Props {
  tradingActive: boolean;
  onToggle: () => void;
}

const Header: React.FC<Props> = ({ tradingActive, onToggle }) => {
  return (
    <header className="flex items-center justify-between py-5">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-xl bubble flex items-center justify-center">
          <span className="text-indigo-300 font-black">🧠</span>
        </div>
        <div>
          <h1 className="text-2xl font-bold text-white">Neura</h1>
          <p className="text-[12px] text-gray-400 -mt-0.5">EMA 9/15 Auto Trader</p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-emerald-500/10 border border-emerald-400/20">
          <span className={`h-2 w-2 rounded-full ${tradingActive ? "bg-emerald-400" : "bg-gray-500"}`}></span>
          <span className="text-sm text-gray-300">{tradingActive ? "Trading Active" : "Trading Paused"}</span>
        </div>

        <button
          onClick={onToggle}
          className={`px-4 py-2 rounded-lg font-semibold shadow-soft transition ${
            tradingActive ? "bg-rose-500 hover:bg-rose-600" : "bg-indigo-600 hover:bg-indigo-700"
          }`}
        >
          {tradingActive ? "Pause Trading" : "Resume Trading"}
        </button>
      </div>
    </header>
  );
};

export default Header;
