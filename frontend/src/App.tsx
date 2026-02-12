import { useState } from "react";
import "./App.css";

type HistoryItem = {
  id: number;
  a: number;
  b: number;
  op: string;
  result: number;
  created_at: string;
};

export default function App() {
  const [a, setA] = useState<string>("");
  const [b, setB] = useState<string>("");
  const [op, setOp] = useState<string>("+");
  const [result, setResult] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);

  async function loadHistory(limit = 10) {
    const res = await fetch(`/api/history?limit=${limit}`);
    if (!res.ok) return;
    const data = await res.json();
    setHistory(data.items || []);
  }

  const calculate = async () => {
    setError(null);
    setResult(null);

    try {
      const res = await fetch("/api/calc", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ a: Number(a), b: Number(b), op }),
      });

      const text = await res.text();
      let data: any = {};
      try {
        data = JSON.parse(text);
      } catch {
        data = { error: text || "unexpected response" };
      }

      if (!res.ok) {
        setError(data?.error ?? "error");
      } else {
        setResult(data.result);
        await loadHistory(10);
      }
    } catch {
      setError("backend not reachable");
    }
  };

  return (
    <div className="page">
      <h2>Calculator</h2>

      <div className="row">
        <input placeholder="a" value={a} onChange={(e) => setA(e.target.value)} />

        <select value={op} onChange={(e) => setOp(e.target.value)}>
          <option value="+">+</option>
          <option value="-">-</option>
          <option value="*">*</option>
          <option value="/">/</option>
        </select>

        <input placeholder="b" value={b} onChange={(e) => setB(e.target.value)} />

        <button onClick={calculate}>Calculate</button>
      </div>

      <div className="output">
        {result !== null && <div>Result: {result}</div>}
        {error && <div className="error">{error}</div>}
      </div>

      <button onClick={() => loadHistory(10)}>History</button>

      <div>
        {history.map((h) => (
          <div key={h.id}>
            {h.a} {h.op} {h.b} = {h.result} ({h.created_at})
          </div>
        ))}
      </div>
    </div>
  );
}
