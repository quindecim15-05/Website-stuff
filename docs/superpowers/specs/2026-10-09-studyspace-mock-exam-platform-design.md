# StudySpace — Mock Exam & Study Platform

**Design specification**  
**Date:** 2026-10-09  
**Status:** Approved by user on 2026-10-09 for implementation  
**Process:** Superpowers `brainstorming` — architectural path  
**Scope:** Frontend-only React application for the requester and classmates  
**Basis:** Approved design Sections 1–5 and eight uploaded course materials  
**Working product name:** StudySpace (can be renamed without changing architecture)

## 1. Intent, Success Criteria & Boundaries

### 1.1 Product intent

Provide a shareable, account-free study workspace where classmates can read source-based lessons, review flip flashcards, practice questions with immediate feedback, take configurable mock examinations, understand mistakes, and monitor their **own browser-local progress**. The product is a self-study simulation, **not an official, proctored, or cheat-proof examination platform**.

### 1.2 Non-negotiable constraints

- **No backend, server database, accounts, authentication, or cloud synchronization.** A static Vite build contains the content; React/TypeScript handles interactions. Browser `localStorage` stores device-local study records.
- The **eight supplied sources** are the initial, authoritative scope for reviewer facts, flashcards, and graded questions. Unsupported claims are not invented. Content preparation and verification happen before publication; no runtime AI or Java execution.
- Site visitors do not upload documents or edit the question bank; content updates happen in source control and a new static deployment.
- The four exam formats are multiple choice, True/False, identification, and Java code analysis; both Practice and Mock Exam modes exist; exam coverage can be subject-based, topic-based, or mixed.
- Original source documents are accessed through an integrated browser-viewable PDF viewer **only if distribution permission is secured**. The site will have no dedicated download button; web-delivered PDFs cannot be made non-downloadable.
- Students' saved activity is personal to their browser profile. It may be lost when site data is cleared, private browsing ends, or devices change.

### 1.3 User and success criteria

**Primary users:** requester and classmates preparing for DCIT 50, GNED 07, GNED 10, and PATHFIT 3. No onboarding account is required. Students can open the link, choose any subject and learning mode, complete supported questions, review explanations and references, and return to their saved progress on the same browser.

**The product succeeds when:** all published material is verifiably source-grounded; all four question formats grade consistently; the exact question sequence and timer recover after refresh; submissions produce a single durable result when browser storage permits; the learning experience works on supported desktop/mobile browsers and with keyboard navigation; and a deployable static site passes the defined QA gates.

### 1.4 Explicitly excluded from the initial release

User accounts, leaderboards, social sharing of scores, classwide reporting, official grade submission, live multiplayer, runtime content upload, AI question generation, AI-written grading, remote analytics tied to students, Java code compilation in the browser, spaced-repetition scheduling, guaranteed offline access, and any server synchronization.

## 2. Information Architecture & User Journeys (Approved Section 1)

### 2.1 Primary navigation

Six destinations: **Dashboard**, **Subjects**, **Reviewer**, **Flashcards**, **Exams**, and **Progress**. The source document viewer is a contextual route, not a seventh main-nav item. Desktop uses a persistent sidebar; mobile uses a keyboard-accessible navigation drawer. During an exam, the normal dashboard shell is replaced by the focused examination shell.

### 2.2 Routes

| Route | Purpose |
|---|---|
| `/` | Dashboard and recent activity |
| `/subjects` | Four-subject library |
| `/subjects/:subjectId` | Topic overview and subject actions |
| `/study/:subjectId/:topicId` | Quick Summary / Detailed Lesson |
| `/flashcards` | Filtered flashcard session |
| `/exams` | Choose subject-, topic-, or mixed exam |
| `/exams/new` | Mode, preset, filters, and start confirmation |
| `/exam/:sessionId` | Active Practice or Mock Exam |
| `/results/:attemptId` | Completed result and question-by-question review |
| `/progress` | Attempt history, weak topics, flashcard mastery, local-data controls |
| `/materials/:sourceId` | Source PDF viewer with validated page reference |

Unknown IDs, deleted local attempts, missing sources, or incompatible saved sessions yield explicit recovery/empty states rather than crashes. Direct route refresh works through an SPA-host fallback.

### 2.3 Core journeys

1. **Study:** Dashboard/Subjects → subject → topic → Quick Summary or Detailed Lesson → optional original document → related flashcards or Practice Mode.
2. **Assess:** Exams → subject/topic/mixed coverage → Practice or Mock Exam → preset/custom configuration → question navigator → submission review → results → explanations / weak-topic practice / retry mistakes.
3. **Return:** Dashboard → continue the most recent valid session, or retrieve prior results from local attempt history. For an expired timed mock exam, the return path first finalizes the saved answers and then opens Results.

No lesson-completion prerequisite blocks exams or flashcards.

## 3. Visual Design & Screen Specifications (Approved Section 2)

### 3.1 Visual direction and tokens

**Modern Productivity Dashboard**, light-first, student-oriented, clean and readable, without generic corporate SaaS decoration.

| Token | Proposed value |
|---|---|
| Primary action/accent | `#2563EB` blue |
| App canvas | `#F6F8FC` |
| Surfaces | `#FFFFFF` |
| Main text | `#172033` |
| Dividers / borders | `#E2E8F0` |
| Interface type | Plus Jakarta Sans, fallback sans-serif |
| Java code | JetBrains Mono, fallback monospace |
| Icons | Lucide |
| Styling | Tailwind CSS with shared semantic tokens |

Use clear type scale, restrained elevation, comfortable spacing, accessible contrast, and limited card nesting. Avoid gratuitous gradients, emoji icons, decorative 3D elements, bounce animations, and invented progress metrics. All buttons, radio controls, inputs, and navigation states must show selection, hover/focus, disabled, and error behavior. Support `prefers-reduced-motion`.

### 3.2 Page requirements

| Page | Required layout and interactions |
|---|---|
| **Dashboard** | Welcome and continue panel; Quick Actions (Reviewer, Flashcards, Exams); four subjects; recent activity and actual local progress. First visit shows a helpful empty state, **not example statistics**. |
| **Subjects** | Searchable four-subject list; distinct subject overview with topics, supported question counts, and actions to study, use flashcards, practice, or take a mock exam. |
| **Reviewer** | Breadcrumbs, topic title, Quick Summary / Detailed Lesson switch, scannable definitions/tables/code, source citations, related cards and practice links. Preserve topic reading position when reasonable. |
| **Original Document Viewer** | Browser-viewable PDF with validated page navigation, zoom, fit-to-width and fullscreen if supported; responsive fallback to native PDF viewing. Original-to-converted page mapping is explicit. |
| **Flashcards** | One centered question/answer card, flip interaction, previous/next, shuffle, Known / Study Again actions, deck filters and mastery status. Rating becomes available after revealing an answer. |
| **Exam Selection & Setup** | Choose coverage (subject/topic/mixed), mode (Practice/Mock), preset or custom count, difficulty, question types, timer; show matching verified-question count and preflight conflicts before starting. |
| **Focused Exam** | Dedicated shell, progress, timer if enabled, one question at a time, Previous/Next, numbered question navigator, unanswered/answered/flagged indicators, flag toggle and final review. Navigator collapses into an accessible mobile drawer. |
| **Submission Review** | Counts and links for unanswered/flagged questions, return-to-exam, final confirmation, explicit warning that unanswered items receive zero points. Review does not pause a timed mock exam. |
| **Results** | Percentage and score, counts, time used, topic strengths/weaknesses, tabs for All / Incorrect / Flagged, per-question chosen vs correct response, explanation, evidence link, Review Weak Topics and Retry Mistakes. |
| **Progress** | Local attempt history, score trend and topic-level statistics (only when enough observations), separate flashcard mastery, last activity, and deliberate Clear Local Progress flow. |

### 3.3 Question renderers

A common question frame provides numbering, source-neutral prompt rendering, flagging, navigation, and accessibility labels. Type-specific controls provide: (a) four MCQ options; (b) two True/False options; (c) identification text input; (d) read-only, accessible syntax-highlighted Java snippet with reviewed choice or text-output response. Syntax-highlighted content is escaped/safe, never executable. Practice shows **Check Answer** → immediate feedback; Mock conceals correctness until finalization.

### 3.4 Responsive behavior

Test at **375, 768, 1024, and 1440 px**, plus zoom and representative long-content cases. Mobile: drawer navigation, stacked statistics, fit-width reviewer, horizontally scrollable code blocks, usable identification input, and compact question navigator. Desktop: sidebar and spacious reading/exam panels. No important control is hover-only.

## 4. Source Materials & Content Coverage (Approved Section 3)

### 4.1 Source registry

Each source receives a stable ID, original title, subject ID, original format, page/slide metadata, published PDF asset path when rights are cleared, and provenance/coverage notes. PPTX and DOCX are converted to viewable PDFs during content preparation; **conversion is not a live student feature**. Conversion mappings must preserve citations, including original slide numbering.

| ID | Uploaded file | Subject | Source-based coverage |
|---|---|---|---|
| `pathfit-pickleball` | `PICKLEBALL.pptx` | PATHFIT 3 | History, courts/equipment, service, two-bounce and kitchen rules, faults, scoring, singles/doubles, strokes, grips |
| `pathfit-table-tennis` | `TABLE-TENNIS_CVSUTANZA.pdf` | PATHFIT 3 | History, equipment, grips, strokes, footwork, legal serve, rules and scoring |
| `pathfit-fundamentals` | `FUNDAMENTAL-SKILLS-IN-RACKET-SPORTS.pdf` | PATHFIT 3 | Ready position, grips, movement, coordination drills, forehand/backhand, ball control |
| `gned10-reviewer` | `GNED 10 Midterm Reviewer.docx` | GNED 10 | Gender and Work, Gender and School, Gender and Media, with **explicit incomplete-source caveat** for Media |
| `gned07-reviewer` | `GNED 07 Midterm Reviewer.docx` | GNED 07 | Globalization, economic structures and market integration, interstate systems and governance, global divides, Asian regionalism |
| `dcit50-constructors` | `Java Constructors Lecture.pdf` | DCIT 50 | Rules, default/no-arg/parameterized constructors, `this`, overloading, chaining, copy constructors, constructor vs method |
| `dcit50-static-this` | `Static and This Keyword Lecture.pdf` | DCIT 50 | Static fields/methods, restrictions, blocks, instance members, `this` uses |
| `dcit50-classes-objects` | `Classes and Objects Lecture.pdf` | DCIT 50 | Class/object, references, `new`, state, behavior, fields, methods, parameters and return values |

GNED 10's Media content is explicitly marked as summarized from incomplete source content; the platform must **not invent missing original-module content**. All source-specific facts remain faithful to the instructor materials. Content that is dubious or inconsistent is flagged for review rather than silently corrected by general knowledge. Image/diagram reuse and document redistribution require permission prior to public hosting.

### 4.2 Topic hierarchy

- **DCIT 50:** Classes & Objects; Java Constructors; Static & This Keyword; finer lesson sections nested under these three sources.
- **GNED 07:** Introduction to Globalization; Global Economy; Market Integration; Global Interstate System; Contemporary Global Governance; A World of Regions (including divides and Asian Regionalism).
- **GNED 10:** Gender and Work; Gender and School; Gender and Media (limited source scope).
- **PATHFIT 3:** Pickleball; Table Tennis; Fundamental Skills in Racket Sports, with their source-derived lesson sections.

### 4.3 Content entities and relationships

**Subject** `id, title, shortLabel, description, topicIds, sourceIds`.  
**Topic** `id, subjectId, title, order, lessonSectionIds, sourceIds`.  
**Concept** `id, topicId, label, evidenceRefs` (stable conceptual link shared by learning modes).  
**LessonSection** `id, topicId, kind, summaryBlocks, detailedBlocks, conceptIds, evidenceRefs, coverageNotice?`.  
**SourceDocument** `id, filename, originalFormat, displayAssetPath?, pageMap, rightsStatus, sourceNotes`.  
**Flashcard** `id, subjectId, topicId, conceptId, question, answer, sourceRefs`.  
**Question** has a common core plus a **discriminated union** for type-specific answers.

Common question fields: `id, subjectId, topicId, conceptId, type, difficulty, prompt, explanation, sourceRefs, verificationStatus, contentVersion` and optional presentation metadata. MCQ has `options[4]` and `correctOptionId`; True/False has `correctValue: boolean`; Identification has canonical answer plus reviewed `acceptedAnswers[]` and normalization policy; Java Analysis has code language/source, code snippet, task subtype (output/error/concept), and a **single predefined grading strategy** (choice ID or accepted textual output). Questions may have additional explanation of distractors but must not claim unsupported details.

**Example record** (illustrative and source-grounded):

```ts
const example = {
  id: "dcit50-constructors-001",
  subjectId: "dcit50",
  topicId: "java-constructors",
  conceptId: "constructor-purpose",
  type: "multiple-choice",
  difficulty: "easy",
  prompt: "What is the primary purpose of a Java constructor?",
  options: [
    { id: "a", text: "Execute a loop" },
    { id: "b", text: "Initialize an object's state" },
    { id: "c", text: "Delete a class" },
    { id: "d", text: "Import a package" }
  ],
  correctOptionId: "b",
  explanation: "Constructors initialize an object's state when it is created.",
  sourceRefs: [{ sourceId: "dcit50-constructors", originalPage: 1 }],
  verificationStatus: "verified",
  contentVersion: 1
} as const;
```

### 4.4 Source verification and publication gates

Content preparation pipeline:

1. Inspect all source pages/slides, including embedded diagrams and image-only portions; collect definitions, claims, comparisons, rules, examples, and source locations.
2. Create a concept-coverage ledger per source/topic. Prepare a concise reviewer and a detailed reviewer without adding unsupported facts. Assign concept IDs for question/flashcard cross-links.
3. Draft questions with plausible non-misleading distractors, accepted answers, explanations and exact source references. Create flashcards from supported key concepts.
4. Independently check answers against the original documents; verify Java expected outputs/error classifications against the presented code and, when feasible, a compatible Java compiler during preparation.
5. Review ambiguity, alternate acceptable responses, source conflicts, near-duplicates, question difficulty, page mappings and missing media rights.
6. Publish only **verified** questions. Draft, needs-review, and rejected items are excluded from examination pools. A build-time validator rejects malformed verified records, duplicate IDs, missing answers, orphaned concepts and invalid citations.

There is **no fixed minimum of 50–100 questions per subject**. Cover all useful supported concepts with non-repetitive questions. Report actual verified counts and gaps per topic. The site never pads exams with duplicates or unsupported generated questions.

### 4.5 Grading and difficulty

- Every question is worth **one point**; unanswered and incorrect answers earn zero. Flagged status never changes scoring.
- `percentage = correct / total * 100` (round for display only; retain exact counts).
- MCQ uses stable answer IDs regardless of shuffled display order. True/False is a boolean.
- Identification normalization trims surrounding whitespace, normalizes Unicode, folds case, and collapses repeated interior whitespace. Do **not** indiscriminately remove meaningful punctuation (e.g. `this()` vs `this`). Only explicitly curated accepted answers count as correct. Do not apply fuzzy AI similarity.
- Java Analysis is read-only code interpretation, **not live Java execution**. Each question must define its subtype and exact grading strategy. Relevant output whitespace normalization is question-specific.
- **Easy:** direct recall; **Medium:** differentiate/apply a single concept; **Hard:** reason through a scenario or code interacting across rules. No artificial tricky wording.

### 4.6 Selection, exam configuration, and coverage

**Coverage:** subject (one subject), topic (one topic), mixed (2–4 selected subjects; optionally topic-filtered only if this can be represented unambiguously in setup). **Mode:** Practice or Mock Exam.

**Presets:** Quick 10 questions/10 min; Standard 30/30 min; Full 50/60 min. Presets are templates, not promises of inventory. **Custom:** choose 1–100 requested questions, verified difficulty (Easy/Medium/Hard/Mixed), any supported subset of question types, and timer (Untimed, 10, 20, 30, 60 or 90 minutes). Filter combinations offered must have eligible questions; users can accept a smaller count or change settings if insufficient. Default configuration: Standard, Mixed difficulty, all eligible formats. Untimed Mock Exam still withholds feedback until submission; strict deadlines apply only to timed Mock Exams.

Use seeded/session-frozen randomization to select distinct question IDs and shuffle MCQ options. Balance mixed-subject selection and avoid over-concentration in one concept where supply allows; when the bank lacks diversity, keep questions unique and communicate the limitation. Preserve selected IDs, question versions, and option order in the session; refresh **must not reshuffle**. A Retry Mistakes session selects previously incorrect IDs from a completed attempt if matching verified versions remain available, otherwise explicitly excludes incompatible items.

## 5. Frontend Architecture & Module Boundaries

### 5.1 Stack

React + Vite + TypeScript, React Router, Tailwind CSS, Lucide icons, Vitest, React Testing Library, Playwright, Lighthouse; optional minimal library for syntax highlighting and PDF viewing selected during implementation based on bundle, accessibility and browser support. **No Next.js server runtime, API endpoints, hosted database, or analytics tracking required.** Deploy Vite static output to Vercel with SPA fallback.

### 5.2 Modules

| Module | Responsibility | Does not own |
|---|---|---|
| `content` | Static typed source, lesson, card, question registry and validation | Student progress |
| `exam-engine` | Filters, seeded selection, grading, session transitions, timing | React UI |
| `persistence` | Schema validation, safe reads/writes, migration and recovery | Exam grading |
| `study-ui` | Reviewer/flashcard presentation, user actions | Direct database/storage writes |
| `exam-ui` | Exam renderer, navigator, timer display, confirmation | Separate duplicate scoring logic |
| `analytics-local` | Derive scores, weak-topic summaries and charts from attempts | Remote telemetry |
| `routing-shell` | Route guards, navigation layout, deep-link handling | Question answer keys |
| `document-viewer` | Map source ID and original page to PDF asset viewer page | Alter source facts |

Use React state/Context for local view state and `useReducer` for exam transitions, with pure TypeScript domain functions. Central services own persistence; components never write competing snapshots independently.

### 5.3 Proposed repository structure

```text
src/
  app/                 # routes, app shell, providers
  components/          # shared UI primitives
  features/
    dashboard/
    subjects/
    reviewer/
    flashcards/
    exams/
    results/
    progress/
    documents/
  domain/
    exam-engine/
    grading/
    selection/
    timing/
  content/
    subjects/
    topics/
    reviewers/
    questions/{dcit50,gned07,gned10,pathfit3}/
    flashcards/
    sources/
    content-manifest.ts
  lib/
    persistence/
    validation/
    formatting/
public/materials/{dcit50,gned07,gned10,pathfit3}/
tests/{unit,component,e2e}/
```

## 6. Exam State, Persistence, Timing & Recovery (Approved Section 4)

### 6.1 Lifecycle and invariants

`configured → active ↔ paused(practice-only) → completed`, with a separate `abandoned` terminal state. Submission **reviewing is a view within the active lifecycle state**, not an independent terminal state; the deadline continues. Mock Exam has no paused state. Only **one active session per browser profile**. Starting another requires resume/submit/abandon. Status transitions are checked by the centralized reducer/service.

Invariants:

- Session ID, ordered question IDs, selected versions, and shuffled option IDs are immutable after start.
- Answer state is indexed by question ID, not array index. Flags, position, current state, save status and timestamps are stored.
- Before a Practice answer is checked, it may be edited; after **Check Answer** it is locked for that attempt and feedback/explanation displayed. Skipped unchecked items remain unanswered; finishing Practice scores unchecked/blank answers as zero.
- Mock Exam answers can be changed up to submission/deadline; no correct answer or explanation is displayed prematurely.
- Submission/expiration is **idempotent**, identified by a stable attempt ID derived from the session. A repeated submit/refresh must not create duplicate results.

### 6.2 Stored session and results

A versioned session persists `{ schemaVersion, sessionId, mode, status, contentVersion, configuration, immutableQuestionSelection, answers, checkedPracticeQuestionIds, flags, currentQuestionIndex, activeSubview, timing, updatedAt }`. Preserve a compact, immutable question/answer-review snapshot sufficient to interpret old submitted attempts and recover an active session across compatible content releases without remapping to different questions. No PDFs or full reviewer library are stored locally.

Completed attempts persist `{ attemptId, sessionId, configuration, startedAt, submittedAt, completionReason, questionSnapshots, submittedAnswers, correctness, score, topicBreakdown, elapsedMs }`. Correctness is calculated once from that attempt's pinned answer-key versions. Historical scores are not silently regraded after future content updates.

Storage keys (namespace can use final product name):

```text
studyspace:v1:active-session
studyspace:v1:attempts
studyspace:v1:flashcards
studyspace:v1:preferences
studyspace:v1:metadata
```

`localStorage` writes are synchronous and can fail. Persist on answer/flag/navigation changes, debounce text typing briefly and flush on blur/navigation; display **Saved** only after a successful write. Preserve existing data if writing a new record fails. On full/disabled storage, continue in memory with a prominent warning that refreshing may lose progress. Validate every restored value against the expected schema; attempt defined migrations, otherwise show recovery options. Never pretend a partially written result is durable.

### 6.3 Timing

A **timed Mock Exam** saves `deadlineAt = startedAt + durationMs`. Display `remainingMs = max(0, deadlineAt - Date.now())`; an interval updates the display but does not act as the timing authority. A suspended/closed tab cannot perform code execution; when reopened, an expired deadline triggers finalization from last saved eligible answers before resuming UI. Check deadline again before answer commits/submission; reject late changes. Mock submission review does not pause time.

**Untimed Mock Exam:** no deadline; manual submission. **Practice:** optional timer, pausable; track accumulated elapsed time and resumedAt separately, show expiration of a practice study timer as informational (no forced grading/submission). Browser clock tampering remains possible without a server.

### 6.4 Recovery and concurrency

On load: validate local schema → detect prior completed attempt for session (deduplicate) → check content/snapshot compatibility → enforce timer deadline → resume/finish/show recovery state. Restore answers, selected question versions, option order, flags, current question and time. If sources are incompatible, **never silently substitute** new questions; offer an explicit error/restart path and preserve raw data where possible.

Use browser storage notifications (and optional BroadcastChannel if supported) for **best-effort single-editor control** across tabs. A second tab shows a warning and does not silently overwrite newer known state. This is not a secure transactional cross-tab lock.

### 6.5 Privacy and progress

Persist card-level `unrated | known | study_again` status, last-updated metadata, and recent positions; the student must flip a card before rating it. Flashcard self-ratings are **separate** from exam correctness. Weak-topic insights derive from completed question attempts and must show insufficient-data states rather than misleading conclusions. Include a confirmation flow for clearing all local data. No name/email/password is collected.

## 7. Failure Modes & Recovery UX

| Failure | Required behavior |
|---|---|
| No questions match filters | Explain which filters are too restrictive; invite adjustment |
| Fewer questions than requested | Show exact matching count; offer count reduction or broader filters; never pad |
| Invalid or missing question/source | Block broken content in build; handle incompatible saved session without remapping |
| Malformed or outdated storage | Validate/migrate, then explain recovery choices; do not crash |
| Local storage denied/full | In-memory mode with clear save-risk warning |
| Duplicate clicks/submission | Idempotent result record; submission disabled after finalization |
| Timer expires during review or answer entry | Apply deadline before further commits; finalize accepted saved answers |
| PDF missing/unavailable | Clear viewer error and native-browser fallback when asset exists |
| Browser back/exit during exam | Confirm; preserve session unless explicitly abandoned |
| Multiple tabs edit same exam | Best-effort conflict warning and prevention of silent overwrite |
| Original asset not licensed | Exclude from public bundle; retain permissible citations/content only |

## 8. Accessibility, Performance & Visual Quality (Approved Section 5)

### 8.1 Accessibility target

Target **WCAG 2.2 AA** in the app UI: semantic controls; keyboard-accessible drawer, question navigator, and flashcards; visible focus; understandable errors; accessible names and landmarks; appropriate contrast; large touch targets; headings and screen-reader reading order; meaningful timer warnings (e.g. five-minute/one-minute/timeout announcements, **not every second**); support browser zoom and `prefers-reduced-motion`; provide HTML lesson content as an accessible alternative when PDF tagging is insufficient.

### 8.2 Performance and diagnostics

Lighthouse targets on representative deployed pages: Performance **90+**, Accessibility **95+**, Best Practices **95+**, SEO **90+**. Core Web Vitals goals: LCP ≤2.5 s, CLS ≤0.1 and field INP ≤200 ms (a lab Lighthouse audit alone cannot establish field INP). These are **targets**, not currently measured scores. Use route-level code splitting; defer PDF viewer/charts/syntax-highlighting code where useful; avoid unnecessary React rerenders and heavy animation; do not ship original-source PDFs unless rights are established.

### 8.3 Role of approved skills

1. [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill): tailored design system, responsive patterns, typography, color/contrast.
2. [Hallmark](https://github.com/Nutlope/hallmark): anti-AI-slop structural critique and distinctive UI refinement.
3. [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills): React best practices, web-design guidelines, performance and accessibility checks.
4. [Impeccable](https://github.com/pbakaus/impeccable): design critique, layout, typography, polish, hardening, adaptive states.

These skills guide actual design/QA work when their implementation stage is reached; none is invoked to create app code as part of this approved brainstorming/spec-writing stage.

## 9. Testing Strategy & Acceptance Matrix

| Level | Tool | Required coverage |
|---|---|---|
| Static validation | TypeScript + schema/content validator | Source IDs, topic links, content versions, verified answers, accepted responses, duplicate IDs, page mappings, completeness |
| Unit | Vitest | All four graders, identification normalization, score math, randomization, sampling/limits, timer math, idempotent finalize, migrations |
| Component | React Testing Library | Radio/input/code renderers, check-answer locking, navigator/flags, confirmation, flashcard flip/rating, errors, focus states |
| Browser E2E | Playwright | Study → flashcards → practice; mock setup → submit → review; refresh/recovery; expiry with controlled time; local storage failures; deep links; responsive interactions |
| Visual/a11y audit | Manual + Lighthouse/automated checks | Contrast, focus, reduced motion, 375/768/1024/1440 layouts, long content, mobile exam controls |
| Content QA | Source traceability and Java code checks | Source-derived facts, no unsupported material, question keys/explanations, mapped citations, verified source assets |

**Must-pass scenarios** include: same question/answer order after refresh; one attempt per submission; Practice pause/resume; Mock expiration after tab close/reopen; time expiration during submission review; no leaked correctness in Mock; unsupported question-count messaging; source viewer page navigation; safe handling of corrupted or unavailable local storage; and correct initial empty states (no fabricated analytics).

## 10. Deployment & Permissions

- Static `vite build` output on **Vercel** (or equivalent static host) with React Router SPA fallback. Deep-link navigation and refresh to study, exam, source and results routes must work.
- No Vercel server functions, backend secrets, Java API, hosted database, or required external runtime services.
- Ask for/confirm permission to redistribute each uploaded file and embedded media before bundling it into publicly served assets. If unavailable, do not deploy that document; retain permissible source attribution and disable viewer actions that would point to missing assets.
- The website does not promise preventing downloads of files exposed to visitors.
- Production validation: build, tests, verified question bank/content report, source asset checks, browser QA, Lighthouse results, deep links and local-progress recovery. Real measured results replace all illustrative prototype figures.

## 11. Implementation Sequence (Handoff Only — Not Authorization)

1. **Foundation:** Vite/React/TypeScript project, routing, shared tokens, responsive shell, testing setup.
2. **Content preparation:** inspect and map every source, confirm rights, prepare converted PDFs, concept ledger, verified lessons, questions and cards.
3. **Learning experience:** Dashboard, Subjects, Quick/Detailed Reviewer, source viewer.
4. **Flashcards:** flip, navigation, filters, mastery, persistence.
5. **Exam engine/UI:** selection/configuration, four renderers, navigator, flags, immediate Practice feedback, Mock concealment.
6. **Reliability:** storage, deadlines, resume, submission, duplicate prevention, compatibility.
7. **Results/Progress:** grading, explanations, weak topics, retry mistakes, attempt history.
8. **QA/polish:** skills-based critiques, unit/component/E2E tests, accessibility, responsive and Lighthouse audits.
9. **Release:** permission checks, static Vercel deployment, route/recovery smoke tests, documented known limitations.

Implementation work is **blocked** until this written specification has been reviewed and explicitly approved; after approval, use the Superpowers **writing-plans** step to prepare and review the detailed implementation plan before any application coding.

## 12. Definition of Done

The initial release is complete only when:

- Four supported subjects and all verified source-derived lesson sections are present, with clear GNED 10 source-coverage notices.
- Quick and Detailed Reviewer views, context links and licensed source document viewer work.
- Flashcards flip, track Known/Study Again, filter and persist locally.
- Subject, topic and mixed exams support the four question formats with verified content and valid presets/custom configuration.
- Focused exam navigator, answer/flag/previous/next, Practice immediate feedback, Mock deferred feedback, submission review and scoring behave correctly.
- Paused Practice sessions and timed/untimed Mock sessions recover correctly. Deadline expiration and repeated submission never create inconsistent or duplicate attempts.
- Results and Progress show actual data, explanations, source citations, weak-topic analysis and retry mistakes; new students see honest empty states.
- Keyboard, mobile and accessibility requirements are met; core automated tests pass and Lighthouse metrics are recorded against targets.
- Deployment works for static deep links and does not publish unlicensed documents.

## 13. Risks, Explicit Trade-offs & Review Notes

| Risk / trade-off | Resolution |
|---|---|
| Frontend answer keys are inspectable | Acceptable because this is self-study, not proctored testing |
| Browser storage loss/quota limits | Visible warning, in-memory fallback, careful versioned persistence and deliberate clear-data control |
| Closing a tab stops JavaScript | Store deadline; finalize a timed-out attempt on reopening, not magically while closed |
| Browser clock can be manipulated | Accept simulation-only timer security |
| Uploaded sources vary in depth | Verified question counts are adaptive; never invent to reach quotas |
| GNED 10 Media source is incomplete | Label limited coverage; do not fabricate missing original content |
| Original copyrighted materials | Public document viewer gated on redistribution permission |
| Potentially outdated factual claims in lecture/reviewer | Faithfully attribute to source; flag contentious/ambiguous questions for review, do not silently replace |
| Static content updates can invalidate old attempts | Pinned question versions and compact attempt snapshots; safe migration/explicit recovery |
| Responsive PDF experience differs by browser | Tested viewer controls and native-PDF fallback |

### Written-spec review decision

**Requested action:** Review this complete specification and respond **Approve** or request particular revisions. Approval of this document permits the next **writing-plans** step only; it does **not** authorize implementation. The spec is portable and should be committed to `docs/superpowers/specs/2026-10-09-studyspace-mock-exam-platform-design.md` in the actual project repository when one is supplied. No repository was provided with this request, so no user-repository commit was performed.
