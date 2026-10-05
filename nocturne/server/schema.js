import { z } from "zod";

export const InputSchema = z.object({
  grade: z.coerce.number().int().min(1).max(8),
  pieces: z.string().trim().min(2).max(1000),
  daysPerWeek: z.coerce.number().int().min(1).max(7),
});

const DaySchema = z.object({
  day: z.number().int(),
  focus: z.string(),
  minutes: z.number().int(),
  goals: z.array(z.string()),
  tempoTarget: z.string(),
});

const WeekSchema = z.object({
  week: z.number().int(),
  theme: z.string(),
  milestone: z.string(),
  days: z.array(DaySchema),
  tip: z.string(),
});

export const PlanSchema = z.object({
  summary: z.string(),
  pieces: z.array(
    z.object({
      title: z.string(),
      difficulty: z.string(),
      finalTempo: z.string(),
    }),
  ),
  weeks: z.array(WeekSchema),
  generalTips: z.array(z.string()),
});
