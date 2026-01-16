# Data QueryAI

This project lets anyone ask questions in plain language and get answers from MongoDB. The web app is built in React. The server uses a lightweight LLM call (no LangChain, no chat flow) to turn a single question into a safe MongoDB query, runs it, and returns a short answer plus the raw JSON. Users never see Mongo credentials.

## How it works (simple view)
1) The React page sends your one-off question to the backend (`POST /query` with `user_question`).
2) The backend reads the Mongo schemas in this folder, uses them as context, and asks the LLM (simple API call) to propose a safe query.
3) The backend checks the proposed query against allowlists (collections, fields, read-only only) and rejects risky operators.
4) A read-only Mongo client runs the query.
5) The backend returns both: (a) the raw JSON results (capped/page-limited) and (b) a short plain-language summary.

## Mongo collections available
- `Survey` (`SURVEY SCHEMA...md`): survey setup (name, type, reward, filters, status/lifecycle, limits, panel info).
- `SurveyHistory` (`SURVEY HISTORY SCHEMA...md`): what each user did in a survey (status, answered IDs, panel/source, verification status).
- `Question` (`QUESTION SCHEMA...md`): questions for a survey (type like MCQ/video/image/rating, choices, branching, timing).
- `Answer` (`ANSWER SCHEMA...md`): user answers (who answered what, rank/choice, media, scheduler fields, locations).
- `User` (`USER SCHEMA...md`): user profile (mobile, gender/age/location, wallet, notifications, platform/source, fraud flags).
- `MODEL DOCUMENTATION...md` links all of the above.

Key links between collections:
- `surveyHistory.surveyId` -> `survey._id`; `surveyHistory.userId` -> `user._id`; optional `surveyHistory.panelId`.
- `question.surveyID` -> `survey._id`; `answer.questionId` -> `question._id`; `answer.surveyId` -> `survey._id`; `answer.userId` -> `user._id`.
- Completion/drop-off: use `surveyHistory.answeredQuestionsId` and `status`. Branching: `question.child_questions`.

Sensitive data to hide by default:
- Phone fields (`user.number`, `answer.phone`), hashed numbers (`user.md5Number`), location details, device tokens. Summaries should group/aggregate, not show raw values.

## Build plan (MVP to hardened)
1) Set up projects: FastAPI (or Node) backend + Vite React frontend; `.env` holds Mongo URI and LLM key.  
2) Load schemas: parse these markdown files and add a small scrubbed `find_one` example per collection for context. Cache field allowlists.  
3) LLM call (no LangChain): single HTTP call to the model with a clear prompt and JSON response format. Only two operations: `find` and `aggregate` with `$project`, `$match`, `$group`, `$limit`, `$sort`; cap limit=200. Block writes/updates/mapReduce/$where/$function/geo (unless explicitly allowed).  
4) Translator: prompt + examples -> JSON `{operation, collection, pipeline/query, limit}`. Validate fields/collections and operators before running. Reject or clamp broad queries.  
5) Execute + summarize: run via PyMongo; return paged JSON plus a short “Key takeaways” summary.  
6) React UI: simple question form (no chat thread). Show summary, raw JSON tab, and “See generated query” preview.  
7) Logging/eval: store (question, generated query, timing, rows). Create a small test set (completion vs abandonment, reward type splits, panel vs non-panel, verification funnel).  
8) Security: backend-only creds, read-only Mongo role, IP allowlist, rate limits, scrub PII in prompts/logs, JSON-schema validation of model output.  
9) Deploy: containerize frontend and backend separately; add health checks.  
10) Harden: feedback button to flag bad answers; regression tests to catch query drift; drop any prompt-injection attempts.

## LLM usage (simple rules, no LangChain)
- One HTTP call per question, expect strict JSON back (operation, collection, pipeline/query, limit).  
- Always inject: parsed schema fields, sample docs, allowed fields, and any index hints you have.  
- Validate before running: unknown collection/field -> reject; wide-open queries -> clamp limits.  
- Cache repeated questions (in-memory or Redis).  
- Tests: mock Mongo + golden queries; property tests to ensure no write ops are emitted.

## React interface
- Vite + TypeScript; single page (one question at a time).  
- Components: input box, response pane (summary vs JSON tabs), query preview, short history list, feedback toggle (“useful / not useful”).  
- Behaviors: loading states, error messages, optional streaming text, copy buttons for summary and JSON.

## Recommendations (keep it simple)
- Put all Mongo access in one `db_client.py` with read-only roles; match allowlists to the schema files.  
- Start with GPT-4o or Claude 3.5; keep a local fallback (Llama 3.1 8B) if you need on-prem.  
- Pre-build small lookup tables (enums/statuses) and pass them into the prompt to cut down on mistakes.  
- Add synthetic questions that cover status rollups, panel vs non-panel, validation questions, reward splits, and verification funnels.  
- Add indexes or hints on `surveyId`, `userId`, `questionId`, `panelId`, `survey_status`, `status`, `questionType` if not present.

## Known limits
- Frontend never talks to Mongo directly; everything goes through the backend validator.  
- No writes, index changes, or custom JS (`$where`, `$function`).  
- Full-text answers need proper text indexes or Atlas Search.  
- Large results are paged and summarized, not streamed in full.  
- If schemas drift and docs are stale, answer quality drops—keep these markdowns updated.

## Run the new UI locally (no backend yet)
The UI you added lives at `Data QueryAI/data-queryai-assistant-main/data-queryai-assistant-main` and ships as a Vite + React + TypeScript app. It currently shows a simulated answer; you can wire it to your backend later.

Steps:
1) `cd "Data QueryAI/data-queryai-assistant-main/data-queryai-assistant-main"`
2) Install deps: `npm install` (or `bun install` if you prefer Bun)
3) Start dev server: `npm run dev`
4) Open the printed localhost URL (usually `http://localhost:5173`)

Hook it to your backend (when ready):
- In `src/pages/Index.tsx`, replace the simulated `setTimeout` block with a real `fetch` to your API, e.g. `POST http://localhost:8000/query` sending `{ user_question: query }`.
- Update the UI to display the summary and raw JSON from that response.  
- Keep the backend read-only and validate queries as described above.
