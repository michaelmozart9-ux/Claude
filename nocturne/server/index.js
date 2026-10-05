import express from "express";
import { fileURLToPath } from "node:url";
import { InputSchema } from "./schema.js";
import { generatePlan } from "./plan.js";
import { demoPlan } from "./demo.js";

const app = express();
app.use(express.json({ limit: "20kb" }));

app.post("/api/plan", async (req, res) => {
  const input = InputSchema.safeParse(req.body);
  if (!input.success) return res.status(400).json({ error: "Please fill in your grade, pieces, and practice days." });

  if (!process.env.ANTHROPIC_API_KEY) return res.json({ plan: demoPlan(input.data), demo: true });

  try {
    res.json({ plan: await generatePlan(input.data) });
  } catch (err) {
    console.error(err);
    res.status(502).json({ error: err.message || "Plan generation failed." });
  }
});

const dist = fileURLToPath(new URL("../dist", import.meta.url));
app.use(express.static(dist));

const port = process.env.PORT || 3001;
app.listen(port, () => console.log(`NOCTURNE API on http://localhost:${port}`));
