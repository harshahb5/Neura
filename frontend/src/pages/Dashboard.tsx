import React, { useEffect, useState } from "react";
import Header from "../components/Header";
import StatsCard from "../components/StatsCard";
import TradeChartModal from "../components/TradeChartModal";
import TradesTable from "../components/TradesTable";
import TradeSummaryCard from "../components/TradeSummaryCard";
import { Trade } from "../types/trade";
import { api } from "../utils/api";

const Dashboard: React.FC = () => {
  const [tradingActive, setTradingActive] = useState(true);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [pnlToday, setPnlToday] = useState(0);
  const [chartData, setChartData] = useState<any>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const fetchTrades = async () => {
    const res = await api.get("/api/trades");
    const data: Trade[] = res.data;
    setTrades(data);

    const today = new Date().toISOString().slice(0, 10);
    let pnl = 0;
    data.forEach((t) => {
      if (t.closed_at && t.closed_at.slice(0, 10) === today) {
        pnl += t.pnl_inr || 0;
      }
    });
    setPnlToday(pnl);
  };

  const handleViewChart = async (trade: Trade) => {
    const res = await api.get(`/api/chart/${trade.id}`);
    setChartData(res.data);
    setModalOpen(true);
  };

  useEffect(() => {
    fetchTrades();
    const interval = setInterval(fetchTrades, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen px-6">
      <Header tradingActive={tradingActive} onToggle={() => setTradingActive((v) => !v)} />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-4">
        <StatsCard title="Today's P&L (₹)" value={pnlToday.toFixed(2)} />
        <StatsCard title="Open Trades" value={trades.filter((t) => t.status === "OPEN").length} />
        <StatsCard title="Symbol" value="XAUUSD" />
      </div>

      <TradesTable trades={trades} onViewChart={handleViewChart} />
      {/* Closed trade summary cards */}
      {trades.filter(t => t.status === "CLOSED").length > 0 && (
        <div className="mt-8">
        <h3 className="text-lg font-semibold mb-3">Completed Trades</h3>
        <div className="flex flex-wrap gap-5">
        {trades.filter(t => t.status === "CLOSED").slice(0, 6).map(t => (
          <TradeSummaryCard
          key={t.id}
          trade={t}
          chartData={chartData}
          onViewChart={() => handleViewChart(t)}
          />
        ))}
          </div>
        </div>
        )}

      <TradeChartModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        chartData={chartData}
      />

      <footer className="flex items-center justify-between mt-10 text-gray-500 text-sm border-t border-white/10 pt-4">
        <p>© 2025 Neura | Built by Harshavardhan G R</p>
        <div className="flex items-center gap-4">
          <a
            href="https://www.linkedin.com/in/harshavardhan-g-r-538005215"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-indigo-400 transition"
            aria-label="LinkedIn"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" className="w-5 h-5" viewBox="0 0 24 24">
              <path d="M19 0H5A5 5 0 0 0 0 5v14a5 5 0 0 0 5 5h14a5 5 0 0 0 5-5V5a5 5 0 0 0-5-5ZM8 19H5V9h3v10ZM6.5 7.7A1.75 1.75 0 1 1 8.25 6 1.74 1.74 0 0 1 6.5 7.7ZM20 19h-3v-5.6c0-1.3-.03-3.1-1.9-3.1s-2.2 1.5-2.2 3v5.7h-3V9h2.9v1.4h.1c.4-.8 1.4-1.6 2.9-1.6 3.1 0 3.8 2 3.8 4.6V19Z"/>
            </svg>
          </a>
          <a
            href="https://github.com/harsha2002gr"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-indigo-400 transition"
            aria-label="GitHub"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" className="w-5 h-5" viewBox="0 0 24 24">
              <path d="M12 .5A11.5 11.5 0 0 0 .5 12c0 5.08 3.29 9.4 7.86 10.93.58.1.79-.26.79-.57v-2c-3.2.7-3.88-1.56-3.88-1.56-.53-1.36-1.3-1.74-1.3-1.74-1.07-.73.08-.72.08-.72 1.17.08 1.79 1.21 1.79 1.21 1.04 1.78 2.73 1.27 3.4.97.1-.76.41-1.27.74-1.56-2.55-.29-5.23-1.28-5.23-5.7 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.47.11-3.06 0 0 .97-.31 3.18 1.18.92-.26 1.9-.4 2.88-.4.99 0 1.97.13 2.9.39 2.2-1.49 3.18-1.18 3.18-1.18.63 1.59.23 2.77.12 3.06.74.81 1.19 1.84 1.19 3.1 0 4.43-2.69 5.4-5.25 5.69.42.36.79 1.08.79 2.18v3.22c0 .31.21.67.8.57A11.5 11.5 0 0 0 23.5 12C23.5 5.74 18.27.5 12 .5Z"/>
            </svg>
          </a>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
