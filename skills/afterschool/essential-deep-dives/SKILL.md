---
name: essential-deep-dives
description: Use when the student asks to go deeper on an essential — an essential summary (key points + a 3 to 5 minute voice note), a three-page HTML lesson (published to here.now with cited sources and a quiz), or a rhyming spoken-word poem. Reads the guide, branches by tradition, and tailors to the student's profile.
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
    - eight-essentials
    - teaching
    - deep-dives
    - here-now
    - tts
    related_skills:
    - eight-essentials-curriculum
    - morning-minute
    - afterschool-checkin
    - setup-walkthrough
---

# Essential Deep Dives

Beyond the daily rhythm (Morning Minute + Afterschool Check-In) and
free-form questions, the student can ask for **three deeper formats**
on any of the Eight Essentials. Each one is a way to *learn* the
essential properly and embed it, not just hear about it:

1. **Essential Summary** — the key points of one essential in plain
   language, plus a 3 to 5 minute voice note the agent generates and
   drops into the chat so the student can listen on the move.
2. **Essential Lesson** — a beautiful three-page lesson built as an
   HTML page and published to the household's here.now account. It
   teaches the essential with **cited sources** (researched via the
   Jina API when the guide needs outside material), **key quotes**,
   and a short **quiz** the student answers on the page. The agent
   sends the link in the chat.
3. **Essential Poem** — a rhyming spoken-word poem on the essential,
   read aloud as a voice note with the text below so the student can
   read along.

All three are **on-demand**: the student just asks. Nothing is
scheduled and nothing requires the student to do anything but say
which essential they want.

## When to use

- The student says "summarise Body for me", "what are the key points
  of Silence", "give me the essentials on Skills", etc. → **Summary**.
- The student says "teach me [essential] properly", "make me a lesson
  on [essential]", "I want to really learn [essential]", "give me a
  full lesson" → **Lesson**.
- The student says "give me a poem about [essential]", "rhyme me
  something on [essential]", "spoken word on [essential]" → **Poem**.

If the request is ambiguous ("tell me about Community"), default to
the **Summary** and offer the lesson or poem as a next step.

## When **not** to use

- For the daily Morning Minute → use `morning-minute`.
- For the daily check-in → use `afterschool-checkin`.
- For a short question or a single-sentence answer → just answer it
  directly, or use `eight-essentials-curriculum`. These three formats
  are for when the student wants *more* than a chat reply.

## Shared preamble — do this first for every format

1. **Read the guide.** Read `essentials/<NN-name>/SKILL.md` (the
   agent's teaching notes) and the relevant `lessons/*.md` file(s)
   first. Branch by tradition: use `<file>.christian.md` /
   `<file>.universal.md` when they exist. The guide is the source of
   truth — these formats *synthesise* it, they never invent
   content from scratch.
2. **Confirm tradition** (`christian` / `universal`) and
   `essentials_order` (`sequential` / `randomised`) from memory
   before drafting. Never mix traditions: a Christian student should
   not get a Marcus Aurelius quote, a Universal student should not
   get a Psalm.
3. **Tailor to the profile.** Pull `student_age`, `focus_goal`,
   `interests`, `location`, `blocker`, and `off_limits` from Mnemosyne
   (set at onboarding). Reference the student's actual life — their
   sport, their city, their goal — not generic examples. Honour
   `blocker` and `off_limits` silently. See `eight-essentials-curriculum`
   Step 3 for the full tailoring contract.

---

## Format 1 — Essential Summary (key points + voice note)

**Goal:** the student can hold the essential in their head in one
listen. Key points in text + a 3 to 5 minute voice note.

### Step 1 — Synthesise the key points

Read the lesson file(s), then distil **5 to 8 key points**. Each key
point is:

- One short **bold statement** (under ~12 words) that captures one
  idea.
- One or two sentences of plain-language expansion underneath.

Do not restate the guide verbatim. Distil. The student can read the
guide; the summary is what the student *retains*.

### Step 2 — Write the voice script (~550 to 700 words → 3 to 5 min)

At ~150 words/minute spoken, 550 to 700 words lands at 3 to 5
minutes. Structure:

1. Greet the student by name. Name the essential in one line and why
   it matters in one line.
2. Walk the key points **in spoken language** — not bullet points
   read aloud. Use transitions ("first", "then", "the thing that
   surprises most people is…").
3. One small action to try (the same "one small thing" discipline as
   the Morning Minute — singular, concrete, under five minutes).
4. Close warm and steady. No moralising.

Apply the TTS pre-clean rules from `morning-minute` Step 3 before
synthesis: **strip em dashes** (replace with commas/periods), rewrite
references as natural speech (`Psalm 46:10` → "From the book of
Psalms, chapter forty-six, verse ten"), spell out abbreviations,
sentence-end every line, drop Markdown/URLs/hashtags.

### Step 3 — Generate the voice note (Piper → OGG)

Follow `morning-minute` Steps 4–5 exactly:

- Piper synthesis (native `.exe` on Windows; native `C:\...` paths,
  never MSYS `/c/...`).
- ffmpeg WAV → OGG Opus mono ~24 kbps.
- Sanity check: 3 to 5 minutes (~180 to ~300 s), OGG ~400 KB to ~1 MB.

### Step 4 — Deliver

In an interactive chat (the desktop app, or a live Telegram/WhatsApp
thread), deliver the audio **inline** first, then the key points as
text:

```
MEDIA:/absolute/path/to/essential-summary-silence.ogg

**Silence — the key points**

1. <bold statement>
   <one-two sentences>

2. … (5 to 8 total)

**One action to try:** <singular, under five minutes>
```

`MEDIA:<absolute path>` on its own line triggers the inline voice
player. If the audio must be pushed to Telegram by the agent directly
(automated/cron context, no live chat), use the multipart `sendVoice`
pattern in `morning-minute` Step 7 instead — the key points text
follows as a `sendMessage`.

### Step 5 — Archive (optional)

Append a short entry to the profile's archive (date, essential, the
key points, and a link to the audio) so a parent or mentor can review
later.

---

## Format 2 — Essential Lesson (three-page here.now HTML)

**Goal:** a beautiful, self-contained three-page lesson the student
can read in a browser and answer a quiz in. Delivered as a link.

### Step 1 — Read and research

1. Read the essential's `SKILL.md` + `lessons/*.md`, branched by
   tradition (see preamble).
2. Decide whether the lesson needs **external research**. Most
   essentials can be taught straight from the guide. Add external
   material only when the lesson is stronger with evidence the guide
   doesn't carry — a sleep stat for Body, screen-time research for
   Digital Self-Defence, a nature study for Nature.
3. When you do research, use the **Jina API** (free key, set at
   onboarding as `JINA_API_KEY` in `.env`):

   ```bash
   # Fetch a page as clean markdown (to read + cite accurately)
   curl -s -H "Authorization: Bearer $JINA_API_KEY" "https://r.jina.ai/<url>"

   # Search the web (returns results as markdown)
   curl -s -H "Authorization: Bearer $JINA_API_KEY" "https://s.jina.ai/?q=<url-encoded query>"
   ```

   (`r.jina.ai` and `s.jina.ai` are aliases; both carry the same
   Bearer token.) **Cite every external claim** with the source title
   and URL in a sources list. Never fabricate a citation. If Jina
   returns nothing usable, teach from the guide alone and say so
   honestly — a lesson with fewer sources beats one with made-up
   ones.

### Step 2 — Structure the three pages

Each "page" is a full-width, full-height section of one HTML file.
Keep it a **single self-contained HTML file** (inline CSS + JS, no
external build) with three `page` sections and a small sticky in-page
nav. Three sections on one file avoids here.now slug churn and broken
cross-links.

- **Page 1 — The idea.** What the essential is, why it matters, and
  the one-line promise of practising it. Opens with the hero.
- **Page 2 — The key points / evidence.** The core teaching, with
  inline **cited sources** (superscript or small "Source:" links) and
  **key quotes** from the guide or the student's tradition (Bible
  verse for Christian, thinker/reflection for Universal).
- **Page 3 — Test yourself + act.** A **quiz** (5 to 8 questions),
  the "one action to try", and a closing line.

### Step 3 — Build it on brand

The lesson must look like it belongs to the project. Use the fixed
design system:

**Fonts** (Google Fonts):
- `Fraunces` — serif display, italics for accent clauses (headlines)
- `Space Grotesk` — display sans (eyebrows, big numbers)
- `Inter` — body (paragraphs, cards, quiz)

**Palette** — night/dawn two-tone, alternating dark navy ↔ warm
cream, one restrained accent (gold/amber):

```css
--night:#0d1220; --night2:#131a2e; --night3:#1a2340;
--dawn:#f6efe3; --dawn2:#efe6d6; --paper:#fbf7ee;
--ink:#232a3d; --ink-soft:#5a6278;
--terra:#c2603e; --terra-deep:#9c4a2e;
--sage:#7d8a6e; --sage-deep:#5f6d52;
--gold:#d9a441; --gold-soft:#e8c87a;
--blue:#4f6f9e;
```

**Section anatomy** (the proven rhythm):
1. **Fixed dark blurred nav** — serif wordmark (`one <em>to</em>
   eight` or the essential name) + uppercase letter-spaced anchors
   (THE IDEA / THE EVIDENCE / TEST YOURSELF).
2. **Atmospheric hero** — radial-gradient sky (night or golden-hour),
   a conceptual motif that *is* the essential's thesis, a Fraunces
   headline mixing roman + italic accent, a quiet body paragraph, an
   uppercase eyebrow kicker, a scroll cue.
3. **Alternating dark/cream full-bleed sections**, each opened by a
   small-caps `PART n` kicker + hairline rule. Use the content
   patterns: **big-number stat tiles**, **card grids**, **data bars**,
   **pull-quote** blocks.
4. **Quiz** — pure HTML/JS, no backend. Each question is a small
   block; the student clicks an answer and JS reveals
   correct/incorrect plus a one-line explanation. No scoring gate —
   this is learning, not a test.
5. **Sources** — a plainly labelled list of every citation (guide
   chapter + any Jina-sourced pages with title + URL).
6. **Honesty footer** — centred wordmark, plus a plain-text note that
   any research figures are illustrative/estimates and the guide is
   the primary source. Education-and-awareness framing throughout:
   never fear-mongering, never a sales pitch.

**Encoding:** replace all non-ASCII characters with HTML entities
before upload (`—` → `&mdash;`, `'`/`'` → `&rsquo;`, `"`/`"` →
`&ldquo;`/`&rdquo;`, `…` → `&hellip;`) — here.now's CDN can
double-encode Unicode.

### Step 4 — Publish to here.now (the household account)

Upload the single HTML file to the here.now drive and publish once.
Load the key from the household credentials (Brendan's account):

```python
import os, json, hashlib, urllib.request

CRED = os.path.expanduser("~/.herenow/credentials")
API_KEY = open(CRED).read().strip() if os.path.exists(CRED) \
          else os.environ.get("HERENOW_API_KEY", "")
DRIVE_ID = os.environ.get("HERENOW_DRIVE_ID",
                          "drv_01kq8g6hkfmnmfqngr18xyx3mb")
BASE = "https://here.now"

def api(method, path, body=None):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bearer " + API_KEY,
                 "Content-Type": "application/json"},
        method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

html = open(local_file, "rb").read()
sha = hashlib.sha256(html).hexdigest()
drive_path = f"lessons/{slug}.html"        # RELATIVE — no leading slash

# 1. Stage (new file: ifNoneMatch "*" on BOTH stage and finalize)
stage = api("POST", f"/api/v1/drives/{DRIVE_ID}/files/uploads",
            {"path": drive_path, "size": len(html),
             "contentType": "text/html", "sha256": sha,
             "ifNoneMatch": "*"})

# 2. PUT the bytes to the presigned URL (Content-Type byte-identical to stage)
put = urllib.request.Request(stage["uploadUrl"], data=html,
        headers={"Content-Type": "text/html"}, method="PUT")
with urllib.request.urlopen(put, timeout=120) as r:
    pass

# 3. Finalize (fallback: POST /api/v1/drives/{DRIVE_ID}/files/finalize
#    with {"uploadId": ...} if stage["finalizeUrl"] is unreachable)
api("POST", stage["finalizeUrl"],
    {"uploadId": stage["uploadId"], "ifNoneMatch": "*"})

# 4. Publish ONCE, at the very end
pub = api("POST", "/api/v1/publish/from-drive", {"driveId": DRIVE_ID})
lesson_url = pub["siteUrl"].rstrip("/") + "/" + drive_path
```

**Replacing an existing lesson** for the same essential: fetch the
current etag (list the drive, match `path == drive_path`), stage with
`ifMatch: etag` instead of `ifNoneMatch`, and finalize with
`{"uploadId": ...}` (no `ifNoneMatch`). Keep one path per essential —
never create `-v2.html` variants.

### Step 5 — Verify and deliver

1. Verify the published URL serves the real file (a fresh fetch with a
   cache-buster and a browser User-Agent). If it returns a ~1,360-byte
   stub, re-upload + re-publish before sharing.
2. Deliver in the chat: one or two lines saying what the lesson
   covers, then the link. No wall of text — the page is the lesson.

---

## Format 3 — Essential Rhyming Poem (spoken word)

**Goal:** the essential lands emotionally and memorably. A rhyming
spoken-word poem the student can listen to and read along with.

### Step 1 — Write the poem

- Read the essential's lesson file first (branch by tradition).
- Write **12 to 24 lines** with a consistent meter and a real rhyme
  scheme (AABB or ABAB). Rhymes must be natural — a forced rhyme
  reads as mockery. If a line won't rhyme cleanly, rephrase the line,
  not the idea.
- Honour the essential's core idea and finish on the one small
  action. For a Christian student, the verse may be woven in
  naturally; for a Universal student, the reflection.
- Age-appropriate, no jargon, no em dashes. Keep the weight of the
  essential — the project's tone is clear-eyed, not saccharine. A
  poem about Tested Faith or Digital Self-Defence can be honest about
  the hard part.
- End each line with natural punctuation (a comma, period, or full
  stop) — Piper reads line-broken verse more naturally that way.

### Step 2 — Generate the voice note

Piper → OGG as in Format 1 / `morning-minute` Steps 4–5. A poem of
12 to 24 lines is typically 45 to 90 seconds spoken.

### Step 3 — Deliver

Audio inline first, then the poem text so the student can read along:

```
MEDIA:/absolute/path/to/essential-poem-community.ogg

<poem text, line by line>
```

Use the `sendVoice` multipart path (`morning-minute` Step 7) only for
automated/cron Telegram delivery.

---

## Pitfalls

- **Inventing content.** The guide is the source of truth. Synthesise,
  never invent. If the lesson file is missing, say so — don't draft
  teaching the student hasn't authorised.
- **Mixing traditions.** Verify `christian`/`universal` before
  drafting any quote, verse, poem line, or quiz answer.
- **Forced rhyme.** A bad rhyme is worse than no poem. Rephrase the
  line before bending the meaning.
- **Em dashes in TTS input.** Replace with commas/periods; Piper
  stumbles on them.
- **MSYS path mangling** with piper and python. Use native `C:\...`
  paths on Windows (see `morning-minute` Step 4).
- **here.now slug churn.** Publish **once** at the very end. Multiple
  publishes mint multiple URLs and the student (and dashboard) can
  only see the latest. Keep one drive path per essential — never
  `-v2.html` variants.
- **1,360-byte stub trap.** If the published URL returns ~1,360 bytes,
  the upload never landed. Re-stage, re-finalize, re-publish, then
  re-verify before sharing the link.
- **Fabricated citations.** Cite only what you actually read via
  Jina. A lesson with one honest source beats one with five invented
  ones.
- **Voice note too long / too short.** Summary targets ~550 to 700
  words (3 to 5 min). If it drifts over, cut — the discipline is in
  the constraint.

## Related skills

- `eight-essentials-curriculum` — reads the guide and teaches; these
  three formats build on it.
- `morning-minute` — the Piper → OGG → delivery mechanics these
  formats reuse (Steps 3–5 and 7).
- `afterschool-checkin` — the daily reflection these formats sit
  alongside.
- `setup-walkthrough` — ensures Piper, the Jina key, and here.now are
  configured before any of these formats are requested.
