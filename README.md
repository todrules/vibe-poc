# vibe-poc

## Proposed Repository Structure

```text
vibe-poc/
├── backend/
│   ├── app/
│   │   ├── api/routes/           # API layer (FastAPI endpoints)
│   │   ├── core/                 # Config and shared app setup
│   │   ├── schemas/              # Request/response contracts
│   │   └── services/             # Business services (LLM + file parsing)
│   ├── tests/                    # Backend tests
│   └── requirements.txt
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/           # UI building blocks
│       └── services/             # API client layer
├── prompts/                      # Prompt templates for LLM generation
└── docs/
    └── development-plan.md       # Milestones and implementation steps
```

### Why this structure?

- **Clean architecture separation**: API routes, schemas, and services are isolated in backend.
- **Modular frontend**: Components and API service logic are split for maintainability.
- **Prompt-first design**: Prompt templates are externalized in `/prompts` so they can evolve without code changes.
- **Scalable onboarding**: `docs/development-plan.md` captures phased delivery and next steps.

## Scaffolding status

Initial scaffolding has been added for:
- FastAPI backend with a single `/generate` endpoint stub
- React frontend with requirement input and collapsible output sections
- Prompt template files for system/task/persona outputs
- Development plan and first implementation steps
