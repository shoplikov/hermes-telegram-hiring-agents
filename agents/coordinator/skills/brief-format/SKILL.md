---
name: brief-format
description: Format the final application brief once all subtasks of a TASK#N are resolved.
version: 1.0.0
metadata:
  hermes:
    tags: [hiring, output]
---

# brief-format

## When to Use
All subtasks of TASK#N (research, fit, tailor) have a RESULT or FAILED.

## Template
📋 **Application brief — <Role> @ <Company>** (TASK#N)

**Fit:** NN/100 — verdict (from analyst)
**You meet:** top 3 ✅ · **Partially:** top 🟡 · **Missing:** ❌ list
**About the company:** 3 lines from scout + 1 red-flag line
**Tailored CV bullets:** (from analyst RESULT#Nb)
**Likely interview questions (5):** derive from MUST requirements + scout's interview-process notes + gaps
**Questions to ask them (3):**
**Next steps:** 2–3 concrete actions
_Gaps in this brief:_ list any FAILED subtasks, else omit

## Rules
- Copy the ✅/🟡/❌ ratings and the fit score verbatim from the analyst's RESULT; never re-grade a requirement.
- Under 3500 characters. No bot mentions. Don't add facts not present in the specialists' results except the interview/ask questions, which you write yourself.
