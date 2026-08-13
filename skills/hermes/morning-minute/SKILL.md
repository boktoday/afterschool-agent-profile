---
name: morning-minute
description: Use when generating the daily 6 am Morning Minute audio + text plan for the Afterschool Agent student. Reads the day's essential from essentials/, drafts a brief plan, runs Piper TTS, and delivers to the student's chosen channel (Telegram or WhatsApp).
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
    - morning-minute
    - piper
    - tts
    - cron
    - eight-essentials
    related_skills:
    - afterschool-agent-onboarding
    - afterschool-checkin
    - eight-essentials-curriculum
    - setup-walkthrough
---
# Morning Minute

The **Morning Minute** is the daily 6 am plan the student receives
as audio + text in their chosen channel (Telegram or WhatsApp). It
names the day's essential, the day's one small action, and — for
Christian students — a Scripture quote. For Universal students, a
wisdom reflection replaces the verse.

Despite the name, the audio is **not constrained to one minute.**
The name is a brand. The audio is whatever length the day's plan
needs — typically 60 to 120 seconds. Long enough to settle the
student into the day, short enough to listen to while getting ready.

## Input contract

Before generating, the agent must have:

1. **Tradition** — `christian` or `universal` (from onboarding).
2. **Delivery channel** — `telegram` or `whatsapp`, with credentials
   configured in `.env`.
3. **Voice** — the Piper voice the student picked at onboarding,
   plus the path to the voice model.
4. **Day-N essential** — today's essential of the week. The default
   cycle is one essential per day, repeating. The student can pin
   an essential to focus on a season (set in memory).
5. **Recent lessons read** — the agent keeps a memory log of which
   lessons it has already referenced for this student, so it does
   not repeat the same teaching.
6. **Yesterday's check-in** — what the student said they would do
   today. The Morning Minute opens with a brief callback if there
   was one.

## Output contract (every run must produce all three)

1. **Audio file** — OGG Opus, mono, ~24 kbps, 60–120 s typical,
   `morning-minute-YYYY-MM-DD.ogg` written to the canonical path,
   uploaded to the delivery channel as a public URL, and delivered
   inline with `MEDIA:<public-url>` on its own line.
2. **Intro line** — one short greeting in the student's chosen
   voice (e.g., *"Good morning, Sam. Here's your minute."*).
3. **Plan text** — the day's essential, the day's one small
   action, the Scripture quote or wisdom reflection, and a single
   sentence for the student to sit with during the day. This is
   the body that gets both read by Piper and delivered as text.

Never skip the audio. Never skip the text. The student is meant to
do both — listen and read.

## Step 1 — Pick the day's essential and lesson

Default cycle: rotate through the eight essentials one per day, in
order. Day 1 = Silence, Day 2 = Body, ..., Day 8 = Faith, Day 9 =
Silence again.

Read `essentials/<NN-name>/SKILL.md` first to ground yourself in
the essential's teaching notes. Then read the next unread
`lessons/*.md` file in `essentials/<NN-name>/lessons/` (alphanumeric
order, branching by tradition if `<file>.christian.md` or
`<file>.universal.md` exists).

Track which lesson files you have read for this student in memory
(`hermes memory store`) so you do not repeat them within ~30 days.

## Step 2 — Compose the plan text (~120 to ~200 words)

The plan has three parts. Read each aloud as you draft it, because
Piper will read it aloud too.

### Part A — Callback (5 to 15 seconds spoken)

If yesterday's check-in captured a "today I'll do X" promise, open
with a brief, warm callback. *"Yesterday you said you'd try the
two-minute chair before dinner. Today's the day."*

If there was no check-in, skip this part and start with the greeting.

### Part B — The day's essential and action (45 to 90 seconds)

- Greet the student by name (or as the parent named them at
  onboarding).
- Name the day's essential in one short sentence. Not a lecture,
  not a definition. Just the name and a one-line why.
- Give the day's **one small action**. Singular. Concrete. Under
  five minutes. Phrased as a verb the student can do today, not a
  concept they can think about.
- One sentence on *why* this action works in plain language.

### Part C — The quote or reflection (15 to 30 seconds)

**Christian:** one verse, quoted accurately, with the reference read
naturally (see Step 4). One short sentence after it.

**Universal:** one short wisdom reflection — a question, a line
from a thinker, a sentence the student can hold during the day. No
attribution to religious texts. Attribution to a thinker is fine.

### Closing (5 to 10 seconds)

End with a steady, warm line: *"That's your minute. Have a good
day."* Or whatever the student chose at onboarding. Don't moralise.
Don't instruct. Just close.

## Step 3 — Pre-clean the text for TTS

Before passing the text to Piper:

- **Strip em dashes.** Replace `—` with `,` or a period. Piper
  reads em dashes slowly and can stumble on them.
- **Rewrite references as natural speech.** `— Psalm 46:10` becomes
  `From the book of Psalms, chapter forty-six, verse ten.` Bare
  `46:10` reads badly. Same for any other numeric reference.
- **Spell out abbreviations on first use.** `AI` → `A.I.`, `PhD` →
  `Ph.D.`, `St.` (saint) → `Saint`. Piper sometimes pronounces
  abbreviations as words.
- **Sentence-end every line.** Piper is happier with full stops
  than with run-on sentences. Break long sentences.
- **Drop hashtags, URLs, and Markdown formatting.** Piper reads
  `#` as "hash". Strip Markdown.

Save the cleaned text to the canonical path the cron uses. See
"File paths" below.

## Step 4 — Piper TTS (offline, native exe on Windows)

The pre-built pattern, verified to work in this environment:

```bash
"/c/Users/insig/.openhuman/bin/piper/piper/piper.exe" \
  -m "C:/Users/insig/projects/onetoeight-essentials/piper-voices/en/en_GB/<voice>/medium/<voice>.onnx" \
  -f "C:/Users/insig/morning-minute-today.wav" \
  < /c/Users/insig/morning-minute-tts.txt
```

**Voice catalogue** — verify the voice exists at the path before
running. The orientation should have set this up. Common picks:

| Voice | Path fragment |
|---|---|
| `en_GB-alan-medium` (UK male) | `piper-voices/en/en_GB/alan/medium/` |
| `en_GB-jenny_dioco-medium` (UK female) | `piper-voices/en/en_GB/jenny_dioco/medium/` |
| `en_US-amy-medium` (US female) | `piper-voices/en/en_US/amy/medium/` |
| `en_US-joe-medium` (US male) | `piper-voices/en/en_US/joe/medium/` |
| `en_AU-natasha-medium` (AU female) | `piper-voices/en/en_AU/natasha/medium/` |

If the student picked `jenny_dioco` (or any non-Alan voice), fetch
the model on first use:

```bash
mkdir -p "C:/Users/insig/projects/onetoeight-essentials/piper-voices/en/en_GB/jenny_dioco/medium"
curl -sL --fail "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx" \
  -o "C:/Users/insig/projects/onetoeight-essentials/piper-voices/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx"
curl -sL --fail "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx.json" \
  -o "C:/Users/insig/projects/onetoeight-essentials/piper-voices/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx.json"
```

The orientation skill (see `setup-walkthrough`) walks the student
through installing Piper and choosing a voice the first time.

**PATH PITFALL:** every path passed to `piper.exe` must be native
`C:\...`. MSYS `/c/...` paths get mangled. Use forward-slash
native (`C:/...`) for stdin redirect, but back-slash native
(`C:\...`) for `-m` and `-f`.

## Step 5 — Convert to OGG for Telegram / WhatsApp

```bash
ffmpeg -y -hide_banner -loglevel error \
  -i "C:/Users/insig/morning-minute-today.wav" \
  -c:a libopus -b:a 24k \
  "C:/Users/insig/morning-minute-today.ogg"
```

Sanity check the output: ~250 to ~450 KB and ~60 to ~120 s. A
result under 200 KB or under 45 s suggests the TTS input was
truncated.

## Step 6 — Upload to here.now and deliver

Both Telegram and WhatsApp need a **public URL** to render an
inline audio player. Local Windows paths do not render. Upload to
the user's here.now drive first.

```python
import urllib.request, json, hashlib, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Read here.now credentials
API_KEY = open(r"C:\Users\insig\.herenow\credentials").read().strip()
DRIVE_ID = "drv_01kq8g6hkfmnmfqngr18xyx3mb"  # user may have a different drive
BASE = "https://here.now"
h = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

ogg_path = r"C:\Users\insig\morning-minute-today.ogg"
drive_path = "afterschool/morning-minute-today.ogg"

with open(ogg_path, "rb") as f:
    data = f.read()

# Stage + upload + finalize + publish
list_url = f"{BASE}/api/v1/drives/{DRIVE_ID}/files?prefix={drive_path}&limit=10"
req = urllib.request.Request(list_url, headers={"Authorization": f"Bearer {API_KEY}"})
with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
    existing = next((f for f in json.loads(r.read()).get("files", []) if f["path"] == drive_path), None)

stage = {"path": drive_path, "size": len(data), "contentType": "audio/ogg", "sha256": hashlib.sha256(data).hexdigest()}
stage["ifMatch" if existing else "ifNoneMatch"] = existing["etag"] if existing else "*"
req = urllib.request.Request(f"{BASE}/api/v1/drives/{DRIVE_ID}/files/uploads", data=json.dumps(stage).encode(), headers=h, method="POST")
with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
    sd = json.loads(r.read())

req = urllib.request.Request(sd["uploadUrl"], data=data, headers={"Content-Type": "audio/ogg"}, method="PUT")
with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
    print(f"Upload: {r.status}")

fin = {"uploadId": sd["uploadId"]}
req = urllib.request.Request(f"{BASE}/api/v1/drives/{DRIVE_ID}/files/finalize", data=json.dumps(fin).encode(), headers=h, method="POST")
with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
    print("Finalized")

pub = {"driveId": DRIVE_ID}
req = urllib.request.Request(f"{BASE}/api/v1/publish/from-drive", data=json.dumps(pub).encode(), headers=h, method="POST")
with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
    pd = json.loads(r.read())
    ogg_url = f"{pd['siteUrl'].rstrip('/')}/{drive_path}"
    print(f"Public URL: {ogg_url}")
```

## Step 7 — Deliver in the channel

The delivery pattern depends on the channel:

### Telegram

```python
telegram(
    chat_id=os.environ["TELEGRAM_CHAT_ID"],
    text=plan_text_with_intro,
    media_url=ogg_url,
)
```

The Telegram adapter renders the `media_url` as an inline audio
player. The text arrives below the player.

### WhatsApp

WhatsApp delivery uses the WhatsApp Business API (or a personal
bridge like Baileys). The orientation skill walks the student
through this. The pattern is the same: send a media message with
the public URL and the text below.

## Step 8 — Archive (optional but recommended)

Save each day's plan text to `~/.hermes/profiles/afterschool/morning-minute-archive.md`:

```markdown
## 12 August 2026

**Essential:** Silence
**Action:** Sit in the chair for two minutes before dinner.
**Quote:** "Be still, and know that I am God." — Psalm 46:10

<full plan text>

[Listen](morning-minute-2026-08-12.ogg)

---
```

This gives the student (and a parent or mentor) a permanent record
of what was sent. Useful for review and for catching a streak of
missed days.

## Cron configuration

The morning-minute cron runs at 6 am (or whatever the student
chose) in the student's timezone. Schedule format: `0 6 * * *` for
daily, `0 6 * * 1-5` for weekdays, `0 6 * * 0,6` for weekends.

**Pinned model:** `deepseek-v4-flash` via the `deepseek` provider.
Verified working in this environment.

**Delivery target:** `origin` (Telegram or WhatsApp) is the
default. Set `deliver=local` if the channel is flaky — the audio
file lands in the archive, and the agent picks it up the next time
the student chats.

## Pitfalls

- **Telegram delivery timeouts.** A long agent loop can exceed
  Telegram's send window. The audio is always generated and
  archived; only the Telegram push can fail. If it does, deliver
  the audio manually in the chat with `MEDIA:<public-url>` on its
  own line, then the plan text.
- **MSYS path mangling** with piper and python. See Step 4.
- **Em dashes in the TTS input.** Replace with commas. Piper reads
  them slowly and can mispronounce.
- **Repeating the same lesson too often.** Track which lesson
  files have been read for this student. Don't repeat one within
  ~30 days.
- **Repeating the same Scripture or reflection quote.** Maintain a
  recent-quotes log in memory. Pick a verse or reflection not used
  in the last ~14 entries.
- **The plan text drifts longer every day.** If it goes over ~200
  words, the audio goes over two minutes. Cut. The discipline is
  in the constraint.
- **Forgetting tradition.** A Christian student should not get a
  reflection from Marcus Aurelius in their Morning Minute. A
  Universal student should not get a Psalm. Verify tradition in
  memory before generating.

## Related skills

- `afterschool-checkin` — the afternoon check-in that pairs with
  this morning plan.
- `eight-essentials-curriculum` — the skill that reads the guide
  MD files and teaches from them.
- `setup-walkthrough` — walks the student through installing
  Piper, getting a Jina key, configuring Telegram or WhatsApp.
- `afterschool-agent-onboarding` — sets the student's tradition,
  voice, and channel.