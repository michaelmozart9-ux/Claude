# NOCTURNE — AI Piano Practice Planner (MVP)

Grade + pieces + days/week → Claude generates a 6-week practice roadmap (daily goals, weekly milestones, tempo targets).

## Run

```bash
cd nocturne
npm install
cp .env.example .env   # add your ANTHROPIC_API_KEY
npm run dev            # frontend http://localhost:5173, API :3001
```

Without a key the API returns a **demo plan** so the UI still works.

Production: `npm run build && npm start` (Express serves `dist/` + `/api/plan` on `PORT`, default 3001).

## Structure

- `server/plan.js`: Claude call (`claude-opus-5-5`, structured output validated by Zod, server-side refusal fallback)
- `server/schema.js`: input and plan schemas
- `src/`: React UI (form → results with progress tracker, saved in localStorage)

Not in MVP: auth, Supabase, Lemon Squeezy. The "Create Your Free Trial" button is a placeholder.
