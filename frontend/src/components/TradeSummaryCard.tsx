import { createChart } from "lightweight-charts";
import React, { useEffect, useRef } from "react";
import { Trade } from "../types/trade";

interface Props {
  trade: Trade;
  chartData?: any;
  onViewChart: () => void;
}

const TradeSummaryCard: React.FC<Props> = ({ trade, chartData, onViewChart }) => {
  const chartRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!chartData || !chartRef.current) return;
    const chart = createChart(chartRef.current, {
      width: 220,
      height: 80,
      layout: { background: { color: "#ffffff" }, textColor: "#111" },
      grid: { vertLines: { visible: false }, horzLines: { visible: false } },
      timeScale: { visible: false },
      rightPriceScale: { visible: false },
    });
    const candle = chart.addCandlestickSeries({
      upColor: "#22c55e",
      downColor: "#ef4444",
      borderVisible: false,
      wickUpColor: "#22c55e",
      wickDownColor: "#ef4444",
    });
    const times = chartData.times.slice(-30).map((t: string) => t.slice(0, 19));
    candle.setData(
      times.map((t: string, i: number) => ({
        time: t,
        open: chartData.opens[i],
        high: chartData.highs[i],
        low: chartData.lows[i],
        close: chartData.closes[i],
      }))
    );
    return () => chart.remove();
  }, [chartData]);

  // Duration in hours/mins
  const durMs =
    trade.closed_at && trade.opened_at
      ? new Date(trade.closed_at).getTime() - new Date(trade.opened_at).getTime()
      : 0;
  const hrs = Math.floor(durMs / 3600000);
  const mins = Math.floor((durMs % 3600000) / 60000);
  const duration = `${hrs}h ${mins}m`;

  const pnlColor = trade.pnl_inr && trade.pnl_inr > 0 ? "text-emerald-500" : "text-rose-500";

  return (
    <div className="rounded-2xl border border-gray-200 bg-white text-gray-800 shadow-md overflow-hidden flex flex-col w-[250px]">
      <div className="bg-orange-500 text-white p-2 px-4">
        <h2 className="text-sm font-semibold">{trade.symbol}</h2>
        <p className="text-xs opacity-90">Gold vs USD</p>
      </div>
      <div className="p-3 text-xs flex flex-col gap-1">
        <div className="flex justify-between">
          <span>Net P&L</span>
          <span className={`font-semibold ${pnlColor}`}>{trade.pnl_inr?.toFixed(2)} ₹</span>
        </div>
        <div className="flex justify-between">
          <span>Pips</span>
          <span>{(trade.pnl_points || 0).toFixed(2)}</span>
        </div>
        <div className="flex justify-between">
          <span>Duration</span>
          <span>{duration}</span>
        </div>
        <div className="flex justify-between">
          <span>Direction</span>
          <span className="font-semibold">{trade.side}</span>
        </div>
        <div className="flex justify-between">
          <span>Volume</span>
          <span>{trade.qty.toFixed(2)}</span>
        </div>
      </div>
      <div className="h-[80px]" ref={chartRef}></div>
      <button onClick={onViewChart} className="bg-orange-500 text-white text-sm py-2 hover:bg-orange-600">
        View Chart
      </button>
    </div>
  );
};

export default TradeSummaryCard;
