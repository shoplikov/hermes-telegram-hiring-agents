---
name: cv-store
description: Save a newly uploaded CV (PDF/DOCX/MD/TXT) as the user's current CV with versioning. Use whenever the user sends a CV file.
version: 1.0.0
metadata:
  hermes:
    tags: [cv, storage]
    requires_toolsets: [terminal]
---

# cv-store

## When to Use
The user sent a document and called it a CV/resume, or sent a PDF/DOCX to you with "new CV".

## Procedure
1. Find the saved path in the gateway note ("It is saved at: <path>").
2. Run in the terminal: `python3 ~/.hermes/profiles/cv-analyst/bin/cv_store.py store "<path>"`
3. Parse the JSON it prints:
   - `stored` → `read_file` the new `~/.hermes/profiles/cv-analyst/cv/current.md`; if `previous_version` is not null also read `~/.hermes/profiles/cv-analyst/cv/history/v<previous_version>.md` and summarize what changed in 2–3 lines. Reply: "✅ CV v<version> saved (<date>): <headline: current title, years, top skills>. Changes vs v<prev>: …".
   - `unchanged` → reply "Same CV as v<version>, nothing changed."
   - `error` → reply with the message and what to send instead.
4. Update memory: replace the old "Current CV:" entry (or add one) with `Current CV: cv/current.md v<version> (<date>, <headline>)`.

## Pitfalls
- Do not paste the whole CV into the chat.
- Do not skip the script and write CV files by hand — versioning must stay consistent.
- The Telegram document cache is cleaned periodically; the stored copy under cv/ is the one that lasts.

## Verification
`python3 ~/.hermes/profiles/cv-analyst/bin/cv_store.py show` prints the new version.
