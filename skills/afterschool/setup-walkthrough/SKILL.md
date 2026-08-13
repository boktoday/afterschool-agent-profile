---
name: setup-walkthrough
description: Use when the student is at the setup stage of the Afterschool Agent profile and needs help installing Piper TTS, getting a Jina AI free API key, configuring Telegram or WhatsApp delivery, or putting the Eight Essentials guide MD files into essentials/. Walk through each step, verify each, and pause at the credential gates.
version: 1.0.0
author: Afterschool Agent contributors
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - afterschool
    - setup
    - piper
    - jina
    - telegram
    - whatsapp
    related_skills:
    - afterschool-agent-onboarding
    - morning-minute
    - afterschool-checkin
    - eight-essentials-curriculum
---
# Setup Walkthrough

The Afterschool Agent profile needs four things beyond the stock
Hermes setup: **Piper TTS**, **Jina AI search**, a **delivery
channel** (Telegram or WhatsApp), and the **Eight Essentials
guide MD files** in `essentials/01..08/`.

This skill walks the student (or the parent setting up for a
younger student) through each one. Each step pauses at the
credential or installation gate. The student (or parent) does the
work — the agent never types a password, key, or token into chat.

## Order of operations

1. Piper TTS install + voice pick
2. Jina AI free API key
3. Telegram **or** WhatsApp delivery channel
4. Eight Essentials guide MD files in `essentials/`

## Step 1 — Piper TTS install

The Morning Minute is audio. Piper is the TTS engine. The student
needs it installed locally. No cloud TTS — Piper runs offline.

### What the student needs

- A working Python 3.10 or 3.11 (NOT 3.10 from the Windows Store
  shim — use a real install). Verify with:

  ```bash
  python --version
  ```

- The Piper binary. Two options:

  - **Native binary** (recommended on Windows): pre-built
    `piper.exe` shipped with OpenHuman at
    `C:/Users/insig/.openhuman/bin/piper/piper/piper.exe`.
    Verify it exists and runs:

    ```bash
    "/c/Users/insig/.openhuman/bin/piper/piper/piper.exe" --help
    ```

  - **Python package** (Linux/macOS): `pip install piper-tts`.
    Note: in this environment, the Python `piper` package is dead
    in the Hermes venv. Use the native binary if available.

### Voice model download

The student picks a voice at onboarding. The agent fetches the
matching voice model from Hugging Face. The orientation walks
through this.

Common picks:

| Voice | Hugging Face path |
|---|---|
| `en_GB-alan-medium` (UK male) | `rhasspy/piper-voices/resolve/main/en/en_GB/alan/medium/en_GB-alan-medium.onnx` (+ `.onnx.json`) |
| `en_GB-jenny_dioco-medium` (UK female) | `rhasspy/piper-voices/resolve/main/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx` (+ `.onnx.json`) |
| `en_US-amy-medium` (US female) | `rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx` (+ `.onnx.json`) |
| `en_US-joe-medium` (US male) | `rhasspy/piper-voices/resolve/main/en/en_US/joe/medium/en_US-joe-medium.onnx` (+ `.onnx.json`) |
| `en_AU-natasha-medium` (AU female) | `rhasspy/piper-voices/resolve/main/en/en_AU/natasha/medium/en_AU-natasha-medium.onnx` (+ `.onnx.json`) |

The fetch pattern:

```bash
VOICE=en_GB-jenny_dioco-medium
BASE="C:/Users/insig/projects/onetoeight-essentials/piper-voices"
mkdir -p "$BASE/en/en_GB/jenny_dioco/medium"
curl -sL --fail "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/jenny_dioco/medium/${VOICE}.onnx" \
  -o "$BASE/en/en_GB/jenny_dioco/medium/${VOICE}.onnx"
curl -sL --fail "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/jenny_dioco/medium/${VOICE}.onnx.json" \
  -o "$BASE/en/en_GB/jenny_dioco/medium/${VOICE}.onnx.json"
```

### Verify

Run a tiny test synthesis:

```bash
echo "The Morning Minute is ready." | \
  "/c/Users/insig/.openhuman/bin/piper/piper/piper.exe" \
    -m "C:/Users/insig/projects/onetoeight-essentials/piper-voices/en/en_GB/<voice>/medium/<voice>.onnx" \
    -f /tmp/piper-test.wav
```

Listen to the output. If it sounds right, mark Piper as configured
in memory and move on.

### What to write to .env

The voice path goes into the Morning Minute skill's memory, not
`.env`. The Piper binary path is also a memory value. Both are
machine-specific.

## Step 2 — Jina AI free API key

The agent needs a way to do web search and page fetch for
research during lessons. The free Jina AI tier is enough for a
teenager's daily use.

### Sign up

The student (or parent) signs up at <https://jina.ai/> and gets a
free API key. The free tier gives enough searches per month for
daily use. No credit card needed for the basic free tier.

### Add to .env

The agent does NOT ask for the key in chat. The student adds it
themselves:

```bash
JINA_API_KEY=jina_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

The agent then verifies it works:

```bash
curl -s -H "Authorization: Bearer $JINA_API_KEY" \
  "https://s.jina.ai/https://hermes-agent.nousresearch.com/docs"
```

If the response is a clean snippet of the docs page, Jina is
working. Mark it as configured in memory.

## Step 3 — Telegram or WhatsApp delivery

The Morning Minute and the Afterschool Check-In both go to the
student's chosen channel. The agent walks the student through
whichever they pick.

### Option A — Telegram

Easier. Telegram has a clear bot API. The agent walks the student
through:

1. **Create a bot** via BotFather in Telegram. The student opens
   Telegram, searches for `@BotFather`, sends `/newbot`, and
   follows the prompts. Telegram gives a bot token. The student
   pastes it into `.env`:

   ```bash
   TELEGRAM_BOT_TOKEN=123456:abcdef...
   TELEGRAM_CHAT_ID=<student's chat id>
   ```

   The student can find their chat id by messaging
   `@userinfobot` or by sending a message to the bot and reading
   the `chat.id` from the bot's webhook update.

2. **Verify** the agent can send a test message:

   ```python
   import os, urllib.request
   token = os.environ["TELEGRAM_BOT_TOKEN"]
   chat = os.environ["TELEGRAM_CHAT_ID"]
   req = urllib.request.Request(
       f"https://api.telegram.org/bot{token}/sendMessage",
       data=f'{{"chat_id": "{chat}", "text": "Afterschool Agent is set up. See you at 6 am."}}'.encode(),
       headers={"Content-Type": "application/json"},
   )
   urllib.request.urlopen(req, timeout=15).read()
   ```

   If the student receives the test message, Telegram is configured.

### Option B — WhatsApp

Harder. WhatsApp does not have an official bot API for personal
numbers. The agent walks the student through one of:

- **WhatsApp Business API** via a BSP (Business Solution Provider)
  like Twilio. Costs money per message. The student signs up,
  gets a sandbox number, and pastes the credentials into `.env`.
- **A personal bridge** like Baileys (Node.js). Free, but the
  student needs Node.js installed and to keep a session running.
  Mention this only if the student asks — don't push it.

For most teenagers, **Telegram is the right choice** — easier,
clearer, and the audio player renders inline. Recommend Telegram
first. Mention WhatsApp as a fallback for households that don't
use Telegram.

### Verify

After the test message lands, mark the channel as configured in
memory and move on.

## Step 4 — Eight Essentials guide MD files

The agent teaches from `essentials/01..08/lessons/*.md`. The
student (or whoever set up the profile) needs to drop the
relevant chapter of their guide into each folder.

### What to put where

```
essentials/01-silence/lessons/        ← chapter on Silence
essentials/02-body/lessons/           ← chapter on Body
essentials/03-skills/lessons/         ← chapter on Skills
essentials/04-digital-self-defence/lessons/
essentials/05-community/lessons/
essentials/06-knowledge/lessons/
essentials/07-nature/lessons/
essentials/08-faith/lessons/          ← chapter on Faith
                                       (branch into .christian.md
                                        and .universal.md if both
                                        are needed)
```

See `essentials/01-silence/lessons/README.md` for the file schema
(introduction, body, "try this", reflection, quote).

### Verify

The agent reads each folder and confirms at least one lesson file
is present:

```bash
for d in essentials/*/lessons/; do
  echo "--- $d ---"
  ls "$d"
done
```

If a folder has only `README.md`, the chapter hasn't been dropped
yet. Politely say so and offer to help.

## Pitfalls

- **Asking for credentials in chat.** Never ask for the Jina key,
  Telegram bot token, or WhatsApp credentials in chat. Walk the
  student to where they add it themselves.
- **Generating lesson content from scratch.** If `essentials/08-faith/lessons/`
  is empty, say so. Do not invent a chapter on Faith.
- **Skipping verification.** Each step has a real verification
  check (a Piper test synthesis, a Jina search, a Telegram test
  message, a file listing). Don't mark a step complete until the
  check passes.
- **Mixing traditions.** If the student chose Universal at
  onboarding, don't push them into Scripture quotes. If they
  chose Christian, don't push them into "find your own truth"
  framings.

## Related skills

- `afterschool-agent-onboarding` — the broader onboarding flow
  that calls this skill for the four setup steps.
- `morning-minute` — uses Piper and the delivery channel that
  this skill configures.
- `eight-essentials-curriculum` — reads the guide MD files that
  this skill helps the student load.