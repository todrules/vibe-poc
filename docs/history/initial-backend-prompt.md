You are my AI engineering partner. The backend scaffolding for this project already exists. 
Now I want you to generate the full Python implementation following PEP8 standards.

Project Summary:
This backend exposes a single POST /generate endpoint that accepts:
- requirements: string
- fileText: string (optional)

The backend must:
1. Merge the text inputs
2. Load prompt templates from the /prompts directory
3. Call Azure OpenAI using a dedicated LLM service
4. Return structured JSON containing:
   - acceptanceCriteria: list[{ title, gherkin }]
   - agentPrompts: { system, task, persona }
   - userStories: list[str]
   - testCases: list[str]

Architecture Requirements:
- Use FastAPI
- Use Pydantic models for request/response
- Use a service layer:
    - LLMService (loads templates, formats prompts, calls Azure OpenAI)
    - FileParserService (handles uploaded text)
- Keep code modular and clean
- Follow PEP8 strictly
- Add type hints everywhere
- Add docstrings for all classes and functions
- Add clear error handling and validation

What I want you to generate now:
1. The full implementation of main.py (FastAPI app + /generate route)
2. The LLMService implementation with placeholder Azure OpenAI call
3. The FileParserService implementation
4. The Pydantic models for request and response
5. Utility functions if needed
6. Comments explaining intent, but no placeholder logic beyond the Azure call

Rules:
- Do NOT change the folder structure.
- Do NOT generate prompt templates — those already exist.
- Do NOT generate frontend code.
- Follow PEP8 and modern FastAPI best practices.
- Keep the code production-ready and clean.

Begin by generating the Pydantic models and the LLMService implementation.
