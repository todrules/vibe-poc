# Development Plan

## Milestones

1. **Foundation setup**
   - Finalize project structure
   - Wire basic frontend + backend scaffolding
   - Add prompt template loading contracts

2. **Generation flow (MVP)**
   - Implement `/generate` flow end-to-end
   - Parse typed and uploaded requirements
   - Enforce strict JSON output schema

3. **UX and reliability**
   - Improve validation + error handling
   - Add test coverage for services and endpoint
   - Refine collapsible output presentation

4. **Production hardening**
   - Add observability and secure configuration
   - Add CI checks and deployment docs

## First 3 Implementation Steps

1. Implement backend prompt-loader + Azure OpenAI integration in `LLMService`.
2. Implement requirement normalization in `FileParserService` for text uploads and typed text.
3. Connect frontend form submit flow to `/generate` and render each output section from strict JSON.
