# Job War Room

A team of three [Hermes Agent](https://github.com/NousResearch/hermes-agent) bots in one Telegram group that helps you apply for a job. Paste a job posting; the team researches the company, checks the posting against **your latest CV**, tailors CV bullets, and returns one application brief.

| Agent | Bot | Model | Tools | Job |
|---|---|---|---|---|
| Coordinator | `@alish_hr_coordinator_bot` | `gpt-5.4-mini` | memory, session_search, todo, skills | Splits the request, hands off by @mention, tracks results, writes the final brief |
| Company Scout | `@alish_company_scout_bot` | `gpt-5.6-luna` | web, memory | Researches the company on the web (never sees the CV) |
| CV Analyst | `@alish_cv_analyst_bot` | `gpt-5.6-terra` | file, terminal, memory, skills | Stores the latest CV with versions, judges fit, tailors bullets (no web access) |

```
you ──@coordinator posting──▶ Coordinator ──@scout TASK#N──▶ Scout ──RESULT#N──┐
                                  │                                            │
                                  ├──@analyst TASK#N (fit)──▶ CV Analyst ──RESULT#N──┤
                                  │                                            ▼
                                  ├──@analyst TASK#Nb (tailor + scout context)──▶ RESULT#Nb
                                  ▼
                        📋 final brief to you (once every subtask has RESULT/FAILED)
```

Upload your CV once (`@alish_cv_analyst_bot new CV` as the file caption). It is stored as `cv/current.md`; a newer upload becomes v2, v3… and the old one moves to `cv/history/`. Every task re-reads the current version.

## Assignment checklist

| Requirement | Where |
|---|---|
| ≥ 3 Hermes agents, each with its own Telegram bot (1 coordinator + 2 specialists) | `agents/coordinator`, `agents/scout`, `agents/cv-analyst`; table above |
| Handoffs between bots by @mention | `TASK#N` / `RESULT#N` protocol in each `SOUL.md`; live runs in [docs/demo/transcript.md](docs/demo/transcript.md) |
| Working end-to-end flow | Five real postings; clean post-fix run TASK#5 in the transcript |
| Each agent's config and `SOUL.md` in the repo | `agents/*/config.yaml`, `agents/*/SOUL.md`, `agents/*/skills/` |
| README with setup steps | This file |
| No API keys or bot tokens committed | Only `.env.example` files are tracked; secrets stay in `~/.hermes/profiles/*/.env` |
| Defense questions Q1–Q7 | [docs/report.md](docs/report.md) §3 |
| A real failure example | [docs/failures.md](docs/failures.md) (11 logged; #5 is the main one) |

More detail: [docs/report.md](docs/report.md) (architecture and design questions), [docs/failures.md](docs/failures.md) (what broke and why), [docs/demo/transcript.md](docs/demo/transcript.md) (a real end-to-end run).

## Repository layout

```
agents/
  coordinator/  config.yaml  SOUL.md  .env.example  skills/brief-format/
  scout/        config.yaml  SOUL.md  .env.example
  cv-analyst/   config.yaml  SOUL.md  .env.example  skills/cv-store/ (+ scripts/cv_store.py)  skills/fit-assessment/
scripts/
  setup.sh       installs the agents as Hermes profiles (idempotent)
  set-token.sh   stores one bot token in a profile's .env without echoing it
  check.sh       verifies the install (profiles, links, tokens set, gateway settings) without printing secrets
tests/test_cv_store.py
docs/  report.md  failures.md  demo/  superpowers/ (design spec + implementation plan)
```

No secrets are in the repo. Bot tokens and the OpenAI key live only in `~/.hermes/profiles/<name>/.env`; the CV lives only in `~/.hermes/profiles/cv-analyst/cv/`.

## Setup

### 1. Prerequisites

- Linux/macOS with Hermes Agent ≥ 0.21 installed and a working default profile (`hermes` runs; `~/.hermes/.env` contains `OPENAI_API_KEY` and `TELEGRAM_ALLOWED_USERS=<your Telegram user id>`).
- The Hermes gateway running as a service with profile multiplexing (the default): `gateway.multiplex_profiles: true` in `~/.hermes/config.yaml`.
- `pdftotext` (poppler-utils) for PDF CVs: `sudo apt install poppler-utils`.
- `uv` to run the tests (optional).

### 2. Create three Telegram bots

In [@BotFather](https://t.me/BotFather), for each of the three agents:

1. `/newbot` → pick a name and a username ending in `bot`. Keep the token private — never paste it into a chat (including AI assistants).
2. `/mybots` → the bot → **Bot Settings → Group Privacy → Turn off**.
3. Open the BotFather **mini app** (the *Open* button next to the message field) → the bot → enable **Bot-to-Bot Communication**. Without this, Telegram does not deliver one bot's messages to another and handoffs silently fail.

If you use your own usernames, replace `alish_*_bot` in `agents/*/SOUL.md` and `agents/*/skills/*/SKILL.md`.

### 3. Create the group

Create a group (e.g. "Job War Room"), add the three bots, and make all three **admins**.

### 4. Install the agents

```bash
git clone https://github.com/shoplikov/hermes-telegram-hiring-agents.git ~/job-war-room && cd ~/job-war-room
scripts/setup.sh                    # creates profiles coordinator, scout, cv-analyst
scripts/set-token.sh coordinator    # run in a real terminal; paste the token at the hidden prompt
scripts/set-token.sh scout
scripts/set-token.sh cv-analyst
```

`setup.sh` copies each `config.yaml` into `~/.hermes/profiles/<name>/`, symlinks `SOUL.md` back to the repo, points `skills.external_dirs` at the repo's skills, copies `OPENAI_API_KEY` and `TELEGRAM_ALLOWED_USERS` from the default profile, and links `cv_store.py` to a stable path. Re-run it after editing anything under `agents/`.

### 5. One gateway-wide setting

With a multiplexed gateway, `group_sessions_per_user` is read from the **default** profile only. The coordinator must see your request and the specialists' results in one session, so set this in `~/.hermes/config.yaml`:

```yaml
group_sessions_per_user: false
```

(This makes every group your default bot is in share one session per group. DMs are unaffected.)

### 6. Start

```bash
hermes gateway restart
hermes profile list        # coordinator, scout, cv-analyst should show "running"
scripts/check.sh           # every line should say "ok"
```

## Usage

In the group:

1. **Upload your CV** — send the PDF/DOCX with caption `@alish_cv_analyst_bot new CV`. Reply: `✅ CV v1 saved …`. Re-uploading the same file → "Same CV as v1". A changed file → v2 with a summary of what changed.
2. **Ask for a brief** — `@alish_hr_coordinator_bot Prepare me for this job:` followed by the full posting **text** (a link alone is not enough; the coordinator will ask you to paste the text). Within ~1–2 minutes you see the handoffs (`TASK#N`, `RESULT#N`, `TASK#Nb`) and then the 📋 brief: fit score, met/partial/missing requirements, company summary and red flags, tailored CV bullets, likely interview questions, questions to ask, next steps.
3. **Status** — `@alish_hr_coordinator_bot status` lists pending subtasks.

Address one bot per message. A message that mentions several bots wakes all of them.

## Tests

```bash
uv run pytest -q     # cv_store.py: versioning, unchanged detection, history, image-only/near-empty PDFs refused,
                     # PDF/DOCX extraction, recovery from a corrupt or half-deleted store
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| Specialists never react to the coordinator | Enable Bot-to-Bot Communication for the bots (step 2.3); bots must be admins with privacy off |
| Duplicate handoffs or duplicate briefs | `group_sessions_per_user: false` in the **default** profile config, then restart the gateway |
| Bot ignores a message | It must @mention that bot; for files, the mention goes in the file's caption |
| Not sure what is misconfigured | `scripts/check.sh` lists every failing check |
| `set-token.sh` says it needs an interactive terminal | Run it in a normal terminal, not through an AI assistant's shell |
| Analyst says "no CV stored" | Upload a CV first (step 1 of Usage) |
