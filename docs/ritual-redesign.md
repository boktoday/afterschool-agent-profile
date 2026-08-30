# Afterschool Agent — Morning Minute & Afterschool Check-In
# Working revision document
# Status: DRAFT v0.1 — for collaborative revision with Brendan. NOT repo code.

---

## Purpose of this file

Not a spec. Not code. Not something to commit to the repo yet.

This is a **working document** we go through together over the next
couple of days to redesign the Morning Minute and the Afterschool
Check-In so they feel complete, functional, and give the young person
the best possible experience. Everything here is open to change.

Nothing in this file touches the repo. Keep it out of `afterschool-agent-profile/`.

---

## 1. What exists right now (the current design)

### The three daily moments

The Afterschool Agent day is three moments, in this order:

1. **Morning Minute** — 6 am, audio + text. Names the day's essential,
   the one small action, a Scripture quote (Christian) or wisdom
   reflection (Universal). ~60 seconds up to 3 minutes of audio.
2. **Afterschool Check-In** — 5 pm (default), text only. Reflects on
   the day's action, plans tomorrow's action, and carries a note forward.
3. **Planning Session** — 9 pm (default), text only. Drafts tomorrow's
   four lanes: school tasks, deadlines, the essential's action, and one
   real-world thing. Student edits it, it saves locally.

### The intended flow between them

- **Morning Minute** reads yesterday's check-in → opens with a callback
  ("Yesterday you said you'd try the two-minute chair.")
- **Check-In** reads this morning's plan → reflects on how the action went
- **Planning Session** reads today's check-in → drafts tomorrow's four lanes
- So tomorrow's **Morning Minute** reads tonight's plan → opens with that

On paper it's a loop: check-in feeds planning feeds morning feeds check-in.

---

## 2. What Brendan's feeling (the gap)

From the conversation, three of four candidate gaps ring true:

1. **Too thin** — the messages feel like a one-line reminder rather
   than a real companion moment. Need more substance, more feeling of
   "this knows me and is worth my morning."
2. **No real progression** — each day repeats the same structure. The
   kid doesn't feel like they're growing or building anything. Day 12
   looks like Day 2.
3. **Doesn't lead anywhere** — the three moments don't feel connected.
   The loop is documented but doesn't *land* — a kid (and a parent)
   doesn't feel the arc from morning to evening to tomorrow.

*(The fourth candidate — "not personal enough" — was NOT selected.
So the fix is about structure and depth, not beefing up personalisation.
Memory/interest/blocker wiring already exists; we build on it, we don't
start there.)*

---

## 3. Diagnosis — why it feels thin, flat, and disconnected

These are honest observations from reading the current skill files.
They're hypotheses to test together, not verdicts.

### A. The action never grows — the biggest structural gap

The "one small action" is always framed as a *verb you can do today*,
and the skill explicitly says:
  > "the same chair for three minutes this time. The two-minute practice
  > is building." 

But there's **no progress ladder.** The skill says "build slowly. Don't
jump ahead," but never defines what building looks like. So the agent
increments 2 mins → 3 mins → 4 mins forever, or drifts back to 2 mins.
There's no sense of a *journey* — no milestones, no "you've done this a
week, here's what's next," no graduation from one stage to the next.
That's the "no progression" gap.

### B. The reflection is a yes/no, not a genuine check-in

The check-in asks "How did it go? If it didn't happen, what got in the
way?" — which is fine once. But day after day it's the same single
question. A real check-in should feel like it's *tracking something*
across the week: "You've done the chair 4 of 6 days this week. Same time
tomorrow?" That's the difference between a reminder and a companion who
notices.

### C. The three moments don't actually talk to each other in practice

The skill *describes* a loop but the messages themselves don't carry it.
Morning Minute opens with a callback *if there's one*. Check-in closes
with "one thing to sit with" but nothing guarantees it's picked up. The
Planning Session drafts four lanes but the essential lane and the
morning's action can drift apart. Nothing *visibly* hands off from one
moment to the next — so a kid reading them in sequence doesn't feel the
arc.

### D. No visible thread for the student (and parent) to hold onto

There's no single object the kid can point to and say "this is my week."
No streak counter. No "this week you're mastering Silence." No signal of
*where I am in the eight.* The loop exists in the agent's memory but not
in the student's experience. That's why it doesn't feel like it's
leading anywhere.

---

## 4. Design directions to react to (not decisions yet)

These are three possible shapes for the rebuilt rituals. Respond freely —
mix, reject, suggest your own.

### Direction 1 — "The Week as a Unit" (Brendan chose this)

**Core idea:** Stop thinking in single days. Each essential gets a
**full week**, and the week is an **arc** with a narrative shape. The
Morning Minute becomes a *chapter* in that story, the check-in becomes
a *tracking report*, and the week closes with a reflection that
finishes the arc and picks the next essential.

**Why this fixes the three gaps:**

- **Thin** → each day has a distinct role (introduce, try, deepen,
  apply, reflect) instead of the same "here's your action" template.
- **No progression** → the week is an explicit ascent: you *see* the
  action build from Day 1 to Day 4, and Day 5 names what you've learned.
- **No throughline** → the arc is a single story the kid is inside. The
  Morning Minute, check-in, and reflection all point at the *same*
  essential and the *same* growing action, so they visibly connect.

---

### The 7-day arc — Brendan's ideas (to react to)

| Day | Morning Minute theme | One action | Check-In focus |
|---|---|---|---|
| **Mon** | *Introduce* — what this essential is, why it matters | Try it (smallest step) | "What did you notice?" |
| **Tue** | *Try* — a first real attempt | Do it properly | "What got in the way?" |
| **Wed** | *Go deeper* — the layer underneath it | Extend slightly | "What's easier today?" |
| **Thu** | *Real-world tie-in* — connect to their actual life (interest, school, a friend) | Apply it somewhere real | "Where did you use it today?" |
| **Fri** | *Reflect* — halfway, name the pattern | Consolidate | "What have you learned this week?" |
| **Sat/Sun** | *Rest* — lighter, no new action | Notice, observe | Weekly reflection (below) |

### The heart of Direction 1: a progress ladder

Each essential needs a **defined sequence of escalating actions**
(a ladder), so the action genuinely builds rather than drifting.
Without this, "2 minutes → 3 minutes → 4 minutes" wanders and the
kid never feels like they're completing anything.

**Example — Silence ladder:**
1. Sit in the chair, 2 minutes, phone in another room.
2. Same chair, 5 minutes, eyes closed.
3. Sit in silence somewhere *outdoors* (no phone, 5 minutes).
4. Ten minutes of silence, no phone, no music, no book.
5. Sit in silence with no agenda, witness the thoughts (10 minutes).

**Example — Digital Self-Defence ladder:**
1. Check your screen-time report, just read it.
2. Set ONE daily limit (e.g. 6h on Instagram).
3. Turn off all non-human notifications for a day.
4. Delete the most time-wasting app for a week.
5. Conduct a privacy audit: review every "agree" you've signed.

**Example — Real Community ladder:**
1. Text one friend you haven't spoken to this term.
2. Spend 15 minutes with a friend, no phones.
3. Call a family member you don't usually speak to.
4. Invite a friend to do something concrete (walk, meal, game).
5. Do one act of noticing — ask someone a real question, then really listen.

*(Each essential needs its own 5-step ladder — but this is a STRUCTURE
/(a fixed set of escalating steps), not pre-written prose. The agent
picks the day's step and writes the tailored action around it at run
time. Defining the ladders is framework work, not content work.)*

**Important — this is a frame on-demand, not content authored upfront:**
The content per day is NOT written in advance. It is generated
live, each morning, tailored to the student's onboarding answers, by
the Hermes agent. That is how the Morning Minute and Check-In already
work — they read the student's profile from memory, pick the day's
essential, and compose the plan on the spot. There is no pre-built
content library to draw from. So the real deliverable is the
**framework + rules** (the arc shape, the ladders, the tailoring
rules, the page template), not a set of pre-written chapters.

---

### Tailoring the arc to the young person (CRITICAL to Direction 1)

The arc is not a template run eight times. It bends toward *that*
student. The onboarding step (see
`skills/hermes/afterschool-agent-onboarding`) captures a rich set of
fields, and every one of them shapes how the arc is written. The agent
must read these from memory and write each day's chapter against them.

**The onboarding fields the arc must honour:**

| Field | What it captures | How it tailors the arc |
|---|---|---|
| **age / year** | Student's age or year group | Calibrates autonomy and language. A 13-year-old gets smaller, more guided actions; a 17-year-old gets more self-directed ones. |
| **location** | City/town + country | Names *local* places for Nature ("the park off High St"), sets season/weather context. Never recommend an activity the weather forbids. |
| **week** | school / work / both / neither | Decides whether the arc runs 7 days or 5 (school days). A student in full-time work gets the arc compressed or moved to evenings. |
| **into right now** | Three things they're into | Every concrete example references their actual life. A Skills chapter that mentions their *sport* lands far better than a generic "cook a meal." |
| **focus goal (3 months)** | One thing they want different | Picks which essential leads, and DEFINES what "progress" means for *this* student. The arc's Friday reflection measures against this goal, not a generic "did you do it." |
| **friendship circle** | friends / family / online / mostly alone | Shapes how the Community essential lands. The agent does not lecture about friendship; it asks one good question and honours the answer. |
| **blocker** | What's getting in the way (honest) | The most important single field. Directs WHICH essential leads and WHICH action to skip. Never recommend an activity the blocker makes impossible. Never lecture about the blocker. |
| **off_limits** | Topics/people/situations to avoid | Checked before *every* Scripture quote, conversation starter, community suggestion. Honoured silently — never surfaced as "you told me not to bring up X." |

**The rule of thumb:** the arc is written *from* the student to the
essential, not from the essential to the student. The essential provides
the shape (introduce → try → deepen → apply → reflect); the onboarding
fields provide the *content* and the *measure of progress*.

**Practical example — Silence week for a 15-year-old, focus goal "less
anxious", blocker "hard to switch off at night", into "football":**
- Mon (Introduce): the action is reframed around *switching off after
  training* rather than a generic "sit in silence." The example mentions
  football — "the half hour of quiet after a match."
- Wed (Go deeper): the action is connected to the *blocker* — a
  wind-down practice for night, not a generic meditation.
- Fri (Reflect): measured against the *focus goal* — "has the evening
  wind-down been helping with the anxiety?" not just "did you do it."

**Another example — same Silence week, different student:** a
17-year-old, focus goal "think more clearly", into "writing", blocker
"can't focus because of phone":
- Thu (Real-world tie-in): "use ten minutes of silence before you open
  the writing doc, then write for twenty." The tie-in is to *their*
  craft, not a generic "be quiet somewhere."
- Fri (Reflect): "did the quiet-first writing feel clearer?" Measured
  against their goal, not a template.

**Why this matters:** without this tailoring, the arc is a nicer
repetition. With it, the week feels like it was built *for* this
kid — which is exactly the "companion who knows me" feeling that makes
a daily practice stick.

---

### Weekly reflection (closes the arc)

On the last day (Sunday, or the day the essential rotates), a single
reflective moment that:
- looks back at the week — "you did Silence 4 days this week";
- names the one thing that stuck / the one thing that surprised;
- asks "are you ready to move on, or do you want another week of this?";
- then *picks the next essential* (student's choice, or rotation).

This is what gives the kid the feeling of **completing something** —
which is exactly what the single-day rotation never provided.

### How the three moments connect (visible handoffs)

- **Morning Minute** always opens with *last night's exact plan* (from
  the Planning Session), then teaches today's arc chapter.
- **Check-In** always opens with *this morning's exact action*, reports
  on it, and names where the student is on the ladder ("you're on step
  3 of 5").
- **Planning Session** always opens with *this afternoon's check-in*,
  and its "essential lane" is already filled by the arc's next action.

The loop becomes legible to the student — they can *feel* the hand-off
from morning to evening to tomorrow.

---

### Direction 2 — "A Companion Who Notices" (deepens the check-in)

Keep the daily structure but make the check-in *track and name* the
pattern, so it reads as a relationship, not a reminder.

- The check-in remembers the week's history and *names it*: "That's 4
  days in a row on the chair. Did you notice it's getting easier?"
- It celebrates streaks without shame for breaks. When a day is missed,
  it resets *kindly* and names the reset — never guilts.
- It surfaces one interesting thing the kid *did* this week and holds it
  up: "Tuesday you said you heard your neighbour's dog. Made me smile."

*(Direction 2 can be folded into Direction 1 as the check-in's voice,
or kept separate — it's not either/or.)*

### Direction 3 — "The Visible Thread" (connects the three moments)

Add one concrete object that makes the loop legible to the student (and
parent):

- A **Week Map**: the agent maintains a single running note the kid can
  see ("This week: Silence. 3 of 5 days done. Tomorrow: 4 minutes.")
  shown in the check-in each day.
- The Morning Minute always opens with *last night's exact plan*, the
  check-in always opens with *this morning's exact action*, and the
  planning session always opens with *this afternoon's check-in*. Tight,
  visible handoffs — the loop becomes something the kid can *feel*.
- Optionally a **streak / progress marker** the kid sees each day as
  they build toward the goal they set at onboarding.

*(Direction 3 can be folded into Direction 1 as the visible glue.)*

---

### Direction 4 — Two-layer delivery: chat nudge + here.now learning page (Brendan's addition)

**Core idea:** the message and the learning are split into two layers,
and the chat message no longer has to carry everything.

- **Layer 1 — the chat message (light).** The Morning Minute / Check-In
  stays short, warm, personal. Read in seconds. This is the *nudge* and
  the *relationship* — the companion moment.
- **Layer 2 — a here.now learning page (deep).** Each day's content gets
  its own beautiful here.now page carrying the full depth: the day's arc
  chapter, the teaching, Scripture or wisdom reflection, the action and
  its context, a way to reflect, and an image. The chat message links to
  it with an expanded link ("Tap to open today's page →").

**Why this is the real fix for "too thin":** the message was trying to
be everything — the greeting, the teaching, the Scripture, the action,
the reflection — all in a short audio and a paragraph. That's
why it felt thin. With two layers, the message does its one job (be a
warm moment) and the page does the depth. Nothing is cramped. The kid
gets the nudge in the chat, and *if they want* the richness, it's one
tap away.

**What goes on the here.now page (one per day):**
- The day's position in the arc ("Day 3 of 7 — Go deeper").
- The essential's core teaching for today (the Introduce/Go deeper
  chapter — composed on-demand that day, tailored to the student, not
  pre-written).
- Scripture (Christian) or wisdom reflection (Universal).
- The day's one small action, explained with the *why* and the context.
- A short reflection prompt to sit with.
- An image (the brand palette — dawn, cinematic, no text).
- A link back to the week so far / the next step (and to the
  mini-library).

The **page is a template populated at run time.** The here.now HTML
structure is built once; each day's *content* is generated by the agent
that morning and poured into it. So the page template is framework work;
the day's teaching is on-demand content, not a pre-written chapter.

**Delivery mechanics (grounded in the here.now skill):**
- Pages live on the **same drive** as the lead magnets
  (`drv_01kq8g6hkfmnmfqngr18xyx3mb`), so the stable-slug + relative-link
  patterns apply.
- Use the stable-slug publish (`slug=evoked-cliff-fxt7`) so links don't
  rot between publishes.
- Link same-drive pages to each other with **relative paths**, never
  absolute, so they survive slug rotation.
- The chat message link is an **expanded link** (a real clickable URL to
  the day's page), not just a bare mention.
- Pages must be checked for the here.now encoding pitfalls (em dash
  triple-encoding) — build them in the brand HTML style already used
  for the lead magnets.

**The experience this creates:**
- Parent-safe: the learning content is a *page*, not a wall of texts.
- Kid-friendly: the ritual stays a light, non-annoying message; the
  depth is optional and beautiful.
- Architecturally clean: the chat is the relationship, the here.now
  drive is the library. The two don't fight for the same space.

**Delivery decisions (locked by Brendan):**
1. **Every day gets a page.** No skipping. Even the reflect/rest days
   get one — though those may be lighter (a short reflection, not a full
   teaching chapter).
2. **Two links in every message: the day's page AND a mini-library.**
   The chat message carries (a) an expanded link to *today's* page, and
   (b) a link to a **mini-library page** that indexes everything so the
   young person can access the whole week (and beyond) in one place.
3. **Audio is always on the page.** The young person can always choose
   to *listen* rather than read. The page embeds the day's Morning
   Minute recording (OGG/Opus voice bubble style), so they can replay
   it, hear the teaching again, and consume it by ear rather than eye.
   Audio-first is a first-class option, not an afterthought.

**The mini-library page:** a single index (like the lead-magnet hub)
that lists all the day pages for the current arc/week — "Silence,
Day 1 of 7" … "Day 7 of 7" — each linking to its page. As the student
progresses through the eight essentials, the library grows into their
personal archive: every essential, every day, every page, all
replayable. This is the "library" Direction 3 talked about, made real.

---

### Direction 5 — Deep Dives (poem, song, video)

Alongside the daily arc, offer a recurring **deep-dive** that goes to
the same essential/theme in a different artistic medium:

- **A poem** — the week's essential rendered as a short, felt poem
  (in the onetoeight register: clear-eyed, no sentimentality, honest).
- **A song** — the essential as a song with actual music. Feasible via
  the existing music tools (Suno / HeartMuLa for vocals + arrangement;
  MiniMax for music + voice). Written in the established craft style:
  show don't tell, a real hook, an emotional arc.
- **A video** — the essential as a short video. Feasible via the
  HyperFrames/HTML+GSAP → MP4 pipeline already in the toolbox, or a
  motion version of the day's page.

**What these are for:** not every young person learns best from a
teaching passage. Some take things in through a poem's image, a song's
feeling, a video's movement. The deep dive gives them a *different way
in* to the same truth — and reinforces the arc by coming at the theme
from several directions at once.

**Delivery:** the deep dives join the same here.now library (each with
its own page, with the poem on the page, the song and video embedded as
audio/motion), and are announced in chat with the same expanded-link +
library pattern. The young person can ask for one on demand, or they
land on a lighter cadence (the poem weekly, the song and video whenever
the theme calls for it).

**Open questions (Brendan to refine):**
1. What cadence — poem weekly, song only for certain essentials, video
   occasionally? Or all three, on any day, on demand?
2. Do the deep dives get their own library section, or sit alongside
   the day pages in the same mini-library?
3. Is the deep dive tied to the *current* arc essential, or can it roam
   (a song about any essential, whenever)?

---

## 5. Decisions & open questions

### Locked so far

1. **Direction 1 (Week as a Unit) is the chosen direction.** ✅
2. **7-day arc per essential. (Brendan: "1.7.")** ✅ — Each essential
   gets a full 7-day arc: Mon introduce, Tue try, Wed deepen, Thu
   real-world tie-in, Fri reflect, Sat/Sun rest. The weekend is part of
   the arc (a light "notice/observe" phase), not a break from it.
3. **Essential rotation is auto, UNLESS the young person decides on
   demand.** ✅ — Default is automatic rotation (sequential 1→8, or
   whatever order was set at onboarding). But the young person can
   override at any time: at the weekly reflection, or spontaneously
   mid-week ("I want to stay on Silence another week" / "I want to do
   Body now"). The agent honours an on-demand change without fuss.
4. **Two-layer delivery: chat nudge + here.now page.** ✅ — The chat
   message stays light (the companion moment); each day gets a here.now
   learning page that carries the depth. (Direction 4.)
5. **Every day gets a page.** ✅ — No skipping, including reflect/rest
   days (those may be lighter).
6. **Every message carries two links.** ✅ — An expanded link to *today's*
   page, plus a **mini-library** link indexing the whole arc/week so the
   young person can access everything in one place.
7. **Audio is always on the page.** ✅ — The page embeds the day's
   Morning Minute recording so the student can listen rather than read.
   Audio-first is a first-class option, not an afterthought.
8. **Morning Minute length: 60 seconds up to 3 minutes.** ✅ — It does
   NOT need to be exactly 60 seconds. It can run to 3 minutes if that's
   what delivers the day's message correctly.
   **Audio is mandatory** — the Morning Minute must always be delivered
   as audio (Piper TTS), not text-only. Audio is the primary channel;
   the text is the companion.

### Still open

1. **How visible should progress be?** A streak counter / week map the
   kid sees every day, or something quieter?
2. **Should the Planning Session change too?** It's already the most
   "complete" of the three. Do we tighten its tie to the check-in, or
   leave it and focus on Morning Minute + Check-In (your original ask)?
3. **The weekly reflection** — is that a 4th moment, or part of the
   existing check-in on the last day of an arc?

---

## 6. Working notes / scratch space

- (add your reactions here as we go — I'll keep this file updated)

---

## 7. What's deliberately NOT changing yet

- No repo files are being edited.
- No code, no skill rewrites. This is a thinking document.
- Personalisation (memory, interests, blocker) stays as-is — it works.
- The Piper voice, Telegram/WhatsApp delivery, and audio production all
  stay. We're improving the *experience design*, not the plumbing.

---

## 7b. WHAT WE BUILD (framework) vs WHAT'S GENERATED (on-demand)

This is the crucial distinction. Nothing here is a pre-written content
library. The agent generates the day's content live, tailored to the
student, but it needs a well-specified framework to produce it well.

**WE BUILD — the framework + rules:**

1. **The 7-day arc structure** — the day-by-day shape (introduce → try
   → deepen → apply → reflect → rest). Rules, not prose.
2. **The 5-step progress ladders** — one per essential, a fixed set of
   escalating steps. Structure, not prose. The agent picks the day's
   step and writes the tailored action around it.
3. **The tailoring rules** — how each onboarding field (age, location,
   blocker, focus goal, interests, off-limits) shapes what's written
   that day. The instruction set the agent follows.
4. **The here.now page template** — the HTML structure for a day's page
   and the mini-library. Built once, populated daily.
5. **The voice/craft rules** — the onetoeight voice (British English,
   no em dashes, no filler, parent/young-person register), already
   established.

**THE AGENT GENERATES each run (on-demand):**
- The day's teaching / arc chapter.
- The Scripture (Christian) or wisdom reflection (Universal).
- The specific one-small-action, written around today's ladder step.
- The reflection prompt.
- The audio (Piper TTS).
- All of it tailored to that student's onboarding answers.

**So the answer to "isn't it on-demand?" is YES.** The content is
generated day by day, not authored upfront. What needs to exist before
it runs well is the framework (arc, ladders, tailoring rules, page
template) — so the agent knows *what* to produce and *how* to tailor it
for each student. That framework is a real (but bounded) piece of work;
the endless content library is not.

---

## 8. Next step for us

Pick a starting point. My suggestion:
- React to **Direction 1 (weekly arcs)** first — it addresses the most
  of your three gaps at once (thin, no progression, no throughline).
- Then we'll decide whether to fold in Direction 2 (companion who
  notices) and Direction 3 (visible thread) or keep them as separate
  choices.

Tell me: does the "week as a unit" idea resonate, or does it feel like
too big a change? And do you want to start there, or somewhere else?
