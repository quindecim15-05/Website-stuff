# StudySpace Visual System

## Purpose
A focused study platform for classmates: exam preparation first, productivity-app clarity over decorative UI. No fake dashboard values, login, or marketing theatrics.

## Design principles
- Light-first modern productivity dashboard, minimalist but with recognizable brand personality.
- Blue primary (`#2563EB`), off-white canvas (`#F6F8FC`), white surfaces (`#FFFFFF`), dark ink (`#172033`), cool gray borders (`#E2E8F0`).
- Plus Jakarta Sans for app typography, JetBrains Mono for Java snippets, Lucide outline icons.
- Desktop sidebar, compact mobile navigation drawer. Focused exam layout hides regular dashboard nav.
- Visible focus indicators, generous answer tap targets, reduced-motion support.
- Feedback uses semantic color only where meaningful (correct, incorrect, warnings).

## UI conventions
- Page: eyebrow → clear headline → short supporting description.
- Dashboard: clear action-oriented welcome panel → quick actions → subject library → real local progress.
- Reviewer: tabs for quick/detailed reading, page reference in each source section, context links to flashcards/exams.
- Exams: one question per screen, separate navigation panel, flagged/answered states, timer above, input first.
- Results: score, topic breakdown, actionable answer review, retry mistakes.
- Cards represent real selectable objects, not used as unnecessary nesting.

## Design skill provenance
- UI UX Pro Max — https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Hallmark — https://github.com/Nutlope/hallmark
- Vercel Agent Skills — https://github.com/vercel-labs/agent-skills
- Impeccable — https://github.com/pbakaus/impeccable

## Visual QA checklist
- Test 375/768/1024/1440 widths; mobile question navigator must be accessible.
- No text overlap in long questions/Java snippets or original PDF viewer.
- Check empty data, paused exam, expired timer, source unavailable and storage unavailable states.
- Validate contrast, focus, predictable actions, and motion reduction.
