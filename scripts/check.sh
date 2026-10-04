#!/usr/bin/env bash
# Sanity checks for an installed Job War Room. Never prints secrets. Exit 1 if anything is wrong.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
HH="${HERMES_ROOT:-$HOME/.hermes}"
fail=0
ok()  { echo "  ok   $*"; }
bad() { echo "  FAIL $*"; fail=1; }
has() { grep -q "^$1=." "$2" 2>/dev/null; }

echo "Gateway (default profile)"
grep -Eq '^[[:space:]]*multiplex_profiles:[[:space:]]*true' "$HH/config.yaml" && ok "multiplex_profiles: true" || bad "gateway.multiplex_profiles is not true in $HH/config.yaml"
grep -Eq '^group_sessions_per_user:[[:space:]]*false' "$HH/config.yaml" && ok "group_sessions_per_user: false" || bad "group_sessions_per_user must be false in $HH/config.yaml (README step 5)"
command -v pdftotext >/dev/null && ok "pdftotext installed" || bad "pdftotext missing (sudo apt install poppler-utils)"

for p in coordinator scout cv-analyst; do
  home="$HH/profiles/$p"
  echo "$p"
  [ -d "$home" ] || { bad "profile missing; run scripts/setup.sh"; continue; }
  [ "$(readlink -f "$home/SOUL.md")" = "$REPO/agents/$p/SOUL.md" ] && ok "SOUL.md linked to repo" || bad "SOUL.md not linked; run scripts/setup.sh"
  grep -q "$REPO/agents/$p/skills" "$home/config.yaml" 2>/dev/null && ok "config.yaml installed" || bad "config.yaml stale; run scripts/setup.sh"
  for k in TELEGRAM_BOT_TOKEN OPENAI_API_KEY TELEGRAM_ALLOWED_USERS; do
    has "$k" "$home/.env" && ok "$k set" || bad "$k missing in $home/.env"
  done
  [ "$(stat -c %a "$home/.env" 2>/dev/null)" = 600 ] && ok ".env mode 600" || bad ".env should be chmod 600"
done

echo "cv-analyst storage"
[ -x "$HH/profiles/cv-analyst/bin/cv_store.py" ] && ok "bin/cv_store.py" || bad "bin/cv_store.py missing; run scripts/setup.sh"
python3 "$HH/profiles/cv-analyst/bin/cv_store.py" show --root "$HH/profiles/cv-analyst/cv" 2>/dev/null \
  | grep -q '"version"' && ok "CV stored" || echo "  info no CV stored yet (upload one in the group)"

tokens=$(for p in coordinator scout cv-analyst; do grep -h '^TELEGRAM_BOT_TOKEN=' "$HH/profiles/$p/.env" 2>/dev/null; done | sort | uniq -d | wc -l)
[ "$tokens" = 0 ] && ok "bot tokens are distinct" || bad "two profiles share the same bot token"

[ "$fail" = 0 ] && echo "All checks passed." || echo "Some checks failed."
exit "$fail"
