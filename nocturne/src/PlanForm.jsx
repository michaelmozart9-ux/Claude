import { useState } from "react";

export default function PlanForm({ onPlan }) {
  const [grade, setGrade] = useState("3");
  const [pieces, setPieces] = useState("");
  const [daysPerWeek, setDays] = useState(4);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ grade, pieces, daysPerWeek }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Something went wrong.");
      onPlan(data.plan, !!data.demo);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="card form" onSubmit={submit}>
      <label>
        What's your level?
        <select value={grade} onChange={(e) => setGrade(e.target.value)}>
          {Array.from({ length: 8 }, (_, i) => (
            <option key={i + 1} value={i + 1}>Grade {i + 1}</option>
          ))}
        </select>
      </label>

      <label>
        What pieces do you want to learn?
        <textarea
          required
          minLength={2}
          rows={3}
          placeholder={"e.g. Chopin Nocturne Op. 9 No. 2\nBach Prelude in C, BWV 846"}
          value={pieces}
          onChange={(e) => setPieces(e.target.value)}
        />
      </label>

      <label>
        How many days a week can you practise? <strong>{daysPerWeek}</strong>
        <input type="range" min="1" max="7" value={daysPerWeek} onChange={(e) => setDays(Number(e.target.value))} />
      </label>

      {error && <p className="error">{error}</p>}

      <button className="btn btn-primary" disabled={loading}>
        {loading ? "Composing your plan… (up to a minute)" : "Build my 6-week plan"}
      </button>
    </form>
  );
}
