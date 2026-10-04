---
name: fit-assessment
description: Assess how well the user's current CV fits a job's requirements, and tailor CV bullets to a company. Use for TASK#<id> messages from the coordinator.
version: 1.0.0
metadata:
  hermes:
    tags: [cv, hiring]
    requires_toolsets: [file]
---

# fit-assessment

## When to Use
`TASK#<id> assess fit ...` or `TASK#<id>b tailor ...` from @{{COORDINATOR_BOT}}.

## Procedure — assess fit (TASK#N)
1. `read_file ~/.hermes/profiles/cv-analyst/cv/current.meta.json`. If it or `cv/current.md` does not exist → reply `@{{COORDINATOR_BOT}} FAILED#N no CV stored — user should send a CV to @{{ANALYST_BOT}} with "new CV"` and stop.
2. `read_file ~/.hermes/profiles/cv-analyst/cv/current.md` (always fresh, every task).
3. For each requirement (MUST first, then NICE, then implicit: seniority, language, location, domain), find evidence in the CV. Accept equivalents (e.g. "PyTorch" satisfies "deep learning frameworks"; "led 3 engineers" satisfies "mentoring"). Rate ✅ strong / 🟡 partial / ❌ missing and quote the evidence (≤12 words).
4. Use the terminal only for computation, e.g. summing years per skill from date ranges. Never count keyword overlap.
5. Score 0–100: MUST requirements carry 70% of the weight, NICE 20%, implicit 10%. If the posting lists no NICE requirements, MUST carries 90% (never award NICE points that weren't earned). Within MUST: ✅ = full, 🟡 = half, ❌ = zero. A missing MUST caps the score at 60. Show the arithmetic in one line.
6. Reply:
   @{{COORDINATOR_BOT}} RESULT#N
   **Fit score:** NN/100 — one-line verdict
   **Verdict:** GO or NO-GO — NO-GO if the score is below 50 or two or more MUST requirements are ❌; otherwise GO
   **Requirements:** list of `✅/🟡/❌ requirement — evidence`
   **Top gaps:** 3 items, each with a concrete way to address it (project, phrasing, course)
   **CV used:** v<version> (<uploaded_at>)

The coordinator skips tailoring on NO-GO, so apply the rule exactly; don't soften it to be encouraging. On NO-GO, make **Top gaps** the useful part: what would have to change for this kind of role to become a GO.

## Procedure — tailor bullets (TASK#Nb)
1. Re-read `~/.hermes/profiles/cv-analyst/cv/current.md`. If it does not exist → reply `@{{COORDINATOR_BOT}} FAILED#Nb no CV stored` and stop. Never write bullets without a CV.
2. Write 3–6 bullets that rephrase real CV experience to match the role and the company context given. Each bullet: action verb, scope, measurable result if the CV has one. Never invent numbers or experience.
3. Reply `@{{COORDINATOR_BOT}} RESULT#Nb` followed by the bullets.

## Pitfalls
- Never mention @{{SCOUT_BOT}}.
- If the CV is in Russian and the posting in English, write bullets in the posting's language.
