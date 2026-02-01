import { useState } from "react";
import "./App.css";

export default function App() {
  const [a, setA] = useState<string>("");
  const [b, setB] = useState<string>("");
  const [op, setOp] = useState<string>("+");
  const [result, setResult] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const calculate = async () => {
    setError(null);
    setResult(null);

    try {
      const res = await fetch("/api/calc", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          a: Number(a),
          b: Number(b),
          op: op,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data?.error ?? "error");
      } else {
        setResult(data.result);
      }
    } catch {
      setError("backend not reachable");
    }
  };

  return (
    <div className="page">
      <h2>Calculator</h2>

      <div className="row">
        <input
          placeholder="a"
          value={a}
          onChange={(e) => setA(e.target.value)}
        />

        <select value={op} onChange={(e) => setOp(e.target.value)}>
          <option value="+">+</option>
          <option value="-">-</option>
          <option value="*">*</option>
          <option value="/">/</option>
        </select>

        <input
          placeholder="b" 
          value={b}
          onChange={(e) => setB(e.target.value)}
        />

        <button onClick={calculate}>Calculate</button>
      </div>

      <div className="output">
        {result !== null && <div>Result: {result}</div>}
        {error && <div className="error">{error}</div>}
      </div>
    </div>
  );
}
