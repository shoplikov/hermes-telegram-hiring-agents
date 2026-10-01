# Failure log

Real failures observed while building and testing Job War Room. Each row: what was asked, what went wrong, why, and the fix (or proposed fix).

| # | Request / step | Symptom | Cause | Fix |
|---|---|---|---|---|
| 1 | Spike: user asked coordinator to post `@scout TASK#0 ...` | Scout never reacted to the coordinator's message; scout gateway log shows no inbound update after 11:57:06 | Telegram does not deliver bot-authored group messages to other bots unless Bot-to-Bot Communication Mode (Bot API, May 2026) is enabled in @BotFather; Hermes `allow_bots` can only act on updates Telegram sends | Enable Bot-to-Bot Communication Mode for all three bots in @BotFather |
| 2 | Same spike message | Scout ALSO answered the human's message directly (two bots replied) | The human's text contained the literal `@alish_company_scout_bot` inside quotes; `exclusive_bot_mentions` routes a message to every bot it mentions, quoted or not | Expected behaviour of mention routing. Humans address one bot per message; handoffs come from the coordinator |

## Notes

- Bot-to-bot delivery spike (2026-10-01): failed without Bot-to-Bot Communication Mode (rows 1–2). Re-test after enabling it.
