You are my AI engineering partner. We are starting a brand‑new project from scratch.

Goal:
Create a full-stack application that takes user requirements (typed or uploaded as text) and generates:
1. Acceptance criteria (Gherkin format)
2. Agent prompts (system, task, persona)
3. User stories
4. Test cases

Architecture:
- Frontend: React (clean components, minimal styling, collapsible output sections)
- Backend: FastAPI with a single /generate endpoint
- Backend services:
  - LLM service that loads prompt templates and calls Azure OpenAI
  - File parser service for uploaded text
- Prompt templates stored in a /prompts folder
- Strict JSON output from the LLM

What I want from you right now:
1. Propose a clean folder structure for the entire repo.
2. Generate initial scaffolding files (empty or lightly commented).
3. Create a development plan with milestones.
4. Suggest the first 3 implementation steps I should take.
5. Follow clean architecture principles and keep code modular.

Rules:
- Do NOT generate full implementations yet—only scaffolding and structure.
- Use clear comments to explain intent.
- Assume I will refine everything with you step-by-step.

Begin by proposing the folder structure and explaining your reasoning.
