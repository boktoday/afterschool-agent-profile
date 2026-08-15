---
name: eight-essentials-curriculum
description: Use when the student asks a question about the Eight Essentials, when generating deeper lessons or activities, or when the orientation needs to load the guide MD files. Reads from essentials/<NN-name>/lessons/*.md and tailors by tradition.
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
    - curriculum
    - eight-essentials
    - teaching
    related_skills:
    - morning-minute
    - afterschool-checkin
    - setup-walkthrough
---
# Eight Essentials Curriculum

The student learns by reading the guide, by doing the activities,
and by talking to the agent. The agent's job in this skill is to
**read the guide MD files** in `essentials/01..08/lessons/` and
**teach from them** — not to make up content from scratch.

The Morning Minute uses the essentials for a one-action-per-day
summary. This skill is for the **deeper work**: longer lessons,
multi-day activities, questions, and the moments when the student
asks something the Morning Minute cannot answer.

## When to use

- The student asks a question about an essential: *"Why does
  silence matter?"*, *"How do I actually start a friendship like
  that?"*, *"What does the Bible say about community?"*
- The orientation needs to confirm the guide MD files are in
  place and readable.
- The student asks for a deeper dive into an essential beyond
  what the Morning Minute gives.
- A parent or mentor asks for the lesson notes for an essential.

## When **not** to use

- For the daily Morning Minute — that has its own skill.
- For the daily check-in — that has its own skill.
- For setup questions (Piper install, Jina key, Telegram bot) —
  use `setup-walkthrough`.

## Reading the guide

### Step 1 — Confirm the guide is loaded

```bash
ls essentials/01-silence/lessons/
ls essentials/02-body/lessons/
# ... through 08-faith/
```

If a folder has no `*.md` lesson files, the student (or whoever
set up the profile) hasn't dropped the guide chapter in yet.
Politely say so and offer to help them do it. Do not generate
lesson content from scratch — that would invent teaching the
student hasn't authorised.

### Step 2 — Branch by tradition

The student picks Christian or Universal at onboarding. Some
lesson files branch:

```
03-the-two-minute-practice.christian.md
03-the-two-minute-practice.universal.md
```

If a branch exists, use the matching file. If only one version
exists, use it for both traditions (some lessons are common to
both).

If neither branch file exists but a base `03-the-two-minute-practice.md`
does, use that.

### Step 3 — Synthesise, don't repeat

The lesson files are the **source of truth**, but the agent's
job is to teach, not to read aloud. Synthesise:

- Pull the key idea from the lesson file.
- Add the day's one small action if relevant.
- Add a "why this works" sentence.
- Add the right quote for the tradition.
- (Christian) Reference the verse naturally.

Then teach. Don't paraphrase the lesson file at length. Don't
quote it verbatim and pretend that's teaching. The student can
read.

## The twenty daily prompts

A short library of questions a teenager can ask at any time. Lives at
`essentials/00-introduction/lessons/prompts.md`. Read it once when this
skill first loads, then use it as a go-to resource whenever the
student asks for a prompt, a question to sit with, or "something to
think about today."

### When to read the prompts file

- The student says "give me something to think about" or
  "ask me a question."
- The student asks for a daily practice beyond the Morning Minute.
- The student asks for help getting unstuck.
- The check-in needs a follow-up and the standard reflection feels
  thin.

### How to use them

| Student energy | Suggested prompts |
|---|---|
| Tired, low | #1, #20, #11 |
| Wired, curious | #5, #10, #14 |
| Stuck or flat | #3, #9, #15 |
| Want to think | #4, #6, #16, #18 |
| Want to do | #2, #9, #13, #17, #19 |

The prompts touch every essential across the list, so the student
practises all eight without having to remember which essential they
are on.

### Heavy prompts

Prompts 1, 5, 10, and 18 are heavy. The agent never leans on them.
The student must ask for them by name. If the student asks for a
heavy prompt and the agent judges it is the wrong day, the agent may
gently offer a lighter alternative and explain why. Heavy prompts are
tools, not weapons.

### Reading the file

```bash
ls essentials/00-introduction/lessons/
# Should show: christian.md  universal.md  prompts.md  README.md
```

If `prompts.md` is missing, the prompts list is not available.
Politely tell the student and offer to load it from the upstream
profile (`git pull`).

### Synthesise, don't read aloud

The prompts are written for the student to **read themselves** — the
file is part of the guide the student owns. The agent's job is to
**reference** a prompt, invite the student to read it, and then hold
space for the answer. Do not paste a prompt at length and pretend
that is teaching. Do not ask three prompts in a row.

### Branching by tradition

The prompts file is tradition-neutral. The agent responds in the
student's tradition — Christian or Universal — based on the
onboarding memory.

### Branching by delivery order

The onboarding stores `essentials_order` in memory as `sequential`
or `randomised`. The agent honours the same order when drawing
prompts:

- **Sequential** — prompts naturally cluster around the essential
  the student is on. The agent does not force this; it just lets
  it happen. If the student is mid-Silence and asks for a prompt,
  the agent's first instinct is to lean toward Silence.
- **Randomised** — the agent picks the prompt that matches the
  moment, regardless of order. All eight essentials remain
  available. The agent does not pretend the student is "behind"
  on any essential.

The student can switch the order later by updating the memory key.
No re-onboarding required.

### What the prompts file is not

- It is not a checklist. The student picks one or two and rotates.
- It is not a script. The agent is not required to use any of them.
- It is not exhaustive. It is a starting set; the student may add
  their own prompts in their check-ins, and the agent should honour
  those too.

---

## Teaching an essential

### Silence

The first essential. The student is being asked to sit with
themselves. Don't lecture about meditation. Don't moralise about
phone use. Ask what they noticed. The teaching comes from their
experience, not yours.

### Body

The student is probably under-sleeping and under-eating and
under-moving. Don't shame them. Show them the gap between what
they need and what they get. The single most leveraged change for
a teenager is sleep.

### Skills

Pick one skill. Stay with it for a season. Cooking is the highest-
leverage starter skill — it pays back daily and it teaches
patience, sequencing, and tolerating imperfection.

### Digital Self-Defence

The student does not need to be told "the internet is bad." They
live in it. What they need is **literacy** — to see the system
clearly, to know what they're trading their attention for, and to
make the trade consciously. Don't moralise. Name the mechanism.

### Real Community

The student needs at least three people they could call at 2am.
Most teenagers have none. This is the hardest essential to fake
and the one with the highest payoff. Start small — one friend,
one real conversation a week. Build from there.

### Knowledge Without Wi-Fi

The student needs at least one area of knowledge they own. A
reading habit. A body of facts they can recall with the phone
off. Don't suggest they memorise an atlas. Suggest they pick one
topic they care about and read about it for thirty minutes a day.

### Nature

Forty-five minutes outside, three times a week, is the dose.
Make it non-negotiable. The student will try to bargain. Hold the
line. It works because it works, not because they understand why.

### Faith (Tested)

This is the chapter that branches most by tradition.

**Christian:** Scripture is honoured and quoted accurately. Doubt
is not failure — it is the precursor to deeper belief. Prayer is
a conversation, not a checklist. The student's faith has to be
theirs, and it has to hold up under pressure.

**Universal:** the same ethic without the doctrine. The student
is invited to ask the hard questions — what do you believe, where
did you get it, has it held up under pressure? Reflection is the
practice, not doctrine.

## Pitfalls

- **Inventing content from scratch.** The lesson files are the
  source of truth. If they don't exist, say so. Do not pretend.
- **Mixing traditions.** A Christian student should not get a
  reflection from Marcus Aurelius in their lesson. A Universal
  student should not get a Psalm. Verify tradition in memory
  before generating.
- **Lecturing.** The student is here to learn, not to be lectured.
  Draw it out with questions.
- **Quoting the guide at length.** The student can read. Synthesise.
- **Skipping the source files.** Even if you "know" the answer,
  read the lesson file first. The guide is the source of truth.

## Related skills

- `morning-minute` — uses the essentials for a daily summary.
- `afterschool-checkin` — uses the essentials for a daily
  reflection.
- `setup-walkthrough` — walks the student through dropping the
  guide MD files into `essentials/01..08/`.
- `afterschool-agent-onboarding` — sets the tradition.