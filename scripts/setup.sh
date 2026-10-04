#!/usr/bin/env bash
# Install Job War Room agents into Hermes profiles. Idempotent; never prints secrets.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
HH="${HERMES_ROOT:-$HOME/.hermes}"
# Bot usernames fill the {{..._BOT}} placeholders in SOUL.md and skills.
# shellcheck source=/dev/null
. "$REPO/bots.env"
for v in COORDINATOR_BOT SCOUT_BOT ANALYST_BOT; do
  [[ "${!v:-}" =~ ^[A-Za-z0-9_]{5,32}$ ]] || { echo "bots.env: $v must be a bot username without @" >&2; exit 1; }
done
render() { sed -e "s/{{COORDINATOR_BOT}}/$COORDINATOR_BOT/g" -e "s/{{SCOUT_BOT}}/$SCOUT_BOT/g" -e "s/{{ANALYST_BOT}}/$ANALYST_BOT/g" "$@"; }
command -v hermes >/dev/null || { echo "hermes not found: install Hermes Agent first" >&2; exit 1; }
command -v pdftotext >/dev/null || echo "WARN: pdftotext missing; PDF CVs will fail (sudo apt install poppler-utils)" >&2
for p in coordinator scout cv-analyst; do
  home="$HH/profiles/$p"
  [ -d "$home" ] || hermes profile create "$p" --no-skills --no-alias >/dev/null
  sed -e "s#__REPO__#$REPO#g" -e "s#__PROFILE_HOME__#$home#g" \
      "$REPO/agents/$p/config.yaml" > "$home/config.yaml"
  rm -f "$home/SOUL.md"; render "$REPO/agents/$p/SOUL.md" > "$home/SOUL.md"
  # Skills are rendered into the profile too, so the repo itself stays username-free.
  rm -rf "$home/war-room-skills"; mkdir -p "$home/war-room-skills"
  if [ -d "$REPO/agents/$p/skills" ]; then
    cp -r "$REPO/agents/$p/skills/." "$home/war-room-skills/"
    find "$home/war-room-skills" -name SKILL.md -print0 | while IFS= read -r -d '' f; do
      render "$f" > "$f.tmp" && mv "$f.tmp" "$f"
    done
  fi
  touch "$home/.env"; chmod 600 "$home/.env"
  # Copy shared non-bot secrets from the default profile without echoing them.
  for k in OPENAI_API_KEY TELEGRAM_ALLOWED_USERS; do
    if ! grep -q "^$k=" "$home/.env"; then
      grep "^$k=" "$HH/.env" >> "$home/.env" || echo "WARN: $k missing in default profile" >&2
    fi
  done
  grep -q '^TELEGRAM_BOT_TOKEN=.' "$home/.env" && t=set || t=MISSING
  echo "$p: installed (bot token: $t)"
done
mkdir -p "$HH/profiles/cv-analyst/cv/history" "$HH/profiles/cv-analyst/bin"
# Stable path for the CV helper so the skill does not depend on where the repo lives.
ln -sfn "$REPO/agents/cv-analyst/skills/cv-store/scripts/cv_store.py" "$HH/profiles/cv-analyst/bin/cv_store.py"
grep -Eq '^group_sessions_per_user:[[:space:]]*false' "$HH/config.yaml" ||
  echo "WARN: set 'group_sessions_per_user: false' in $HH/config.yaml (README step 5)" >&2
echo "Restart the gateway to apply: hermes gateway restart. Then run scripts/check.sh"
