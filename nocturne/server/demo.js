// Used when ANTHROPIC_API_KEY is not set, so the UI can be tried without a key.
export function demoPlan({ grade, pieces, daysPerWeek }) {
  const titles = pieces.split(/\n|,/).map((s) => s.trim()).filter(Boolean).slice(0, 3);
  const themes = ["Read & map", "Hands separate", "Hands together", "Shape & dynamics", "Build tempo", "Performance ready"];
  const tempos = [50, 58, 66, 74, 84, 96];
  return {
    summary: `DEMO PLAN (no API key set). A 6-week roadmap for Grade ${grade}, ${daysPerWeek} days/week.`,
    pieces: titles.map((title) => ({ title, difficulty: `~Grade ${grade}`, finalTempo: "♩ = 96" })),
    weeks: themes.map((theme, i) => ({
      week: i + 1,
      theme,
      milestone: `${theme}: whole piece at ♩ = ${tempos[i]} with no stops`,
      tip: "Practise the hardest bars first while you're fresh.",
      days: Array.from({ length: daysPerWeek }, (_, d) => ({
        day: d + 1,
        focus: `${titles[d % titles.length] ?? "Piece"} — section ${String.fromCharCode(65 + (d % 3))}`,
        minutes: 30,
        goals: ["Scales warm-up (5 min)", `Bars ${d * 8 + 1}-${d * 8 + 8}, slow and even`, "One full run-through"],
        tempoTarget: `♩ = ${tempos[i]}`,
      })),
    })),
    generalTips: ["Use a metronome every session.", "Record yourself once a week.", "Stop before you're tired."],
  };
}
