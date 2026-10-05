import { useEffect, useState } from "react";
import PlanForm from "./PlanForm.jsx";
import PlanView from "./PlanView.jsx";

const PLAN_KEY = "nocturne-plan";

function loadSaved() {
  try { return JSON.parse(localStorage.getItem(PLAN_KEY)); } catch { return null; }
}

export default function App() {
  const [saved] = useState(loadSaved);
  const [plan, setPlan] = useState(saved?.plan ?? null);
  const [demo, setDemo] = useState(!!saved?.demo);

  useEffect(() => {
    try {
      if (plan) localStorage.setItem(PLAN_KEY, JSON.stringify({ plan, demo }));
      else localStorage.removeItem(PLAN_KEY);
    } catch {}
  }, [plan, demo]);

  return (
    <>
      <header className="nav">
        <span className="logo">NOCTURNE</span>
        <a className="btn btn-ghost" href="#trial">Free trial</a>
      </header>

      {plan ? (
        <PlanView plan={plan} demo={demo} onReset={() => setPlan(null)} />
      ) : (
        <main>
          <section className="hero">
            <Keys />
            <h1>Practise with a plan, not with guilt.</h1>
            <p className="lede">
              Tell NOCTURNE your grade, your pieces and how often you can play. Get a 6-week roadmap with daily
              goals, weekly milestones and metronome targets.
            </p>
          </section>
          <PlanForm onPlan={(p, isDemo) => { setPlan(p); setDemo(isDemo); window.scrollTo(0, 0); }} />
          <section className="how">
            {[
              ["1", "Your level", "Grade 1 to 8, so the plan matches your hands."],
              ["2", "Your pieces", "Anything from Clementi sonatinas to Chopin nocturnes."],
              ["3", "Your week", "1 to 7 days. The plan fits your life, not the other way round."],
            ].map(([n, t, d]) => (
              <div key={n} className="step">
                <span className="num">{n}</span>
                <h3>{t}</h3>
                <p>{d}</p>
              </div>
            ))}
          </section>
        </main>
      )}

      <Trial />
      <footer className="foot">© {new Date().getFullYear()} NOCTURNE</footer>
    </>
  );
}

function Keys() {
  const black = [1, 2, 4, 5, 6];
  return (
    <div className="keys" aria-hidden="true">
      {Array.from({ length: 7 }, (_, i) => (
        <div key={i} className="white">{black.includes(i) && <div className="black" />}</div>
      ))}
    </div>
  );
}

function Trial() {
  return (
    <section id="trial" className="trial">
      <h2>Keep your roadmap going</h2>
      <p>Save plans, track progress and get a new roadmap every 6 weeks.</p>
      <button className="btn btn-primary" onClick={() => alert("Trial sign-up is coming soon.")}>
        Create Your Free Trial
      </button>
      <small>7 days free · no card required</small>
    </section>
  );
}
