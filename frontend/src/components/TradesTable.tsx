import React, { useMemo, useState } from "react";
import { Trade } from "../types/trade";

interface Props {
  trades: Trade[];
  onViewChart: (trade: Trade) => void;
}

const TradesTable: React.FC<Props> = ({ trades, onViewChart }) => {
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    if (!query.trim()) return trades;
    return trades.filter((t) => String(t.id).includes(query.trim()));
  }, [trades, query]);

  return (
    <div className="card mt-6">
      <div className="flex items-center justify-between px-4 pt-4">
        <h2 className="text-lg font-semibold">Active Trades</h2>
        <div className="relative">
          <input
            placeholder="Search by ID..."
            className="pl-9 pr-3 py-2 rounded-lg bg-panel border border-white/10 text-sm outline-none"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <span className="absolute left-2 top-2.5 text-gray-400">🔍</span>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full text-sm text-gray-300">
          <thead className="bg-panel text-gray-400 uppercase text-xs">
            <tr>
              <th className="px-3 py-2 text-left">ID</th>
              <th className="px-3 py-2">Side</th>
              <th className="px-3 py-2">Entry</th>
              <th className="px-3 py-2">Exit</th>
              <th className="px-3 py-2">SL</th>
              <th className="px-3 py-2">TP</th>
              <th className="px-3 py-2">Status</th>
              <th className="px-3 py-2">P&L (₹)</th>
              <th className="px-3 py-2">Opened</th>
              <th className="px-3 py-2">Closed</th>
              <th className="px-3 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((t) => (
              <tr key={t.id} className="border-t border-stroke hover:bg-white/5">
                <td className="px-3 py-2">{t.id}</td>
                <td className={`px-3 py-2 font-bold ${t.side === "BUY" ? "text-emerald-400" : "text-rose-400"}`}>{t.side}</td>
                <td className="px-3 py-2">{t.entry_price?.toFixed(2)}</td>
                <td className="px-3 py-2">{t.exit_price ? t.exit_price.toFixed(2) : "—"}</td>
                <td className="px-3 py-2">{t.sl?.toFixed(2)}</td>
                <td className="px-3 py-2">{t.tp?.toFixed(2)}</td>
                <td className="px-3 py-2">{t.status}</td>
                <td className={`px-3 py-2 ${t.pnl_inr && t.pnl_inr > 0 ? "text-emerald-400" : "text-rose-400"}`}>
                  {t.pnl_inr ? Math.round(t.pnl_inr) : "—"}
                </td>
                <td className="px-3 py-2 text-xs">{t.opened_at?.replace("T", " ").slice(0, 19)}</td>
                <td className="px-3 py-2 text-xs">{t.closed_at ? t.closed_at.replace("T", " ").slice(0, 19) : "—"}</td>
                <td className="px-3 py-2">
                  {t.status === "CLOSED" ? (
                    <button
                      onClick={() => onViewChart(t)}
                      className="px-3 py-1 rounded-lg bg-indigo-600 hover:bg-indigo-700"
                    >
                      View Chart
                    </button>
                  ) : (
                    <span className="text-gray-500">—</span>
                  )}
                </td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr>
                <td className="px-3 py-6 text-center text-gray-500" colSpan={11}>
                  No trades yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TradesTable;
