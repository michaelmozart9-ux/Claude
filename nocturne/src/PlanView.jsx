import { useEffect, useState } from "react";

const KEY = "nocturne-progress";

function loadProgress() {
  try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; }
}

export default function PlanView({ plan, demo, onReset }) {
  const [done, setDone] = useState(loadProgress);
  const [open, setOpen] = useState(1);

  useEffect(() => {
    try { localStorage.setItem(KEY, JSON.stringify(done)); } catch {}
  }, [done]);

  const total = plan.weeks.reduce((n, w) => n + w.days.length, 0);
  const completed = plan.weeks.reduce((n, w) => n + w.days.filter((d) => done[`${w.week}-${d.day}`]).length, 0);
  const pct = total ? Math.round((completed / total) * 100) : 0;

  return (
    <main className="plan">
      {demo && <p className="banner">Demo plan. Set ANTHROPIC_API_KEY on the server to get a real AI-generated plan.</p>}
      <div className="plan-head">
        <h1>Your 6-week roadmap</h1>
        <button className="btn btn-ghost" onClick={() => { setDone({}); onReset(); }}>New plan</button>
      </div>
      <p className="lede">{plan.summary}</p>

      <div className="pieces">
        {plan.pieces.map((p) => (
          <div key={p.title} className="card piece">
            <h3>{p.title}</h3>
            <p>{p.difficulty} · target {p.finalTempo}</p>
          </div>
        ))}
      </div>

      <div className="progress" aria-label={`${pct}% complete`}>
        <div className="bar"><div style={{ width: `${pct}%` }} /></div>
        <span>{completed}/{total} sessions · {pct}%</span>
      </div>

      {plan.weeks.map((w) => {
        const weekDone = w.days.every((d) => done[`${w.week}-${d.day}`]);
        return (
          <section key={w.week} className={`card week ${open === w.week ? "open" : ""}`}>
            <button className="week-head" onClick={() => setOpen(open === w.week ? 0 : w.week)}>
              <span className="wk">Week {w.week}{weekDone ? " ✓" : ""}</span>
              <span className="theme">{w.theme}</span>
              <span className="chev">{open === w.week ? "−" : "+"}</span>
            </button>
            {open === w.week && (
              <div className="week-body">
                <p className="milestone"><strong>Milestone:</strong> {w.milestone}</p>
                <div className="days">
                  {w.days.map((d) => {
                    const id = `${w.week}-${d.day}`;
                    return (
                      <label key={id} className={`day ${done[id] ? "done" : ""}`}>
                        <div className="day-top">
                          <input type="checkbox" checked={!!done[id]} onChange={() => setDone({ ...done, [id]: !done[id] })} />
                          <strong>Day {d.day}</strong>
                          <span className="meta">{d.minutes} min · {d.tempoTarget}</span>
                        </div>
                        <p className="focus">{d.focus}</p>
                        <ul>{d.goals.map((g) => <li key={g}>{g}</li>)}</ul>
                      </label>
                    );
                  })}
                </div>
                <p className="tip">💡 {w.tip}</p>
              </div>
            )}
          </section>
        );
      })}

      <section className="card">
        <h3>General tips</h3>
        <ul>{plan.generalTips.map((t) => <li key={t}>{t}</li>)}</ul>
      </section>
    </main>
  );
}
