#!/usr/bin/env bash
# Usage: scripts/set-token.sh <coordinator|scout|cv-analyst>  — reads the BotFather token without echo.
set -euo pipefail
p="$1"; envf="${HERMES_ROOT:-$HOME/.hermes}/profiles/$p/.env"
[ -f "$envf" ] || { echo "run scripts/setup.sh first" >&2; exit 1; }
read -rsp "Paste bot token for $p: " tok; echo
[[ "$tok" =~ ^[0-9]+:[A-Za-z0-9_-]{30,}$ ]] || { echo "doesn't look like a bot token" >&2; exit 1; }
sed -i '/^TELEGRAM_BOT_TOKEN=/d' "$envf"; printf 'TELEGRAM_BOT_TOKEN=%s\n' "$tok" >> "$envf"
echo "$p: token saved"
