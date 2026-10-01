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
`TASK#<id> assess fit ...` or `TASK#<id>b tailor ...` from @alish_hr_coordinator_bot.

## Procedure — assess fit (TASK#N)
1. `read_file ~/.hermes/profiles/cv-analyst/cv/current.meta.json`. If it does not exist → reply `@alish_hr_coordinator_bot FAILED#N no CV stored — user should send a CV to @alish_cv_analyst_bot with "new CV"` and stop.
2. `read_file ~/.hermes/profiles/cv-analyst/cv/current.md` (always fresh, every task).
3. For each requirement (MUST first, then NICE, then implicit: seniority, language, location, domain), find evidence in the CV. Accept equivalents (e.g. "PyTorch" satisfies "deep learning frameworks"; "led 3 engineers" satisfies "mentoring"). Rate ✅ strong / 🟡 partial / ❌ missing and quote the evidence (≤12 words).
4. Use the terminal only for computation, e.g. summing years per skill from date ranges. Never count keyword overlap.
5. Score 0–100: MUST requirements carry 70% of the weight, NICE 20%, implicit 10%; a missing MUST caps the score at 60. Show the arithmetic in one line.
6. Reply:
   @alish_hr_coordinator_bot RESULT#N
   **Fit score:** NN/100 — one-line verdict
   **Requirements:** list of `✅/🟡/❌ requirement — evidence`
   **Top gaps:** 3 items, each with a concrete way to address it (project, phrasing, course)
   **CV used:** v<version> (<uploaded_at>)

## Procedure — tailor bullets (TASK#Nb)
1. Re-read `~/.hermes/profiles/cv-analyst/cv/current.md`.
2. Write 3–6 bullets that rephrase real CV experience to match the role and the company context given. Each bullet: action verb, scope, measurable result if the CV has one. Never invent numbers or experience.
3. Reply `@alish_hr_coordinator_bot RESULT#Nb` followed by the bullets.

## Pitfalls
- Never mention @alish_company_scout_bot.
- If the CV is in Russian and the posting in English, write bullets in the posting's language.
