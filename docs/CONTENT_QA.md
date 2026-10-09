# Content & QA report

## Source coverage

- 8 PDF-viewable local sources: 3 Java lectures, 2 GNED reviewers, 3 racket-sport lectures.
- 14 study topics, 152 source-page lesson excerpts, 125 authored questions, 170 flashcards.
- Formats: 86 MCQ, 18 True/False, 15 Identification, 6 Java Code Analysis.
- GNED 10 Media source includes a self-described incomplete chapter summary; the reviewer page and website preserve that limitation.

## Verified by local tools in the packaging environment

- Content schema and source page bounds: `node scripts/check-content.mjs`.
- Domain engine syntax and scoring assertions: `npm run check:engine` (requires TypeScript after npm install); 259 local assertions passed.
- Java analysis examples compiled and executed with `javac`, and deliberately invalid Java examples produced expected compilation errors (6/6 checked).
- Converted slides to PDF and reviewed visual output for pickleball court markings page 14.

## Not verified here

The npm registry was unreachable in the sandbox environment. A complete Vite production bundle, typecheck against React/Router/Lucide libraries, Lighthouse metrics and browser E2E suite must be run after dependency installation.

## Rights gate

The source documents were provided for generating this study project, but that does not establish rights to redistribute them publicly. The default build excludes `/materials` PDFs from `dist`. Confirm publication permission before using `build:with-documents`.

## Recommended release test order

1. `npm install`
2. `npm run check:content && npm run check:engine && npm test`
3. `npm run build && npm run preview`
4. `npx playwright install chromium && npm run test:e2e`
5. Lighthouse mobile + desktop; review visual QA and document permissions.
