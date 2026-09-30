# Job War Room — Design Spec

Date: 2026-09-30 · Assignment 1 (Hermes Agent team in Telegram) · Deadline 2026-10-05

## 1. Goal

A Telegram group ("Job War Room") where three Hermes Agent bots cooperate to prepare the user for a job application. The user posts a job posting (text or link); the team returns a single brief: fit score with reasoning, met/missed requirements, tailored CV bullets, likely interview questions, questions to ask, and company red flags. The user's CV is uploaded once and persists; a newer upload replaces it for all future requests.

Success criteria:
- At least one real posting processed end to end in Telegram, with visible @mention handoffs between bots.
- Repo contains each agent's config, `SOUL.md`, skills, README with setup steps, and a report answering the defense questions. No API keys, bot tokens, or CV contents committed.

Non-goals: applying to jobs automatically, scraping job boards in bulk, multi-user support, a UI outside Telegram.

## 2. Agents

Each agent is a separate Hermes profile (`~/.hermes/profiles/<name>/`) with its own Telegram bot token, `config.yaml`, `SOUL.md`, `memories/`, `skills/`, and `state.db`. All three are served by the existing multiplexed gateway (`gateway.multiplex_profiles: true` in the default profile).

| Agent (profile) | Bot | Model | Toolsets | Responsibility | Must never |
|---|---|---|---|---|---|
| `coordinator` | `@<coordinator>_bot` | `gpt-5.4-mini` ($0.75/$4.5 per 1M) | `memory`, `session_search`, `todo` | Parse request, plan subtasks, delegate by @mention, track pending results, synthesize final brief | Search the web, read the CV |
| `scout` | `@<scout>_bot` | `gpt-5.6-luna` ($0.2/$1.2) | `web`, `memory` | Research the company: product, stack, culture, recent news, interview reports (Glassdoor, Reddit, Habr, hh.kz, LinkedIn) | See or ask for the CV |
| `cv-analyst` | `@<analyst>_bot` | `gpt-5.6-terra` ($2/$12) | `file`, `terminal`, `memory`, `skills` | Store the latest CV; assess fit against the posting's real requirements; tailor bullets | Search the web, @mention anyone but the coordinator |

Model rationale: the coordinator needs dependable instruction-following and structured synthesis, not deep reasoning, so a mini tier suffices. The scout does many cheap tool calls (search → read → summarize), so the smallest current tier. The analyst's output is the core value (judging equivalence of experience, prioritizing gaps) and it runs few calls, so the stronger tier is worth its price. Fallback for the analyst if cost/latency is a problem: `gpt-5.6-luna` (also serves as the small-vs-big comparison for defense Q5).

Why split at all: (a) privacy/security — the web-facing scout never holds CV data, so a prompt-injected web page cannot exfiltrate it; (b) least privilege — each agent gets only the tools its role needs; (c) per-role model choice keeps cost down; (d) smaller, focused contexts. A single agent would be cheaper in handoff overhead and latency but mixes CV, dozens of web pages and planning in one context.

## 3. Flow

1. User: `@coordinator TASK: <posting text or URL>` (in the group).
2. Coordinator assigns a task id `N`, posts a short plan, then two handoffs:
   - `@scout TASK#N research <Company>. Focus: <stack/interview process/...>`
   - `@cv-analyst TASK#N assess fit. Requirements: <extracted list, marked must/nice>`
3. Scout replies `@coordinator RESULT#N` + structured company summary (with source links).
   Analyst replies `@coordinator RESULT#N` + fit assessment.
4. Coordinator sends the dependent step: `@cv-analyst TASK#Nb tailor bullets using: <condensed scout summary>`.
5. Analyst replies `@coordinator RESULT#Nb` + 3–6 tailored bullets.
6. When every subtask of N has a RESULT or FAILED, coordinator posts the final brief (addressed to the user, no bot mentions).

CV upload flow (coordinator not involved): user sends PDF/DOCX with caption `@cv-analyst new CV` → analyst runs the `cv-store` skill → replies with version and summary of changes.

If the URL of a posting can't be read by the coordinator (it has no web tool), it asks the scout to fetch the posting text as part of the TASK, or asks the user to paste it. Default expectation in the README: paste the posting text.

## 4. Message protocol

- Handoff: `@<bot> TASK#<id> <instruction>`
- Response: `@<coordinator_bot> RESULT#<id>` followed by the payload, or `@<coordinator_bot> FAILED#<id> <reason>`.
- `<id>` is a short integer chosen by the coordinator (subtasks use suffix letters: `12`, `12b`).
- Specialists act only on messages that explicitly @mention them. They never @mention anyone except the coordinator, and never respond to RESULT/FAILED messages.
- Coordinator keeps an in-context checklist (via the `todo` tool) of pending subtask ids per task; the task is finished when the checklist is empty.

## 5. CV persistence

Location: `~/.hermes/profiles/cv-analyst/cv/` (outside the Telegram document cache, which is periodically cleaned; outside the repo).

```
cv/current.md          # markdown text of the latest CV with header: version, uploaded_at, original filename
cv/current.meta.json   # {version, uploaded_at, sha256, original_filename}
cv/history/v<k>.md     # previous versions
```

Skill `cv-store` (analyst): on receiving a document path
1. Extract text via `read_file` (DOCX built-in; PDF via document extraction) with `pdftotext` fallback in terminal.
2. Compute sha256 of the original file; if equal to `current.meta.json.sha256`, reply "same CV (vN), nothing changed".
3. Otherwise move `current.md` → `history/v<old>.md`, write new `current.md` and meta with version+1.
4. Update built-in memory with a single pointer entry: "Current CV: cv/current.md, vN, <date>, <headline>".
5. Reply with version and a 2–3 line summary of what changed vs the previous version.

A helper script `cv_store.py` (shipped with the skill) does steps 2–3 deterministically so versioning never depends on the model's file handling.

Skill `fit-assessment` (analyst):
1. Always re-read `cv/current.md` at the start of a task (newest upload wins, even in long sessions). If absent, reply FAILED "no CV stored — upload one with @cv-analyst new CV".
2. Split requirements into must-have / nice-to-have / implicit (seniority, language, location, domain).
3. For each requirement, find evidence in the CV, accepting semantic equivalents and transferable experience; rate strong / partial / missing, quoting the evidence.
4. Use the terminal only when computation helps (e.g. summing years of experience per skill from date ranges); no keyword-overlap scoring.
5. Output: score 0–100 with a weighted rationale (must-haves dominate), met/partial/missing table, top 3 gaps with how to address them.

## 6. Memory (defense Q7)

| Agent | Built-in memory (`profiles/<name>/memories/MEMORY.md`, `USER.md`; injected at session start, ~2.2k/1.4k chars) | Other persistent state |
|---|---|---|
| coordinator | user preferences (target roles, city, salary floor, language) | `state.db` sessions, `session_search` |
| scout | notes on which sources are useful for KZ/CIS companies | `state.db` |
| cv-analyst | one pointer to the current CV | `cv/` directory, `state.db` |

## 7. Loop prevention (defense Q3)

1. Prompt layer: role rules in each `SOUL.md` (specialists address only the coordinator; nobody replies to RESULT except the coordinator's next planned step).
2. Gateway config per profile: `telegram.require_mention: true`, `telegram.bots_require_mention: true`, `telegram.exclusive_bot_mentions: true`, `telegram.allow_bots: mentions`, `mention_patterns: []`.
3. Hermes `gateway.bot_loop_guard` (already on): >20 bot messages per chat in 300 s → bot messages dropped for 600 s. Human messages never counted.
4. Hermes ignores its own messages.

## 8. Failure handling

- Scout finds nothing / web errors → `FAILED#N`; coordinator still delivers the brief with a "company research unavailable" note.
- No CV stored → analyst FAILED with upload instructions; coordinator relays.
- A specialist never replies → coordinator cannot time out on its own (it only runs on incoming messages); the user can nudge with `@coordinator status`. Documented as a known limit.
- Every real failure observed during testing is logged in `docs/failures.md` (symptom, cause, fix/proposed fix).

## 9. Platform risk: bot-to-bot delivery

Telegram historically does not deliver messages authored by one bot to other bots in groups. Hermes has `allow_bots`, but it can only act on updates Telegram delivers. **First implementation task is a live spike** with two bots in the test group (privacy mode off / bots as admins). If delivery fails, fallback: bots still post their visible @mention handoff in the group, and the actual delivery to the target agent happens through Hermes' cross-profile mechanism (`send_message`/Bot Mode or the shared kanban board). The chosen mechanism and its reason are documented in the report.

## 10. Repository layout (`~/job-war-room`)

```
agents/
  coordinator/{config.yaml, SOUL.md, .env.example, skills/}
  scout/{config.yaml, SOUL.md, .env.example, skills/}
  cv-analyst/{config.yaml, SOUL.md, .env.example, skills/cv-store/, skills/fit-assessment/}
scripts/setup.sh        # creates profiles, links config/SOUL/skills from repo into ~/.hermes/profiles/*
scripts/check.sh        # sanity checks: profiles exist, tokens set (not printed), models reachable
README.md               # prerequisites, BotFather steps, group setup, run, demo request
docs/report.md          # architecture, flow diagram, answers to defense Q1–Q7
docs/failures.md        # observed failures and fixes
docs/demo/              # screenshots / transcript of an end-to-end run
.gitignore              # .env, cv/, *.db, sessions, caches
```

Secrets: tokens and `OPENAI_API_KEY` live only in `~/.hermes/profiles/<name>/.env`, entered by the user. The repo ships `.env.example` with variable names only.

## 11. Testing

- Unit: `cv_store.py` (new version, same-hash no-op, history rotation) with pytest.
- Spike: bot-to-bot delivery test.
- Integration: CV upload → v1; re-upload same → no-op; upload modified → v2.
- End-to-end: one real posting through the full flow; capture transcript/screenshots in `docs/demo/`.
- Negative: request with no CV stored; company with no web presence; attempt to make a specialist @mention another specialist (loop check).
