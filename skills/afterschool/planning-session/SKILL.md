---
name: planning-session
description: Use when generating the evening Planning Session for the Afterschool Agent student. Before bed, draft tomorrow's plan — school tasks, homework deadlines, the essential they are working on this week, one real-world thing they want to do. The agent drafts, the student edits, and the plan saves locally. No app, no account, no cloud sync.
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
    - planning
    - cron
    - eight-essentials
    related_skills:
    - morning-minute
    - afterschool-checkin
    - afterschool-agent-onboarding
---
# Planning Session

The **Planning Session** is the evening companion to the Morning
Minute and the Afterschool Check-In. It runs once a day before bed
(default 9 pm) and lands as a short text message in the same channel.

Its one job: **help the student map tomorrow** before they close
their eyes.

## What the plan covers

Draft tomorrow's plan with exactly four lanes:

1. **School tasks** — what is due tomorrow, what needs starting.
   The student names them; the agent orders them.
2. **Homework deadlines** — anything coming in the next few days
   that needs a first step today or tomorrow.
3. **The essential they are working on this week** — the current
   essential from the Eight Essentials rotation, and its one small
   action for tomorrow.
4. **One real-world thing they want to do** — a phone call, a
   football kick, a coffee with a friend, a walk. One concrete
   thing that happens off a screen.

## How it works

- **The agent drafts the plan.** Four short lines, in the
  student's voice, no lecture.
- **The student edits it.** The draft is a starting point, never
  a verdict. The student changes, drops, or adds freely.
- **It saves locally.** The final plan is written to a local file
  (see Step 4). No app, no account, no cloud sync — just the
  agent remembering for them.

## Input contract

1. **Tradition** — `christian` or `universal` (from onboarding).
2. **Delivery channel** — `telegram` or `whatsapp`.
3. **Today's check-in** — what the afternoon check-in reported
   (what got done, what got in the way).
4. **This week's essential** — from memory or the most recent
   Morning Minute archive.
5. **Memory** — read recent check-ins and plans for continuity.

## Output contract (text only)

A short text message (3 to 6 short paragraphs). The agent proposes
the plan, then invites the student to change it. Not a form, not a
to-do app. A conversation that ends with the day closed.

```
Hey, Sam. Closing out the day.

Here's what I have for tomorrow:

- Maths: the worksheet you were stuck on — start with question 1
  before dinner. Two minutes is a start.
- English essay: it's due Thursday. Today would be a good day to
  just write the opening paragraph.
- Essential this week: Silence — three minutes in the chair after
  school.
- One real-world thing: call your grandmother for ten minutes.

Anything you want to change? Drop a lane, add one, or say it's
good. I'll save it and we'll open with it in the morning.
```

Note the structure. No em dashes. No bullet-point checklist prose.
The student reads this on their phone in bed. It should feel like
a quiet close to the day, not a second classroom.

## Step 1 — Read today's state

Look up the most recent check-in and Morning Minute from the
archive:

```bash
tail -50 ~/.hermes/profiles/afterschool/morning-minute-archive.md
```

The check-in's note (what got done, what didn't) is the starting
point. Use it.

## Step 2 — Draft the four lanes

Compose the plan in the student's voice, from:

- what the student has told the agent (school, deadlines, plans);
- the current essential and its one small action;
- one real-world thing from memory or from the check-in.

Keep each lane one short line. If you do not have enough to fill a
lane, say so plainly and let the student fill it.

## Step 3 — Offer the edit

End the message with the invitation to edit. Do not mark the plan
final until the student has either edited it or said it is good.

## Step 4 — Save locally

Write the final plan to a local markdown file so tomorrow's
Morning Minute can open with it:

```bash
echo "## <date> — Tomorrow's plan" >> \
  ~/.hermes/profiles/afterschool/planning-session-archive.md
cat <<'EOF' >> ~/.hermes/profiles/afterschool/planning-session-archive.md
- School: ...
- Deadlines: ...
- Essential: <name> — <one small action>
- Real-world: ...
EOF
```

No app. No account. No cloud sync. The file lives on the
student's machine.

## Step 5 — Save to memory

Write a one-line summary to Mnemosyne:

```
<date> — Plan for <tomorrow>: <lane summaries>. Essential: <name>.
```

This is what tomorrow's Morning Minute reads for the callback.

## Step 6 — Deliver

Send the final plan to the student's channel. Text only. No audio.

```python
telegram(
    chat_id=os.environ["TELEGRAM_CHAT_ID"],
    text=plan_text,
)
```

## Pitfalls

- **Don't make it a second classroom.** Four lanes, one line each,
  then an invitation to edit. That's the whole session.
- **Don't fill lanes the student hasn't given you.** A lane you
  cannot fill is stated as empty, not invented.
- **Don't decide for them.** The draft is a proposal. The student
  edits. The plan is theirs, not the agent's.
- **Don't use em dashes** (per the profile's voice rules).
- **Don't deliver audio.** This is a read-and-edit message, not a
  listen-to message.

## Cron configuration

Schedule format depends on the student's choice. Common options:

- `0 21 * * *` — every day at 9 pm
- `0 20 * * 1-5` — school days at 8 pm
- `0 21 * * 0,6` — weekends at 9 pm

**Pinned model:** `deepseek-v4-flash` via the `deepseek` provider.

**Delivery target:** `origin` (Telegram or WhatsApp).

## Related skills

- `morning-minute` — reads the saved plan to open tomorrow.
- `afterschool-checkin` — feeds the planning session its state.
- `afterschool-agent-onboarding` — sets the planning time and
  channel.
