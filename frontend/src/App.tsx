import { useState } from "react";

interface RandomResponse {
  bits: string;
  as_num: number;
  bits_length: number;
  min?: number;
  max?: number;
}

function App() {
  const [data, setData] = useState<RandomResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const API = import.meta.env.VITE_API_URL;


  const get256 = async () => {
    setLoading(true);
    const res = await fetch(`${API}/`);
    const result = await res.json();
    setData(result);
    setLoading(false);
  };

  const getCustom = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);

    const form = new FormData(e.currentTarget);
    const length = form.get("length");
    const min = form.get("min");
    const max = form.get("max");

    let url = `${API}/random?length=${length}`;
    if (min && max) url += `&min=${min}&max=${max}`;

    const res = await fetch(url);
    const result = await res.json();
    setData(result);
    setLoading(false);
  };

  return (
    <div style={{
      fontFamily: "Inter, sans-serif",
      background: "#f5f5f5",
      minHeight: "100vh",
      padding: "40px"
    }}>
      <div style={{
        maxWidth: "700px",
        margin: "0 auto",
        background: "white",
        padding: "30px",
        borderRadius: "14px",
        boxShadow: "0 0 20px rgba(0,0,0,0.1)"
      }}>
        <h1 style={{ fontSize: "32px", fontWeight: 700, marginBottom: 20 }}>
          ⚛️ Quantum RNG
        </h1>

        <button
          onClick={get256}
          style={{
            padding: "10px 20px",
            background: "#4F46E5",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
            fontSize: "16px"
          }}
        >
          Generate 256-bit Random
        </button>

        <h2 style={{ marginTop: 30 }}>Custom Random Number</h2>
        <form
          onSubmit={getCustom}
          style={{
            display: "flex",
            gap: "10px",
            marginTop: "10px",
            marginBottom: "20px"
          }}
        >
          <input
            name="length"
            type="number"
            placeholder="Bit length"
            required
            style={{ flex: 1, padding: "10px", borderRadius: "8px" }}
          />
          <input
            name="min"
            type="number"
            placeholder="Min"
            style={{ width: "120px", padding: "10px", borderRadius: "8px" }}
          />
          <input
            name="max"
            type="number"
            placeholder="Max"
            style={{ width: "120px", padding: "10px", borderRadius: "8px" }}
          />
          <button
            type="submit"
            style={{
              padding: "10px 20px",
              background: "#2563EB",
              color: "white",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer"
            }}
          >
            Generate
          </button>
        </form>

        {loading && (
          <p style={{ fontSize: "16px", color: "#666" }}>
            🔮 Generating quantum randomness...
          </p>
        )}

        {data && (
          <pre style={{
            background: "#111",
            color: "#0f0",
            padding: "20px",
            borderRadius: "8px",
            marginTop: "20px",
            whiteSpace: "pre-wrap"
          }}>
            {JSON.stringify(data, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}

export default App;

