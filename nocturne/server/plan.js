import Anthropic from "@anthropic-ai/sdk";
import { betaZodOutputFormat } from "@anthropic-ai/sdk/helpers/beta/zod";
import { PlanSchema } from "./schema.js";

const client = new Anthropic();

const SYSTEM = `You are an experienced piano teacher (ABRSM/RCM-style grades 1-8) who writes practical practice plans.
Build a 6-week roadmap for the student's pieces at their level and weekly availability.
- Exactly 6 weeks; each week has exactly as many practice days as the student can practise, numbered 1..N.
- Daily goals are concrete and checkable (bars, hands, tempo, technique), 2-4 per day.
- tempoTarget is a metronome marking, e.g. "♩ = 72", rising realistically toward the performance tempo by week 6.
- Session length (minutes) fits the grade: roughly 20-30 for grades 1-3, 30-45 for 4-6, 45-60 for 7-8.
- If a piece is far above or below the stated grade, say so plainly in the summary and adjust the plan.
- Weekly milestones are something the student can verify (e.g. "Section A hands together at ♩ = 80, no stops").`;

export async function generatePlan({ grade, pieces, daysPerWeek }) {
  const response = await client.beta.messages.parse({
    model: "claude-opus-5-5",
    max_tokens: 32000,
    betas: ["server-side-fallback-2026-07-01"],
    fallbacks: "default",
    output_config: { effort: "medium", format: betaZodOutputFormat(PlanSchema) },
    system: SYSTEM,
    messages: [
      {
        role: "user",
        content: `Level: Grade ${grade}\nPractice days per week: ${daysPerWeek}\nPieces I want to learn:\n${pieces}`,
      },
    ],
  });

  if (response.stop_reason === "refusal") throw new Error("The request was declined. Try rephrasing your pieces.");
  if (response.stop_reason === "max_tokens") throw new Error("The plan was too long to generate. Try fewer pieces.");
  if (!response.parsed_output) throw new Error("Could not read the generated plan. Please try again.");
  return response.parsed_output;
}
