import { createChart, IChartApi } from "lightweight-charts";
import React, { useEffect, useRef } from "react";
import Modal from "react-modal";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  chartData: any | null;
}

const TradeChartModal: React.FC<Props> = ({ isOpen, onClose, chartData }) => {
  const chartContainerRef = useRef<HTMLDivElement | null>(null);
  const chartRef = useRef<IChartApi | null>(null);

  useEffect(() => {
    if (!isOpen || !chartContainerRef.current || !chartData) return;

    // destroy previous instance
    if (chartRef.current) {
      chartRef.current.remove();
      chartRef.current = null;
    }

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 520,
      layout: { background: {color: "#0f172a" }, textColor: "#e6edf3" },
      grid: { vertLines: { color: "rgba(255,255,255,0.05)" }, horzLines: { color: "rgba(255,255,255,0.05)" } },
      rightPriceScale: { borderVisible: false },
      timeScale: { borderVisible: false },
      crosshair: { mode: 1 }
    });

    chartRef.current = chart;

    const candle = chart.addCandlestickSeries({
      upColor: "#16a34a",
      downColor: "#ef4444",
      wickUpColor: "#16a34a",
      wickDownColor: "#ef4444",
      borderVisible: false
    });

    const ema9 = chart.addLineSeries({ color: "#60a5fa", lineWidth: 2 });
    const ema15 = chart.addLineSeries({ color: "#fb923c", lineWidth: 2 });

    const times = chartData.times.map((t: string) => t.slice(0, 19));
    candle.setData(
      times.map((t: string, i: number) => ({
        time: t,
        open: chartData.opens[i],
        high: chartData.highs[i],
        low: chartData.lows[i],
        close: chartData.closes[i],
      }))
    );
    ema9.setData(times.map((t: string, i: number) => ({ time: t, value: chartData.ema9[i] })));
    ema15.setData(times.map((t: string, i: number) => ({ time: t, value: chartData.ema15[i] })));

    // horizontal SL/TP lines
    const drawHLine = (price: number, color: string) => {
      const line = chart.addLineSeries({ color, lineWidth: 1 });
      line.setData([{ time: times[0], value: price }, { time: times[times.length - 1], value: price }]);
      return line;
    };
    if (chartData.sl) drawHLine(chartData.sl, "rgba(248,113,113,.7)");
    if (chartData.tp) drawHLine(chartData.tp, "rgba(74,222,128,.7)");

    // entry/exit markers
    const markers: any[] = [];
    if (chartData.entry) {
      markers.push({ time: times[Math.max(0, times.length - 3)], position: "belowBar", color: "#38bdf8", shape: "arrowUp", text: `Entry ${chartData.entry.toFixed(2)}` });
    }
    if (chartData.exit) {
      markers.push({ time: times[times.length - 1], position: "aboveBar", color: "#f87171", shape: "arrowDown", text: `Exit ${chartData.exit.toFixed(2)}` });
    }
    candle.setMarkers(markers);

    const onResize = () => chart.applyOptions({ width: chartContainerRef.current!.clientWidth });
    window.addEventListener("resize", onResize);
    return () => {
      window.removeEventListener("resize", onResize);
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
      }
    };
  }, [isOpen, chartData]);

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onClose}
      style={{
        content: { backgroundColor: "#0b0f1a", border: "1px solid #1e293b", borderRadius: "16px", inset: "5% 10%" },
        overlay: { backgroundColor: "rgba(0,0,0,.5)" }
      }}
    >
      <h2 className="text-lg font-semibold text-white mb-2">Trade Chart</h2>
      <div ref={chartContainerRef}></div>
      <button onClick={onClose} className="mt-4 px-4 py-2 bg-indigo-600 rounded-md hover:bg-indigo-500">
        Close
      </button>
    </Modal>
  );
};

export default TradeChartModal;
