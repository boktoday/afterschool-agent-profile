# Afterschool Agent — overview and setup workflow

The **Afterschool Agent** is a personalised AI assistant built on
[Hermes Agent](https://hermes-agent.nousresearch.com/docs) for
teenagers (13–17) learning to put the **Eight Essentials** into daily
practice. It is a gentle mentor that runs a daily rhythm of audio
plans, reflection check-ins, and small actions, taught from a guide of
Markdown files the student (or their parent) drops into the repo.

This README is the overview and the workflow for getting the agent
working end to end. It is meant to be read once, with the video
tutorial alongside.

---

## What this product is

A teen learns the Eight Essentials best by **doing one small thing a
day** over weeks and months — not by reading a book. The Afterschool
Agent exists to make that daily rhythm stick:

- A **Morning Minute** lands at 6 am in the student's chat (Telegram
  or WhatsApp). It's a brief audio plan for the day, plus text.
- An **Afterschool Check-In** lands in the afternoon. It's a short
  text message: how the day went, what's next, one question to sit
  with overnight.
- The agent teaches from the **Eight Essentials guide** stored in the
  repo (`essentials/01..08/lessons/*.md`), branching by the student's
  chosen tradition.

The agent does not lecture. It draws the wisdom out of the student
with questions, holds the rhythm gently, and restarts them when they
fall off — without scolding.

### Two traditions

Every student picks one at onboarding. The agent stays inside the
chosen tradition; it never mixes the two:

- **Christian** — Bible-anchored. Scripture is honoured and quoted
  accurately. The Morning Minute includes a Scripture quote. The
  check-in frames the day inside a living faith.
- **Universal (secular)** — wisdom traditions honoured without
  doctrine. The Morning Minute includes a wisdom reflection. The
  check-in frames the day inside reflection, gratitude, and
  intention.

The student can change tradition later, but lessons will branch from
that moment on.

### The Eight Essentials (in the order the guide teaches them)

1. **Silence** — sit still, be alone with your own thoughts
2. **Body** — sleep, food, water, movement, sunlight
3. **Skills** — useful real-world competence (cook, fix, build, budget)
4. **Digital Self-Defence** — privacy, attention, identity literacy
5. **Real Community** — people who know your name
6. **Knowledge Without Wi-Fi** — owned, not rented
7. **Nature** — prescribed time outside, non-negotiable
8. **Tested Faith** — yours, and it holds under pressure

---

## How it works

### The daily loop

```
06:00  Morning Minute       Piper TTS audio + text → Telegram or WhatsApp
        ↓
day    Student does the one small action
        ↓
17:00  Afterschool Check-In  Text only → Telegram or WhatsApp
        ↓
        Plan tomorrow
        ↓
        Sleep
        ↓
        Repeat
```

The agent reinforces the loop without nagging. Missed days restart
gently. No scolding. No moralising.

### The agent's job at each turn

| When | The agent |
|---|---|
| First chat on a fresh profile | Offers the orientation, briefly, in its own voice |
| Student says "set me up" | Runs `afterschool-agent-onboarding` (consent-gated, phased) |
| Student asks a question | Reads the relevant `essentials/<NN-name>/lessons/*.md`, synthesises, teaches |
| Morning Minute cron fires | Generates the day's plan, runs Piper, uploads, delivers inline |
| Check-In cron fires | Reads the most recent Morning Minute, drafts a short reflection, delivers as text |
| Student asks for a deeper dive | Uses the `eight-essentials-curriculum` skill — reads the guide, teaches from it |

### What runs in the background

Two cron jobs, both off until the student approves them at onboarding:

1. **Morning Minute** — default schedule `0 6 * * *` (every day at 6
   am in the student's timezone). Generates audio + text and delivers.
2. **Afterschool Check-In** — default schedule `0 17 * * *` (every
   day at 5 pm). Sends a short text message.

Both can be customised: weekdays only, weekends only, different
times. Both are **opt-in** — the orientation creates them only after
explicit approval.

---

## The setup workflow

This is the end-to-end process to go from a fresh clone to a working
agent that sends its first Morning Minute.

### 1 — Prerequisites (one-time, on the machine)

You need:

- **Hermes Agent** installed. Quick check: `hermes --version`. See
  the [install guide](https://hermes-agent.nousresearch.com/docs).
- **Python 3.10 or 3.11** (not the Windows Windows Store shim — a
  real install). `python --version`.
- **Piper TTS.** A working install. Either a pre-built `piper.exe`
  (e.g. `C:/Users/insig/.openhuman/bin/piper/piper/piper.exe`) or the
  `piper-tts` package via `pip install piper-tts`.
- **ffmpeg** for WAV → OGG conversion. `ffmpeg -version`.
- **A model provider key** (opencode, OpenRouter, or another
  OpenAI-compatible endpoint). The profile defaults to
  `opencode + deepseek-v4-flash`. You add the key with `hermes setup`.
- **A Jina AI free API key** for web search. Sign up free at
  <https://jina.ai/> — no credit card. The free tier is enough for a
  teenager's daily use.
- **A Telegram bot** (recommended) or a WhatsApp bridge. Telegram is
  much easier — see step 4.

### 2 — Clone the profile (one-time)

```bash
mkdir -p ~/.hermes/profiles
git clone https://github.com/boktoday/afterschool-agent-profile.git \
  ~/.hermes/profiles/afterschool
hermes --profile afterschool chat
```

That's it. The repo **is** the profile. Updates later are just
`git -C ~/.hermes/profiles/afterschool pull`.

### 3 — First chat → orientation

On the first chat, the agent opens with:

> "Before we dive in — want me to walk you through setup? It takes a
> couple of minutes and gets your tools, memory, and the morning
> minute working the way you want. Or we can skip it and just start."

Say yes (or just ask *"help me set up my profile"* any time). The
`afterschool-agent-onboarding` skill runs.

### 4 — The orientation (10 steps, consent-gated)

The orientation is conversational. The agent asks one small group of
related questions at a time and **pauses at every credential gate** —
it never asks for keys or tokens in chat. Here is what it covers, in
order:

| Step | What happens | Where you add things |
|---|---|---|
| 1. Identity | Names (yours, the student's, the agent's), reply style | Stored in the profile memory |
| 2. Tradition | Christian or Universal | Stored in profile memory |
| 3. Piper install + voice | Verifies Piper works, picks a voice, downloads the voice model | Voice model in `piper-voices/` |
| 4. Jina API key | Sign up free, add to `.env`, agent verifies with a real search | `JINA_API_KEY=` in `.env` |
| 5. Delivery channel | Telegram or WhatsApp bot credentials | `TELEGRAM_BOT_TOKEN=` / `WHATSAPP_*` in `.env` |
| 6. Eight Essentials guide | Confirms the lesson MD files are in `essentials/01..08/lessons/` | Files in the repo |
| 7. Memory | Mnemosyne recommended (local-first, no external account) | `hermes memory setup` |
| 8. Morning Minute schedule | What time, what timezone, what days | Created as a cron job |
| 9. Afterschool Check-In schedule | What time, what timezone, what days | Created as a cron job |
| 10. Token Router (optional) | The plugin that narrows the tool surface | `plugins.enabled` in `config.yaml` |

At the end the agent shows a **Proposed setup** summary and waits for
your explicit approval before applying anything.

### 5 — Verify

Before the first scheduled Morning Minute, verify each piece
individually:

```bash
# Piper works
"/c/Users/insig/.openhuman/bin/piper/piper/piper.exe" --help

# Jina works
curl -s -H "Authorization: Bearer $JINA_API_KEY" \
  "https://s.jina.ai/https://hermes-agent.nousresearch.com/docs"

# Telegram bot works (sends a test message)
# (your test script using urllib + bot token + chat id)

# Guide MD files are present
ls essentials/01-silence/lessons/   # → christian.md + universal.md + README.md
ls essentials/02-body/lessons/      # → christian.md + universal.md
# ... through 08-faith/

# Mnemosyne is configured
hermes memory status

# Cron jobs are queued
hermes cron list    # or `cronjob(action="list")` in chat
```

### 6 — First scheduled run

The Morning Minute fires at the next 6 am in the student's timezone.
It generates audio (Piper), uploads to here.now for a public URL,
delivers to Telegram or WhatsApp as `MEDIA:<url>` plus text. The
Check-In fires at the next 5 pm.

### 7 — Day-to-day operation

The student doesn't interact with the agent through a terminal every
day. The Telegram or WhatsApp chat **is** the daily surface:

- **Morning Minute** arrives as audio + text
- **Afterschool Check-In** arrives as text
- **Reply to the check-in** with a one-line note on how the day went.
  The agent reads it, saves a summary to memory, and uses it as the
  callback in tomorrow's Morning Minute.
- **Ask questions any time.** "What does tested faith actually look
  like?" "How do I find a real community?" The agent reads the guide
  and teaches.

### 8 — Maintenance

Occasional:

- `hermes update` — pulls the standard Hermes skill library into the
  profile (curated skills are never overwritten).
- `git -C ~/.hermes/profiles/afterschool pull` — gets upstream
  improvements to the guide or skills.
- `hermes cron list` — confirms both jobs are still scheduled.

---

## What you'll configure in `.env`

The profile ships with `.env.example` showing every variable. Here is
what you actually set, grouped by who needs what:

### Required (any setup)

```bash
# Model provider key
OPENCODE_API_KEY=...

# Fallback provider (optional)
OPENROUTER_API_KEY=...

# Web search (free)
JINA_API_KEY=jina_...

# Delivery channel — pick one
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

### Required for audio

```bash
# here.now drive (the audio file needs a public URL for Telegram/WhatsApp)
HERENOW_API_KEY=...
HERENOW_DRIVE_ID=drv_...
```

### Optional integrations

```bash
# Notion
NOTION_API_KEY=...

# GitHub (for tracking, opening issues)
GITHUB_TOKEN=...

# Bluesky (if you publish there)
BLUESKY_HANDLE=...
BLUESKY_APP_PASSWORD=...
```

### Things that are NOT env vars

- **Voice model path** — stored in the profile memory, not env. Path
  is machine-specific.
- **Cron schedules** — set via `cronjob(action="create", ...)`,
  stored in the cron registry, not env.
- **Piper binary path** — stored in the profile memory.
- **Mnemosyne** — local-first, no key needed.

---

## What's in the repo

```
afterschool-agent-profile/
├── README.md                              ← this file
├── SOUL.md                                ← persona and operating voice
├── AGENTS.md                              ← operating principles
├── profile.yaml                           ← profile descriptor
├── config.yaml                            ← Hermes runtime config
├── .env.example                           ← every variable, with comments
├── .gitignore
├── LICENSE                                ← MIT
│
├── essentials/                            ← the Eight Essentials source content
│   ├── 00-introduction/lessons/
│   │   ├── README.md                      ← schema for the lesson files
│   │   ├── christian.md                   ← Introduction (Christian edition)
│   │   └── universal.md                   ← Introduction (Universal edition)
│   ├── 01-silence/
│   │   ├── SKILL.md                       ← agent's teaching notes
│   │   ├── lessons/
│   │   │   ├── README.md                  ← file schema
│   │   │   ├── christian.md               ← Chapter 1 (Christian edition)
│   │   │   └── universal.md               ← Chapter 1 (Universal edition)
│   │   └── activities/README.md
│   ├── 02-body/        (same structure)
│   ├── 03-skills/      (same structure)
│   ├── 04-digital-self-defence/
│   ├── 05-community/
│   ├── 06-knowledge/
│   ├── 07-nature/
│   ├── 08-faith/
│   │   ├── lessons/
│   │   │   ├── christian.md               ← Tested Faith + Christian Customisation
│   │   │   └── universal.md               ← Tested Faith + Secular Customisation
│   │   └── activities/README.md
│   ├── 09-conclusion/lessons/{christian,universal}.md
│   └── 10-before-after/lessons/{christian,universal}.md
│
├── skills/                                ← curated skill library
│   ├── hermes/
│   │   ├── afterschool-agent-onboarding/  ← the orientation
│   │   ├── morning-minute/                ← daily 6 am plan
│   │   ├── hermes-mnemosyne/              ← memory provider skill
│   │   ├── mnemosyne-maintenance/
│   │   └── skill-auditor/
│   ├── afterschool/
│   │   ├── afterschool-checkin/           ← afternoon check-in
│   │   ├── eight-essentials-curriculum/   ← teaches from the guide
│   │   └── setup-walkthrough/             ← Piper, Jina, channel setup
│   ├── autonomous-ai-agents/              ← Hermes and OpenCode delegation
│   ├── github/                            ← full GitHub lifecycle
│   ├── note-taking/                       ← Obsidian, daily wrap-up, vault
│   ├── productivity/                      ← Notion, Google, maps
│   ├── research/                          ← source verification, digests
│   ├── creative/                          ← HTML artifacts, collateral
│   ├── software-development/              ← security, reviews
│   └── social-media/                      ← publication link audit
│
├── plugins/hermes-token-router/           ← optional tool-narrowing plugin
├── memories/                              ← generic operating-practice seeds
└── skins/afterschool.yaml                 ← colour theme
```

---

## Configuration reference

### Model provider (`config.yaml`)

```yaml
model:
  default: deepseek-v4-flash
  provider: opencode
fallback_providers:
  - provider: opencode
    model: deepseek-v4-flash
  - provider: openrouter
    model: deepseek-v4-flash
```

Change `provider` and `default` to switch. The fallback chain runs
only when the primary is unavailable.

### Toolsets (`config.yaml`)

Every CLI toolset is **enabled by default**. The orientation walks the
student through reviewing each one. To manually disable:

```bash
hermes --profile afterschool tools
# Or:
hermes --profile afterschool chat --toolsets "web,terminal,file,memory"
```

The `tts` toolset must stay on for the Morning Minute.

### Cron jobs

Create via the orientation. To manage manually:

```python
# List
cronjob(action="list")

# Create Morning Minute
cronjob(
    action="create",
    schedule="0 6 * * *",
    name="Morning Minute",
    prompt="""...""",
    enabled_toolsets=["file", "terminal", "tts"],
)

# Pause without deleting
cronjob(action="pause", job_id="<id>")

# Resume
cronjob(action="resume", job_id="<id>")

# Remove (requires approval — deletes the schedule)
cronjob(action="remove", job_id="<id>")
```

See `skills/hermes/morning-minute/SKILL.md` for the full Morning
Minute cron contract.

---

## Common pitfalls

| Symptom | Likely cause | Fix |
|---|---|---|
| Piper fails to load | Voice model path wrong, or voice not downloaded | Verify path with `piper --help`; re-fetch the model from Hugging Face |
| Morning Minute audio is silent | `piper.exe` got a mangled MSYS path | Use `C:\...` for `-m` and `-f`, `/c/...` only for stdin redirect |
| Telegram audio doesn't render | Local Windows path used instead of public URL | The audio must be uploaded to here.now; the `MEDIA:` directive needs the public URL |
| Cron fails with "Timed out" on the Telegram send | Agent loop ran too long before send | Set `deliver=local`; deliver manually in chat; the audio file is always archived |
| Schedule says daily but only fires weekdays | Wrong cron format | `0 6 * * *` = every day. `0 6 * * 1-5` = weekdays |
| Jina search returns nothing | Key not in `.env` or wrong | `echo $JINA_API_KEY` should show the value; verify with a curl test |
| Agent gives a different tradition's content | Tradition not stored in memory | Run `hermes memory status`; re-run the tradition step of the orientation |
| Lesson file isn't being read | Path wrong, or missing `.christian.md` / `.universal.md` suffix | Check `ls essentials/<NN>/lessons/` |
| Telegram bot doesn't respond | Wrong `chat_id` or the bot hasn't been started | DM `@userinfobot` in Telegram to find your chat id |

---

## Reference: Piper voices

The orientation picks one voice. All of these work offline with Piper:

| Voice | Locale | Style | Hugging Face path |
|---|---|---|---|
| `en_GB-alan-medium` | UK | male | `rhasspy/piper-voices/resolve/main/en/en_GB/alan/medium/` |
| `en_GB-jenny_dioco-medium` | UK | female | `rhasspy/piper-voices/resolve/main/en/en_GB/jenny_dioco/medium/` |
| `en_US-amy-medium` | US | female | `rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/` |
| `en_US-joe-medium` | US | male | `rhasspy/piper-voices/resolve/main/en/en_US/joe/medium/` |
| `en_AU-natasha-medium` | AU | female | `rhasspy/piper-voices/resolve/main/en/en_AU/natasha/medium/` |

Fetch pattern (Alan as example):

```bash
VOICE=en_GB-alan-medium
BASE="C:/Users/insig/projects/onetoeight-essentials/piper-voices"
mkdir -p "$BASE/en/en_GB/alan/medium"
curl -sL --fail "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alan/medium/${VOICE}.onnx" \
  -o "$BASE/en/en_GB/alan/medium/${VOICE}.onnx"
curl -sL --fail "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alan/medium/${VOICE}.onnx.json" \
  -o "$BASE/en/en_GB/alan/medium/${VOICE}.onnx.json"
```

---

## What's in the standard library

`hermes update` pulls the standard Hermes skill library on top of the
curated Afterschool Agent skills. The full inventory at any time:

```bash
hermes --profile afterschool skills list
```

---

## License

MIT — see `LICENSE`.

The Afterschool Agent persona is an original assistant archetype
written for this project. The Eight Essentials guide content is from
the onetoeight *Eight Essentials* Universal Edition V.3.0.0, included
with permission for use inside this profile.