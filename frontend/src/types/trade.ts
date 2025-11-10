export interface Trade {
  id: number;
  symbol: string;
  side: "BUY" | "SELL";
  qty: number;
  entry_price: number;
  sl: number;
  tp: number;
  opened_at: string;
  status: "OPEN" | "CLOSED";
  exit_price?: number;
  closed_at?: string;
  pnl_points?: number;
  pnl_inr?: number;
  note?: string;
}
