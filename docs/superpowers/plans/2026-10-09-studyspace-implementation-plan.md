# StudySpace implementation plan

## Scope
Implement the approved browser-only React + Vite + TypeScript study tool using the eight attached course documents. The user explicitly requested implementation in this turn. No server or user registration.

## Workstreams
1. Convert and organize local source documents for the PDF viewer. Keep copyright clearance as a required pre-deployment gate.
2. Extract reusable subject/topic/reviewer content, create curated source-cited questions and flashcards.
3. Implement source-verified grading and session/timing/persistence modules with stable IDs and idempotent attempt storage.
4. Implement responsive application shell and all approved routes (dashboard, subjects, reviewer, flashcards, exams, results, progress, document viewer).
5. Add schema/content validation, domain tests and deployment configuration.
6. Run available static/functional validation, record limitations from missing npm internet access, and package source.

## Release constraints
- Do not publish lecture source files without rights confirmation.
- No fabricated course facts; all authored questions have source location and explanation.
- Node deps must install in a networked environment if unavailable offline here.
- Document original copies bundled for local use; Vercel deployment must exclude private content until cleared.
