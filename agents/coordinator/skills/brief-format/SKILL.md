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
All subtasks of TASK#N (research, fit, tailor) are resolved: RESULT, FAILED, or tailoring skipped. Use the short variant when the analyst's verdict was NO-GO.

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

If the posting came from a link (TASK#Nf), add its source URL on the first line under the title.

## Short variant — NO-GO (tailoring skipped)
📋 **Not a match — <Role> @ <Company>** (TASK#N)

**Fit:** NN/100 — NO-GO (from analyst)
**Missing:** the ❌ MUST requirements, verbatim
**What would close the gap:** the analyst's top gaps
**About the company:** 2 lines from scout + red flags (if any)
**Worth it anyway?** one honest line (e.g. "apply only if the role is flexible on X")
_Reply "tailor anyway" to get tailored CV bullets._

## Rules
- Copy the ✅/🟡/❌ ratings and the fit score verbatim from the analyst's RESULT; never re-grade a requirement.
- Under 3500 characters. No bot mentions. Don't add facts not present in the specialists' results except the interview/ask questions, which you write yourself.
